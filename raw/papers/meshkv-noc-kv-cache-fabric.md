---
type: Raw Source
title: "MeshKV: A Network-on-Chip KV Cache Fabric for Scalable Transformer Decoding Accelerators"
source_url: https://arxiv.org/abs/2609.19207
arxiv: '2609.19207'
ingested: 2026-09-21
sha256: 3de679e8c29a24c28592df1192bcd4b8527f38a9c158ecfad032d92496c3e4e7
---

# MeshKV: A Network-on-Chip KV Cache Fabric for Scalable Transformer Decoding Accelerators

**Authors:** Dong Liu, Yanxuan Yu (equal contribution)
**Affiliation:** UCLA; Columbia University
**PDF:** [MeshKV_NoC_KV_Cache_Fabric_2026.pdf](MeshKV_NoC_KV_Cache_Fabric_2026.pdf)
**arXiv:** [2609.19207](https://arxiv.org/abs/2609.19207)（2026-09-16，cs.AR；9/18 早报漏扫，今日补）

## 问题

瓦片加速器上 autoregressive decode 的 KV 访问不规则；集中式内存路径在长上下文下把流量压在同一条二分割，背压占大量链路周期。

## 方法要点

- **TaKV**：仿射条带放置 \(\pi(\ell,s)\) + 占位交换，摊平 home 热点。
- **Mare**：多播树 + exact-tag/bloom 去重；VN0 单播 PART / VN1 多播 KV，Turn Model 无死锁。
- **Pad**：预取 / tile 乘 / 流式 softmax 与信用对齐 FIFO 重叠。
- 实现：Alveo U280 **8×8** mesh，512-bit wormhole；LLaMA-2-7B / Mistral-7B，T=8K–32K，B=1/4/8；硬件实测。

## 摘录数字（仅论文给出）

- 互连流量 vs CENT（T=32K,B=1）：LLaMA **0.42×**（−58%）、Mistral **0.40×**。
- 二分 KV 带宽利用率（LLaMA T=32K）：MeshKV **61%** vs SHARED **29%**（约 **2.1×**）。
- 多流吞吐（T=32K LLaMA）：B=1 **1.35×**、B=8 **1.90×** vs CENT。
- 链路能量 vs CENT **−48%**；每 token 净能量 **−17%**（活动估计）。
- Ablation（B=8）：去 Mare 吞吐 **0.62×**、流量 **1.55×**（相对完整 MeshKV）。
