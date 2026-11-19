---
type: Raw Source
title: "LaFlash: Capacity-Driven Acceleration for Coding Agent Workflows via QLC-HBF"
source_url: https://arxiv.org/abs/2611.22746
pdf: LaFlash_QLC_HBF_Coding_Agents_2026.pdf
retrieved: 2026-11-19
ingested: 2026-11-19
org: GIST / KAIST / Stanford
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.22746)

As large language models (LLMs) evolve toward agentic AI, coding agents are emerging as memory-intensive workloads that repeatedly reuse persistent states, including contexts and KV caches. Emerging agentic workflows, including Loop/Graph Engineering, cause state amplification through frequent active/dormant transitions, increasing memory pressure. Evicted states incur costly recomputation upon reactivation, particularly under long-context, short-decode workloads. This motivates Capacity-Driven Acceleration (CDA), which explicitly accounts for state amplification to allocate memory capacity between active concurrency and dormant-state retention, replacing recomputation with memory access. In this work, we propose LaFlash, a High-Bandwidth Flash (HBF) architecture that exploits the large capacity of Quad-Level Cell (QLC)-based flash to realize CDA. However, QLC's long read latency demands massive read parallelism under irregular state reactivation and varying context lengths, while limited write endurance constrains placement. LaFlash introduces Session Grouping to balance active request counts and aggregate context lengths across groups, sustaining read parallelism and block utilization through request-exclusive allocation. Furthermore, Fast-Page Allocation exploits QLC's read-latency heterogeneity to mitigate residual inter-group imbalance and sustain bandwidth utilization. On end-to-end coding agent workloads, LaFlash achieves 7.04× higher throughput and 10.96× higher energy efficiency over SLC-HBF with batch expansion, and 2.36× higher throughput over QLC-HBF with CDA. HBM buffering further reduces unnecessary NAND writes, improving QLC write endurance. These results demonstrate the benefits of jointly optimizing state retention and physical data placement for capacity-driven acceleration.

# Excerpts / key facts

- Authors: Yuseon Choi、Eunjong Lee、Sanghyeon Park、Sangjin Kim（通讯，GIST）；Seongyon Hong（KAIST）；Thierry Tambe（通讯，Stanford）。arXiv:2611.22746，cs.AR，2026-11-18 公告（提交标注 17 Nov 2026）。预印本。
- 评测是仿真：Python 逻辑仿真器隔离 CDA 的逻辑收益；硬件评测扩展 HBFSim，前端换成 coding agent 轨迹驱动，并改 C++ host FTL、加入 QLC 页相关读时序。控制逻辑用 RTL 对照行为级 QLC 阵列（4/6/14/14 µs 页相关延迟），45 nm、400 MHz 综合。
- 平台（Table 1）：A100 + Qwen3-Coder-30B-A3B（1 GPU）；H100 + MiniMax-M2.7（四卡 TP/EP）；H200 + GLM-5.1（八卡 DP/EP）。A100/H100 保留 1 个 HBM 栈、H200 保留 2 个，用 HBF 替换 4 个栈；HBF 峰值带宽与对应 HBM 对齐，SLC/QLC 容量为 8×/32×，对标 OCP HBF Speed Grades 1 和 2。
- 工作负载：Loop Engineering（FreeInference、π Terminal-Bench 2.1）与 Graph Engineering（SWE-bench Pro）；框架 Claude / Hermes / LangGraph，服务引擎 vLLM。正文概括：平均会话上下文约 106K token，每轮 decode 约 386 token，每轮约 1.15 次工具调用。
- QLC 读延迟模型：t_R(n) = t_fixed + n t_sense。按公开的 16 KiB 下 48/76/134/228 µs（1-2-4-8 sensing）拟合，t_fixed : t_sense ≈ 1 : 1。
- 端到端（Fig. 14，sessions/s 与归一化 sessions/J，三个 GPU–模型配置平均）：相对 SLC-HBF+BE（FlashAccel 风格映射 + CONCUR 风格并发管理）吞吐 **7.04×**、能量效率 **10.96×**。SLC-HBF+CDA 相对 SLC-HBF+BE 吞吐 **1.82×**；QLC-HBF+CDA 到 **3.04×**。LaFlash 在 QLC-HBF+CDA 之上再加 **2.36×** 吞吐、**1.59×** 能量效率。
- 逻辑 CDA（Fig. 15，去掉物理映射约束）：SLC-HBF+CDA 相对 SLC-HBF+BE 理想吞吐最高 **8.62×**。
- 物理映射（Fig. 16，相同 QLC-HBF+CDA，会话组 128 planes）：相对 Ideal CDA，LaFlash 平均达到约 **68%** 端到端吞吐，FlashAccel / HBFlex / Flint 分别为 **38% / 54% / 62%**。带宽/块利用率：LaFlash **63%/74%**，FlashAccel 32%/83%，HBFlex 46%/79%，Flint 63%/55%。
- 消融（Fig. 17(a)，MiniMax-M2.7 Loop）：朴素 QLC-HBF 相对 SLC-HBF 吞吐 **0.33×**；CDA 到 **2.84×**；会话分组到 **5.31×**；再加快页分配到 **6.18×** 吞吐，能量效率相对 SLC-HBF **9.98×**。
- 写入寿命（Fig. 17(b)，均含 FlashAccel 的 FCR/Warm）：把 KV 重计算写回会把寿命从 **19.4 年** 降到 **0.29 年**；CDA 提到 **8 年**；HBM 缓冲再提到 **10.9 年**（相对 CDA +36.3%）。
- Table 7：Qwen3-Coder / Terminal-Bench 相对 HBM **12.5×**、相对 SLC **3.63×**；Qwen3-Thinking / Terminal-Bench 相对 HBM **2.42×**、相对 SLC **1.58×**；Qwen3-Thinking / ShareGPT 相对 HBM **2.19×**、相对 SLC **1.26×**。
- Table 8：同容量下相对 CachedAttention 式 GPU+HBM+SSD，端到端吞吐 **84×**（3.86 vs 0.0461 sessions/min，总容量同为 2064 GB；峰值聚合带宽 2048 vs 14.7 GB/s）。
- 开销：Table 6 给出每 GPU（A100）元数据 CDA State 28.3 KB、Session Group 7.5 KB，页映射表 1,707 KB（正文另写会话/休眠/容量分配共 11.2 KB、页映射表 1.5 MB）。CBA CMOS 裸片综合面积 165.2 mm²，约占 OCP HBF 器件脚印 175.6 mm² 的 94.1%。
