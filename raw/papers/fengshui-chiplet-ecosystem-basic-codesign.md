---
type: Raw Source
title: "Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign"
source_url: https://arxiv.org/abs/2609.10970
arxiv: '2609.10970'
ingested: 2026-09-14
sha256: bfa0bc5f58298c6e140b0ae2f78a8443b7f84b9b8263f8d6a82e672d16ad9419
---

# Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign

**Authors:** Haoran Jin, Jirong Yang, Zhiheng Zhang, Justin Shin, Barry Lyu, Kangqi Zhang, Yunpeng Liu, Nathan Bleier
**Affiliation:** University of Michigan
**PDF:** [Fengshui_Chiplet_Ecosystem_BASIC_Codesign_2026.pdf](Fengshui_Chiplet_Ecosystem_BASIC_Codesign_2026.pdf)
**arXiv:** [2609.10970](https://arxiv.org/abs/2609.10970)（2026-09-10，cs.AR）

## 问题

算子级异构（微架构/批/内存）能显著提效，但单体 BASIC 的 NRE 不可承受；chiplet 复用摊薄 NRE，但「池子里做哪些 die」与「怎么拼成加速器」互相依赖。

## 方法要点

- **Fengshui**：联合优化 chiplet pool 与 BASIC 拼装。
- 算子级拆分；共探 chiplet/内存异构、tensor fusion、PP/TP/EP，并用 P&R 校验可实现性。
- 约 **8** 颗策略选型 chiplet 覆盖多种微架构。

## 摘录数字（仅论文给出）

- vs 同构加速器：能量 / energy×$ / EDP / EDP×$ 分别降 **48.5% / 88.1% / 93.0% / 97.8%**；相对无约束异构设计评分差距 **≤4.1%**。
- 数据中心 MoE/稠密 LLM serving：prefill 能量与 energy×$ 最高降 **16.8% / 28.7%**。
- 边缘自动驾驶感知：能量 / energy×$ **12.0% / 23.6%**（实时延迟约束下）。
