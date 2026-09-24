---
type: Raw Source
title: "Hot–Cold Tiering of HBM and High Bandwidth Flash for Agentic LLM Serving"
description: "HBM 热集 + HBF 冷池；Qwen3-Coder-30B-A3B：14 ms TBT、resume +≈0.1 ms、并发会话 24×；相对全闪读功耗 −7.6 kW/8-GPU。"
timestamp: '2026-09-24T00:00:00Z'
source_url: https://arxiv.org/abs/2609.25782
arxiv: '2609.25782'
ingested: 2026-09-24
sha256: 0ed33586aa6c253698c71cc0f10d2f210c664747b636f78f8480fe7d86c170a0
---

# Hot–Cold Tiering of HBM and High Bandwidth Flash for Agentic LLM Serving

**Authors:** Jongjin Baek, Won Ji, Seungjae Yoo, Joo-Young Kim  
**PDF:** [HotCold_HBM_HBF_Agentic_LLM_2026.pdf](HotCold_HBM_HBF_Agentic_LLM_2026.pdf)  
**arXiv:** [2609.25782](https://arxiv.org/abs/2609.25782)（2026-09-22，cs.AR；IEEE CAL）

## 问题

Agentic 多轮会话在 tool/用户等待期间 idle，但需保留完整 KV。HBM 容量不够撑住大量暂停会话；把全部 KV 放 HBF 则每步 decode 读功耗与写寿命不可接受。

## 方法要点

- 观察双峰访问：热集（活跃会话）每步读；冷池（暂停会话）仅 resume 时读。
- 架构：共封装 HBM+HBF；热集驻 HBM，冷池迁 HBF；resume 经 D2D/base-die 预取；写策略 write-on-evict。
- 评测：B200 192 GiB HBM + 3 TiB SLC HBF（带宽对齐 HBM）；Qwen3-Coder-30B-A3B agentic 轨迹仿真。

## 摘录数字（仅论文给出）

- TBT：Na=48 时 **14 ms**（72 tok/s）、Na=128 时 **27 ms**（37 tok/s）；均在 50 ms SLO 内。
- Resume：相对 prefill 仅加 **≈0.1 ms**（文中 HBF 路径约 0.084 ms；NVLink-C2C 1.0 ms、PCIe 7 ms、recompute 14 ms）。
- 并发：相对无 HBF 冷层，每 GPU 会话 **24×**。
- 功耗：相对 all-KV-to-flash，20 pJ/bit 假设下每卡约 **950 W**、8-GPU 节点 **7.6 kW**（扫能量 2.1–12.2 kW/节点）。
- 双峰：Na=48 时热集占驻留容量 **3%**、读流量 **98%**。
- 寿命：write-on-evict 在 Na=48 约 **20 年**；all-KV-to-flash 约 11→8 年（Na=48→128）。

**Working page:** [Hot–Cold HBM/HBF](/papers/hotcold-hbm-hbf-agentic-llm.md)
