---
type: Raw Source
title: "UNISON: A Co-Designed Near-Memory Scheduler of Session KV Residency for LLM Agents"
source_url: https://arxiv.org/abs/2609.09643
arxiv: '2609.09643'
ingested: 2026-09-16
sha256: 7806057eda2854b6084f1b0021892bba918c6b484f7bfad703c5bb1abb23bdb0
---

# UNISON: Near-Memory Scheduler of Session KV Residency for LLM Agents

**Authors:** Fan He, Yan Li, Xiaoyang Zeng
**Affiliation:** State Key Laboratory of Integrated Chips and Systems, Fudan University
**PDF:** [UNISON_Near_Memory_Scheduler_LLM_Agents_2026.pdf](UNISON_Near_Memory_Scheduler_LLM_Agents_2026.pdf)
**arXiv:** [2609.09643](https://arxiv.org/abs/2609.09643)（2026-09-09，cs.AR）

## 问题

Agent 循环跨 tool wait 保留增长 KV 前缀，多会话共享 SRAM/HBM；recency/timeout/identity 代理把「活着的等待」当冷数据淘汰。

## 方法要点

- UNISON：事件驱动近存调度核；SPEAR（Survival-Penalty Eviction）与 TIDE（Idle-window DMA Tiering）共享同一 live ranking。
- 结构必然性：不可拆成独立 IP / 纯软件而不重引入失败模式。
- **28 nm CMOS** 调度核。

## 摘录数字（仅论文给出）

- 1415 sessions / 33596 turns；三模型族；相对非 oracle 基线 hit rate **+0.3–23.1%**，AMAT **−22–51%**，长程 traces TTFT **−58–89%**。
- 硅：面积 **0.169 mm²**，功耗 **13.6 mW** @ **150 MHz**；Kendall τ **>0.998**。
