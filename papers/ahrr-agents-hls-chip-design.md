---
type: Paper
title: "AHRR: 更高抽象能否让 Agent 设计更好的芯片"
description: "UCLA — Agent HLS + Post-HLS RTL 精炼（AHRR）；11 任务相对 Direct RTL 几何均值 2.6×；ICCAD’26。"
tags:
- architecture
- agentic-ai
- ai-agent
- accelerator
- compiler
- methodology
- llm
created: 2026-09-23
updated: 2026-09-23
timestamp: '2026-09-23T00:00:00Z'
paper_author: [Zijian Ding, Yang Zou, Yizhou Sun, Jason Cong]
year: 2026
arxiv: '2609.21157'
sources:
  - raw/papers/AHRR_Agents_Higher_Abstraction_Chip_Design_2026.pdf
  - raw/papers/ahrr-agents-hls-chip-design.md
---

# AHRR：更高抽象能否让 Agent 设计更好的芯片

## 一句话结论

多数 agent 直接写 RTL；UCLA 展示 **AHRR（Agent-based HLS + Post-HLS RTL Refinement）** 在 11 任务套件上相对 Direct RTL 达 **2.6×** 几何均值加速——HLS 把设计知识蒸馏进抽象，RTL 精炼回收底层优化。

## 动机

Agentic chip design 已常见于 RTL 生成，但抽象层级是否改变设计质量缺少对照。作者用 FPGA 做可部署的端到端评测平台（强调取舍大体与目标工艺无关）。

## 方案

四条流对照：Direct RTL、Agent-based HLS、Post-Compiler HLS Refinement、Post-HLS RTL Refinement；后两者与 Agent HLS 组合为 **AHRR**。基准覆盖 LLM 推理、agentic memory、机器人、GEMM 等 11 任务。

## 量化结果

- **AHRR vs Direct RTL：2.6×** geomean。
- **Agent-based HLS alone：2.31×** geomean vs Direct RTL。
- 弱模型在 HLS 路径上可达强模型加速的 **0.95×**，Direct RTL 路径仅 **0.40×**（六任务成功子集）。
- ROB1（NMS）案例：HLS 路径用 pragma 拉到 256-way；同 agent Direct RTL 仅 32/8-way，周期约 1.86M vs 127K。

## 局限与解读

属 **agentic AI × chip design 流程** 增量，不是新 ASIC 微架构；落地依赖 HLS/FPGA 工具链质量。与 [DSA Processor Design Tradeoffs](../concepts/dsa-processor-design-tradeoffs.md) 的“抽象/简化控制核”叙事相连：把并行意图交给 HLS 比让 agent 手写 Verilog 更稳。代码：https://github.com/ZijD/AHRR

# Citations

1. Ding, Zou, Sun, Cong. “Can Agents Design Better Chips with a Higher Level Abstraction?” arXiv:2609.21157, ICCAD ’26, 2026. [arXiv](https://arxiv.org/abs/2609.21157)
2. [本地原文 PDF](../raw/papers/AHRR_Agents_Higher_Abstraction_Chip_Design_2026.pdf)；[原始来源记录](../raw/papers/ahrr-agents-hls-chip-design.md)
