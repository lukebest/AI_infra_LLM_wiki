---
type: Raw Source
title: "BOOST: Concurrent Access to Host Memory and HBM to Accelerate LLM Inference"
source_url: https://arxiv.org/abs/2609.13592
arxiv: '2609.13592'
ingested: 2026-09-16
sha256: a1b255c2145f1ddd8b2e00e8a9eb4ad8de462d4238c03b929f444f1356fcda37
---

# BOOST: Concurrent Access to Host Memory and HBM to Accelerate LLM Inference

**Authors:** Anish Saxena†, Jae Hyung Ju†, Hritvik Taneja, Po-An Tsai, Aamer Jaleel, Christos Kozyrakis, Moinuddin Qureshi（†共同一作）
**Affiliations:** Georgia Tech; Nvidia Research; Stanford
**PDF:** [BOOST_Concurrent_Host_HBM_LLM_Inference_2026.pdf](BOOST_Concurrent_Host_HBM_LLM_Inference_2026.pdf)
**arXiv:** [2609.13592](https://arxiv.org/abs/2609.13592)（2026-09-11，cs.DC/cs.AR）

## 问题

GPU 把 HBM 与 host 内存当层级：能放进 HBM 就只用 HBM；溢出则 prefetch 到 HBM——prefetch 占 HBM 写带宽，host 带宽从未与 HBM 并发吃满。

## 方法要点

- Concurrent and Proportional (CAP)：每个 GPU wave 按带宽比并发访问两层。
- 静态权重：Modulo-Based Page Placement (MPP)，消除 wave 内访问比方差。
- 动态 KV：wave-aware 空闲 KV page 池。
- 集成 vLLM；Grace Hopper 实测；无改 kernel。

## 摘录数字（仅论文给出）

- Grace Hopper host 带宽约为 HBM 的 **9–11%**；理论合并约 **1.1×** HBM-only。
- iso-batch：相对 HBM-only **TPOT +4.3%**；prefetch 使 TPOT **恶化 6%**。
- 高吞吐 serving：平均吞吐 **+31%**；相对 prefetch **+15%**；并发访问相对纯扩容额外约 **4%**。
