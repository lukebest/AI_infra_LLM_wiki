---
type: Paper
title: "UlaCache: Unified Logical Addressing for Sparse LLM Serving"
description: "Scitix.AI — 统一逻辑 KV 地址跨 GPU/可选 CPU；相对 HiSparse 投机 decode 峰值吞吐 8×H200 1.16×(DP)/1.70×(TP)、8×B300 1.73×/2.51×；B300 TP 无投机峰值 3.51× SGLang；PB-LRU 调度约 1.5–2.3× naive LRU"
tags:
- inference
- kv-cache
- serving-system
- decode
- gpu
- memory
- batching
- latency
- throughput
- llm
- speculative-decoding
created: 2026-11-02
updated: 2026-11-02
timestamp: '2026-11-02T00:00:00Z'
paper_author: [Isaac Zhu, Alan Cao, Hugh Yin, Rocky Wang, Orion Wang, Hscos Zhang, Jack Li, Jason Zhao]
year: 2026
venue: arXiv
arxiv: '2610.29820'
sources:
  - raw/papers/UlaCache_Unified_Logical_Sparse_KV_Serving_2026.pdf
  - raw/papers/ulacache-unified-logical-sparse-kv-serving.md
---

# UlaCache：稀疏 LLM serving 的统一逻辑 KV 地址

## 一句话结论
稀疏 attention 仍需保留历史 KV；固定 per-request GPU 缓冲会浪费空闲容量并抬高 TPOT。UlaCache 用**跨 GPU 池与可选 CPU 的统一逻辑地址**解耦分配/选择与物理放置，TP 侧用本地 GPU 缓冲只补缺失项，CPU 开启时用 **PB-LRU** 共享 GPU 池；相对 HiSparse、在匹配 CPU/GPU 预算且开启投机时，峰值 decode 吞吐 **8×H200 1.16×(DP)/1.70×(TP)**、**8×B300 1.73×(DP)/2.51×(TP)**；B300 TP 无投机峰值吞吐达 GPU-resident SGLang 峰值的 **3.51×**。

## 动机
- 长上下文抬高 KV 内存；稀疏 attention 减计算与流量，但被选中的历史 KV 在后续 decode 仍须可达。
- HiSparse 等按请求固定 GPU 配额：空闲容量无法被其他请求共享；在 8×B300 DP + 投机的一档配置里，HiSparse TPOT 比 GPU-resident SGLang 高 **23.5%**。

## 方案
1. **统一逻辑地址空间**：推理引擎按逻辑引用分配/选择 KV，再映射到 GPU 池或可选 CPU。
2. **DP / TP 接口**：DP 为 rank 本地历史；TP 为分布式历史，本卡 GPU 缓冲保留已选 KV，只对缺失项做传输。
3. **PB-LRU**：CPU 存储开启时，按 recency bucket 并行更新元数据与选 victim；相对 naive LRU，较大 batch 下 GPU 调度时间约 **1.5–2.3×** 更快。
4. **实现与负载**：接入 SGLang；GLM-5.3（FP8 权重/KV、BF16 激活）；Multi-LexSum 64K–128K 输入、贪心生成 **2,048** token；投机为 MTP 两步草稿。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 峰值吞吐 vs HiSparse（投机开，匹配预算）8×H200 | **1.16× (DP) / 1.70× (TP)** |
| 同上 8×B300 | **1.73× (DP) / 2.51× (TP)** |
| B300 TP 无投机峰值 vs SGLang 峰值 | **3.51×** |
| PB-LRU vs naive LRU（调度时间） | 约 **1.5–2.3×** 更快 |
| HiSparse TPOT vs GPU-resident SGLang（一档 DP B300） | **+23.5%** |

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 页式 KV 与 SGLang 稀疏服务路径；统一逻辑地址把选择与物理放置拆开
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — GPU↔CPU KV 池与 PB-LRU 替换路径
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — DP/TP 下历史存储角色拆分，与 PD 解耦正交
- [ZipFusion](/papers/zipfusion-lossless-kv-attention-fusion.md) — 同属 SGLang KV 路径优化，侧重压缩融合 attention

## 开放问题
- 评测以 GLM-5.3 + Multi-LexSum 为主；跨模型稀疏索引器与多租户共享池的干扰未系统展开。
- PB-LRU 与多层存储（SSD/远端）叠加、以及与 disagg P/D KV 交接的组合未报告。

# Citations
- [arXiv:2610.29820](https://arxiv.org/abs/2610.29820) — Zhu et al., Scitix.AI, 2026
- [raw stub](/raw/papers/ulacache-unified-logical-sparse-kv-serving.md)
