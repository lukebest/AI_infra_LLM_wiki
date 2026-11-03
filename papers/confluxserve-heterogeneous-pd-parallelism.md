---
type: Paper
title: "ConfluxServe: Heterogeneous Prefill–Decode Parallelism"
description: "Waterloo — 算子级异构共执行（线性共批不同 SP、attention 分路径）；生产负载 serving goodput 相对最强基线 1.26–1.62×"
tags:
- inference
- serving-system
- prefill
- decode
- parallelism
- throughput
- latency
- llm
- batching
- gpu
- scheduling
created: 2026-11-03
updated: 2026-11-03
timestamp: '2026-11-03T00:00:00Z'
paper_author: [Wenhao Chen, Hong Zhang]
year: 2026
venue: arXiv
arxiv: '2610.37810'
sources:
  - raw/papers/ConfluxServe_Heterogeneous_PD_Parallelism_2026.pdf
  - raw/papers/confluxserve-heterogeneous-pd-parallelism.md
---

# ConfluxServe：算子级异构 Prefill–Decode 并行

## 一句话结论
Prefill/Decode 资源互补却偏好不同并行度：分相执行浪费互补资源，共批又常被迫统一并行配置。**Conflux Parallelism (XP)** 在同一 batch 内让两阶段用不同并行度——**稠密线性算子跨不同 SP 共批，attention 分路径**（decode 本地、prefill 跨 rank SP）。ConfluxServe 在 TTFT/TBT SLO 下最大化集群 goodput，生产负载上相对最强基线 **1.26–1.62×**。

## 动机
- 资源视角：prefill 偏算力、decode 偏带宽/KV 容量，共执行能抬利用率。
- 并行视角：长 prefill 为 TTFT 倾向 scale-out；decode 满足 TBT 往往只需更窄执行组，过度 scale-out 增加通信、伤效率。
- 统一并行配置的共批与相隔离执行分别牺牲效率或利用率，形成 utilization–efficiency 困境。

## 方案
1. **Conflux Parallelism**：按算子拆异构执行路径；线性层（QKV/O/FFN）充分共批并容纳不同 SP；attention 不在同一调用内硬共批不同并行，decode attention 留本地、prefill attention 走 SP。
2. **空间复用**：在可重复窗口内协调两阶段 attention，稳定跨相位干扰。
3. **ConfluxServe**：共享线性算子保留 CUDA Graph；attention 复用靠 SM 划分；关键路径时延模型 + 拟合估计；水位线式 prefill 分发；按共执行机会选 decode residency rank；按 TTFT 紧急度优先待处理 prefill。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| Serving goodput vs 最强基线（生产负载） | **1.26–1.62×** |

## 与 wiki 的关系
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 把「并行度也随阶段分歧」落到算子级异构共执行
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 与跨机 PD 解耦正交：同实例内保留共执行收益
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构不在设备类型，而在同 batch 内的并行配置
- [HAWK](/papers/hawk-gpu-npu-heterogeneous-kv-transfer.md) — 另一条异构 PD 路径（跨设备）；ConfluxServe 侧重同集群内 SP/共批

## 开放问题
- 摘要给出的是 goodput 区间；不同模型宽度与互联拓扑下的临界 SP 组合需对照全文图表。
- 与完全解耦 P/D 池 + 远端 KV 池（Mooncake/KVLearn）的组合未报告。

# Citations
- [arXiv:2610.37810](https://arxiv.org/abs/2610.37810) — Chen & Zhang, Waterloo, 2026
- [raw stub](/raw/papers/confluxserve-heterogeneous-pd-parallelism.md)
