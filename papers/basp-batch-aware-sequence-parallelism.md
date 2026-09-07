---
type: Paper
title: "BASP: Communication-Efficient Batch-Aware Sequence Parallelism for LLM Training"
description: Clemson — 按 micro-batch 切 Ulysses all-to-all 子组；Llama/Qwen 相对 Ulysses 1.17–1.32×，B=8 时 A2A 可降约 85×（8×A100）
tags:
- llm
- training
- parallelism
- communication
- attention
- transformer
- collective
- gpu
- nvidia
- training-system
timestamp: '2026-09-07T00:00:00Z'
created: 2026-09-07
updated: 2026-09-07
sources:
- raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf
- raw/papers/basp-batch-aware-sequence-parallelism.md
---

# BASP: Communication-Efficient Batch-Aware Sequence Parallelism for LLM Training

**Authors:** Bigyan Ghimire, Jon C. Calhoun
**Affiliation:** Clemson University
**arXiv:** [2609.03151](https://arxiv.org/abs/2609.03151)（2026-09-04，cs.DC）
**Venue:** 预印本
**PDF:** [raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf](raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf)

DeepSpeed-Ulysses 把长序列沿 sequence 维切开，attention 用全局 **N-way all-to-all** 做头重排。BASP 观察到这与 micro-batch **B** 无关：当 \(N=KB\) 时，可把全局集体拆成 **B 组并行的 K-way all-to-all**，每 GPU 仍持 \(BS/N\) tokens。对照 wiki [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) 的 All-to-All 行：这是 **SP 侧拓扑感知子组**，不是新原语。

## 动机

- 长上下文训练：Ulysses 在 8×A100 上 all-to-all（NCCL Send/Recv）可占 iteration **~34%**；B 增大时 all-to-all 墙钟近似线性涨。
- 简单把 `sequence_parallel_size` 降到 \(N/B\) 会改变负载：每 GPU tokens 变成 \(B^{2}S/N\)，牺牲序列分片的内存收益。
- 需要同时保留 **SP=N 的内存足迹** 与 **小集体** 的延迟/带宽好处，并尽量关在 NVLink 域内。

## 方案

1. **Batch-aware group：** \(K=N/B\)，建 B 个不相交 process group；连续 rank 映射，使 \(K=\) 每节点 GPU 数时集体不出节点。
2. **联合切 batch×sequence：** 每组只负责一条（或一批）序列的 \(S/K\) 分片，不再让每个 GPU 持有所有序列的 chunk。
3. **Subgroup all-to-all：** attention 前后各做组内 K-way A2A；证明 per-GPU 计算与内存与 Ulysses（SP=N）同阶。
4. **与 ZeRO-3 叠加**；要求 \(N\) 整除 \(B\)（非整数情形列为 future work）。

## 效果（仅论文数字）

**平台：** 2 节点 × 4×A100 40GB NVLink + 400Gbps IB；改 DeepSpeed；ZeRO-3 + mixed precision；30 iter 平均。

| 设定 | 相对 Ulysses |
|------|----------------|
| 16K、B=2、Llama/Qwen 族端到端 | **1.17–1.32×** |
| Llama 3.1-8B | **1.21×** |
| Qwen 1.5-1.8B | **1.31–1.32×**（文中亦写 24% step 降） |
| all-to-all 墙钟 | **2.23–3.10×** 更快 |
| B=8（8K，Llama 3.2-1B）A2A | 约 **85×** 更快；端到端约 **1.25×**（其余被 ZeRO 集体卡住） |
| 32K（Llama 3.2-3B）step | 降 **25.9%** |

Loss 曲线 800 iter 与 Ulysses 重叠。**实测**小集群；非新硅。

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — SP/Ulysses All-to-All 的 batch 拓扑优化
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 子组关在 NVLink 域的动机
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) — 集体参与者数 ↓ 也降 barrier 面；本文主叙事是带宽/跳数
- [Einsummable](/papers/einsummable-multi-gpu-parallelism.md) — 自动发现类似 Ulysses 的 head/token 分解；BASP 是训练运行时手写优化
- [Comm/Comp Parallelism](/papers/optimizing-comm-comp-parallelism-training.md) — 训练通信-计算重叠对照

## 开放问题

1. \(N \bmod B \neq 0\) 时如何组组而不破坏内存等价？
2. 更大多节点（跨多 IB hop）时，ZeRO 集体是否总是吃掉 A2A 收益？
3. 与 Ring/USP/FlexSP 自适应切换如何组合？

# Citations

[1] [raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf](raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf) — Ghimire & Calhoun, arXiv:2609.03151
[2] [raw/papers/basp-batch-aware-sequence-parallelism.md](raw/papers/basp-batch-aware-sequence-parallelism.md) — ingest stub
