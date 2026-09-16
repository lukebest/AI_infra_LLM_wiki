---
type: Paper
title: "Trillion-Parameter MoE in a Box: HBF Memory Provisioning"
description: Huawei — 万亿 MoE 权重驻留 HBF 后状态层只需 1.4–4.0 s⁻¹（vs HBM3e 33.3）；HBF×6 暴露 2.30 TB/s 即可逼近全暴露
tags:
- hbf
- hbm
- memory
- moe
- llm
- inference
- kv-cache
- serving
- architecture
- packaging
- memory-bandwidth
- agentic-ai
- huawei
- storage
timestamp: '2026-09-16T00:00:00Z'
created: 2026-09-16
updated: 2026-09-16
sources:
- raw/papers/Trillion_Param_MoE_HBF_Memory_Provisioning_2026.pdf
- raw/papers/trillion-param-moe-hbf-memory-provisioning.md
---

# Trillion-Parameter MoE in a Box: Decoupling Memory Provisioning with High-Bandwidth Flash

**Authors:** Pengfei Xia, Tuo Hao, Shengwei Li, Jinjing Chen, Shiru Wei, Wenjun Zou, Rui Zhang, Hui Zang
**Affiliation:** Huawei Technologies Co., Ltd.
**arXiv:** [2609.15636](https://arxiv.org/abs/2609.15636)（2026-09-14，cs.AR）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.15636)

相对 [FLINT](/papers/flint-hbf-llm-inference.md) / [DASH](/papers/dash-dual-path-hbf-moe-inference.md) 做 HBF 路径与 FTL，本文回答 **权重已在 HBF 之后** 的供给问题：状态 DRAM 要多少带宽/容量比？host 暴露是否必须跟 HBF 内部带宽同比？

## 动机

数据中心常用 continuous batching + PD 解耦摊销驻留；本文转向 **低并发（约 1–8）万亿 MoE 一体机**：整模驻一节点，冷/热 prefill、投机校验与 decode 共享固定资源。量化权重达 TB（DSV4-Pro **865 GB**、Kimi-K3 **1560 GB**），HBM-only 难做紧凑节点。HBF 适配合读权重；一旦权重迁出，DRAM 不再随模型规模涨，而 HBF 包数随容量涨时「全暴露」会让 host I/O 跟着模型规模跑。

## 方案

设计空间覆盖 HBF×DRAM（HBM3e / SOCAMM2 / LPCAMM2）、暴露比 η_exp=B_ext/B_int（按 96 GB/s host-link quanta）、可选 HBF 上 FP8 near-data 引擎。工作负载含实测专家路由与 **多轮 agentic** traces。结论强调两个 **正交膝点**：状态带宽 vs HBF 传输。

## 效果（仅论文数字）

- **Q1**：256-GB 状态层地板上，两模型达 **1.10×** 完成时间目标只需带宽/容量比 **1.4–4.0 s⁻¹**（Kimi-K3 1.4 / DSV4-Pro 4.0），相对 HBM3e **33.3 s⁻¹** 约 **8×–24×** 放松。LPCAMM2×8（512 GB、**1.09 TB/s**）可达 DSV4-Pro 目标；同容量若干 SOCAMM/LPCAMM 配置仍在线外。
- **Q2**：HBF×6 每包暴露 **384 GB/s**，聚合 **2.30 TB/s**，比全暴露参考 **6.14 TB/s** 低 **62.5%**，仍可落在约 10% 性能窗；更多包可在同目标下降低每包所需 host 带宽。
- 状态膝点约在 **0.6–1.2 TB/s**（DSV4-Pro）与 **0.4–0.6 TB/s**（Kimi-K3）量级（Trace A）；越过膝点后再加该维带宽收益扁平。

**口径提醒：** 分析/仿真供给膝点，非商用一体机实测 tok/s；模型规格取自文内 Table 1。

## 与 wiki 的关系

- [FLINT](/papers/flint-hbf-llm-inference.md) / [DASH](/papers/dash-dual-path-hbf-moe-inference.md) / [OXMIQ HBF](/papers/hc2026-oxmiq-hbf.md) — HBF 作为容量层；本文做 **供给膝点** 而非路径微架构
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 权重层与状态层解耦后的 AMAT/带宽比
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 本文是 **单节点一体机**，不是机柜 PD 池；与 PD 解耦对照
- [Heterogeneous Computing for AI Agent Inference](/papers/heterogeneous-computing-ai-agent-inference.md) — agentic 上下文雪崩；本文用 agentic traces 压状态层

## 开放问题

1. 膝点对更宽投机草稿长度 / 更高并发是否漂移。
2. near-data FP8 引擎对低用专家的增益未成主结果数字。
3. 与 FLINT/DASH 路径栈如何联合闭式供给。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.15636) — Xia et al., arXiv:2609.15636
[2] [raw/papers/trillion-param-moe-hbf-memory-provisioning.md](raw/papers/trillion-param-moe-hbf-memory-provisioning.md) — 结构化摘录
