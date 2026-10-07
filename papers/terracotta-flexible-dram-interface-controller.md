---
type: Paper
title: "Terracotta: Enabling the Adoption of New DRAM Techniques via a Flexible DRAM Interface and Memory Controller"
description: "ETH SAFARI（MICRO 2026）— DDR5 上一次性标准化的自定义命令编码 + 可编程内存控制器（state/trigger/update/action），4 类 DRAM 技术保留 >96% 定制实现收益；DRAM 能耗开销 0.6–3.2%、面积 0.03%、功耗 0.56%"
tags:
- memory
- pim
- hardware
- architecture
- programming-model
created: 2026-10-07
updated: 2026-10-07
timestamp: '2026-10-07T00:00:00Z'
paper_author: [Harsh Songara, Konstantinos Kanellopoulos, F. Nisa Bostancı, Konstantinos Marios Sgouras, Ataberk Olgun, İsmail Emir Yüksel, Andreas Kosmas Kakolyris, A. Giray Yağlıkçı, Onur Mutlu]
year: 2026
arxiv: '2610.06475'
venue: "MICRO 2026 (extended version)"
sources:
  - raw/papers/Terracotta_Flexible_DRAM_Interface_Controller_2026.pdf
  - raw/papers/terracotta-flexible-dram-interface-controller.md
---

# Terracotta：让新 DRAM 技术不用每次改标准和控制器

## 一句话结论

DRAM 内计算（PuD）、低成本维护、子阵列并行、降延迟等技术，每一项都要 **改 DRAM 接口（新命令）+ 改内存控制器**，要么等新 JEDEC 标准，要么已部署系统用不上。Terracotta 观察到 32 种技术的命令结构和控制器流程高度相似，抽成原语：DRAM 厂商在一次性标准化的命令编码里自定义命令，系统设计者在 **可编程内存控制器** 里 post-silicon 写出新技术。DDR5 上 4 类技术保留 **>96%** 的定制实现收益，面积/功耗开销很小。

## 动机

- 刚性接口 + 固定控制器逻辑 = 每种新技术都要重复改；利益相关方目标冲突，已部署系统服役多年（卫星/航天更久）。
- AI/ML 的内存需求让这个问题更急。

## 方案

1. **自定义命令扩展**：命令 = 操作类型 + 目标 DRAM 位置（如 bank）+ 载荷（如行地址）；只标准化位宽/位置，语义由厂商定义（利用 DDR5 C/A 总线保留命令编码）。
2. **可编程内存控制器**：四原语 —— state（如最近访问行表）、trigger（请求命中条件时触发）、update（随已发请求维护状态）、action（发自定义命令）。例：ChargeCache 与 CROW 都是"跟踪合格行 → 命中 → 用降延迟时序"。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 4 种技术（PuD、低成本维护、子阵列并行、降延迟） | 保留定制实现相对基线收益的 **>96%** |
| 组合 ChargeCache + MASA | 优于各自单独的 Terracotta 实现，且各保留 >96% 定制收益 |
| DRAM 能耗开销 | **0.6–3.2%** |
| 面积 / 功耗（相对高端服务器 CPU） | **0.03%** / **0.56%**（摘要口径）；每 DDR5 通道 0.083 mm²、静态功耗 324 mW（45nm 综合后缩放到 10nm） |
| 系统配置 | DDR5-3200，1 通道 1 rank，8 bank group |

## 与 wiki 的关系

- [DRAM and Memory System](/concepts/dram-memory-system.md) — row buffer / bank / 子阵列并行是这些技术的作用点；Terracotta 把"控制器策略"变成可编程层
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 与 HBF、CXL 分层一样，是"内存侧要可演进"的另一个切面
- [SPIMOE](/papers/spimoe-hybrid-sparsity-reasoning-moe-pim.md) — PIM 加速 MoE 的工作若想落到商用 DRAM，需要类似的命令/控制器可扩展性

## 局限与开放问题

- 只做 DDR5；HBM / LPDDR（AI 加速器与端侧 SoC 主流）的命令总线与控制器如何适配未展开。
- 依赖 JEDEC 接受一次性的编码扩展；安全/隔离（自定义命令被滥用）需要额外机制。
- 对 AI 芯片：若 HBM 控制器也可编程，PuD 或 KV 相关的 DRAM 内操作可绕过标准周期上线。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.06475) — Songara et al., arXiv:2610.06475（MICRO 2026 extended）
[2] [raw stub](raw/papers/terracotta-flexible-dram-interface-controller.md)
[3] [Code](https://github.com/CMU-SAFARI/Terracotta)
