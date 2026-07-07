---
type: Raw Source
title: 'AI Accelerators for Large Language Model Inference: Architecture Analysis and Scaling Strategies'
source_path: /home/luke/wiki/raw/papers/AI_Accelerators_LLM_Inference_2025.pdf
arxiv: '2506.00008'
ingested: 2026-07-07
---

# AI Accelerators for Large Language Model Inference: Architecture Analysis and Scaling Strategies (Source)

**Author:** Amit Sharma (IEEE Member) | **arXiv:** [2506.00008](https://arxiv.org/abs/2506.00008) (2025) | **PDF:** [raw/papers/AI_Accelerators_LLM_Inference_2025.pdf](AI_Accelerators_LLM_Inference_2025.pdf)

## 核心论点

> "no single architecture dominates across all workload categories, with **performance variations of up to 3.7×** between architectures depending on batch size and sequence length."

第一篇**真正定量横评** GPU / TPU / LPU / WSE / RDU 跑 LLM inference 的论文。

## 五类架构分类

| 类别 | 代表 | 关键特性 |
|------|------|----------|
| **GPU SIMD/SIMT** | NVIDIA Blackwell GB200, AMD MI300X | 双 die 5nm、192GB HBM3e、tensor core |
| **Systolic array** | Google TPU v7 | 5nm、192GB HBM3、7.37 TB/s |
| **Many-core SRAM-centric** | Graphcore IPU, Meta MTIA v2 | 900MB / 256MB on-chip SRAM、45 TB/s internal |
| **Wafer-scale** | Cerebras WSE-3 | 900K AI core、44GB SRAM、SwarmX fabric |
| **Deterministic pipeline** | Groq LPU | 230MB SRAM、80 TB/s、亚毫秒 latency |

## 主要数据点

### NVIDIA Blackwell GB200
- TSMC 4N 工艺，~208B transistors，**1000W TDP**
- 4500 TFLOPS FP16 (with sparsity)
- 192GB HBM3e、8 TB/s
- **NVLink 5.0** 1.8 TB/s/GPU，**NVSwitch 3** 扩展到 256 GPU

### Google TPU v7
- 5nm、~100B+ transistors、192GB HBM3、7.37 TB/s

### Meta MTIA v2
- RISC-V 控制核 + vector engine、**256MB shared SRAM**、LPDDR5
- 强调 heterogeneous 推理

### Groq LPU v1
- **230MB on-chip SRAM**、**80 TB/s** internal bandwidth
- 编译期静态调度 → **亚毫秒 latency**
- 模型大小受 SRAM 限制，跨 chip 走 tensor parallel

### Cerebras WSE-3
- **~900K core**、**44GB SRAM**、SwarmX fabric
- 多 wafer 互联

## Memory hierarchy 三分类

1. **HBM-focused**: Blackwell, TPU v7, MI300X — 192GB HBM、大模型驻场
2. **On-chip memory focused**: WSE-3, IPU — 44GB / 900MB SRAM、低延迟
3. **Hybrid**: MTIA v2, Inferentia2 — 256MB SRAM + LPDDR5/HBM2e

## 四个 scaling strategies for 万亿参数

| 策略 | 参数-计算比 | 延迟方差 |
|------|------------|----------|
| Tensor parallelism | baseline | 1.0× |
| Pipeline parallelism | 1.5× | 1.3× |
| Expert parallelism | **8.4×** | **2.1×** |
| Hybrid | 3-5× | 1.5× |

**Key insight**: Expert parallelism (MoE/CoE) 参数容量优势明显（8.4×）但**延迟方差 2.1×** —— 对 agentic / interactive LLM 场景是隐患。

## Architecture-workload alignment

> "The performance variations align closely with the architectural design philosophies"

- 长 context / 单请求低延迟 → Groq / WSE
- 大 batch / 高吞吐 → Blackwell / TPU
- 大模型 + 中 batch → WSE（weight streaming） + Hybrid

## 软件>硬件

> "Performance variations of up to **40%** were observed for the same hardware with different software stacks"

→ **编译器 / runtime** 的优化空间 ≥ 硬件设计空间

## 跟 wiki 已有内容的关联

- [Cerebras WSE](/entities/cerebras-wse.md) — WSE-3 数据
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPU 数据（虽然 v1 不完全等于 Groq 3 Lpx，但同设计哲学）
- [WaferLLM System](/concepts/waferllm-system.md) — 系统级 evaluation
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 阶段差异
- [Deterministic Execution](/concepts/deterministic-execution.md) — Groq/WSE 共同范式
- [Cerebras WSE vs Groq Network Comparison](/analyses/cerebras-wse-vs-groq-network-comparison.md) — 双架构横评
