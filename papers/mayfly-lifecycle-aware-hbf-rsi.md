---
type: Paper
title: "Mayfly: 按生命周期管理递归自我改进中的高带宽闪存"
description: "新加坡国立 / 华中科大 — H200 校准的离散事件仿真、HBF 路径建模；128 会话 / 四个 HBF 位点上，相对 HBF-Park 提前 34% 结束、相对满 HBM 就读 HBF 提前 23%；256 会话 / 八个位点上相对停车提前 55%"
tags:
- hbf
- hbm
- kv-cache
- agentic-ai
- inference
- serving
- flash
- energy
- memory
- architecture
- llm
created: 2026-11-26
updated: 2026-11-26
timestamp: '2026-11-26T00:00:00Z'
paper_author: [Chunlin Tian, Mingjia Fan, Feng Yu, Qingyun Zou, Wenju Zhao, Weng-Fai Wong, Bingsheng He]
year: 2026
venue: preprint
arxiv: '2611.32264'
sources:
  - raw/papers/Mayfly_Lifecycle_Aware_HBF_RSI_2026.pdf
  - raw/papers/mayfly-lifecycle-aware-hbf-rsi.md
---

# Mayfly：让就绪 KV 跟着爆发与回落在 HBF 和 HBM 之间移动

## 一句话结论
新加坡国立大学与华中科技大学提出 Mayfly：按递归自我改进（RSI）一代会话的爆发-回落来管理封装上的高带宽闪存（HBF）。溢出时按每步带宽门控就地读 HBF，会话结束后把 KV 迁回腾出的 HBM；块被逐出 HBM 时保留一份有效闪存拷贝，并把编排器宣布的会话结束转给控制器，避免垃圾回收再拷已死 KV。评估是离散事件仿真：GPU 模型在 H200 回放上校准，HBF 路径为模型，回放统一用 Qwen3-32B（FP8）。128 个会话、四个新增 HBF 位点上，相对把同一份 KV 停在 HBF（HBF-Park）提前 **34%** 结束，相对「HBM 一满就就地读 HBF」（HBF-Greedy）提前 **23%**；256 个会话、八个位点上，相对停车提前 **55%**。一份拷贝加会话结束修剪后，写放大因子（WAF）为 **1.00**。

## 动机
Harness RSI 固定模型、改提示/工具/控制流，并在任务上评分候选。一代里的会话一起启动、一起长大 KV，结束后再释放，形成爆发再回落。高并发时，连已经就绪、等待或正在做 LLM 调用的会话，其 KV 也会超出 HBM：在 32 个会话、只靠 H200 HBM 的轨迹仿真里，就绪 KV 单独超出 HBM 的时间占 **86%**，而无限内存、无排队时全部存活 KV 超出的时间是 **55%**。卸到主机 DRAM 或 SSD 能加容量，就绪会话仍要等 HBM 空位才能执行。HBF 可以就地服务溢出，但无节制的读会拉长每一步，反复写入会消耗闪存寿命。RSI 的编排器自己宣布会话结束，私有 KV 可以立刻作废。

## 方案
Mayfly 把「从哪里读就绪 KV」跟爆发与回落对齐：

- 溢出期间，每步门控只允许估计不会降低该步 token 吞吐的请求就地读 HBF，且一次接纳就对整段上下文做注意力。
- 会话结束、HBM 腾出后，把仍从闪存读取的 KV 迁回 HBM。
- 就绪/停放切换只决定是否读取，闪存拷贝保持有效，避免每次切换都重写。
- 把会话结束信号交给 HBF 控制器，垃圾回收不再拷贝已结束会话的私有 KV。

实现覆盖服务运行时、双路径注意力 kernel，以及 HBF 基片上的 KV 感知控制器。

评测重实现 vLLM 的 block pool、调度与抢占；步时间与能量在 H200 回放上拟合（含一次把 KV 溢到主机 DRAM，误差 0.5%）。留出回放、20 GB KV 池上，运行时间误差 **0.9%**、能量 **1.6%**、抢占 **5%**。轨迹来自 DGM、RRSI 与 Harness² 的真实运行，回放一律用 Qwen3-32B、FP8 权重。硬件模型：H200 六个 HBM 位点共 **141 GB**，其中 **99 GB** 给 KV；HBF 为封装上另加位点，每 32 个会话一只 **512 GB** TLC 堆栈；位点读带宽取 **467 GB/s**（也跑 **202 GB/s** 热限制），写为读的十分之一；读/写能量取 **20 / 100 pJ/bit**，页读 20 µs。HBF-Park 使用与 Mayfly 相同的容量和写控制，并按 OCP 接口 **1.5 TB/s** 把 KV 恢复进 HBM。

