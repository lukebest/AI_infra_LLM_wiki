---
type: Concept
title: Core Group (DRAM Access Synchronization)
description: 3D AI 芯片 core group：物理相邻 core 组内通过 hardware tracker 同步 DRAM 访问，缓解 row-buffer 冲突
tags:
- accelerator
- memory-bandwidth
- memory
- inference
- decode
- architecture
- mesh
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf
---

# Core Group（DRAM 访问同步）

## 定义

**Core group** 是 [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) 上的一项硬件-软件协同优化：将**物理相邻**的 AI core 划分为若干组，组内通过 **hardware request tracker** 同步 DRAM 请求，减少多 core 异步访问共享 tensor 导致的 **row-buffer 冲突**。

由 Voxel 论文（§4.4）提出，用于在增加 core 数量 scale FLOPS 时维持 DRAM 带宽利用率。

## 动机

3D AI chip 上单纯增加 core 数会：
- 更多 core 访问共享 tensor shard → 访问 **desync** → 同一 DRAM bank 内 row 交错访问
- Row-buffer 冲突加剧 → **DRAM 带宽利用率下降** → memory-bound decode 性能受损

这与 §2.3 讨论的「多 core 数据共享导致 row conflict」直接相关；software-aware tensor-to-bank placement（§4.3）解决放置问题，core group 解决 **并发访问时序** 问题。

## 机制

```
Core Group (size = 8)
┌────┬────┬────┬────┐
│ C0 │ C1 │ C2 │ C3 │  ← 物理相邻 core
├────┼────┼────┼────┤
│ C4 │ C5 │ C6 │ C7 │
└────┴────┴────┴────┘
         │
    Hardware Request Tracker
    （同步组内 DRAM 请求 dispatch）
```

- 组内 core 的 DRAM 请求经 **request tracker** 协调：在第 *i* 个请求被所有 core dispatch 完成前，不发起下一批请求
- 与 **software-aware tensor-to-bank mapping** 配合，可避免大部分不必要的 row conflict
- 默认探索配置中 **group size = 8**（见 [Voxel Simulator](/concepts/voxel-simulator.md) baseline）

## 实验结论（Voxel 论文）

| 场景 | 发现 |
|------|------|
| **无 core group** | 大 SA 或高 core count 设计 decode 性能差；SA 与 DRAM 利用率均低（Figure 15） |
| **有 core group** | 所有 core 配置均改善；core 数越高收益越大 |
| **1024 core, group size 8 vs 1** | LLM decode 最高 **57%** 加速 |
| **group size > 8** | 额外收益可忽略；**8 为 sweet spot** |
| **与 core scaling 协同** | 适当 group size 使 3D chip 可更有效 scale core 数（Figure 14d） |

Takeaway D2：scale core count 时，用简单 hardware logic（request tracker）同步同组 memory access；**8 core 一组** 可显著改善端到端性能与 DRAM 利用率。

## 与其他优化的关系

| 优化 | 解决的问题 | 层级 |
|------|-----------|------|
| [Software-aware tensor-to-bank mapping](/concepts/3d-stacked-ai-chip.md) | tensor 放置导致的 conflict | Compiler / placement |
| **Core group** | 多 core 并发访问时序导致的 conflict | Hardware + 局部同步 |
| Compute-shift | NoC 与 compute 重叠 | Compute paradigm |
| Dimension-ordered mapping | NoC hop 最小化 | Tile-to-core mapping |

Core group **不替代** tensor placement，二者互补。

## 适用工作负载

- **Decode / memory-bound**：收益最大（DRAM 利用率是瓶颈）
- **Prefill / compute-bound**：core group 非主优化路径；prefill 更依赖 compute-shift 与 NoC mapping

见 [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md)。

## 相关

- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — core group 所针对的架构
- [Voxel Simulator](/concepts/voxel-simulator.md) — 提出并评估 core group 的仿真框架
- [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) — 来源论文 §4.4
- [Graphcore IPU](/entities/graphcore-ipu.md) — Voxel 验证平台（非 core group 实现载体，但同论文）

# Citations

[1] [raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf](raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf)
