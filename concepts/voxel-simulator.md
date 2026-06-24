---
type: Concept
title: Voxel Simulator
description: Voxel：编译器感知的 3D AI 芯片端到端仿真框架，支持 compute paradigm / mapping / NoC / DRAM 协同探索
tags:
- architecture
- benchmark
- inference
- accelerator
- compiler
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf
---

# Voxel Simulator

## 定义

**Voxel** 是 UIUC 提出的 **compiler-aware、event-driven** 3D AI 芯片端到端仿真框架，用于 LLM inference 的软硬件协同设计空间探索。相对现有工具（TimeLoop、AccelSim、LLMCompass 等），Voxel 支持 **分布式 DRAM 非均匀访问**、**自定义 compute paradigm**、**tile-to-core / tensor-to-bank mapping**，并可仿真完整 LLM 工作流。

## 设计目标

1. **Software awareness** — 反映 tiling、mapping、compute paradigm 对性能的影响
2. **Accurate behaviors** — 细粒度建模每个 DRAM bank、AI core、NoC link
3. **Fast simulation** — 数百 core + 数百 operator 的 LLM 仍可快速评估
4. **Reliable statistics** — 可与真实 silicon 交叉验证

## 软件接口

ML compiler 通过三类原语指定执行计划：

| 函数 | 作用 |
|------|------|
| `compute(op_tile, core_id)` | 指定 operator tile 在哪个 core 执行 |
| `copy_data(src, dst, size)` | core↔core 或 core↔DRAM 数据搬运 |
| `sync(cores)` | core 间同步 barrier |

Voxel 据此构建 **execution event graph**；兼容 XLA 类 compiler（仅需为每个 tile 调用 `compute()`）。

## 仿真栈

```
ML Compiler → Execution Graph → 事件分发
                                    ├─ AI Core: Scale-Sim v3（VU / SA / SRAM）
                                    ├─ NoC: hop 数 + 带宽共享
                                    └─ DRAM: Ramulator 2.0（per-channel 请求队列）
```

**加速技巧**：结构等价的 memory access pattern 缓存复用；LLM trace **99.91% cache hit**（每 pattern ~1100× 复用）。

**热建模**：跟踪 power density（默认 **0.7 W/mm²**），超限时降频；避免 DRAM refresh 惩罚干扰 pattern 分析。

## 与现有 simulator 对比

Voxel 相对 SOTA 的独特支持（Table 1）：

- 非均匀分布式 DRAM 访问
- 自定义 compute paradigm（SPMD / dataflow / compute-shift）
- Software 自定义 tile-to-core / tensor-to-bank mapping
- 完整 LLM 快速仿真

## 验证方法

无商用 3D AI chip → 用 [Graphcore IPU Mk2](/entities/graphcore-ipu.md) 构建 emulator：
- 960 core 作 AI core，512 core 模拟 DRAM bank
- 对比 Voxel Simulated Time vs IPU Emulated Time + DRAM latency replay
- 多模型误差 **0.24%–6.8%**（Llama2-13B、Gemma2-27B、OPT-30B、Llama3-70B、DiT-XL）

## 默认探索配置（论文 baseline）

| 参数 | 默认值 |
|------|--------|
| Core 数 | 256 |
| DRAM 总带宽 | 12 TB/s |
| NoC 拓扑 | 2D mesh |
| NoC link BW | 32 B/cycle |
| Per-core SRAM | 2048 KB |
| Systolic array | 32×32 |
| Core group size | 8（见 [Core Group](/concepts/core-group-dram-access.md)） |
| DRAM 容量 | 192 GB（8 layer × 16 bank/layer） |
| 频率 | 1.6 GHz |
| Batch / seq | 32 / 2048, BF16 |

## 相关

- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Voxel 建模的目标架构
- [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) — 论文全文摘要与 takeaway 表
- [Graphcore IPU](/entities/graphcore-ipu.md) — 验证平台规格与 emulator 划分
- [Core Group (DRAM Access Synchronization)](/concepts/core-group-dram-access.md) — baseline 中的 group size 参数
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — Voxel 区分 prefill/decode 的设计空间结论

# Citations

[1] [raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf](raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf)
