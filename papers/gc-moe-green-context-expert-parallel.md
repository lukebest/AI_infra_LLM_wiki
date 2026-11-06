---
type: Paper
title: "GC-MoE: Overlapping Expert-Parallel Token Dispatch with FP8/FP4 Grouped GEMM via CUDA Green Contexts"
description: "阿里 — Green Context 拆通信/计算分区重叠 EP dispatch×FP8/FP4 grouped GEMM；8×H20 均值 1.188×（峰 1.296×/1.353×）；8×B300 1.106×/1.123×；54 点全面胜 Mega MoE"
tags:
- moe
- expert-parallelism
- kernel
- quantization
- inference
- serving
- gpu
- nvidia
- green-context
- llm
- parallelism
created: 2026-11-06
updated: 2026-11-06
timestamp: '2026-11-06T00:00:00Z'
paper_author: [Yong Li, Kan Liu, Tao Lan]
year: 2026
venue: arXiv preprint
arxiv: '2611.04222'
sources:
  - raw/papers/GC_MoE_Green_Context_Expert_Parallel_2026.pdf
  - raw/papers/gc-moe-green-context-expert-parallel.md
---

# GC-MoE：Green Context 上的 EP Dispatch × Grouped GEMM

## 一句话结论
阿里开源 [GC-MoE](https://github.com/Bruce-Lee-LY/gc-moe)：用 **CUDA Green Contexts** 在驱动层把 GPU 拆成**小通信分区 + 大计算分区**，各自独立内核、资源与同步域，重叠 EP token dispatch 与 FP8/FP4 grouped GEMM。B300 上 dispatch 仅占 **20 / 148 SM**；8×H20 DeepSeek-V4.1-Flash 均值 **1.188×**（路由峰 **1.296×**、融合共享专家峰 **1.353×**）；8×B300 上 GLM-5.2 / DeepSeek-V4.1-Flash 无 SE **1.106×**、融合 SE **1.123×**（峰 **1.209×**）；在全部 **54** 个测点上优于 DeepGEMM Mega MoE，数值精度对齐。

## 动机
- Decode 每 rank 往往只有 1–256 token：dispatch 与权重流量主导，tensor core 利用率本就偏低。
- Mega MoE 把 dispatch 与计算挤在同一批 SM：通信 warp 与 TMA/MMA/epilogue 争寄存器与 shared memory，同步域覆盖整机，每次 replay 还要 workspace-clean + 跨 rank barrier。

## 方案
1. **Green Context 分区**：小通信分区跑 dispatch，大计算分区跑 grouped GEMM；驱动级独立 workqueue。
2. **CUDA Graph**：三节点（Hopper 融合共享专家时四节点）并发根启动；token-ring handshake 让首批 ring block 就绪即开算。
3. **去尾障**：双缓冲 receive counter，削弱 replay 之间的跨 rank 尾部屏障。
4. **算子**：Blackwell 上 operand-swapped tcgen05 block-scaled MMA；Hopper 上 register-A WGMMA + 寄存器内 FP4 解码；融合 SwiGLU / requant / 可选共享专家。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| B300 SM 划分 | dispatch **20 / 148** |
| 8×H20 DeepSeek-V4.1-Flash | 均值 **1.188×**；峰 **1.296×**（routed）/ **1.353×**（fused SE） |
| 8×B300 GLM-5.2 + DeepSeek-V4.1-Flash | 无 SE **1.106×**；融合 SE **1.123×**（峰 **1.209×**） |
| vs DeepGEMM Mega MoE | **54** 测点全面领先；cosine ≥ 0.97 等精度对齐 |

## 与 wiki 的关系
- [MegaMoE Kernel](/concepts/megamoe-kernel.md) — DeepGEMM Mega MoE 同 SM 融合基线；GC-MoE 用分区重叠替代
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — 单 persistent EP kernel 路线；与 Green Context 分区正交
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — EP 服务中的算通共调度
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 生产 MoE serving 栈语境

## 开放问题
- 分区比例随 batch / 机型的自适应策略仍可扩展。
- 与交换机内集体（如 INC-MoE）的联合部署空间未展开。

# Citations
- [arXiv:2611.04222](https://arxiv.org/abs/2611.04222) — Li, Liu, Lan, Alibaba；https://github.com/Bruce-Lee-LY/gc-moe
- [raw stub](/raw/papers/gc-moe-green-context-expert-parallel.md)
