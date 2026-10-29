---
type: Concept
title: 3D-Stacked AI Chip
description: 3D 堆叠 AI 芯片：TSV 垂直堆叠 DRAM bank 于 AI core 之上，分布式内存与专用总线带来带宽扩展与利用率新挑战
tags:
- accelerator
- chiplet
- memory-bandwidth
- memory
- noc
- interconnect
- inference
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-06-24
updated: 2026-10-29
sources:
- raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf
---

# 3D-Stacked AI Chip（3D 堆叠 AI 芯片）

## 定义

将 **DRAM bank 网格垂直堆叠** 在 AI core + NoC 计算层之上，通过高密度 **TSV（Through-Silicon Via）** 为每个 core 提供到本地 bank 的专用数据通路。与 2.5D 封装（die 并排、带宽受 perimeter 限制）不同，3D 集成的连接数随 **die 面积** 扩展，memory bandwidth 可与 compute 同步 scale。

## 典型架构

```
┌─────────────────────────────────────┐
│  DRAM Bank Grid（多层，TSV 下行）      │
├─────────────────────────────────────┤
│  NoC（mesh / torus / all-to-all）     │
├─────────────────────────────────────┤
│  AI Core × N                         │
│  Vector Unit + Matrix Unit + SRAM     │
└─────────────────────────────────────┘
```

每个 AI core：本地 SRAM 缓冲 DRAM 数据；Matrix Unit（systolic array）处理 MatMul；Vector Unit 处理 elementwise；NoC 连接 core 间及 core-to-DRAM 远端访问。

## 与 2.5D AI 芯片对比

| 维度 | 2.5D（H100、TPU） | 3D-stacked AI chip |
|------|-------------------|---------------------|
| DRAM 连接 | 少量共享 bus，多 bank 时分 | 每 bank 专用 TSV bus |
| 内存空间 | 全局统一、近均匀延迟 | 分布式、非均匀访问延迟 |
| 带宽扩展 | Perimeter 受限 | 随 die 面积扩展 |
| 利用率机制 | Inter-bank 调度隐藏 row conflict | 专用 bus stall 时无 bank 可共享 → 利用率难维持 |
| Dataflow/layout | — | [FEATHER](/concepts/feather-accelerator.md) 式 per-layer co-switch 缓解 bank conflict |
| 典型 BW 密度 | — | ~**400 GB/s per 0.02 mm²**（当前工艺 [1]） |

## 效率挑战

### 1. DRAM 总线利用率

2.5D 中多 bank 共享 bus，row-buffer conflict 可被其他 bank 的传输隐藏。3D 中每 bus 专属于一 bank，bank 因 row conflict 未 ready 时 bus 直接 idle，**峰值带宽难以吃满**。

### 2. Row-buffer 冲突

- **单 core**：多 tensor 并发访问（fused op 3+ 输入）→ 同 bank 多 row 交错
- **多 core**：tensor parallelism 下多 core 共享 tensor shard → 访问 desync → 冲突加剧
- 16 TBps 下冲突开销可达 decode 延迟 **43.35%**（uniform placement）

### 3. NoC 争用

Core 访问远端 DRAM 或 core 间共享数据经 NoC；无优化 placement 时 NoC 拥塞可达 **1.35×** slowdown。

### 4. Core 与 DRAM 协同

Core FLOPS、DRAM BW、NoC BW、SRAM 容量必须协同配置；单纯 scale 任一维度可能恶化其他组件利用率。

## 软件-硬件协同优化（Voxel 论文结论）

| 优化 | 机制 | 效果量级 |
|------|------|----------|
| **Compute-shift** | 环形 shift 共享 tensor，重叠 compute / NoC / DRAM | 相对 SPMD prefill **46.73%** 提升 |
| **Dimension-ordered mapping** | 共享数据 tile 映射到同行/列 core | NoC latency 最高 **57.48%** 降低 |
| **Software-aware tensor-to-bank** | 按访问模式放置 tensor | 冲突开销最高 **80.7%** 降低 |
| **Core group** | 物理相邻 core 组内同步 DRAM 访问 | 缓解多 core 导致的 bank 冲突；详见 [Core Group](/concepts/core-group-dram-access.md) |
| **Mesh NoC** | 低面积 + dimension-ordered → 近最优 | 相对 all-to-all 面积更优 |

## 物理层前置

本页是 Voxel 视角下的 3D AI 芯片工作负载与协同设计空间；物理前置见 [Through-Silicon Via Physical Layer](/concepts/tsv-3d-physical-layer.md) 与 [3D Stacking Technologies](/concepts/3d-stacking-technologies.md)（TSV / Monolithic / Hybrid Bonding 三路线 + 对 3D 集成的根本含义）。

