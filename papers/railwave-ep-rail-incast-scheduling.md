---
type: Paper
title: "RailWave: Adaptive Spatial and Temporal Scheduling for Expert-Parallel Communication"
description: "中山大学等 — DeepEP 之上的 EP 通信层：源端 RailBalance 跨 Rail 均衡 + 可复用循环置换波次压 incast + 离线标定选择器；GLM-4.5-Air 回放 P50 通信 H800 2.02–5.84×、H20 1.74–4.36× vs Native"
tags:
- moe
- expert-parallelism
- communication
- collective
- scale-out
- rdma
- congestion-control
- scheduling
- training
- gpu
- nvidia
- networking
created: 2026-10-06
updated: 2026-10-06
timestamp: '2026-10-06T00:00:00Z'
paper_author: [Chutian Wang, Wenhao He, Jingmin Zhu, Qingyu Yin, Heng Xu, Xiuyu Li]
year: 2026
arxiv: '2610.03415'
sources:
  - raw/papers/RailWave_EP_Rail_Incast_Scheduling_2026.pdf
  - raw/papers/railwave-ep-rail-incast-scheduling.md
---

# RailWave：EP 通信的空间（Rail）+ 时间（波次）整形

## 一句话结论

专家路由与放置都固定后，MoE all-to-all 仍会因 **单 Rail 过热** 和 **receiver incast** 变慢。RailWave 在 DeepEP 之下"只改执行、不改需求矩阵"：源端本地把流量均摊到可用 Rail，再用拓扑派生的循环置换把节点对分波次发送限制 fan-in，并按每相位流量特征选路径。GLM-4.5-Air 训练回放上 P50 通信 **H800 2.02–5.84×、H20 1.74–4.36×**（vs Native DeepEP）。

## 动机

- Rail-optimized 集群：节点内 NVLink/NVSwitch + 每节点 R 条 scale-out Rail。专家负载均衡 ≠ Rail 均衡：900 个 step–layer 样本中，专家负载不均对源/目的 Rail 不均的线性解释力仅 **R² = 0.019 / 0.296**；专家 max/mean 都在 8.2–8.4 的六个样本，最忙目的 Rail 份额 **15.5–24.1%** 不等。
- 同样的 rank-to-rank 需求、仅改并发节点对，45 层 P50 dispatch–combine 延迟和从 **1.801 s → 3.009 s（+67.1%）**——incast 单独就是一大块。
- EPLB/MoonEP/UltraEP 等改的是逻辑需求 D；FAST 用需求相关 Birkhoff 调度需全局同步且每相位重建。

## 方案

1. **RailBalance（空间）**：对每个节点对 (s,d) 在可用 Rail 集上给出相差至多 1 条记录的配额，按确定性余数轮转；超额记录映射到不足 Rail 的 proxy（无原子分配）；Rail 对称拓扑下源端 egress 均衡即得 ingress 均衡，无需目的端交换配额。
2. **可复用置换调度（时间）**：N 节点 N−1 个波次，π_k(s) = (s+k) mod N，每波每节点至多 1 出 1 入；计划只依赖组成员，初始化一次、跨相位复用。
3. **四条执行路径 + 标定选择器**：Native / Rail-only / Permutation-only / Joint（波内再做 RailBalance）；特征 = 每 GPU 远端载荷 B、全局源 Rail 偏斜 ρg、接收集中度 κ；离线锚点邻域内复用测得的最优路径，否则回落 Joint。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 平台 | H800、H20 各 **4 节点×8 GPU = 32 GPU**；GLM-4.5-Air（106B）DAPO-Math-17k 训练路由回放，全部 **45** MoE 层；Ring/Moderate/Extreme 三种发送模式 |
| P50 通信 vs Native | H800 **2.02–5.84×**，H20 **1.74–4.36×**；P95/P99 同样保持 |
| Joint vs 更好的单机制（H800） | Moderate **1.44×**，Extreme **1.97×** |
| NIC 份额（H20 Moderate） | Native **54.12% / 24.33% / 14.85% / 6.69%** → Rail-only / Joint 近似均分 |
| 高偏斜高集中样例 | Joint **4.11 ms** vs Permutation-only **10.96 ms**、Rail-only **73.28 ms** |
| 选择器（12 个未见请求） | 4 次切离 Joint，中位延迟再降 **5.7–16.4%**（**1.061–1.196×**）；其余 8 次回落 Joint |
| 对比基线 | 还与 NCCL all_to_all_single 及开源 FAST 比较（见原文图 4–6） |

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP all-to-all 物理执行层优化
- [Multi-Plane Clos Topology](/concepts/multi-plane-clos-topology.md) — rail/多平面网络的负载均衡与 incast
- [GPU-Initiated Communication Dissected](/papers/gpu-initiated-communication-dissected.md) — 底层 IBGDA 机制成本；RailWave 是其上的流量整形
- [MegaFlux](/papers/megaflux-skew-resilient-moe-megakernels.md) — 上层用热专家复制改需求，RailWave 在需求固定后改执行，可叠加
- [ThunderEP](/papers/thunderep-pcie-consumer-gpu-moe.md) — 另一端：无 RDMA 的消费卡 EP 通信

## 局限与开放问题

- 只测通信区间（GPU event），CPU 规划/索引/预打包不计入；未报端到端训练 step 加速。
- 规模仅 4 节点；循环置换 N−1 波在 64+ 节点时波数与串行化开销如何？
- 依赖 Rail 对称拓扑；非对称/故障 Rail 下的配额与 incast 界需额外处理。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.03415) — Wang et al., arXiv:2610.03415
[2] [raw stub](raw/papers/railwave-ep-rail-incast-scheduling.md)
[3] [Code](https://github.com/CyberSecurityErial/RailWave-EP)
