---
type: Raw Source
title: "Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches"
source_url: https://arxiv.org/abs/2609.17652
arxiv: '2609.17652'
ingested: 2026-09-18
sha256: c4827558328983002fabcb68d2f29c90ea3cf1a204ee6d4aeb48dd798471d0ad
---

# Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches

**Authors:** Vivek Kalyanarangan
**Affiliation:**（文内；独立作者署名）
**PDF:** [Fathom_Sparse_Decoding_Offloaded_KV_2026.pdf](Fathom_Sparse_Decoding_Offloaded_KV_2026.pdf)
**arXiv:** [2609.17652](https://arxiv.org/abs/2609.17652)（2026-09-15，cs.LG；Thu 9/17 cs.DC 列表）

## 问题

长上下文 agent 会话 KV/索引在 host 时，top-k 前的全量 key scan 成为 decode 主导流量；既有 per-token scan 对每通道固定读深。

## 方法要点

- 4-bit K 按 channel-major bit plane 存放；每 query 按 reverse water-filling 分配每通道读深。
- 面向 host 卸荷 / PCIe 扫索引的 regime；HBM 驻留索引时无加速。

## 摘录数字（仅论文给出）

- Qwen3-8B @ 1M tokens，A100：decode GPU time vs 136-bit 扫（Double Sparsity / Loki / SparQ r=32）**1.67×**；@256k **1.37×**。
- 同 GPU time 相对 SparQ r=16（68-bit）：少读 **18%** 字节；7 设定中 6 个更低 attention error。
- Coding-agent 会话：达最准 136-bit 扫的 step agreement 仅需 **92 bits**。
