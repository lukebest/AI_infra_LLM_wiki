---
type: Paper
title: "ThunderEP: Expert-Parallel Communication on PCIe Consumer GPUs"
description: "SNU — 无 P2P PCIe MoE EP；dispatch/combine vs NCCL 均值 2.00×/1.53×；prefill 最高 1.66×、decode 吞吐最高 1.26×"
tags:
- architecture
- llm
- moe
- inference
- serving
- expert-parallelism
- collective
- interconnect
- gpu
- nvidia
- distributed
- kernel
- throughput
created: 2026-10-02
updated: 2026-10-02
timestamp: '2026-10-02T00:00:00Z'
paper_author: [Jaehwan Lee, Sangmin Lee, Chaewon Kim, Junsik Shin, Jaejin Lee]
year: 2026
arxiv: '2609.40093'
sources:
  - raw/papers/ThunderEP_PCIe_Consumer_GPU_MoE_2026.pdf
  - raw/papers/thunderep-pcie-consumer-gpu-moe.md
---

# ThunderEP：把 Host 内存当共享通信介质

## 一句话结论

面向 **无 NVLink / 无 P2P** 的 PCIe 消费级 GPU（RTX 4090/5090），ThunderEP 用单步 All-Gather / Reduce-Scatter + DMA 搬数 + 细粒度完成同步；相对 NCCL dispatch/combine 均值 **2.00× / 1.53×**，相对 vLLM prefill 延迟最高 **1.66×**、decode 吞吐最高 **1.26×**。

## 动机

- 细粒度 MoE 每 token 激活更多专家 → EP dispatch/combine 占比上升。
- DeepEP / HybridEP / NCCL EP / NIXL 等假设 GPUDirect P2P 或 RDMA；消费卡驱动关闭 P2P，只能经 CPU bounce buffer。
- 框架回退 NCCL CPU-staged：多余 PCIe 中继，且与专家计算争 SM，重叠差。

对照 [Purlin](/papers/purlin-collectives-orchestration-datapath.md)、[Mixture-of-Kittens](/papers/mixture-of-kittens-moe-megakernel-nvl72.md)、[LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)、[NVLink/NVSwitch](/concepts/nvlink-nvswitch-scale-up-fabric.md)。

## 方案

1. **Host 作共享介质**：单步 All-Gather / Reduce-Scatter，去掉 ring 多跳 PCIe 中继。
2. **DMA 引擎搬 bulk**：避免与专家计算争用 SM。
3. **细粒度完成标志**：降低在 CPU 内存上轮询无关 GPU 的同步等待。
4. **集成**：vLLM；模型 Qwen3-30B-A3B（BF16）、GPT-OSS-20B/120B（MXFP4）；双机 PCIe 4.0×16 / 5.0×16。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| dispatch / combine vs NCCL（均值） | **2.00× / 1.53×** |
| prefill 延迟 vs vLLM | 最高 **1.66×** |
| decode 吞吐 vs vLLM | 均值 1.17× / 1.12× / 1.16×（三模型）；最高 **1.26×** |
| decode 吞吐 vs SGLang / Megatron-Core | 均值 **1.28× / 1.90×**（Megatron-Core 在 120B OOM） |
| 暴露 MoE 通信 / Transformer 层延迟 | **−64.4% / −38.9%**（相对文中基线剖析） |

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP All-to-All 在 **无 scale-up** 上的对照极端
- [Purlin](/papers/purlin-collectives-orchestration-datapath.md) — 集体 datapath 可换；ThunderEP 专攻 **PCIe+host 介质**
- [MoK](/papers/mixture-of-kittens-moe-megakernel-nvl72.md) / [Weave](/papers/weave-dynamic-sm-moe-overlap.md) — NVL72/H100 EP；本文是消费卡落点
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 非数据中心 GPU 上的 MoE 可达性

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.40093) — Lee et al., arXiv:2609.40093
[2] [raw stub](raw/papers/thunderep-pcie-consumer-gpu-moe.md)
