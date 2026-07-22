---
type: Concept
title: TPU v4 OCS Reconfigurable Fabric
description: Jouppi et al. ISCA 2023 — TPU v4 pod 光电路交换（OCS）可重构拓扑；4096-chip；topology-as-software；vs 固定 torus/mesh
tags:
- tpu
- ocs
- photonic
- reconfigurable
- scale-up
- topology
- google
- llm
timestamp: '2026-07-22T00:00:00Z'
created: 2026-07-22
sources:
- raw/articles/paper-deepdive-day-07.md
---

# TPU v4 OCS Reconfigurable Fabric（TPU v4 光可重构互连）

Jouppi et al., **ISCA 2023**（+ v5p 报告）。paper-deepdive **Day 7**：[raw/articles/paper-deepdive-day-07.md](raw/articles/paper-deepdive-day-07.md)。摘要：[papers/tpu-v4-optically-reconfigurable.md](/papers/tpu-v4-optically-reconfigurable.md)。

哲学：**Topology is a function**——用 **Optical Circuit Switch (OCS)** 在运行时把 4096-chip pod 的逻辑拓扑切成更适合 workload 的形态（训练偏 torus/collective，推理偏低维 mesh）。

## 关键数字（笔记量级）

| 项 | 值 |
|----|-----|
| Chip | ~275 TFLOPS BF16 / chip（7nm） |
| Pod | **4096** chips ≈ 1.1 PFLOPS BF16 |
| Supercomputer | 9 pods ≈ **36K** chips ≈ **1.1 EFLOPS** |
| OCS 切换 | ~**100 ms** 级（远慢于 packet hop） |
| 光学能效 | 笔记称 ~**1 pJ/bit** 量级 vs packet switch 更高 |

有效带宽：可重构 + 适配 collective → 笔记称 pod 内可达很高利用率（相对固定拓扑的 30–50% 有效带宽叙事）。

## 相对前序论文

| Day | 关系 |
|-----|------|
| 4 Balfour | 固定拓扑下 mesh Pareto；可重构使**每个 workload 选自己的 Pareto 点** |
| 6 Kim Clos | 高基数/多路径；OCS 是 **全局自适应** 的物理实现（换拓扑而非 per-packet） |
| 5 VC/WH | OCS 电路交换段可绕开 packet 死锁问题 |
| 1 FRED | 为 AllReduce 选更优逻辑拓扑（直径/流量匹配） |

对照路线：[NVLink/NVSwitch](/concepts/nvlink-nvswitch-scale-up-fabric.md)——固定 fat-tree + 极高每链路带宽，拒绝运行时换拓扑。

## 与 WSE

| | TPU v4 pod | [Cerebras WSE](/entities/cerebras-wse.md) |
|--|------------|------------------------------------------|
| Scale-up 边界 | 4096 chip + OCS | 单晶圆 ~90 万 PE |
| 拓扑 | 可重构 4D torus 族 | 固定 2D Mesh |
| 介质 | 电 + 光电路 | 片上电 Mesh |

研究启发：可重构 wafer/逻辑拓扑；**Pod = scale-up boundary** 的工程定义。

## 相关页面

- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 对立哲学
- [High-Radix Clos Adaptive Routing](/concepts/high-radix-clos-adaptive-routing.md)
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — 光互连
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)
- [Multi-plane Clos Topology for AI Training](/concepts/multi-plane-clos-topology.md)
- [Paper Deep-Dive Map](/summaries/paper-deepdive.md)

# Citations

[1] [raw/articles/paper-deepdive-day-07.md](raw/articles/paper-deepdive-day-07.md) — TPU v4 OCS 精读（Day 7）
