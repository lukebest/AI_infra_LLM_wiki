---
type: Raw Source
title: "Flux: Optimal Scheduling of Optical Circuit Switches for LLM Training"
description: "Flux 原始论文来源：LLM 训练 workload-aware OCS MILP 调度。"
timestamp: '2026-09-25T00:00:00Z'
source_url: https://arxiv.org/abs/2609.25949
arxiv: '2609.25949'
ingested: 2026-09-25
sha256: 6961d63e8c829aeeff0562e6e9874b6a1d83ac0e28a5122f2d4c022988aac127
---

# Flux: Optimal Scheduling of Optical Circuit Switches for LLM Training

**Authors:** Arno Troch, Seyyidahmed Lahmer, Abubakr Nada, Jeroen Famaey, Michael Peeters  
**Affiliation:** IDLab, University of Antwerp - imec; imec  
**PDF:** [Flux_OCS_Scheduling_LLM_Training_2026.pdf](Flux_OCS_Scheduling_LLM_Training_2026.pdf)  
**arXiv:** [2609.25949](https://arxiv.org/abs/2609.25949)（2026-09-22，cs.NI/cs.DC）

## 问题

OCS 高带宽但有非零重配置延迟。既有调度多把电路安排当成纯网络问题，用聚合流量矩阵定拓扑与时隙，丢掉 LLM 训练图的执行顺序，导致通信空转、NIC 缓冲膨胀。

## 方法要点

- 把整次 training iteration 的 compute/communication 依赖图与 OCS 重配置一起建模为 MILP（Gurobi）。
- 相对 RotorNet（周期轮转）与 BvN（流量矩阵分解后周期）做对照。
- 仿真：ASTRA-sim + 内部 OCS；Llama 3 8B、8 GPU、2 OCS、每 GPU 每开关 800 Gbps 双向；重配置延迟 1 μs–1 ms；TP4×DP2。

## 摘录数字（仅论文给出）

- 摘要：相对传统周期 OCS 调度，训练 iteration 时间最高 **10×** 更低；峰值 NIC buffer **超过三个数量级**更低。
- 评测正文：Flux 在 1 μs–1 ms 重配置延迟区间 consistently 最低 iteration time；相对 RotorNet/BvN，峰值 on-chip NIC memory **more than three orders of magnitude**。

**Working page:** [Flux](/papers/flux-ocs-scheduling-llm-training.md)  
**Related:** [TPU v4 OCS](/concepts/tpu-v4-ocs-reconfigurable-fabric.md)、[LLM Training Collectives](/concepts/llm-distributed-training-collectives.md)
