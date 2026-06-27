---
type: Concept
title: Architecture Benchmark Methodology
description: 体系结构量化评估方法论：几何均值、Speedup 计算、SPEC/MLPerf 原则与常见数据陷阱
tags:
- architecture
- benchmark
- methodology
- formal-analysis
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-06.md
---

# Architecture Benchmark Methodology（体系结构评估方法论）

体系结构是**以数据为核心的工程科学**。读论文、做对比、评估加速器均需遵循可复现、公平的量化方法。

## 几何均值 (Geometric Mean)

多 benchmark 汇总加速比时，**几何均值**是 H&P 标准：

```
GM = (S₁ × S₂ × ... × Sₙ)^(1/n)
Speedup = Time_old / Time_new
Overall Speedup = GM(Speedup₁, ..., Speedupₙ)
```

**关键性质**：GM(A/B) = 1/GM(B/A)（对称性）。算术均值对加速比**不对称**，会高估/低估差异。

## Benchmark 选择原则

| 原则 | 含义 |
|------|------|
| 代表性 | 覆盖目标 workload 典型操作 |
| 多样性 | compute-bound / memory-bound / branch-heavy 兼有 |
| 可重现 | 固定输入、编译选项、环境 |
| 公平性 | 同编译器优化级、同库版本 |
| 时效性 | 定期更新（SPEC ~3–5 年） |

代表套件：**SPEC CPU2017**（通用 CPU）、**MLPerf**（AI 训练/推理）。

## 公平比较约束

- 相同工艺节点、频率、内存/互连带宽预算
- 报告**绝对值**与相对提升（"50% 快"可能 1ms→0.67ms）
- 披露 outliers 与置信区间

## 常见陷阱

1. **Cherry-picking** — 只展示擅长 workload
2. **不对称约束** — 限对手频率不限自己
3. **忽略能效** — Performance/Watt 在功耗墙时代与性能同等重要
4. **混淆 peak vs sustained** — TFLOPS 峰值 vs 实际利用率

## 相关页面

- [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — Amdahl 与性能公式
- [WSE Performance Model](/concepts/wse-performance-model.md) — collective 性能建模实例
- [Voxel Simulator](/concepts/voxel-simulator.md) — 3D 芯片端到端仿真评估

# Citations

[1] [raw/articles/arch-study-30d-day-06.md](raw/articles/arch-study-30d-day-06.md) — 量化方法论（Day 6）
