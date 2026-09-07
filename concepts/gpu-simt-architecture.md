---
type: Concept
title: GPU SIMT Architecture
description: H&P Ch.4 GPU/SIMT：Warp 锁步、Warp Divergence、Occupancy 延迟隐藏、H100 内存层次、Tensor Core；与 CPU OoO / WSE MIMD 对比
tags:
- architecture
- gpu
- simt
- simd
- cuda
- tensor-core
- warp
- wse
- npu
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
updated: 2026-09-07
sources:
- raw/articles/arch-study-30d-day-24.md
- raw/papers/CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf
---

# GPU SIMT Architecture（GPU 与 SIMT）

arch-study **第四阶段 Day 24**：H&P Ch.4 **数据级并行 (DLP)**——向量/SIMD 扩展与 **GPU SIMT (Single Instruction, Multiple Threads)**。与 Day 23 [Multicore SMT and NUCA](/concepts/multicore-smt-nuca.md)（多核复用）互补：GPU 用**数千轻量 thread 锁步**换吞吐，而非深 OoO 单核。

**Source:** [raw/articles/arch-study-30d-day-24.md](raw/articles/arch-study-30d-day-24.md)（H&P Ch.4.1–4.5，Day 24）

## Flynn 与 SIMT 定位

| 类别 | 代表 | 并行粒度 |
|------|------|----------|
| SISD | 传统单核 | — |
| **SIMD** | AVX/NEON 向量指令 | ISA 暴露，单指令多 lane |
| **SIMT** | NVIDIA GPU | 程序员写标量 kernel；硬件 **Warp 32 thread 锁步** |
| MIMD | 多核 CPU、[Cerebras WSE](/entities/cerebras-wse.md) | 独立 PC/控制流 |

**关键洞察**：SIMT 编程像 MIMD（每 thread 可分支），执行像 SIMD（Warp 内同指令）。这是「标量程序员自动获得 SIMD 性能」的抽象——代价是 **Warp Divergence**（见 [Branch Prediction](/concepts/branch-prediction.md) 对照：CPU 用硬件预测，GPU 用软件避免分支）。

## GPU 硬件层次（H100 量级）

```
GPU
  └── SM (Streaming Multiprocessor) ×132
        ├── Warp Scheduler
        ├── Warp 0..N-1 (每 Warp 32 threads)
        ├── 32-wide Dispatch (INT/FP/Tensor)
        ├── Register file ~256 KB/SM
        ├── Shared Memory 128 KB/SM
        └── L1 ~128 KB/SM
  └── L2 ~50 MB
  └── HBM ~80 GB
```

典型规模：132 SM × 64 warps/SM × 32 = **~270K concurrent threads**。

与 [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md)：CPU 在**小窗口**挖 ILP/OoO；GPU 在**大窗口**显式 TLP + SIMT。

## Warp Divergence 与有效加速

```
if (tid < 16) path A; else path B;   // 32-wide warp

Cycle 1: path A 活跃 (16 lanes)，B 闲置
Cycle 2: path B 活跃 (16 lanes)，A 闲置
→ 2 cycles，有效利用率 50%
```

**4-way divergence**（10 条指令）：有效时间 ×4。Day 24 例题：100 条 SIMT 指令中 10 条 4-way divergence → 实际加速 **~0.77×**（比无 divergence 更慢）。

来源：if/else、循环边界、间接寻址。

## Occupancy 与延迟隐藏

```
内存延迟 L cycles，每 SM W 个 Warp
→ 每 Warp 平均 L/W cycles 时间片

H100 例：L≈400（HBM），W=64 → ~6.25 cycles/Warp
W=32 → 吞吐显著下降
```

工业经验：**W ≥ 4** 才接近峰值利用率——stall 时切换其他 Warp（上下文切换 ~1 cycle）。

## GPU 内存层次（H100）

| 层次 | 容量/SM 或全片 | 延迟/带宽 | 作用域 |
|------|----------------|-----------|--------|
| Register | 256 KB/SM | ~0 cycle | thread |
| Shared Memory | 128 KB/SM | ~20 c，~10 TB/s/SM | block |
| L1 | 128 KB/SM | ~30 c | SM |
| L2 | ~50 MB | ~200 c，~5 TB/s | 全 GPU |
| HBM | ~80 GB | ~500 c，**3 TB/s** | 全 GPU |

Register vs HBM：**~500× 延迟、~1000× 带宽差**——一次 HBM 访问 ≈ 500 条 FP32 指令窗口。Roofline Ridge Point 见 [DRAM and Memory System](/concepts/dram-memory-system.md)。

