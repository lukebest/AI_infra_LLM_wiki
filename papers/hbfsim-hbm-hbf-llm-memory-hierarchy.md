---
type: Paper
title: "HBFSim: A Simulator for Exploring HBF in Memory Hierarchies for LLMs"
description: "MBZUAI RACS'26 — 事件驱动 HBM+HBF 仿真（主机侧 FTL、校准过的 vLLM 式调度）；HBM 放不下的数据由 HBF 供给比 host DRAM 快 11.0–19.0×；HBM 优先留给运行中序列的 KV；Llama-3.1-70B 峰值负载下 HBF 寿命 2.0–6.9 年"
tags:
- hbf
- hbm
- memory
- memory-bandwidth
- kv-cache
- inference
- decode
- moe
- storage
- simulator
created: 2026-10-20
updated: 2026-10-20
timestamp: '2026-10-20T00:00:00Z'
paper_author: [Jinheng Li, Guosheng Wang, Hongchao Du, Shangyu Wu, Qiao Li, Chun Jason Xue]
year: 2026
arxiv: '2610.23503'
venue: RACS 2026
sources:
  - raw/papers/HBFSim_HBM_HBF_LLM_Memory_Hierarchy_RACS26.pdf
  - raw/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md
---

# HBFSim（MBZUAI）：LLM 内存层级里的 HBF 仿真

> 与 wiki 已有的 [HBF-Sim（Accel-Sim 集成版）](/papers/hbfsim-extensible-hbf-simulator.md) 是两项独立工作：那篇偏 GPU 微架构端到端路径，本篇偏服务层语义 + 闪存管理 + 寿命。

## 一句话结论
HBF 能给加速器多一个数量级的本地容量，但只有在用法贴合闪存特性时才划算：容量不够时它远好于 host DRAM 和 SSD；HBM 应优先放运行中序列的 KV；KV 写入决定 HBF 寿命，按当前负载估算只有几年。

## 动机
- 八个 128K 上下文会话就能占满 H200 的 131 GiB HBM3e；70B 级长上下文服务可超过整台八卡节点容量。
- HBF 每栈容量为 HBM 的 8–16 倍、接口带宽相近，但页读是微秒级、写入异地更新、擦写次数有限；OCP 规范把地址映射、GC、磨损均衡交给主机软件，尚无公开 P/E 指标。

## 方案
- LLM 感知的事件驱动仿真器：同一仿真里建模 HBM、带主机侧闪存转换的 HBF、host DRAM / CXL SSD / NVMe SSD 容量层，由校准过的服务前端驱动（调度器对照 vLLM 0.26 校验）。
- 器件参数（论文表）：HBM4 栈 48 GiB、2.0 TB/s、读 42 ns；HBF 栈 512 GiB、1.5 TB/s、读 4 µs、编程 75 µs；host DRAM 经 PCIe 5.0 54 GB/s；CXL SSD 36 GB/s 链路；NVMe SSD 16 GB/s 链路。
- 负载：Llama-3.1-70B 与 Qwen3-235B-A22B decode，三种输入/输出长度组合。

## 效果（论文五条结论与数字）
1. 容量有压力时 HBF 最有价值：放不下 HBM 的数据由 HBF 供给，TPOT 比 host DRAM 低 **11.0–19.0×**、比 NVMe SSD 低 **86.6–154.1×**；工作集装得下时收益很小。
2. 常规缓存替换（4 MiB 行）不适合 HBM–HBF 分层：工作集超出 HBM 时各策略都有大量回填。Qwen3 Zipf 专家路由下，2 HBM + 6 HBF 时按地址切分仍胜出，衰减 LFU 慢 **1.07–1.10×**，LRU/FIFO 慢 **1.4–1.5×**。
3. KV 优先留在 HBM，只在容量压力下才落到 HBF；按需落盘在实验中无性能损失，主动迁移会产生多余写入。
4. 映射要保持闪存内部并行：按 extent 跨所有 plane 条带化，以很少的表内存达到页级映射效果；块级映射把一块固定在单 plane 上，decode 明显变慢。
5. 寿命是一阶约束：假设 SLC 100,000 P/E，Llama-3.1-70B 公开峰值负载下 HBF 寿命 **2.0–6.9 年**，与分担 KV 写入的栈数成正比。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBF 作为 HBM 与 host 之间的新层
- [Lachesis](/papers/lachesis-lifetime-aware-kv-hbm-hbf.md) — 按 KV 寿命放置以延长 HBF 寿命，与结论 3、5 一致
- [Hot–Cold HBM/HBF](/papers/hotcold-hbm-hbf-agentic-llm.md) — 热集放 HBM、冷池放 HBF 的另一实现
- [Agentic KV Residency](/papers/agentic-kv-residency-m365-production.md) — 生产侧几百 TB 驻留需求，正是 HBF 容量层的动机

## 开放问题
- HBF 时序与寿命参数仍是假设，作者说明会随公开器件数据更新 artifact。
- 只评测 decode；prefill 写入与 KV 交接对寿命的影响未覆盖。

# Citations
- Li et al., "HBFSim: A Simulator for Exploring HBF in Memory Hierarchies for LLMs", RACS 2026, arXiv:2610.23503. [raw](/raw/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md) · [PDF](/raw/papers/HBFSim_HBM_HBF_LLM_Memory_Hierarchy_RACS26.pdf)
