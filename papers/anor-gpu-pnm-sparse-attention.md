---
type: Paper
title: "ANOR: 用 GPU–PNM 计算层次放大稀疏注意力"
description: "KAIST / SK hynix / Penn State — LLMServingSim（H100 NVL 剖析 GPU kernel、PNM 按 M2NDP 建模）；离线最大 batch 上相对 HiSparse，Qwen3-4B / 30B-A3B 平均吞吐 2.6× / 2.1×，相对 PNM 基线 2.3× / 1.7×"
tags:
- gpu
- cxl
- near-memory-processing
- kv-cache
- sparse
- attention
- inference
- serving
- serving-system
- hbm
- pcie
- agentic-ai
- sk-hynix
- architecture
- memory
- throughput
- nvidia
created: 2026-11-26
updated: 2026-11-27
timestamp: '2026-11-27T00:00:00Z'
paper_author: [Hyunsu Ye, Hyunmin Choi, Jaehong Cho, Jaeseo Lee, Hyeongseok Gwak, Joohee Lee, Donguk Moon, Woosuk Chung, Hoshik Kim, Kiwan Maeng, Jongse Park]
year: 2026
venue: preprint
arxiv: '2611.30417'
sources:
  - raw/papers/ANOR_GPU_PNM_Sparse_Attention_2026.pdf
  - raw/papers/anor-gpu-pnm-sparse-attention.md
---

# ANOR：把稀疏注意力的命中放在 GPU，把缺失交给近存

## 一句话结论
KAIST、SK hynix 与宾夕法尼亚州立大学提出 ANOR：在 GPU 与 CXL 近存（PNM）之间按选择局部性分工——最近选中的条目在 GPU 缓存上算大部分注意力，缺失留在 PNM 上算，并与当前步的执行解耦更新。评估用 LLMServingSim：GPU kernel 在 H100 NVL 上剖析，PNM 时延按 M2NDP 建模。离线最大 batch、三套智能体负载平均，相对 HiSparse，Qwen3-4B-Thinking / Qwen3-30B-A3B-Thinking 的 decode 吞吐为 **2.6× / 2.1×**，相对以 PNM 为主的基线为 **2.3× / 1.7×**；两模型再平均后，摘要写为相对 HiSparse **2.3×**、相对 PNM 基线 **2.0×**。

## 动机
长上下文服务必须保留完整 KV，因为后续步可能选到别的条目。稀疏注意力每步只读一小部分，但容量仍会超出 HBM。把完整缓存放到 CXL-PNM 并在近存上算注意力，可以避开把缺失先经 PCIe 搬回 GPU；现有 CXL-PNM 的带宽远低于 GPU HBM，若把大部分注意力都放在 PNM 上，PNM 会成为瓶颈，GPU 只能空等。

## 方案
ANOR 利用「刚被选中的条目稍后还可能再被选中」这一局部性：

- GPU 缓存保存最近选中的条目，命中在 GPU 上计算。
- 缺失直接在 PNM 上计算，不必先经 GPU 面临接把 KV 取回再算，从而把缺失传输移出当前步临界路径。
- **有界缓存更新**：只更新到后续命中率趋于饱和的那一点，降低面向 GPU 的链路流量。
- **Early Streaming Buffer（ESB）**：在 PNM 做注意力时把更新数据捕获下来并流给 GPU，减少因 PNM DRAM 与 GPU 面临接带宽不匹配而重复读 DRAM。
- **自适应 cache factor**：按负载调整每请求 GPU 缓存大小，在命中率与 batch 之间折中。

评测配置：Qwen3-4B-Thinking 用一张 H100 NVL，Qwen3-30B-A3B-Thinking 用两张，主机为 Intel Xeon 6520P。四个 CXL-PNM 器件按模型给出，各四通道 DDR5-6400（200 GB/s）、512 GB，合计 2 TB 池；HiSparse 使用同等容量的主机内存池，两者到 GPU 都走 PCIe Gen5×16。负载为 SWE-chat、Open-SWE、OpenResearcher，系统评估回放 SeerAttention-R 轨迹，Top-2K。默认 30% 按新近排序的更新比例、每器件 8 MiB ESB。

