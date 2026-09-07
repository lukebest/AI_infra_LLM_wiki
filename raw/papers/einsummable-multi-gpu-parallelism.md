---
type: Raw Source
title: Einsummable — Automatic Multi-GPU Parallelism for AI Computations
source_url: https://arxiv.org/abs/2609.03905
arxiv: '2609.03905'
ingested: 2026-09-07
sha256: b60ffe7f37c707dbac7a048bb65807be5b78e076f2f798c1a4064bef1b776872
---

# Every Kernel Is a Join: Automatic Multi-GPU Parallelism for AI Computations in Einsummable

**Authors:** Zhimin Ding, Chen-Kuan Liao, Chima Adiole, Brianna Barrow, Fangzhou Du, Yu Hsiao, Ge Huang, Yicheng Jin, Ismail Syed, Chris Jermaine
**Affiliations:** Rice University
**PDF:** [Einsummable_Multi_GPU_Parallelism_2026.pdf](Einsummable_Multi_GPU_Parallelism_2026.pdf)
**arXiv:** [2609.03905](https://arxiv.org/abs/2609.03905)（2026-09-04，cs.DC；PVLDB 风格）

## 问题

多 GPU 服务器上自动做 intra-operator 并行：现有 mesh 注解式自动并行器搜不到 3D matmul、数据依赖切分、GQA 继承 sharding 等。

## 方法要点

- 每个算子 = 张量关系上的 join + aggregation；算子导出 join-agg specs。
- DP 逻辑优化按通信字节代理选分解；物理层合成拓扑感知 **exchange program**（Volcano exchange 推广），不调用罐头 NCCL 集体。
- 8×A100 LLaMA-scale transformer block：几何均值 **8.97 ms** vs 手调 PyTorch **13.65 ms**、vLLM **14.87 ms**。
- 128K 单序列自动发现类似 Ulysses（头并行 attention + token 分片外围）计划：**143 ms** vs PyTorch **506 ms** / vLLM **498 ms**（约 3.5×）。

## 摘录数字（仅论文给出）

- 平台：DGX A100 8×40GB NVSwitch；另测 DGX V100 cube-mesh。
- 通信代理与实测 runtime Pearson r 多在 0.72–0.92。
- V100 上优化 exchange vs naive：transformer 几何均值约 **5.6%**，bushy matmul chain 最高 **1.41×**。
