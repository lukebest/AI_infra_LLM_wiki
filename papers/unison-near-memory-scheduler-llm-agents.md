---
type: Paper
title: "UNISON: Near-Memory Session KV Scheduler for LLM Agents"
description: 复旦 — agent 会话近存调度核 SPEAR+TIDE；hit +0.3–23.1%、AMAT −22–51%、长程 TTFT −58–89%；28nm 0.169 mm² / 13.6 mW
tags:
- agentic-ai
- ai-agent
- kv-cache
- memory
- hbm
- sram
- accelerator
- scheduling
- llm
- inference
- serving
- latency
- architecture
- hardware
timestamp: '2026-09-16T00:00:00Z'
created: 2026-09-16
updated: 2026-09-16
sources:
- raw/papers/UNISON_Near_Memory_Scheduler_LLM_Agents_2026.pdf
- raw/papers/unison-near-memory-scheduler-llm-agents.md
---

# UNISON: A Co-Designed Near-Memory Scheduler of Session KV Residency for LLM Agents

**Authors:** Fan He, Yan Li, Xiaoyang Zeng
**Affiliation:** State Key Laboratory of Integrated Chips and Systems, Fudan University
**arXiv:** [2609.09643](https://arxiv.org/abs/2609.09643)（2026-09-09，cs.AR）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.09643)

相对纯软件 KV 淘汰（AgentKV 等）与通用近存调度，UNISON 把 **agent 会话级 KV 驻留**做成 **事件驱动近存 ASIC 调度核**，并论证不可拆成独立 IP/纯软件。

## 动机

Agent 循环（规划→调工具→恢复）跨 wait 保留增长 KV 前缀，多会话挤在同一 SRAM/HBM 池。Recency / timeout / identity 代理把 **仍在等待工具返回的会话** 当冷数据丢掉，导致重 prefill 与 TTFT 恶化。问题是 **会话级驻留效率**，与算子/计算模式优化正交。

## 方案

**UNISON**（Unified Native Inter-turn Session Orchestration Nexus）：

- **SPEAR**：按 gap 均值与 turn 索引 hazard 选淘汰受害者。
- **TIDE**：把观测到的 wait 当作 DMA 预算，决定谁升入快层。
- 二者共享同一 live ranking；事件驱动近存实现。
- 结构必然性分析：统一近存设计不能拆成独立 IP 或纯软件而不重引入文内失败模式。

## 效果（仅论文数字）

- 评测：coding + general-mission；三模型族；**1415** sessions / **33596** turns。
- 联合策略为每条 trace 上最佳非 oracle：hit rate **+0.3%–23.1%**，AMAT **−22%–51%**；长程 traces 上 TTFT **−58%–89%**。
- **28 nm CMOS** 调度核：**0.169 mm²**，**13.6 mW** @ **150 MHz**；浮点排序复现 Kendall τ **>0.998**。

**口径提醒：** 调度核面积/功耗相对其管理的 KV 层次可忽略；主数字来自 trace 驱动策略对比 + 硅核保真，不是端到端商用 agent 集群实测。

## 与 wiki 的关系

- [Heterogeneous Computing for AI Agent Inference](/papers/heterogeneous-computing-ai-agent-inference.md) — agent CF 墙；本文落地 **近存调度硬件**
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — AMAT / 多层 KV 驻留
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — 分层放置对照；UNISON 强调 agent return-gap 机制信息
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 会话驻留与 PD 池正交的另一轴

## 开放问题

1. 与生产 block-cache / SGLang 前缀树的接口边界（文内有替换实验，需读正文）。
2. 多租户 QoS 下 SPEAR hazard 表的公平性。
3. 相对纯软件 AgentKV 类方法的硬件必要性边界在更高容量 SRAM 时是否收缩。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.09643) — He/Li/Zeng, arXiv:2609.09643
[2] [raw/papers/unison-near-memory-scheduler-llm-agents.md](raw/papers/unison-near-memory-scheduler-llm-agents.md) — 结构化摘录
