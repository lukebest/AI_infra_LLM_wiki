---
type: Paper
title: "LaFlash: Capacity-Driven Acceleration for Coding Agent Workflows via QLC-HBF"
description: "GIST / KAIST / Stanford — 用 QLC-HBF 把容量分给休眠 KV 保留；相对 SLC-HBF+BE 平均 7.04× 吞吐、10.96× 能量效率（HBFSim）"
tags:
- hbf
- flash
- kv-cache
- agentic-ai
- ai-agent
- serving
- inference
- memory
- hbm
- nvidia
- energy
- simulator
- llm
created: 2026-11-19
updated: 2026-11-19
timestamp: '2026-11-19T00:00:00Z'
paper_author: [Yuseon Choi, Eunjong Lee, Sanghyeon Park, Seongyon Hong, Sangjin Kim, Thierry Tambe]
year: 2026
venue: preprint
arxiv: '2611.22746'
sources:
  - raw/papers/LaFlash_QLC_HBF_Coding_Agents_2026.pdf
  - raw/papers/laflash-qlc-hbf-coding-agents.md
---

# LaFlash：用 QLC-HBF 的容量给编程智能体留下休眠 KV

## 一句话结论
GIST、KAIST 与 Stanford 提出 LaFlash：针对编程智能体「长上下文、短 decode、状态频繁休眠再唤醒」的特点，把多出来的闪存容量优先用来保留休眠 KV（Capacity-Driven Acceleration, CDA），再用会话分组和快页分配把 QLC 的长读延迟转成可利用的平面并行。扩展 HBFSim 的端到端评测里，相对 SLC-HBF + 批扩展（FlashAccel 风格映射 + CONCUR 风格并发管理），平均吞吐 **7.04×**、能量效率 **10.96×**；在已经做了 CDA 的 QLC-HBF 之上，再加 **2.36×** 吞吐、**1.59×** 能量效率。

## 动机
Loop / Graph Engineering 一类编程智能体工作流会把会话上下文和 KV 在活跃与休眠之间反复切换。状态被逐出后再唤醒，就要重新做 prefill；作者给出 100K 上下文时，重计算延迟可以比外部存储器取回高出三个数量级。现有服务引擎倾向于用多出来的容量做批扩展，但长上下文的 KV 无法跨请求共享，休眠状态一多还是会逐出。QLC 相对 SLC 有约 4× 容量，读延迟更长，需要更高的平面并行，同时写寿命更紧。

## 方案
CDA 在分配活跃并发时显式计入状态放大，把容量在「正在跑的请求」和「休眠状态保留」之间切开，用访存替换重计算。LaFlash 在 QLC-HBF 上落实这件事：Session Grouping 按活跃请求数和合计上下文长度给各会话组做均衡，并保持请求独占块分配与组内 FIFO；Fast-Page Allocation 利用 QLC 不同页类型的读延迟差异，补上组间残留不平衡。新生成的 KV 先在 HBM 缓冲，再按复用情况回写 NAND。

