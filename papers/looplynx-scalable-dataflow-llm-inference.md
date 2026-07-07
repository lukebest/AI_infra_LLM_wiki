---
type: Summary
title: 'LoopLynx: A Scalable Dataflow Architecture for Efficient LLM Inference'
description: FPGA hybrid spatial-temporal dataflow：Macro Dataflow Kernels + state-machine 调度 + multi-FPGA ring；解决"spatial dataflow 在 decode 串行依赖下利用率不足"；双节点 1.67× A100、四节点 2.52× A100
tags:
- dataflow
- fpga
- spatial
- temporal
- llm
- inference
- decode
- looplynx
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- raw/papers/LoopLynx_Scalable_Dataflow_LLM_Inference_2025.pdf
---

# LoopLynx: A Scalable Dataflow Architecture for Efficient LLM Inference

**Authors:** Jianing Zheng, Gang Chen (Sun Yat-sen University) | **arXiv:** [2504.09561v1](https://arxiv.org/abs/2504.09561) (Apr 2025) | **Venue:** IEEE conference | **PDF:** [raw/papers/LoopLynx_Scalable_Dataflow_LLM_Inference_2025.pdf](LoopLynx_Scalable_Dataflow_LLM_Inference_2025.pdf)

## 一句话总结

**FPGA 上的 hybrid spatial-temporal dataflow**：把 LLM 操作符实现为**大型 dataflow kernel (MDK)**，state-machine 调度器在时序上复用同一组 MDK —— 解决了"spatial dataflow 在 decode 串行依赖下利用率不足"这一根本问题。

## 核心问题与解法

> "the parallel processing capabilities of such dataflow architectures are **largely underutilized in the decoding phase** due to the sequential processing pattern."

| 架构 | 优 | 劣 |
|------|----|----|
| **Temporal (instruction-driven)** | 灵活、kernel 可复用 | 串行执行、资源利用率低 |
| **Spatial (纯 dataflow)** | 流水吞吐、kernel 全活跃 | **decode 串行依赖**下，task-level pipeline 不连续 |
| **LoopLynx (hybrid)** | spatial 显式 kernel + temporal 隐式调度 | 设计复杂度高 |

## 三个关键技术

1. **Macro Dataflow Kernels (MDK)**: Fused MP / MHA / LN&Res 通过共享 buffer 互连，由 scheduler 时序复用
2. **Head-wise pipelining**: 重新排列多头注意力计算 —— head_i 的 softmax 隐入 head_{i+1} 的 attention 计算中
3. **Transmission latency hiding**: 多 FPGA 节点间 ring network 同步开销被 dataflow 计算掩盖（仅最后一个 block 暴露同步成本）

## 资源占用（Xilinx Alveo U50 单 SLR 节点）

| 组件 | DSP | LUT | FF | BRAM |
|------|-----|-----|-----|------|
| Fused MP | 522 | 34K | 56K | 241 |
| Fused MHA | 382 | 38K | 45K | 16 |
| Fused LN | 192 | 23K | 30K | 240 |
| DMA | 0 | 16K | 28K | 97 |
| **节点总计** | **1128** | **128K** | **185K** | **595** |

频率 285 MHz（place & route 通过 FIFO 解耦实现）。

## 评测

- 模型：GPT-2 (345M) + W8A8 (smoothquant)
- 平台：AMD Alveo U50，1-2 SLR / 卡，2-4 节点
- **2-node: 1.67× A100 latency、2.3× energy**
- **4-node: 2.52× A100、2.7× energy**
- 优势集中在长生成（[32:512]、[64:512]、[128:512]）
- prefill 短时 GPU 更强（批处理）

## 对 Direction 2（Compiler-Aware Decode on Mesh-NoC）的启示

- **"spatial dataflow 在 decode 上利用率不足"是普遍问题**，不只 WSE —— FPGA / RDU / WSE 都有
- **解决思路多样**：LoopLynx 用 hybrid + state machine scheduler；WaferLLM 用 replicate + K-tree allreduce；Cerebras vendor 用 pipeline
- **编译器视角的共同机会**：用 MLIR/TVM 在 pass 层面**显式建模** "spatial-temporal 切换"和"串行依赖下的 kernel 复用"

## 与 wiki 已有内容关联

- [WaferLLM System](/concepts/waferllm-system.md) — WSE-2 上同问题但用不同解法
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — Row Stationary dataflow（CNN 时代）
- [FEATHER Accelerator](/concepts/feather-accelerator.md) — 可重构 dataflow + layout reorder
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — Tenstorrent 上 MLIR-based dataflow planning
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 空间数据流 DSL
- [Plasticine](/concepts/plasticine.md) — Stanford CGRA parallel patterns
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 阶段差异

# Citations

[1] [raw/papers/LoopLynx_Scalable_Dataflow_LLM_Inference_2025.pdf](LoopLynx_Scalable_Dataflow_LLM_Inference_2025.pdf) — Zheng, Chen (2025)
