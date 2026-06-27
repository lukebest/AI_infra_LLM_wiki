---
type: Concept
title: Quantitative Architecture Fundamentals
description: Hennessy & Patterson 量化体系结构基石：CPU 性能公式、Amdahl 定律、局部性、功耗墙、Dennard Scaling 终结与暗硅
tags:
- architecture
- cpu
- benchmark
- power
- wse
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-01.md
- raw/articles/arch-study-30d-day-02.md
---

# Quantitative Architecture Fundamentals（量化体系结构基石）

Hennessy & Patterson 量化方法的核心：**用公式和测量驱动设计决策**，而非凭直觉。AI 加速器（含 [Cerebras WSE](/entities/cerebras-wse.md)）的选型同样建立在这些权衡之上。

## CPU 性能公式

```
CPU Time = IC × CPI × Clock Cycle Time
         = (IC × CPI) / Clock Rate
```

| 因子 | 决定因素 | 典型杠杆 |
|------|----------|----------|
| **IC** (Instruction Count) | ISA、编译器、算法 | 指令集精简、向量化 |
| **CPI** (Cycles Per Instruction) | 微架构 | 流水线、Cache、OoO |
| **Clock Rate** | 工艺、功耗、关键路径 | 工艺节点、电压 |

三因子**强耦合**：提频可能增 CPI（更深流水线 → 分支惩罚）；减 IC（复杂指令）可能增 CPI。

## Amdahl 定律

```
Speedup = 1 / ((1 - f) + f / S)

f = 可加速部分占比，S = 该部分加速比
```

即使 S→∞，上限为 **1/(1−f)**。优化应优先找**系统瓶颈**（最慢且占比大的部分）——与 [WSE Performance Model](/concepts/wse-performance-model.md) 四瓶颈项思路一致。

## 局部性原理

- **时间局部性**：近期数据可能再访问 → Cache / SRAM 保留
- **空间局部性**：相邻地址可能一起访问 → Cache line 预取

所有存储层次（Register → L1 → DRAM → [SRAM-first LPU](/concepts/lpu-architecture.md)）的理论基础。

## 动态功耗与功耗墙

```
P_dynamic = α × C × V² × f
```

- **V²** 使降电压成为最有效降功耗手段，但 f ∝ V，不能无限降
- 频率 +20%、电压 +20% → 功耗约 **×1.73**

### Dennard Scaling 终结（~2005）

理想缩放：每代工艺 s 倍缩小 → V↓、f↑、C↓、**功耗密度恒定**。2005 后阈值电压无法继续降低 → 主频停滞 ~4–5 GHz → **功耗墙 (Power Wall)**。

### 暗硅 (Dark Silicon)

可用晶体管数 >> 功耗预算可同时驱动的面积。启示：**专用化、低功耗 PE** 优于全芯片高频通用核——与 WSE 大量简单 PE、[Groq LPU](/concepts/lpu-architecture.md) 确定性低功耗路径一致。

## 晶圆成本与良率

```
Yield ≈ (1 - defects/area)^die_area
```

大面积 die（如 WSE 整晶圆）良率是**核心经济约束**——冗余/容错设计直接受良率模型驱动。

## 相关页面

- [Architecture Benchmark Methodology](/concepts/architecture-benchmark-methodology.md) — 如何公平量化比较
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 局部性的工程实现
- [Cerebras WSE](/entities/cerebras-wse.md) — 暗硅/良率/专用 PE 的实例
- [Deterministic Execution](/concepts/deterministic-execution.md) — 规避 OoO 功耗的替代路径

# Citations

[1] [raw/articles/arch-study-30d-day-01.md](raw/articles/arch-study-30d-day-01.md) — H&P Ch.1 导论（Day 1）
[2] [raw/articles/arch-study-30d-day-02.md](raw/articles/arch-study-30d-day-02.md) — 功耗与成本（Day 2）
