---
type: Summary
title: 'SIGMA: A Sparse and Irregular GEMM Accelerator with Flexible Interconnects for DNN Training'
description: HPCA 2020 MAERI 团队的 sparse + training 延伸：Flex-DPE + FAN（Forwarding Adder Network）+ global NoC；任意 GEMM 形状 + 任意稀疏度；5.7× vs systolic、3× vs 稀疏加速器
tags:
- accelerator
- gemm
- sparse
- training
- noc
- flexible
- interconnect
- hpca
- krishna
timestamp: '2026-07-22T00:00:00Z'
created: 2026-07-22
sources:
- raw/papers/SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf
---

# SIGMA

**Authors:** Eric Qin, Ananda Samajdar, Hyoukjun Kwon, Vineet Nadella, Sudarshan Srinivasan, Dipankar Das, Bharat Kaul, Tushar Krishna (Georgia Tech + Intel) | **Venue:** HPCA 2020 | **PDF:** [raw/papers/SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf](SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf)

## 一句话总结

**SIGMA** 是 MAERI 的 **sparse + training 延伸**：Flex-DPE 树 + **FAN（Forwarding Adder Network）** + 全局 NoC，让**任意 GEMM 形状 + 任意稀疏度**都能高效利用 PE。vs systolic arrays **5.7× 加速**，vs SOTA 稀疏加速器 **3× 加速**。**柔性互连在 sparse training 上同样必要**。

## 三大趋势驱动 SIGMA

| 趋势 | 表现 | 对 systolic 的打击 |
|------|------|------------------|
| **非方形 GEMM** | minibatch、weight factorization | systolic 数据流对非方形低效 |
| **稀疏 GEMM** | weight pruning（10-90%）+ activation sparsity | systolic 不能跳过零运算 |
| **快速模型演化** | 每几个月新架构 | 刚性 fabric 跟不上 |

## 关键创新：Flex-DPE + Flex-DPU

**Flex-DPE (Flexible Dot Product Engine)** = **基本计算 tile**（MAC tree）
- 内部：MAC 树 + 加法器
- 任意大小、任意 shape

**Flex-DPU (Flexible Dot Product Unit)** = 多个 Flex-DPE 通过 **global NoC** 组成
- 可以 morph：1 个大 Flex-DPU 跑 1 个 GEMM
- 或 N 个小 Flex-DPU 并行跑 N 个 GEMM
- **SIGMA 的真本事**：**NoC 让 cluster 形态可动态调**

## FAN（Forwarding Adder Network）

替代 systolic 的固定 reduction tree：
- **Partial sum 在中间节点直接转发**给下游
- 避免固定层级 reduction 的 latency
- **对稀疏不规则 pattern 特别友好**（中间节点可以绕路）

## 数字

- **5.7× speedup** vs systolic on irregular sparse matrices
- **3× speedup** vs SOTA sparse accelerators
- **10.8 TFLOPS effective** across arbitrary sparsity
- 28nm, **65.10 mm², 22.33 W**
- 覆盖 sparse + dense 训练 / 推理

## 与 FEATHER / MAERI 的关系

| | MAERI (2018) | SIGMA (2020) | FEATHER (2024) |
|---|--------------|--------------|----------------|
| **场景** | 通用 DNN | sparse + training | DNN + (dataflow, layout) co-switch |
| **interconnect 形态** | tree + tiny switches | Flex-DPE + FAN | BIRRD butterfly + reorder |
| **layout 重排** | 任意 distribution | 任意 sparse + dense layout | RIR 归约中重排 |

**SIGMA 是 MAERI → FEATHER 之间的桥梁**：把"灵活 NoC"扩展到 sparse + training 场景，证明了 **interconnect flexibility 是 dense / sparse / 训练 / 推理都通用的需求**。

## 与 wiki 已有内容的关联

- [FEATHER Accelerator](/concepts/feather-accelerator.md) — 继承者，加 reorder 能力
- [MAERI (paper summary)](/papers/maeri-flexible-dataflow-reconfigurable-interconnects.md) — 前置工作
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — systolic rigid 对比
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — 同 CGRA 思想但不同形态
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — MoE 稀疏相关的现代工作
- [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md) — SIGMA 关注 dense GEMM

# Citations

[1] [raw/papers/SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf](SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf) — Qin et al. HPCA 2020