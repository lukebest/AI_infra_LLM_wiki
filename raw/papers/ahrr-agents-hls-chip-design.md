---
type: Raw Source
title: "Can Agents Design Better Chips with a Higher Level Abstraction?"
description: "UCLA — AHRR=Agent HLS + RTL 精炼；11 任务相对 Direct RTL 几何均值 2.6×（ICCAD’26）。"
timestamp: '2026-09-23T00:00:00Z'
source_url: https://arxiv.org/abs/2609.21157
arxiv: '2609.21157'
ingested: 2026-09-23
sha256: f8a06282a66d3fcef6558ccbdcbd0b9836482ae8425d09859353e61171df32a5
---

# AHRR: Agents + Higher-Level Abstraction for Chip Design

**Authors:** Zijian Ding, Yang Zou, Yizhou Sun, Jason Cong  
**Affiliation:** UCLA  
**PDF:** [AHRR_Agents_Higher_Abstraction_Chip_Design_2026.pdf](AHRR_Agents_Higher_Abstraction_Chip_Design_2026.pdf)  
**arXiv:** [2609.21157](https://arxiv.org/abs/2609.21157)（2026-09-17，cs.AI/cs.AR；ICCAD ’26）

## 问题

多数 LLM agent 直接写 RTL；作者问更高层抽象（HLS）是否能让 agent 设计出更好的芯片。

## 方法要点

对比四条流：Direct RTL、Agent-based HLS、Post-Compiler HLS Refinement、Post-HLS RTL Refinement；组合后两者为 **AHRR**。FPGA 端到端评测（设计流取舍大体与目标工艺无关）。

## 摘录数字（仅论文给出）

- 11-task suite：AHRR 相对 Direct RTL **2.6×** 几何均值加速。
- Agent-based HLS  alone 相对 Direct RTL **2.31×** geomean。
- 案例：弱模型在 HLS 路径上可达强模型 **0.95×** 的加速比，而 Direct RTL 仅 **0.40×**。

**Working page:** [AHRR](/papers/ahrr-agents-hls-chip-design.md)  
**Code:** https://github.com/ZijD/AHRR