评测有两层：Python 逻辑仿真器去掉物理映射约束，只看 CDA；硬件评测扩展 [HBFSim](/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md)，前端换成编程智能体轨迹，并加入 QLC 页相关读时序。平台为 A100 + Qwen3-Coder-30B-A3B（单卡）、H100 + MiniMax-M2.7（四卡 TP/EP）、H200 + GLM-5.1（八卡 DP/EP）；保留 1 或 2 个 HBM 栈，用 HBF 替换 4 个栈，SLC/QLC 容量为 8×/32×。工作负载包括 FreeInference / Terminal-Bench 2.1 的 Loop Engineering 与 SWE-bench Pro 的 Graph Engineering，服务引擎为 vLLM。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 端到端平均（三套 GPU–模型，sessions/s 与归一化 sessions/J） | 相对 SLC-HBF+BE：**7.04×** 吞吐、**10.96×** 能量效率。SLC-HBF+CDA 相对 BE 为 **1.82×** 吞吐；QLC-HBF+CDA 为 **3.04×**。LaFlash 相对 QLC-HBF+CDA 再加 **2.36×** 吞吐、**1.59×** 能量效率 | Fig. 14 / §7.1 |
| 逻辑 CDA（去掉物理映射） | SLC-HBF+CDA 相对 SLC-HBF+BE，理想吞吐最高 **8.62×** | Fig. 15 |
| 相同 QLC-HBF+CDA 下的映射对照 | 相对 Ideal CDA：LaFlash 平均约 **68%** 吞吐，FlashAccel / HBFlex / Flint 为 **38% / 54% / 62%**。带宽/块利用率：LaFlash **63%/74%** | Fig. 16 |
| 消融（MiniMax-M2.7 Loop，相对 SLC-HBF） | 朴素 QLC-HBF **0.33×**；CDA **2.84×**；加会话分组 **5.31×**；再加快页分配 **6.18×** 吞吐、能量效率 **9.98×** | Fig. 17(a) |
| 写入寿命（均含 FCR/Warm） | KV 重计算写回把寿命从 **19.4 年** 打到 **0.29 年**；CDA 提到 **8 年**；HBM 缓冲再提到 **10.9 年**（相对 CDA +36.3%） | Fig. 17(b) |
| 推理 / 多轮聊天（Table 7） | Qwen3-Coder + Terminal-Bench：相对 HBM **12.5×**、相对 SLC **3.63×**。Qwen3-Thinking + Terminal-Bench：相对 HBM **2.42×**、相对 SLC **1.58×**。同模型 + ShareGPT：相对 HBM **2.19×**、相对 SLC **1.26×** | Table 7 |
| 相对 SSD 取回（Table 8，同为 2064 GB） | 相对 CachedAttention 式 GPU+HBM+SSD，端到端 **84×**（3.86 vs 0.0461 sessions/min） | Table 8 |
| 面积 | CBA CMOS 裸片综合 165.2 mm²，约占 OCP HBF 脚印 175.6 mm² 的 94.1% | Table 6 / §7.5 |

## 与已有 HBF 页的增量
已有页面主要讨论 SLC 组织下 HBF 何时划算、如何隐藏读延迟、以及 KV/专家在 HBM–HBF 之间怎么放，例如 [When Is HBF Cost-Effective](/papers/when-is-hbf-cost-effective-llm-inference.md)、[SlipStream](/papers/slipstream-hbf-gpu-prefetch.md)、[FLINT](/papers/flint-hbf-llm-inference.md)、[HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md)、[HBFSim](/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md)。本篇把容量用到编程智能体的休眠状态保留上，并针对 QLC 的长读延迟与写寿命给出映射与回写策略。对照对象是 FlashAccel / HBFlex / Flint 与批扩展；数字来自扩展后的 HBFSim，和上述工作的评测栈不宜直接横比。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把 QLC-HBF 容量接到活跃并发与休眠 KV 保留的分配上
- [Host-Tier KV on Static-Graph NPU](/papers/host-tier-kv-npu-agent-workflows.md) — 同样面对智能体反复 prefill；本篇走的是近存闪存保留而非宿主层 KV
- [HBFSim](/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md) — 本篇的硬件评测前端与 FTL 都改在这份模拟器上
- [FLINT](/papers/flint-hbf-llm-inference.md) / [HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md) — Fig. 16 的映射对照

## 开放问题
- 端到端数字来自扩展 HBFSim 与逻辑仿真器；控制逻辑只做了 45 nm 综合，没有在真实 QLC-HBF 器件上跑。
- MiniMax-M2.7 因每 token KV 更大，扩容后活跃并发仍然受限，逻辑收益更窄。
- 写寿命数字依赖 FCR/Warm 等放宽保持时间的技术；作者也写明 QLC-HBF 还要面对外围面积、读重试和保持退化。
- 1-2-4-8 等更长读延迟的编码会增加所需平面数，可能超出 OCP 脚印，需要和页编码、读延迟、外围面积一起设计。

# Citations
- [arXiv:2611.22746](https://arxiv.org/abs/2611.22746) — Choi, Lee, Park（GIST）；Hong（KAIST）；Kim（GIST，通讯）；Tambe（Stanford，通讯）
- [raw stub](/raw/papers/laflash-qlc-hbf-coding-agents.md)
- [PDF](/raw/papers/LaFlash_QLC_HBF_Coding_Agents_2026.pdf)
