---
type: Paper
title: "Hot Chips 2026: Handy HBM Tutorial Introduction"
description: Objective Analysis — Hot Chips 2026 HBM 教程开场；HBM 吃 3× DDR 晶圆面积、DRAM 产能十年未涨；PIM/base-die 被推理推上台
tags:
- hbm
- memory
- inference
- architecture
- memory-bandwidth
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Handy_HBM_Tutorial_Introduction.pdf
- raw/papers/hc2026-handy-hbm-tutorial.md
---

# Memory: Feeding AI’s Voracious Hunger for Data

**Speaker:** Jim Handy（Objective Analysis）  
**Venue:** Hot Chips 2026 Tutorial（开场）  
**PDF:** [raw/papers/HC2026_Handy_HBM_Tutorial_Introduction.pdf](raw/papers/HC2026_Handy_HBM_Tutorial_Introduction.pdf)

市场账，给后面三星 / SK hynix / d-Matrix / OXMIQ 教程当分母。不含工艺数字。图表纵轴年份/美元大多不可读 → **未知**。

同场后续：[Samsung B-die](/papers/hc2026-samsung-hbm-base-die.md)、[SK hynix packaging](/papers/hc2026-skhynix-hbm-advanced-packaging.md)、[d-Matrix Raptor](/papers/hc2026-dmatrix-raptor-3d-dram.md)、[OXMIQ HBF](/papers/hc2026-oxmiq-hbf.md)。Micron 同场教程页眉 Confidential，**未 ingest**。

## 议程

三块：当前 AI 内存市场、长期方向、当天讲师。讲师目录：Micron Raghu Sreeramaneni；Samsung Sangwook Han（Custom HBM4E Design Lead）；SK hynix Jaesik Lee（VP Package Engineering）；d-Matrix Sudeep Bhoja + Meta Aayush Ankit；OXMIQ Anurag Agrawal + Praxmati Radhakrishna Giduthuri。

## 市场账（仅幻灯片正文）

DRAM 短缺三驱动：

1. AI 开支超预期（Alphabet / Meta / Amazon / Azure / Alibaba / Apple 资本开支曲线有图，具体 $B 刻度 **未知**）。
2. 带宽需求吃掉过量晶圆——**HBM takes 3× the die area of DDR**。
3. DRAM 晶圆产能 **static for >10 years**，新产能 **>2 years** 才能装上。

结果是内存营收创新高（Samsung / Kioxia / SanDisk / Micron / SK hynix）；图中绝对 $B **未知**。增长主要来自涨价：spot 图标注 branded DRAM **7.1×**、NAND **6.9×**（相对低点的倍数；绝对 $/GB 刻度 **未知**）。

预告 Objective Analysis 新报告：HBM 为何贵、供应链、HBM vs DRAM 价格、收入/出货/ASP；**September** 可从 Objective-Analysis.com/reports 下载。

## 长期与 PIM

推理资源从 MCU 到 hyperscale LLM；算法 refinement 可能让今天的 data-movement 问题淡出。PIM / 近存三条：用 HBM **base die**；定制 memory 芯片冲更高性能；低端 Analog Neural Nets。**Software support is currently weak — This is a gating factor.**

设计原则：信道带宽需求与两端智能成反比。口号 “AI Everywhere”。

## 与 wiki 的关系

- [DRAM and Memory System](/concepts/dram-memory-system.md) — HBM 带宽公式与内存墙的 2026 市场分母
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — HBM 吃 3× DDR 面积，是 TSV 栈的成本侧
- [Samsung HBM Base Die](/papers/hc2026-samsung-hbm-base-die.md) — 开场预告的 B-die / cHBM / zHBM
- [OXMIQ HBF](/papers/hc2026-oxmiq-hbf.md) — 容量点（HBF）不是更便宜的 HBM

# Citations

[1] [raw/papers/HC2026_Handy_HBM_Tutorial_Introduction.pdf](raw/papers/HC2026_Handy_HBM_Tutorial_Introduction.pdf) — Jim Handy, Hot Chips 2026 Tutorial
[2] [raw/papers/hc2026-handy-hbm-tutorial.md](raw/papers/hc2026-handy-hbm-tutorial.md) — 结构化摘录
