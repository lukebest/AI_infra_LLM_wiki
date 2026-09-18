---
type: Paper
title: "Fathom: Per-Query Bit-Plane Scan for Offloaded KV"
description: 独立 — host 卸荷 KV 上 per-query 读深；Qwen3-8B@1M vs 136-bit 扫 1.67×；同 time 少读 18%
tags:
- kv-cache
- inference
- serving
- llm
- memory
- memory-bandwidth
- agentic-ai
- ai-agent
- quantization
- sparse
- latency
- throughput
- architecture
- hbm
timestamp: '2026-09-18T00:00:00Z'
created: 2026-09-18
updated: 2026-09-18
sources:
- raw/papers/Fathom_Sparse_Decoding_Offloaded_KV_2026.pdf
- raw/papers/fathom-sparse-decoding-offloaded-kv.md
---

# Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches

**Authors:** Vivek Kalyanarangan
**Affiliation:**（文内独立署名）
**arXiv:** [2609.17652](https://arxiv.org/abs/2609.17652)（2026-09-15，cs.LG；Thu 9/17 cs.DC 列表）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.17652)

面向 **百万 token agent 会话、多会话常驻、KV/索引在 host** 的 regime：top-k 前的全量 key scan 主导 PCIe 流量。Fathom 让每个 query 决定每个 key 通道读多少 bit。

## 动机

- Dense attention 读整份 KV；top-k 把 winner 行压到 ~200 MB/step，但排名用的 scan 随 n 线性涨（Qwen3-8B @1M 约 **5.1 GB**/step 量级的 136-bit 扫）。
- Loki / Double Sparsity / SparQ 等固定每通道读深；重要通道的第 1 bit 远比第 4 bit 值钱。

## 方案

1. **Bit-plane K store**：4-bit K 按 channel-major 存为平面；前 t 个平面即该通道 t-bit mid-rise 量化器。
2. **Per-query reverse water-filling**：按方差加权边际收益分配 bit 预算。
3. 评测：A100；对照 Loki / Double Sparsity / SparQ / thumbnail / landmark；含 RULER 与真实 coding-agent 会话。

## 效果（仅论文数字）

| 设定 | 数字 |
|------|------|
| Qwen3-8B @1M，host KV+index | GPU time vs 136-bit 扫 **1.67×**；vs landmark **2.50×** |
| 同模型 @256k | vs 136-bit **1.37×** |
| 同 GPU time vs SparQ r=16 | 少读 **18%** 字节；7 设定中 **6** 个更低 attention error |
| Coding-agent 会话 | 达最准 136-bit 扫的 step agreement 仅需 **92 bits** |
| Index 在 HBM | **不更快**（扫核本身不赢） |

**口径：** 算法/系统测量在 A100；加速来自 **host 卸荷扫索引**，非新 ASIC。

## 与 wiki 的关系

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — host↔GPU KV 扫流量
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — 更冷层卸荷对照
- [UNISON](/papers/unison-near-memory-scheduler-llm-agents.md) — agent 会话驻留 vs 本文 **扫带宽**
- [Ask the Tool](/papers/ask-tool-progress-agent-kv-serving.md) — 工具期 KV 控制面 vs 本文 decode 期稀疏扫
- [Vortex](/papers/vortex-extreme-compression-llm-inference.md) — 另一条 KV/权重压缩路径

## 开放问题

1. 与 PagedAttention / 分层 KV 索引的正交组合。
2. 写路径（K 更新）对 bit-plane 布局的开销。
3. 多租户并发扫对 PCIe QoS 的影响。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.17652) — Kalyanarangan, arXiv:2609.17652
[2] [raw/papers/fathom-sparse-decoding-offloaded-kv.md](raw/papers/fathom-sparse-decoding-offloaded-kv.md) — 结构化摘录
