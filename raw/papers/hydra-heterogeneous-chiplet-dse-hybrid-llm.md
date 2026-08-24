---
type: Raw Source
title: HYDRA Heterogeneous Chiplet DSE Hybrid LLM
source_url: https://arxiv.org/abs/2608.19395
arxiv: '2608.19395'
ingested: 2026-08-24
sha256: f65acdf7df5f621f60ed3af36aa405a71a1806efbf4556f337efcdfa6164daad
---

# HYDRA: A Heterogeneous Chiplet DSE Framework for Serving Dynamic Hybrid LLM Workloads

**Authors:** Jiahao Lin, Alish Kanani, Sangwan Lee, Jaehyun Park, Umit Y. Ogras  
**Affiliations:** University of Wisconsin–Madison; University of Ulsan  
**PDF:** [HYDRA_Heterogeneous_Chiplet_DSE_Hybrid_LLM_2026.pdf](HYDRA_Heterogeneous_Chiplet_DSE_Hybrid_LLM_2026.pdf)  
**arXiv:** [2608.19395](https://arxiv.org/abs/2608.19395)  
**Submitted:** 2026-08-19  
**Code:** 文内写 available at Github，**未给出可打开 URL**

## 问题

Hybrid Transformer–Mamba 的计算/通信异构，加上 serving 的动态 batch 与弹性调度，使 2.5D chiplet 的组成、放置、D2D 带宽和运行时策略无法穷尽仿真。

## 方法要点

- 库：Attention/Mamba × prefill/decode 四种计算 chiplet + HBM；NoI 为 2D mesh；D2D 按 UCIe x64 advanced-package。
- 联合探索：组成、通信感知放置、D2D 带宽、动态 batch、弹性调度。
- 快速剪枝：Markov 估计器（平均 cosine similarity **0.9**），再对候选做事件驱动仿真。

## 摘录数字（仅 PDF）

- 全负载平均：**1.55×** 吞吐、TTFT 低 **43.7%**；吞吐最高 **2.3×**（相对 SOTA 基线）。
- 规模：最多 **24** 个计算 chiplet；interposer **2700–3000 mm²**；单 chiplet 面积上限约 **121 mm²**。
- D2D 档：**256 / 384 / 512 / 640 GB/s**。
- 相对穷尽：仿真点数少 **2520–8520×**。
- 探索时间（Table V）：LLAMA3-7B 穷尽 **2 d 8 h** vs HYDRA **4 min**；MAMBA2-2.8B **3 d 1 h** vs **4 min**；Nemotron-H-4B **8 d 8 h** vs **15 min**。最大吞吐：穷尽 **100%**、roofline **74%**、HYDRA **93%**。