## 量化结果
主结果来自把 DGM 评估会话扩成每代 32/64/128/256 个会话（每 32 个会话对应一个 HBF 位点）。Table 3：

| 会话/代 | HBF-Park 运行时间 / 中位 TTFT | Mayfly 运行时间 / 中位 TTFT | 提前结束 |
|---|---|---|---|
| 32 | 172 min / 7.8 s | 159 min / 2.8 s | 8% |
| 64 | 279 min / 34 s | 235 min / 22 s | 16% |
| 128 | 482 min / 89 s | 316 min / 46 s | 34%（中位 TTFT 约 1.9×） |
| 256 | 919 min / 187 s | 417 min / 73 s | 55%（中位 TTFT 约 2.6×） |

十次任务抽样的平均提前为 **8.0 / 17.5 / 36.3 / 53.9%**（95% CI ±1.5 / 1.8 / 0.6 / 0.3 个百分点）。128 会话时 Mayfly 的 decode 为 243 分钟（其中 223 分钟带 HBF 读取），HBF-Park 为 421 分钟。相对 HBF-Greedy，门控在 32–256 会话上分别节省 **29 / 28 / 23 / 11%** 运行时间。热限制 202 GB/s 时，相对 HBF-Park 仍提前 **1 / 7 / 19 / 36%**。Mayfly 的抢占次数为 0；HBF-Park 为 71–735。能量（模型）：128 会话 14.0→12.3 MJ，256 会话 27.4→22.3 MJ；相对 NVMe-Park 少 **9–22%**。

在完整运行回放上（每 H200 错开 900 s、两个 HBF 位点）：就绪 KV 大部分时间超出 HBM 时，4 / 8 路 DGM 相对 HBF-Park 提前 **19% / 22%**，8 / 16 路 Harness² 提前 **24% / 20%**。一份拷贝加会话结束修剪后 WAF 为 **1.00**；没有结束信号时，2% 空闲、1 GB 擦除单元下，垃圾回收拷贝可占物理写的 **10–44%**，WAF 随空闲下降可到 1.16 / 1.77 / 2.32。

## 局限与解读
- GPU 时间在 H200 回放上校准，**HBF 路径、能量与磨损是模型**，没有 HBF 硅片测量。
- 读带宽 467 GB/s 低于 OCP Grade 的 1.5 / 3.1 TB/s；改到 202 GB/s 后收益明显收窄。
- 主扫描按每 32 个会话一只 512 GB 堆栈配置位点；一只位点装不下 128 会话的就绪溢出时，运行时间会明显变长。
- 收益出现在就绪 KV 经常超出 HBM 的负载上；单路 DGM 溢出时间只有 1.4% 时，各设计彼此相差不超过 3.1%。

## 与 wiki 的关系
- [Hot–Cold HBM/HBF](/papers/hotcold-hbm-hbf-agentic-llm.md) — HBF-Park 的停车策略参考了把暂停会话的 KV 放在 HBF、运行前再恢复的做法；Mayfly 继续处理就绪溢出的就地读与回落迁回
- [Synapse](/papers/synapse-hbm-hbf-nmc-agentic.md) — 在 HBF 上做近存注意力与专家计算并与 GPU 重叠；Mayfly 管的是 RSI 爆发期的 KV 放置、读带宽门控和写放大
- [LaFlash](/papers/laflash-qlc-hbf-coding-agents.md) — 面向编程智能体的休眠 KV 与 QLC 编码；Mayfly 处理的是仍在运行的就绪 KV
- [Lachesis](/papers/lachesis-lifetime-aware-kv-hbm-hbf.md) — 按生命周期在分配时选择层次；Mayfly 强调后续每一步从哪里读，以及会话结束后如何迁回
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把 HBF 就地读、HBM 迁回和会话结束修剪记到同一条 KV 路径上
- [HBF-Sim](/papers/hbfsim-extensible-hbf-simulator.md) — GPU–HBF 请求路径仿真底座；本文的 HBF 通路同样是模型

# Citations
- [arXiv:2611.32264](https://arxiv.org/abs/2611.32264) — Tian 等（NUS / HUST）
- [raw stub](/raw/papers/mayfly-lifecycle-aware-hbf-rsi.md)
- [PDF](/raw/papers/Mayfly_Lifecycle_Aware_HBF_RSI_2026.pdf)
- [arXiv:2609.25782](https://arxiv.org/abs/2609.25782) — Hot–Cold HBM/HBF
