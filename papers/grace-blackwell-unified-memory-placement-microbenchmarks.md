---
type: Paper
title: "Grace–Blackwell Unified Memory Placement Microbenchmarks"
description: "UDel — GB200 CUDA UM 按放置拆测：1 GiB triad HBM 3963 GB/s vs host-mapped 304；冷 first-touch 14.1 vs prefetch/reuse 4606/4504；125% 超订跌到 968/1214 GB/s"
tags:
- gpu
- nvidia
- hbm
- memory
- memory-bandwidth
- inference
- architecture
- benchmark
created: 2026-10-16
updated: 2026-10-16
timestamp: '2026-10-16T00:00:00Z'
paper_author: [Nathan Graddon, Aaron Jarmusch, Sunita Chandrasekaran]
year: 2026
arxiv: '2610.20354'
sources:
  - raw/papers/Grace_Blackwell_Unified_Memory_Placement_Microbenchmarks_2026.pdf
  - raw/papers/grace-blackwell-unified-memory-placement-microbenchmarks.md
---

# Grace–Blackwell：统一内存的放置控制微基准

## 一句话结论
CUDA Unified Memory 在 GB200 上「地址统一 ≠ 性能统一」。同一 `cudaMallocManaged` 可走本地 HBM、host 映射、冷 first-touch 迁移、prefetch、复用或超订换出；必须按 **放置 / 访问史 / 局部性 / 容量压力** 分别标定。

## 动机
- 单一「UM 带宽」数字掩盖路径差异；GB200 相对 GH200 的升级点与仍慢的路径需要对照测量。
- 方法论：分路径测 HBM、host-mapped、显式拷贝、managed 各状态、访问模式、超订、CPU–GPU handoff，再拟合成本模型。

## 方案
| 组 | 隔离内容 |
|---|---|
| HBM / host | `cudaMalloc` vs `cudaHostAlloc` mapped |
| Managed | 冷 first-touch、prefetch、advice、reuse |
| 模式 | stream / stride / random / page-touch |
| 压力 | 相对 CUDA-visible 容量的百分比 |
| Handoff | managed / prefetch / host-mapped / explicit 在不同 GPU 复用次数 |

## 效果（仅论文数字；GB200 主测，GH200 基线）
- **1 GiB STREAM triad**：本地 HBM **3963 GB/s**（GH200 3165，约 **1.25×**）；host-mapped **304 GB/s**（约 HBM 的 **7.7%**；GH200 345）。
- **256 MiB stream**：显式 HBM **4582 GB/s**；冷 managed **14.1 GB/s**（约 **0.3%**）；prefetch **4606**；reuse **4504**（约 **98.3%**）。
- 显式 H2D/D2H 1 GiB：GB200 **211 / 193 GB/s**；managed prefetch CPU→GPU **115 GB/s**（GH200 42）。
- 超订：25–90% 容量下 prefetch/reuse 仍 **>4.6 TB/s**；**125%** 时跌至 **968 / 1214 GB/s**。
- Handoff（1 GiB，R=1 GPU pass）：managed 交替 **272.1 ms** vs CPU+GPU 基线 **54.2 ms**；prefetch **79.9**；explicit **60.5**。R=32 时 explicit **73.3**、host-mapped **218.7**。
- 复用模型在较大工作集上中位 APE 约 **0.40%**；host vs explicit 交叉约 **R\*≈1.06**。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 与 Ember（UVM 超订）同族；本文钉在 GB200 路径带宽
- [DRAM and Memory System](/concepts/dram-memory-system.md)、[Ember](/papers/ember-uvm-oversubscription-discrete-gpu.md) — host/device 放置与超订
- [HBM2 power 实测](/papers/hbm2-power-characterization-real-chips.md) — 同属 HBM 行为刻画

## 局限
- 单 GPU 范围；不含 NVL72 多 GPU。
- 部分页故障/计数器受工具权限限制，行为由带宽趋势推断。

# Citations
- Graddon et al., "Understanding NVIDIA Grace–Blackwell Unified Memory Through Placement-Controlled Microbenchmarks", arXiv:2610.20354. [raw](/raw/papers/grace-blackwell-unified-memory-placement-microbenchmarks.md) · [PDF](/raw/papers/Grace_Blackwell_Unified_Memory_Placement_Microbenchmarks_2026.pdf)
