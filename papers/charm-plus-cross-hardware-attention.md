---
type: Paper
title: "CHARM+: Cross-Hardware Attention with Re-Merge Multistream Mechanism"
description: "联想 — Ring-Attention 上 Re-Merge 多流 + 跨硬件 Query 并行；PCIe 均值 1.3×/1.7×（峰 1.4×/1.9×），NVLink 均值 2.8×/3.9×（峰 3.2×/4.3×）；H100 最高约 2.72×/4.21×；Megatron E2E 最高 2.17×"
tags:
- attention
- context-parallelism
- sequence-parallelism
- gpu
- nvidia
- training
- inference
- numa
- pcie
- nvlink
- collective
- parallelism
- llm
created: 2026-11-09
updated: 2026-11-09
timestamp: '2026-11-09T00:00:00Z'
paper_author: [Xinhang Zhang, Boning Zhang, Chengchun Liu, Chunpu Li, Lei Sun, Weifeng Zhang, Limin Xiao]
year: 2026
venue: NeurIPS 2026
arxiv: '2611.05906'
sources:
  - raw/papers/CHARM_Plus_Cross_Hardware_Attention_2026.pdf
  - raw/papers/charm-plus-cross-hardware-attention.md
---

# CHARM+：跨硬件 Re-Merge 多流 Attention

## 一句话结论
联想提出 **CHARM+**：用 **Re-Merge Multistream（RM+）** 把 Ring-Attention 的串行通信重排为多层可并行流，并用 **Cross-Hardware Query Parallelism** 解耦跨 NUMA/跨节点与机内通信。相对 Ring-Attention，前/反向平均 **1.3×** / **1.7×**（双 NUMA PCIe）、**2.8×** / **3.9×**（双节点 NVLink）；贡献陈述峰值可达 **1.4×**/**1.9×**（PCIe）与 **3.2×**/**4.3×**（NVLink）。H100 Table 5 中例如 4×8 前向约 **2.72×**、反向约 **4.21×**；Megatron 端到端最高 **2.17×**（Table 7）。

## 动机
- Ring-Attention 等序列并行把长序列切开，但通信环依赖强，算通重叠受限。
- 跨硬件（双 NUMA PCIe / 跨节点）带宽不均时，频繁同步放大空闲。
- PCIe 上并发通信还会争用链路；需要既减依赖、又隔离跨域同步的调度。

## 方案
1. **Merge / Re-Merge**：把环上串行 KV 通信重组成多层；层内可并行，通信深度趋向 \(O(\log n)\)。
2. **RM+ 多流**：多通信流与计算重叠；在 NVLink 上收益更大，PCIe 上需考虑链路争用。
3. **Cross-Hardware Query Parallelism**：解耦跨硬件与机内通信，避免带宽失衡带来的全局同步拖尾。
4. **评测**：单机/多机、L20 PCIe 与 H20/H100 NVLink；并接入 Megatron-LM 做端到端对照。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| vs Ring：双 NUMA PCIe 前/反向平均 | **1.3×** / **1.7×** |
| vs Ring：双节点 NVLink 前/反向平均 | **2.8×** / **3.9×** |
| 贡献陈述峰值（PCIe / NVLink） | **1.4×**/**1.9×**；**3.2×**/**4.3×** |
| H100 Table 5（例 4×8） | 前向最高约 **2.72×**；反向最高约 **4.21×** |
| Megatron 端到端（Table 7） | 最高 **2.17×**（H100） |

## 与 wiki 的关系
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 序列/上下文并行上的通信重排与重叠
- [NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 双节点 NVLink 相对 PCIe 争用的收益差
- [FlashAttention](/concepts/flashattention.md) — 分布式 attention 数值对齐 FlashAttention 量级
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 跨硬件带宽不均下的调度语义（训练 SP 也可对照）

## 开放问题
- Megatron 环 attention 已有大量优化，CHARM+ 尚未全部吸收；非 attention 线性层仍主导 E2E。
- PCIe 链路争用下 RM+ 可能慢于 Ring，需要与拓扑感知调度联合。

# Citations
- [arXiv:2611.05906](https://arxiv.org/abs/2611.05906) — Zhang et al., Lenovo Research；NeurIPS 2026
- [raw stub](/raw/papers/charm-plus-cross-hardware-attention.md)