**带宽密度**（Day 24）：H100 HBM ~0.05 TB/s/cm²；[WSE-3](/entities/cerebras-wse.md) 片上 SRAM **~100+ TB/s/cm²**（~7000×）——数据流架构根本优势。

## Tensor Core

| | CUDA Core | Tensor Core (Hopper FP16) |
|--|-----------|---------------------------|
| 每 cycle | 1 FMA | **4×4 矩阵 FMA**（256 FMA） |
| 峰值 | ~50 TFLOPS FP32 | **~450 TFLOPS** FP16 |
| 加速比 | 1× | **~9×** |

[FlashAttention-3](/concepts/flashattention-3.md) 利用 **TMA + WGMMA + FP8 Tensor Core**；[FlashAttention-2](/concepts/flashattention-2.md) 优化 warp 划分减少 inter-warp 归约。

**NPU 对照**：Tensor Core = 小矩阵（4×4）× 多实例；脉动阵列 = 大 MAC 网格×少实例——共同哲学：**空间换时间、专用换灵活**（见 [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md)、[Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) RS dataflow）。

## Roofline 例题（H100 简化）

| 配置 | Peak | HBM BW | Ridge (FLOPs/Byte) |
|------|------|--------|---------------------|
| FP32 | 50 TFLOPS | 3 TB/s | **16.7** |
| FP16+TC | 450 TFLOPS | 3 TB/s | **150** |

AI=100 FP32 GEMM → compute-bound（100 > 16.7），实测 35/50 = **70%** peak。AI=200 FP16+TC → compute-bound，380/450 = **84%** peak。

## CPU vs GPU vs WSE

| 维度 | CPU | GPU | WSE |
|------|-----|-----|-----|
| 并行 | 4–128 重核 + SMT | ~270K 轻 thread SIMT | ~900K 独立 PE MIMD |
| 单核/PE | 高 IPC（OoO/BP） | 低（in-order SIMD） | 简单 SLA |
| 分支 | 硬件预测 | 避免 divergence | 数据流无 BP |
| 内存 | Cache + coherence | 弱一致 + 层次 | 私有 SRAM + NoC |
| 适用 | 控制流/延迟敏感 | 数据并行吞吐 | 空间 dataflow |

**黄金法则**：latency-bound → CPU；throughput-bound → GPU/DSA；混合 → heterogeneous。

**Shared Memory ↔ WSE 邻居**：GPU `__shared__` 是**软件管理** block 级 scratchpad；WSE 邻居消息是**硬件 NoC**——[NoC Fundamentals](/concepts/noc-fundamentals-hp-appendix-f.md)。**Placement 优化** ↔ 避免 divergence：把依赖任务放物理邻近位置（[SpaDA Programming Language](/concepts/spada-programming-language.md) placement）。

## 与 LLM 推理

[Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md)：prefill 高算力利用 Tensor Core；decode 常 memory/sync bound（671B decode HBM util ~50–60%）。GPU SIMT 是主流训练/推理 baseline；WSE/NPU 走 MIMD/DSA 路径——见 [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md)。


## DSMEM / Thread Block Cluster（Hopper+）

Hopper 起 CTA 可组成 cluster，经 **DSMEM** 直接访问 peer SMEM（逻辑分布式、物理仍属各 CTA）。[CREDIT](/papers/credit-dsmem-inter-cta-tiling.md) 测得远程 load 约 **6.4×** 本地延迟，并给出 reduction-reuse 盈利筛：宽行归约后复用时，用紧凑 partial 交换换掉 HBM 重读；N=64K 时相对最快 baseline 几何均值 RTX 5090 **1.466×** / H100 **1.318×**。小形状常仍输给单 CTA。

## 相关页面

- [Multicore SMT and NUCA](/concepts/multicore-smt-nuca.md) — 并行篇 Day 23（SMT vs SIMT）
- [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md) — ILP vs TLP
- [Branch Prediction](/concepts/branch-prediction.md) — CPU 分支 vs Warp divergence
- [DRAM and Memory System](/concepts/dram-memory-system.md) — HBM Roofline
- [Cerebras WSE](/entities/cerebras-wse.md) — MIMD 对照
- [FlashAttention-2](/concepts/flashattention-2.md) / [FlashAttention-3](/concepts/flashattention-3.md) — Tensor Core kernel
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — Day 25 硬件 SIMD / 脉动
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — RS dataflow 流片基线

# Citations

[1] [raw/articles/arch-study-30d-day-24.md](raw/articles/arch-study-30d-day-24.md) — H&P Ch.4 GPU/SIMT（Day 24）
