---
type: Summary
title: 'AI Accelerators for Large Language Model Inference: Architecture Analysis and Scaling Strategies'
description: 首篇 LLM 推理加速器跨架构定量横评：五类（GPU/Systolic/SRAM-centric/WSE/Deterministic pipeline）六大操作域评估；expert parallelism 8.4× 参数-计算比但 2.1× 延迟方差
tags:
- accelerator
- survey
- gpu
- tpu
- wse
- lpu
- inference
- scaling
- expert-parallelism
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- raw/papers/AI_Accelerators_LLM_Inference_2025.pdf
---

# AI Accelerators for LLM Inference: Architecture Analysis and Scaling Strategies

**Author:** Amit Sharma (IEEE Member) | **arXiv:** [2506.00008](https://arxiv.org/abs/2506.00008) (2025) | **PDF:** [raw/papers/AI_Accelerators_LLM_Inference_2025.pdf](AI_Accelerators_LLM_Inference_2025.pdf)

## 一句话总结

第一篇**真正定量横评** GPU / TPU / LPU / WSE / RDU 跑 LLM inference 的论文。结论：**无单一架构统治所有 workload**，batch × seq 维度上**架构间最大 3.7× 性能差**；**软件>硬件**（同硬件不同栈达 40% 性能差）。

## 五类架构 + 关键数字

| 架构 | 平台 | 工艺 | 关键数字 |
|------|------|------|---------|
| **GPU SIMD/SIMT** | NVIDIA Blackwell GB200 | TSMC 4N | 192GB HBM3e、8 TB/s、4500 TFLOPS FP16(s)、1.8 TB/s NVLink5、1000W TDP |
| GPU SIMD/SIMT | AMD MI300X | TSMC 5nm | 192GB HBM3、5.3 TB/s、256MB L3 Infinity Cache |
| **Systolic** | Google TPU v7 | 5nm | 192GB HBM3、7.37 TB/s、~100B+ transistors |
| **Many-core SRAM-centric** | Graphcore IPU | - | 900MB on-chip SRAM、45 TB/s internal |
| Many-core SRAM-centric | Meta MTIA v2 | - | 256MB shared SRAM (RISC-V + vector) + LPDDR5 |
| **Wafer-scale** | Cerebras WSE-3 | 5nm | ~900K core、44GB SRAM、SwarmX fabric |
| **Deterministic pipeline** | Groq LPU v1 | - | **230MB on-chip SRAM**、**80 TB/s** internal、亚毫秒 latency |

## 内存层次三分类

1. **HBM-focused**: Blackwell / TPU v7 / MI300X — 192GB HBM
2. **On-chip memory focused**: WSE-3 / IPU — 44GB / 900MB SRAM
3. **Hybrid**: MTIA v2 / Inferentia2 — 256MB SRAM + LPDDR5/HBM2e

## 四个 Scaling 策略（trillion-param 模型）

| 策略 | 参数-计算比 | 延迟方差 |
|------|------------|----------|
| Tensor parallelism | baseline | 1.0× |
| Pipeline parallelism | 1.5× | 1.3× |
| **Expert parallelism (MoE/CoE)** | **8.4×** | **2.1×** |
| Hybrid | 3-5× | 1.5× |

**关键洞察**：Expert parallelism 参数容量 8.4× 是其他策略 2-5×，**但延迟方差 2.1×** —— 对 agentic/interactive LLM 场景（需要稳定 per-token latency）是隐患。

## Architecture-workload 匹配

- **长 context / 单请求低延迟** → Groq / WSE（deterministic + on-chip SRAM）
- **大 batch / 高吞吐** → Blackwell / TPU（HBM 大容量 + 高 inter-GPU 带宽）
- **大模型 + 中 batch** → WSE（weight streaming） + Hybrid
- **稀疏激活（MoE/CoE）** → SambaNova RDU / Groq（数据流 + 多档内存）

## 关键结论

> "Performance variations of up to **40%** were observed for the same hardware with different software stacks."

→ **编译器 / runtime 优化空间 ≥ 硬件设计空间**。这是 Direction 2（compiler-aware decode）选择的最强论据。

> "no single architecture dominates across all workload categories, with performance variations of up to **3.7×** between architectures depending on batch size and sequence length."

→ **没有"最优架构"**，只有"匹配 workload 的架构"。这给"通用 LLM 推理编译器"留空间。

## 与 wiki 已有内容关联

- [Cerebras WSE](/entities/cerebras-wse.md) — WSE-3 数据
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPU 数据（v1 vs Groq 3 Lpx）
- [WaferLLM System](/concepts/waferllm-system.md) — 系统级 evaluation
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 阶段差异
- [Deterministic Execution](/concepts/deterministic-execution.md) — Groq/WSE 共同范式
- [Cerebras WSE vs Groq Network Comparison](/analyses/cerebras-wse-vs-groq-network-comparison.md) — 双架构横评

# Citations

[1] [raw/papers/AI_Accelerators_LLM_Inference_2025.pdf](raw/papers/AI_Accelerators_LLM_Inference_2025.pdf) — Sharma (2025)
