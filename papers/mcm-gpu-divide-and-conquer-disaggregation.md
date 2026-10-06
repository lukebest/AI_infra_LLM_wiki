---
type: Paper
title: "Divide and Conquer: Scalable Performance and Energy in MCM GPUs"
description: "Cantabria — MCM GPU scale-out/scale-up/hybrid × Ring/Mesh/Torus/Flat-B 系统 DSE；16-chiplet Torus（256 SM）相对同算力 SOTA MCM 性能 2.40×、能耗 −4.45×；Ring 在 16/64 chiplet 跌破单片 50%/10%"
tags:
- architecture
- gpu
- chiplet
- noc
- interconnect
- topology
- mesh
- routing
- packaging
- power
- benchmark
created: 2026-10-06
updated: 2026-10-06
timestamp: '2026-10-06T00:00:00Z'
paper_author: [Mario Ibáñez Bolado, Borja Pérez Pavón, Jose Luis Bosque Orero, Julio Ramón Beivide]
year: 2026
arxiv: '2610.03061'
sources:
  - raw/papers/MCM_GPU_Divide_and_Conquer_Disaggregation_2026.pdf
  - raw/papers/mcm-gpu-divide-and-conquer-disaggregation.md
---

# 分而治之：MCM GPU 的性能与能耗扩展

## 一句话结论

"多切小 chiplet + 够强的 inter-chiplet 网络"比"把资源堆进少数大 chiplet"更能扩展：**16-chiplet 2D Torus、256 SM** 相对同算力的 SOTA MCM（4-chiplet ring 范式）性能 **2.40×**、能耗降 **4.45×**。决定性因素是 **网络可扩展性而非算力密度**；业界常见的 4-chiplet ring 在 chiplet 数增大时迅速崩溃。

## 动机

- MCM GPU 设计空间（每 chiplet SM 数 × chiplet 数 × 拓扑）大，既有工作多假设 **4 chiplet + ring**、固定规模，无法外推到下一代更细粒度拆分。
- 动机实验（4-chiplet ring）：scale-up 128→1024 SM（算力 8×）平均性能仅 **1.23×**（≈15% 扩展效率）；scale-out 固定 512 SM、4→64 chiplet，性能降到 **0.76×（16）/0.59×（64）**，平均通信延迟升 **3.84×/16.22×**；ring 在 128 SM 时峰值带宽已贴近网络上限 **2048 GB/s**。

## 方案

1. 三种扩展策略：scale-out（固定 16 SM/chiplet 加 chiplet：4/16/36/64）、scale-up（固定 chiplet 加 SM）、hybrid（128–1024 SM × 4/16/64 chiplet）。内存控制器与 L2 bank 随 chiplet 线性增长。
2. 四种拓扑：Ring、2D Mesh、2D Torus（DOR）、Flattened Butterfly（含 64 chiplet 的 **Flat-4×4** concentration：4 chiplet/路由器）。链路按 **UCIe 3.0** 建模：单向 2 GHz × 256 B flit = **512 GB/s**（≈64-lane @64 GT/s）；有限缓冲、credit 流控、背压。
3. **MANGO** 模拟器：GPGPU-Sim（NVIDIA-like SIMT，跑未改 CUDA）+ BookSim（片内/片间网络）+ AccelWattch/BookSim 功耗模型；计划开源。
4. 负载：Rodinia / Parboil / FNNDSC 的 BFS、GEMM、Kmeans、Hotspot、SSSP、FFT、Cutcp；强扩展、固定指令数、占用率 >95%。

## 效果（仅论文数字）

| 发现 | 数字 |
|------|------|
| 16-chiplet Torus / 256 SM vs 同算力 SOTA MCM | 性能 **2.40×**，能耗 **−4.45×** |
| Ring vs 单片（hybrid 分析） | 16 chiplet 跌破 **50%**，64 chiplet 跌破 **10%** |
| 16 chiplet 时 | Mesh ≈ **80%** 单片；Torus / Flat-B 持平或超过单片 |
| 36 chiplet scale-out | Flat-B ≈ Torus **1.32×**、Mesh **1.77×** |
| 64 chiplet scale-out | Flat-B IPC ≈ Mesh/Torus **2×**、Ring **10×**；FFT 达单片 **2×** |
| GEMM 峰值带宽（64 chiplet，归一 4-chiplet ring） | Flat-B **13.5×**，Torus **8.7×**，Mesh **7.5×** |
| 64-chiplet（非 ring，256/512 SM） vs 16-chiplet 1024 SM | 最高 **1.39× / 2×** —— 更少算力反而更快 |
| 16-chiplet 1024 SM 加到 4 MC/chiplet | 仅 **+11%**，仍远低于 64-chiplet |
| 单片能耗 / 能效 | 能耗为 chiplet 方案 **4.82–253.37×**；IPC/J 低 **4.46–246.87×** |
| 能耗主因 | 每 chiplet > ~**32 SM** 后片内 crossbar 主导；16→64 chiplet 后片间网络主导 |
| 能效 | 多数配置 Torus 最优；Flat-4×4 在大 SM 数时最优 |

## 与 wiki 的关系

- [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) — 本文把 FBFLY + concentration 从 NoC 搬到 chiplet 间网络，给出 64 chiplet 下的性能/能效拐点
- [Mesh/Torus Topology](/concepts/mesh-torus-topology.md) — Torus 在 16 chiplet 是"性能—能效—成本"平衡点
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — "吞吐 ∝ 端口数 / 平均距离" 的经典分析在 MCM GPU 的复现
- [Die-Scaling GPU Fine-Grained Scheduling](/papers/die-scaling-gpu-fine-grained-scheduling.md) — 同为 GPU 拆 die；该文偏调度，本文偏拓扑与能耗
- [Fengshui chiplet ecosystem](/papers/fengshui-chiplet-ecosystem-basic-codesign.md) — chiplet 粒度与互连共设计

## 局限与开放问题

- 负载是 Rodinia/Parboil 等经典 GPGPU 核，不含 LLM 训练/推理（attention、MoE all-to-all）；LLM 流量下结论需复核。
- "SOTA MCM" 基线即 4-chiplet ring 范式；真实产品（如双 die NVLink-C2C）的片间带宽高得多，2.40× 不能直接外推。
- 未涉及良率/成本量化与长链路（Flat-B 跨行列长线）的封装可行性；作者列为未来工作：自适应路由、异构链路、数据放置。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.03061) — Ibáñez Bolado et al., arXiv:2610.03061
[2] [raw stub](raw/papers/mcm-gpu-divide-and-conquer-disaggregation.md)
