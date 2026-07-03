---
type: Entity
title: Graphcore IPU
description: Graphcore Colossus Mk2 IPU：1472 全互联 core、896 MB 分布式 SRAM，Voxel 论文用于 3D AI chip 仿真验证
tags:
- graphcore
- accelerator
- inference
- mesh
- sram
- memory-bandwidth
- benchmark
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf
---

# Graphcore IPU (Intelligence Processing Unit)

Graphcore 的 AI 加速器产品线，以 **Colossus** 架构为核心：大量简单 core 全互联，每 core 配本地 SRAM，形成**分布式内存空间**而非 HBM 统一寻址。Hot Chips 2021 披露的 **Colossus Mk2 IPU** 是 Voxel 论文选用的 silicon 验证平台。

## Colossus Mk2 关键规格

| 参数 | 数值 |
|------|------|
| AI core 数 | **1,472**（全互联） |
| 片内互连总带宽 | **7.8 TB/s** |
| 分布式 SRAM 总容量 | **896 MB** |
| 分布式 SRAM 聚合带宽 | **62 TB/s** |
| 架构特点 | 每 core 本地 SRAM；core 间经 NoC 访问远端 SRAM |

单颗 operator 的 tensor 可完整放入片上分布式内存，适合 emulate 3D AI chip 的 **distributed DRAM bank** 访问模式。

## 与 wiki 中其他加速器对比

| 维度 | Graphcore IPU Mk2 | Cerebras WSE | Groq LPU |
|------|-------------------|--------------|----------|
| Core 规模 | 1,472 | ~900K PE | 256/chip |
| 内存模型 | 分布式 per-core SRAM | 分布式片上 SRAM | 片上 SRAM |
| 互连 | 全互联 NoC | 24-color mesh | C2C plesiosynchronous |
| 典型用途 | 训练/推理（Poplar） | 大模型训练/推理 | 低延迟 decode |

与 [Cerebras Wse](/entities/cerebras-wse.md) 同属 **多 core + 分布式内存** 范式，但 IPU 规模更小、更适合作 research emulator。

## Voxel 论文中的验证角色

尚无商用 3D-stacked AI chip，Voxel 作者在 IPU Mk2 上构建 **hardware emulator**：

```
960 core  → 模拟 3D AI chip 的 AI core
512 core  → 模拟分布式 DRAM bank（数据存于对应 core SRAM）
```

验证流程：
1. **Emulated Time**：在 IPU 上执行，数据从 SRAM 加载（无 DRAM latency）
2. **Emulated Time + DRAM Latencies**：replay IPU trace，叠加 Ramulator DRAM 延迟
3. **Voxel Simulated Time**：Voxel 端到端仿真

Llama2-13B、Gemma2-27B、OPT-30B、Llama3-70B、DiT-XL 上，Voxel 与带 DRAM 延迟的 emulator 误差 **0.24%–6.8%**。纯 SRAM emulator 平均快 **12.7%**（SRAM 任意 access pattern 均可满带宽）。

详见 [Voxel Simulator](/concepts/voxel-simulator.md)、[Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md)。

## 相关页面

- [Voxel Simulator](/concepts/voxel-simulator.md) — 以 IPU 为验证平台的 3D AI chip 仿真器
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — IPU emulator 所模拟的目标架构
- [Cerebras Wse](/entities/cerebras-wse.md) — 同类分布式内存 wafer-scale 加速器
- [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md) — T10 rTensor 编译器（Cannon 形式化）
- [Deterministic Execution](/concepts/deterministic-execution.md) — IPU 编译器调度与数据流执行

# Citations

[1] [raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf](raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf)
[2] Simon Knowles, "Graphcore Colossus Mk2 IPU," IEEE Hot Chips 33, 2021.
