---
type: Paper
title: "Flux: LLM 训练的 OCS 最优调度"
description: "把整次 training iteration 的 compute/通信依赖与 OCS 重配置建成 MILP；相对周期 RotorNet/BvN，iteration 最高 10×、峰值 NIC buffer >1000×。"
tags:
- architecture
- training
- llm
- ocs
- optical
- photonic
- interconnect
- scheduling
- networking
- gpu
created: 2026-09-25
updated: 2026-09-25
timestamp: '2026-09-25T00:00:00Z'
paper_author: [Arno Troch, Seyyidahmed Lahmer, Abubakr Nada, Jeroen Famaey, Michael Peeters]
year: 2026
arxiv: '2609.25949'
sources:
  - raw/papers/Flux_OCS_Scheduling_LLM_Training_2026.pdf
  - raw/papers/flux-ocs-scheduling-llm-training.md
---

# Flux：LLM 训练的 OCS 最优调度

## 一句话结论

Flux 用 MILP 把整次 LLM training iteration 的计算/通信依赖与光电路开关（OCS）重配置绑在同一张日程上；相对 RotorNet / BvN 等周期调度，摘要称训练 iteration 时间最高 **10×**、峰值 NIC buffer **超过三个数量级**（>1000×）。仿真为 Llama 3 8B、8 GPU、2 OCS、每链路 800 Gbps，重配置延迟扫 **1 μs–1 ms**。

## 动机：流量矩阵丢掉了训练图的时间顺序

OCS 提供确定性高带宽路径，但换拓扑有非零重配置延迟。既有工作常把电路调度当成纯网络问题：用一段时间内的**聚合流量矩阵**决定配哪些电路、何时轮转（RotorNet 需求无关周期轮转；BvN 对流量矩阵做置换分解后周期）。对 LLM 训练而言，通信发生在严格依赖的时刻——矩阵求和抹掉顺序后，可能在加速器空等数据时仍在传大流量，也可能在电路未就绪时就把包堆进 NIC，抬高缓冲峰值。目标应从「网络完成时间」换成「端到端 iteration 墙钟」。

## 方案

### 1. Workload 图 + 系统模型

一次 iteration 建模为带计算与点对点通信任务的依赖图；系统为 \(n\) 加速器与 OCS 集合 \(S\)。每个通信任务分配到某开关上的电路；同一开关上共享端点的任务之间需插入重配置延迟 \(\tau\)。目标是最小化 makespan \(\max_v (t_v + p_v)\)。

### 2. MILP：固定序与自由序重配置

对图中有先后关系的冲突对，约束强制重配置开销；对不可比任务引入二进制序变量，决定谁先占电路。求解器用 Gurobi；得到的电路状态序列交给离散事件仿真重放。

### 3. 仿真栈与基线

基于改过的 ASTRA-sim + 内部 OCS 仿真器；Chakra 风格 trace 来自 Llama 3 8B。硬件：8 GPU、\(s=2\) OCS，每 GPU 到每开关一条 **800 Gbps** 双向链路；计算用 Kelis 层次 roofline 的 A100。基线：RotorNet（Direct / VLB，90% duty cycle）与 BvN 流量矩阵分解调度；\(\tau \in \{1\,\mu\mathrm{s}, 10\,\mu\mathrm{s}, 100\,\mu\mathrm{s}, 1\,\mathrm{ms}\}\)，8/16 layer、TP4×DP2。

## 量化结果

摘要与 §4 一致的主张（图 2 为曲线，正文未再给逐点表格）：

- **Iteration time**：Flux 在扫过的重配置延迟上 consistently 最低；摘要相对传统周期调度最高 **10×**。
- **Peak on-chip NIC memory**：相对 RotorNet/BvN **more than three orders of magnitude**（>1000×）。
- **重配置次数**：更少重配置≠更好——RotorNet 在低 \(\tau\) 时重配置更多但 iteration 仍可竞争；BvN 重配置更少但墙钟与缓冲更差。关键是重配置是否对准有用电路，以及是否能藏在计算后。

## 局限与解读

- 规模为 8 GPU / 2 OCS 的仿真，非百机柜实测；MILP 精确求解最坏指数，论文承认大规模需启发式。
- 数字峰值来自摘要与定性正文；图 2 对数坐标未在文中再摘逐点 ms/KB。
- NIC 缓冲假设「无限」以便量峰值，实际硬件有容量上限。

Flux 把 [TPU v4 OCS](../concepts/tpu-v4-ocs-reconfigurable-fabric.md) 的「拓扑可软件化」推进到 **按训练图时刻表排电路**；相对仅优化集体算法的 [LLM Distributed Training Collectives](../concepts/llm-distributed-training-collectives.md)，它把旋钮放在光层调度，也落在 [Interconnection Network Design Space](../concepts/interconnection-network-design-space.md) 的应用→拓扑时间维。

# Citations

1. Troch, A., Lahmer, S., Nada, A., Famaey, J., Peeters, M. “Flux: Optimal Scheduling of Optical Circuit Switches for LLM Training.” arXiv:2609.25949, 2026. [arXiv](https://arxiv.org/abs/2609.25949)
2. [本地原文 PDF](../raw/papers/Flux_OCS_Scheduling_LLM_Training_2026.pdf)；[原始来源记录](../raw/papers/flux-ocs-scheduling-llm-training.md)
