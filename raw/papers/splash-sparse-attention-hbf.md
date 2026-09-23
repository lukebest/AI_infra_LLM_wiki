---
type: Raw Source
title: "SPLASH: Co-Designing Sparse Attention with High-Bandwidth Flash for Efficient Long-Context Inference"
description: "NUS — HBM+HBF 虚拟化 KV + 面向 HBF page/plane 的稀疏注意力；100 ms TPOT 下每 GPU decode 吞吐 3.5–11.4×。"
timestamp: '2026-09-23T00:00:00Z'
source_url: https://arxiv.org/abs/2609.23816
arxiv: '2609.23816'
ingested: 2026-09-23
sha256: bb24d0924a09614d9414586521abd26e9196283b809ce8f49811d1c68308f254
---

# SPLASH: Sparse Attention × High-Bandwidth Flash

**Authors:** Aditya Anirudh Jonnalagadda, Agasthi Haputhanthri, Pranav Dangi, Rohan Juneja, Wenshuo Yue, Aritra Bagchi, Bin Gao, Tulika Mitra  
**Affiliation:** National University of Singapore  
**PDF:** [SPLASH_Sparse_Attention_High_Bandwidth_Flash_2026.pdf](SPLASH_Sparse_Attention_High_Bandwidth_Flash_2026.pdf)  
**arXiv:** [2609.23816](https://arxiv.org/abs/2609.23816)（2026-09-20，cs.AR）

## 问题

长上下文 + 高并发下 KV 容量远超 HBM；host/CXL/SSD 二级带宽约低两个数量级。HBF 读带宽接近 HBM，但 page 粒度与 plane 并行要求稀疏注意力协同设计。

## 方法要点

- 把 KV 虚拟化到 **HBM + HBF**：新条目进 HBM，旧页迁 HBF，选中页经同一接口回读。
- 稀疏注意力改为 **page-aligned / scan-hidden / plane-balanced**，适配 HBF 全页读与数千 plane 聚合带宽。
- 动机数字：Qwen3-235B-A22B、64 并发 1M 上下文约需 **12.9 TB** KV（约 68 颗 B200 的 HBM）。

## 摘录数字（仅论文给出）

- 100 ms p50 TPOT 目标下，十五组模型×上下文：相对 HBM-only **11.4×** geomean；H3 **9.3×**；FlashAccel-CLI **6.4×**；FlashAccel-CSI **5.8×**；LongSight-HBF **3.5×**（摘要区间 **3.5–11.4×**）。
- 长上下文套件精度相对 dense attention 在 **4%** 内。

**Working page:** [SPLASH](/papers/splash-sparse-attention-hbf.md)
