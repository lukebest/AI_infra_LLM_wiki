---
type: Raw Source
title: BASP — Communication-Efficient Batch-Aware Sequence Parallelism for LLM Training
source_url: https://arxiv.org/abs/2609.03151
arxiv: '2609.03151'
ingested: 2026-09-07
sha256: 4c97bd3acc2528f17f0e398ac91f325e8fc911c8ef940e91b9b92c17798787e8
---

# BASP: Communication-Efficient Batch-Aware Sequence Parallelism for LLM Training

**Authors:** Bigyan Ghimire, Jon C. Calhoun
**Affiliations:** Clemson University
**PDF:** [BASP_Batch_Aware_Sequence_Parallelism_2026.pdf](BASP_Batch_Aware_Sequence_Parallelism_2026.pdf)
**arXiv:** [2609.03151](https://arxiv.org/abs/2609.03151)（2026-09-04，cs.DC）

## 问题

长上下文 LLM 训练用 DeepSpeed-Ulysses 时，attention 阶段做全局 N-way all-to-all，与 micro-batch 大小无关；B 增大时 all-to-all 占比上升（8×A100 上可达约 34%）。

## 方法要点

- 当 N=K·B 时，把 N GPU 分成 B 个大小为 K 的不相交 SP 子组，每组只处理一条（或一批）序列。
- 全局 N-way all-to-all 变成 B 组并行的 K-way all-to-all；每 GPU 通信邻居从 N−1 降到 K−1。
- 连续 rank 映射：K=每节点 GPU 数时 all-to-all 可关在 NVLink 域内。
- 每 GPU token 数仍为 BS/N（与 SP=N 的 Ulysses 同内存足迹），不同于简单把 SP 设为 N/B（会变成 B²S/N tokens/GPU）。
- 可与 ZeRO-3 叠加；要求 N 整除 B。

## 摘录数字（仅论文给出）

- 平台：2 节点 × 4×A100 40GB NVLink + 400Gbps IB；ZeRO-3 + mixed precision；DeepSpeed 改写。
- 16K seq、B=2、8 GPU：端到端相对 Ulysses **1.17–1.32×**（Llama/Qwen 族）；Llama 3.1-8B **1.21×**，Qwen 1.5-1.8B **1.31–1.32×**。
- all-to-all 时间降 **2.23–3.10×**；B=8 时 all-to-all 可降到约 **85×**（端到端约 1.25×，其余被 ZeRO 集体拖住）。
- 序列缩放到 32K（Llama 3.2-3B）：step 时间降幅到 **25.9%**。
- loss 曲线与 Ulysses 重叠（800 iter），声称数学等价。
