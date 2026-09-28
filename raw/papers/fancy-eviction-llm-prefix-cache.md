---
type: Raw Source
title: "When Fancy Eviction Fails: Rethinking Cache Replacement For LLM Prefix Reuse"
description: "Harvard — 生产 prefix-cache 轨迹×14 淘汰算法；LRU 难被击败；partial-node compute-aware vs LRU TTFT −19.9%、prefill +18.8%。"
timestamp: '2026-09-28T00:00:00Z'
source_url: https://arxiv.org/abs/2609.28870
arxiv: '2609.28870'
ingested: 2026-09-28
sha256: a722eccab3e868da0ac061ee19f3165de4066c02d9f72da91bba15675502842e
---

# When Fancy Eviction Fails: Prefix-Cache Replacement

**Authors:** Yiyu Liu, Minlan Yu, Juncheng Yang  
**Affiliation:** Harvard University  
**PDF:** [Fancy_Eviction_LLM_Prefix_Cache_2026.pdf](Fancy_Eviction_LLM_Prefix_Cache_2026.pdf)  
**arXiv:** [2609.28870](https://arxiv.org/abs/2609.28870)（2026-09-24，cs.DC）

## 问题

Agentic / 长会话 LLM 依赖 prefix cache 降 prefill，但生产轨迹下「花哨」淘汰策略相对 LRU 几乎无增益，而 Belady 仍有巨大空间——需要解释原因并给出可落地原则。

## 方法要点

- 两条生产轨迹（FreeInference / Chutes）+ 忠实 prefix-cache 仿真器（相对 vLLM Python 最高约 **160×** 评估加速）。
- 系统评估 **14** 种在线淘汰算法 vs Belady。
- 提出 compute-savings 目标与 offline oracle；RandomCompute / PartialNode RandomCompute。

## 摘录数字（仅论文给出）

- 命中率：多容量设定下 SOTA 策略均无法稳定超过 LRU（Figure 2）。
- vLLM + Qwen3-Coder-30B @48 GiB：partial-node compute-aware vs LRU — 平均 TTFT **−19.9%**（1.04 vs 1.29 s），prefill 吞吐 **+18.8%**（65.6K vs 55.2K tok/s）；p99 TTFT **26.0 → 16.8 s**。
- 块级 RandomCompute 因碎片化：TTFT **4.0×**、吞吐 **3.9×↓** vs LRU。
- 轨迹规模：FreeInference **327.5K** req / **10.5B** tokens / 7 d；Chutes **515.8K** / **9.7B** / 130.9 d；top 10% 会话占 **76.2%** KV 字节。

**Working page:** [Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md)