## LLM 工作负载差异

- **Decode（memory-bound）**：扩 DRAM BW 显著降 latency；大 SRAM 利于 prefetch；NoC BW 不敏感
- **Prefill（compute/NoC-bound）**：扩 DRAM BW 收益有限；compute-shift + dimension-ordered 关键；大 SRAM 收益小（core 已高 FLOPS 利用）

见 [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md)。

## 相关

- [DRAM and Memory System](/concepts/dram-memory-system.md) — HBM/TSV 带宽与内存墙
- [Voxel Simulator](/concepts/voxel-simulator.md) — 3D AI 芯片设计空间探索工具
- [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) — 来源论文摘要
- [Core Group (DRAM Access Synchronization)](/concepts/core-group-dram-access.md) — core scaling 时的 DRAM 访问同步优化
- [Graphcore IPU](/entities/graphcore-ipu.md) — Voxel 验证用 silicon 平台
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — NoC 拓扑与 mapping 协同
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — prefill/decode 对 3D 设计旋钮的不同响应
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — logic-on-logic：用垂直维隔离 KVT 与 decode AllReduce，不是 DRAM-on-logic
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — DRAM-PNM 做 attention、FeFET-NAND-PNM 做 expert，树 NoC 扛 MoE scatter-gather
- [Network-on-Wafer](/concepts/network-on-wafer.md) — 整晶圆 WoW 与 3.5D chiplet 树
- [d-Matrix Raptor](/papers/hc2026-dmatrix-raptor-3d-dram.md) — Hot Chips 2026：**1-Hi logic-on-top** 3D DRAM（不是 Voxel 的 DRAM-on-logic 网格）；36 μm F2F；自称 ≈20× BW/mm² vs HBM4

## 编译器侧解 row-buffer 冲突：TileDRAM（2026-10-20）
- [TileDRAM](/papers/tiledram-tile-to-dram-layouts-3d-dram-gpgpu.md)：CU 本地 3D DRAM（混合键合）上，惯常放置让 MoE FFN tile 访问行冲突率 **75.7%**；把 tile→DRAM 布局做成编译器可选的 F2 线性布局后降到 **15.2%**，几何均值 **1.77×**，六种 3D DRAM 组织 **2.20×**，只靠地址算术（RTX 3090 开销 0.17%）[2]。
- 与上文 Voxel「row-buffer 冲突占 decode 延迟可达 43.35%」互补：Voxel 量化问题，TileDRAM 在不改硬件的前提下给出放置解法。

## HBM 逻辑 die 内嵌近存计算：DuoPD（2026-10-21）
HBM4 逻辑 die 约 140.8 mm²，去掉 TSV/PHY 后空余 38.6 mm²；[DuoPD](/papers/duopd-hybrid-gpu-pnm-pd-disaggregation.md) 在其中放 6.51 mm²（7 nm 折算）的 PNM 跑完整 decode，DRAM core die 不改，靠 TSV 层与 GPU 分时共享带宽。

## MoE decode 负载均衡与单片 3D DRAM（2026-10-22）
- [3D-MoE](/papers/3d-moe-complementarity-nmp-moe-decode.md)：通道-核瓦片组织下本地便宜、远程贵；利用专家负载跨步反相波动做离线分组，逻辑 die 加局部广播通路（面积 +2.11%），MoE 层比 EP 平均 4.63×，端到端比最强 NMP 基线 1.58–1.86×。
- [M3D-FLOW](/papers/m3d-flow-monolithic-3d-pnm-normalizing-flow.md)：单片 3D DRAM 按层延迟分 8 个 tier 放数据，Cu-Cu 混合键合逻辑 die 上用随机计算尾数乘法提升热预算内 MAC 密度。


## 近存 RAG 选择（2026-10-29）
[p-DCIM](/papers/pdcim-sram-ising-rag-context-selection.md) 提案把 28 nm SRAM DCIM Ising 宏放在混合 **HBM+HBF** 的逻辑 base-die：集合级证据选择在存储子系统内完成，仅回传 passage ID；选择能耗约 **0.9 µJ**，整查询能耗 **−67%**。与 decode 近存（DuoPD / 3D-MoE）互补——加速的是检索后组合优化而非 GEMV。

# Citations

[1] [raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf](raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf)
[2] [arXiv:2610.23767](https://arxiv.org/abs/2610.23767) — TileDRAM
- [arXiv:2610.26131](https://arxiv.org/abs/2610.26131) — DuoPD
- [arXiv:2610.26991](https://arxiv.org/abs/2610.26991) — 3D-MoE
- [arXiv:2610.27371](https://arxiv.org/abs/2610.27371) — M3D-FLOW
