---
type: Raw Source
title: "Entwine: Coordinating Tiled Computation and Fine-Grained Communication across GPUs"
source_url: https://arxiv.org/abs/2609.11562
arxiv: '2609.11562'
ingested: 2026-09-14
sha256: 77feff0620d360a1726e1e5d4b48794db412166f429046c8c8a2ab3b5591aa62
---

# Entwine: Coordinating Tiled Computation and Fine-Grained Communication across GPUs

**Authors:** Kai Ma, Quanfeng Lv, Jingguo Ge, Bowei Dai, Kefan Ruan
**Affiliation:** 中科院信息工程研究所 / 国科大 / 中科院微电子所
**PDF:** [Entwine_Tiled_Computation_Fine_Grained_GPU_Comm_2026.pdf](Entwine_Tiled_Computation_Fine_Grained_GPU_Comm_2026.pdf)
**arXiv:** [2609.11562](https://arxiv.org/abs/2609.11562)（2026-09-10，cs.DC；cs.AR cross）

## 问题

GEMM tile 陆续完成，但通信节奏与 tile 产出不匹配：要么饿死、要么突发；SM 上通信核还会拖慢计算，抵消 overlap。

## 方法要点

- 重排 tile 计算顺序，使通信侧数据更均匀到达。
- 细粒度 SM 通信核低延迟消费 tile。
- 协调 SM 资源分配，在通信进度与计算减速间折中。
- 主场景：NVLink 域内 GEMM–ReduceScatter。

## 摘录数字（仅论文给出）

- vs cuBLAS+NCCL：geomean **1.232×**，最高 **1.433×**。
- vs SOTA overlap（FlashOverlap / Async-TP / FLUX 等）：geomean 再高 **3.1–9.8%**。
- 测试床：单节点 2/4/8× A800-SXM4-80GB，NVLink；Llama 70B/405B 等 TP 形状。