## 量化结果
离线 decode（batch 扫到 4B 的 128、30B 的 256，输出长度取负载中位数，cache factor 固定 1.0），最大 batch 上三负载平均：

- 相对 HiSparse：**2.6×**（4B）、**2.1×**（30B）
- 相对 PNM 基线：**2.3×**（4B）、**1.7×**（30B）

在线 SWE-chat，请求按泊松过程以 5–20 requests/s 到达，注入 200 s 后跑完，prompt KV 已在后备内存中：

- 相对 cache factor 1.0 的 HiSparse，P50 TPOT 最高降到 **16.0×**（4B）与 **7.8×**（30B）；相对 PNM 基线最高 **10.8× / 5.8×**。
- 相对最好的固定大缓存 HiSparse（factor 4.0），中低到达率下 P50 TPOT 最高 **2.1×**；20 requests/s 时 ANOR 会降低 cache factor 以纳入更多请求，TPOT 接近该基线，同时并发 decode 请求多 **1.2–1.3×**。
- 20 requests/s 下，相对最好基线，完成延迟 P50 / P99 在 4B 上为 **2.7× / 2.8×**，在 30B 上为 **3.3× / 2.2×**。排队峰值低 **2.1× / 6.6×**，到达停止后队列早 **115 s / 43 s** 排空。
- 相对最好的静态 GPU–PNM 划分（约 60% GPU 份额之后开始变差），ANOR 仍快 **1.43×**。30% 更新比例下，相对 HiSparse 的 decode 延迟为 **2.55×**。
- 自适应 cache factor 在 20 requests/s 时把因子降到 2.8；对 30B，相对固定因子 4.0，每用户吞吐 **1.13×**，平均完成延迟降为 **1.21×**。

硬件开销用 CACTI 7.0 在 22 nm 建模，再经 DeepScaleTool 投影到 7 nm：每只 PNM 器件新增 **2.01 mm²**、平均动态功耗 **186 mW**（ESB 1.6981 mm² / 111.12 mW），四只合计 **8.04 mm²**、**0.74 W**。默认 30% 更新比例下，8 MiB ESB 几乎捕获全部更新数据；提到 40% / 50% 时，4B 上溢分别为 11.1% / 24.4%。

## 局限与解读
- 这是 **H100 NVL 剖析加 LLMServingSim / M2NDP 建模**，四个 CXL-PNM 器件不是硅片或整机实测。
- 稀疏选择轨迹来自 SeerAttention-R、Top-2K，所有系统共用同一组轨迹。
- 面积与功耗是 22 nm→7 nm 投影，只覆盖 ESB、驻留候选表和传输控制。
- 在线数字针对 SWE-chat 的到达过程；离线吞吐在固定 cache factor 1.0 下报告。

## 与 wiki 的关系
- [IndexerStage](/papers/indexerstage-indexerk-memory-tiers.md) — 同样面对稀疏注意力的容量墙，但把 Indexer-K 分页暂存到高带宽 backing，并在 16+16 张 H800 上实测；ANOR 把注意力计算本身拆到 GPU 与 PNM
- [XM-Sparse](/papers/xm-sparse-scale-up-memory-pool.md) — 把 KV 与 indexer 卸到 scale-up 内存池；ANOR 的后备层是带计算能力的 CXL-PNM
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — 把 CXL 从容量层推进到「缺失在近存上算完再更新 GPU 缓存」
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 记录 GPU 缓存、PCIe / CXL 链路与 PNM DRAM 之间的临界路径划分
- [Synapse](/papers/synapse-hbm-hbf-nmc-agentic.md) — 近存计算放在 HBF 上与 GPU 重叠；ANOR 的近存对象是 CXL-PNM 上的稀疏注意力缺失


2026-11-27：[L2C2](/papers/l2c2-chiplet-sparse-distributed-attention.md) 同样处理稀疏注意力下的 KV 访问，把分布式注意力放到封装上的芯粒阵列，并用上下文并行保存完整 KV 块。

# Citations
- [arXiv:2611.30417](https://arxiv.org/abs/2611.30417) — Ye 等（KAIST / SK hynix / Penn State）
- [raw stub](/raw/papers/anor-gpu-pnm-sparse-attention.md)
- [PDF](/raw/papers/ANOR_GPU_PNM_Sparse_Attention_2026.pdf)
