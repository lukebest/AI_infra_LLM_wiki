---
type: Concept
title: FlashMoE Kernel
description: NeurIPS 2025 单 persistent GPU kernel 融合分布式 MoE：actor 调度、NVSHMEM 设备端 RDMA、payload-efficient dispatch；8×H100 相对 SOTA 最高 6× 延迟、5.7× 吞吐、93% SM 利用率
tags:
- moe
- gpu
- kernel
- expert-parallelism
- communication
- llm
- training
- inference
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf
---

# FlashMoE Kernel

**FlashMoE**（Aimuyo et al., NeurIPS 2025）将 **分布式 MoE 整层**（gate → dispatch → expert FFN → combine）融合为 **单个 persistent GPU kernel**，用 **设备端发起的一 sided RDMA**（NVSHMEM）替代 CPU 协调的 bulk AlltoAll，并通过 **tile 级 actor 流水线**消除数百次 kernel launch 空隙。

**Authors:** Osayamen Jonathan Aimuyo, Byungsoo Oh, Rachee Singh | **arXiv:** [2506.04667](https://arxiv.org/abs/2506.04667) | **Code:** https://github.com/osayamenja/FlashMoE

## 问题：EP MoE 的三重低效

| 瓶颈 | 表现 |
|------|------|
| **AlltoAll 集体通信** | 占 MoE 层 runtime 可达 **~68%**；straggler 拖全局 |
| **Kernel launch 风暴** | 单层 **33–550** 次 launch（FlashMoE **1**）；CUDA Graph 不适配动态路由 |
| **Padding  payload** | 集体 API 对称性 → 零填充 token 上链，带宽与计算浪费 |

现有 overlap 方案（Comet、FasterMoE、DeepEP）仍依赖 **多 kernel + NCCL**，SM 空闲可达 **~90%**。

## 架构：Actor 模型 + 单 Megakernel

```
Block 0 … Block n-2     Block n-1 (OS)
[ Processor × (N−1) ]   [ Scheduler (1 warp) | Subscriber (3 warps) ]
        │                        │
        └─ tile GEMM/combine ──────┴─ decode remote packets, schedule tasks
                    │
              NVSHMEM RDMA (device-initiated)
```

- **Processor**：CUTLASS 内嵌 GEMM；执行 FFN 与 expert-combine tile
- **Scheduler**：work-conserving，按 readiness 派活 → 高 SM 占用
- **Subscriber**：解析对端 tile packet → task descriptor
- **Tile 尺寸**：**(128, 64)**，128 threads/block

统一 **task** 抽象：t = (M, ⋆, ϕ)，FFN 两步 matmul + combine 的 Hadamard 加权均映射为 fused `__device__` 例程。

## 通信：对称布局 + payload-efficient

**Symmetric tensor layout** L（dispatch/combine 双 round × 双 staging buffer）保证 one-sided 写 **无写冲突**，内存约 **4×** token 矩阵（推理总内存 **≤2%** 增量）。

**In-place padding**：仅在本地计算前对齐 tile，**不在网络上发送 null token** — 相对传统 zero-pad AlltoAll 节省带宽。

## 与相关方案对比

| 方案 | Kernel 数/层 | 通信模型 | 侧重点 |
|------|-------------|----------|--------|
| **FlashMoE** | **1** | NVSHMEM RDMA，设备端 | 单节点 EP megakernel |
| Comet / FasterMoE | 33+ | NCCL AlltoAll | 部分 compute–comm overlap |
| Megatron+DeepEP | 432 | NCCL + DeepEP | 生产栈 |
| [MegaMoE Kernel](/concepts/megamoe-kernel.md) | wave pipeline | pull-based EP | DeepSeek-V4 推理 wave overlap |

FlashMoE 与 MegaMoE **正交互补**：前者是 **算子级单 kernel 融合 + 集体通信替代**；后者是 **wave 级调度** 在现有栈上最大化 overlap。

## 实测摘要（8× H100，FP32 vs 基线 FP16）

| 指标 | 结果 |
|------|------|
| SM 利用率 | **93.17%**（FasterMoE **9.67%**） |
| Forward latency | 最高 **~6.4×** vs Megatron-TE（16K tokens） |
| Throughput @ 8 GPU | **17.7 MTokens/s**（**5.7×** FasterMoE） |
| Overlap efficiency | **4×** |
| Expert 扩展 | 8→128 experts **近线性** latency |

## 在 LLM 栈中的位置

```
Model (MoE Transformer)
    ↓
Parallelism — [Expert Parallelism](/concepts/parallelism-transition-point.md) + DDP
    ↓
MoE Operator — FlashMoE（单 kernel EP）| MegaMoE / DeepEP（多 kernel overlap）
    ↓
Serving — [Disaggregated Inference](/concepts/disaggregated-inference.md) + [M2N Communication](/concepts/m2n-communication.md)（attention↔expert 解耦）
```

## 相关页面

- [MegaMoE Kernel](/concepts/megamoe-kernel.md) — DeepSeek wave EP overlap
- [M2N Communication](/concepts/m2n-communication.md) — 解耦推理 many-to-N 流量
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — attention / expert 分部署
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — MoE hybrid PP+TP
- [papers/flashmoe-fast-distributed-moe-single-kernel.md](/papers/flashmoe-fast-distributed-moe-single-kernel.md) — 论文摘要

# Citations

[1] [raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf](raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf) — Aimuyo et al., NeurIPS 2025
