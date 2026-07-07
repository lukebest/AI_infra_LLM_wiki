---
type: Summary
title: 'SambaNova SN40L: Scaling the AI Memory Wall with Dataflow and Composition of Experts'
description: SN40L RDU（TSMC 5nm, 1040 PCU+PMU, 638 BF16 TFLOPS, 520 MiB SRAM+64 GiB HBM+1.5 TiB DDR）+ Samba-CoE（150 个 8B expert, 1T 总参）；streaming dataflow 编译期融合数百 op；vs DGX H100 3.7× speedup
tags:
- sambanova
- rdu
- dataflow
- streaming
- memory-wall
- moe
- coe
- hbm
- sram
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- raw/papers/SambaNova_SN40L_Memory_Wall_Dataflow_CoE_2024.pdf
---

# SambaNova SN40L: Scaling the AI Memory Wall with Dataflow and Composition of Experts

**Authors:** Prabhakar, Sivaramakrishnan, Gandhi et al. (SambaNova Systems) | **arXiv:** [2405.07518v2](https://arxiv.org/abs/2405.07518) (Nov 2024) | **PDF:** [raw/papers/SambaNova_SN40L_Memory_Wall_Dataflow_CoE_2024.pdf](SambaNova_SN40L_Memory_Wall_Dataflow_CoE_2024.pdf)

## 一句话总结

**SambaNova SN40L RDU**（TSMC 5nm，可重构 dataflow 芯片）+ **Samba-CoE**（150 个 8B expert 的 trillion-param 系统）—— 用 **streaming dataflow** 编译期融合**数百个**含复杂 access pattern 的 op，把 memory wall 转换为 compute-friendly pipeline；vs **DGX H100** CoE inference **3.7× 加速**、footprint **19× 减少**、model switching **15-31×**。

## 核心论点：Memory Wall

> "systems that cater to monolithic models have scaled compute TFLOPs much faster than memory bandwidth and capacity, **creating the memory wall** where the memory system can no longer feed the compute efficiently."

**CoE 设计哲学**：用**许多独立训练的**小 expert + 1 个 router 替代大 monolithic 模型。CoE > MoE（expert 异构、独立训练），但需要解决 **op fusion + 内存管理** 双重挑战。

## SN40L RDU 硬件

- **TSMC 5nm**、**2.5D CoWoS** 封装
- 每个 socket = 2 个 RDD (Reconfigurable Dataflow Die) + HBM
- **1040 PCU**（Pattern Compute Unit）+ **1040 PMU**（Pattern Memory Unit）
- **638 BF16 TFLOPS** peak
- **三档内存**：
  - 520 MiB on-chip PMU SRAM（~百 TB/s aggregate）
  - 64 GiB co-packaged HBM
  - 1.5 TiB DDR DRAM（DIMM）
- DDR→HBM 加载：>1 TB/s（**单 socket** Node）

## Streaming Dataflow 范式

- 算子融合：**单 kernel call** 融合**数百个 complex op + 任意 access pattern**
- 编译期决定 placement（spatial）+ 数据路由
- 算子间 pipeline + data + tensor parallelism 混合
- 与 [PyTorch2][TensorRT][cuDNN] 融合对比：常规融合**不支持** complex shuffle/transpose，SN40L 编译器**全自动支持**

## 评测

- **Unfused baseline**: 2×–13× speedup
- **CoE inference**: 8-socket SN40L Node vs **DGX H100**:
  - Machine footprint: **19×** 减少
  - Model switching: **15×–31×** 快
  - Overall: **3.7×** (vs H100) / **6.6×** (vs A100)
- 评测含 Llama2-7B、Monarch FFT (图 3)、BERT、ViT

## 与 wiki 已有内容的关联

- [Cerebras WSE](/entities/cerebras-wse.md) — 同样 dataflow 哲学、同样 SRAM-centric
- [WaferLLM System](/concepts/waferllm-system.md) — WSE 上的 LLM 推理代表
- [AI Accelerators Cross-Architecture](/concepts/ai-accelerators-llm-inference.md) — 跨架构横评
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — Row Stationary dataflow（CNN 时代）
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — Tenstorrent dataflow 编译
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 空间数据流 DSL
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 异构推理

## 对 Direction 2（Compiler-Aware Decode on Mesh-NoC）的启示

> "Our aggressive fusion techniques are well beyond the capabilities of state-of-the-art techniques used with conventional architectures [37], [41]–[43]."

**SN40L 编译器做 fuse；Cerebras CSL 是 language-level 决定 placement；WaferLLM system-level 解决 GEMM/GEMV。** 这是**不同抽象层的 fusion 范式**，对应不同可控性 / 优化空间。

- **SN40L 路线**：编译器全自动融合 → 灵活但不可控
- **Cerebras 路线**：程序员写 CSL（精细控制 placement）→ 可控但生产力低
- **WaferLLM 路线**：专有 LLM 推理系统（算法 + 运行时）→ 高效但不易扩展到其他 workload
- **Direction 2 路线**：**MLIR 编译器中间层**，抽象 hardware placement，同时让算法专家能用 declarative pass 表达 decode 优化

# Citations

[1] [raw/papers/SambaNova_SN40L_Memory_Wall_Dataflow_CoE_2024.pdf](SambaNova_SN40L_Memory_Wall_Dataflow_CoE_2024.pdf) — Prabhakar et al. (2024)
