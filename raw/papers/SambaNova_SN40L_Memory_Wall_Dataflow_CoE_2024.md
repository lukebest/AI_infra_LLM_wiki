---
type: Raw Source
title: 'SambaNova SN40L: Scaling the AI Memory Wall with Dataflow and Composition of Experts'
source_path: /home/luke/wiki/raw/papers/SambaNova_SN40L_Memory_Wall_Dataflow_CoE_2024.pdf
arxiv: '2405.07518'
ingested: 2026-07-07
---

# SambaNova SN40L: Scaling the AI Memory Wall with Dataflow and Composition of Experts (Source)

**Authors:** Prabhakar, Sivaramakrishnan, Gandhi et al. (SambaNova Systems) | **arXiv:** [2405.07518v2](https://arxiv.org/abs/2405.07518) (Nov 2024) | **PDF:** [raw/papers/SambaNova_SN40L_Memory_Wall_Dataflow_CoE_2024.pdf](SambaNova_SN40L_Memory_Wall_Dataflow_CoE_2024.pdf)

## Motivation: The Memory Wall

> "systems that cater to monolithic models have scaled compute TFLOPs much faster than memory bandwidth and capacity, **creating the memory wall** where the memory system can no longer feed the compute efficiently."

## Samba-CoE 设计

- **150 个 expert**（每个 8B Llama2）+ 1 个 **router**（也叫 8B Llama2）
- 总参 ~1 trillion，但**每次只激活一个** expert + 可能的 router
- 与传统 MoE 不同：expert **独立训练**（heterogeneous），可**动态切换**

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

## Streaming Dataflow 核心

- 算子融合：**单 kernel call** 融合**数百个 complex op + 任意 access pattern**
- 编译期决定 placement（spatial）+ 数据路由
- 算子间 pipeline + data + tensor parallelism 混合
- 与 [PyTorch2][TensorRT][cuDNN] 融合对比：常规融合**不支持** complex shuffle/transpose，SN40L 编译器**全自动支持**

## 评测

- **Unfused baseline 对比**: 2×–13× speedup 各种 bench
- **CoE inference**: 8-socket SN40L Node vs **DGX H100**:
  - Machine footprint: **19×** 减少
  - Model switching: **15×–31×** 快
  - Overall: **3.7×** (vs H100) / **6.6×** (vs A100)
- 评测模型含 Llama2-7B、Monarch FFT (图 3)、BERT、Vision Transformer 等

## Key insight for Direction 2

> "Our aggressive fusion techniques are well beyond the capabilities of state-of-the-art techniques used with conventional architectures [37], [41]–[43]."

SN40L **编译器**做 fuse；Cerebras CSL 是 **language-level** 决定 placement；WaferLLM **system-level** 解决 GEMM/GEMV。**这是不同抽象层的 fusion 范式**，对应不同可控性 / 优化空间。
