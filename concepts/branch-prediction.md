---
type: Concept
title: Branch Prediction
description: 分支预测：1-bit/2-bit 饱和计数器、局部与全局历史、TAGE/BTB、分支惩罚对 CPI 的量化影响
tags:
- architecture
- cpu
- pipeline
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-11.md
- raw/reports/superscalar-cpu-report.md
---

# Branch Prediction（分支预测）

超标量需 **前瞻发射**；分支在 EX 才确定方向 → 不预测则每分支 stall 10–20+ 周期。**分支预测** 是让 IPC > 1 的关键组件。

## 分支惩罚量化

```
CPI ≈ 理想 CPI + 分支占比 × (1 - 准确率) × 惩罚
惩罚 ≈ 流水线深度（× 发射宽度，最坏情况）
```

示例：分支占 20%、15 级流水线、准确率 95%  
→ CPI ≈ 1 + 0.2 × 0.05 × 15 = **1.15**

准确率每降 1%，高发射宽度下可损失数个百分点性能 → Intel/AMD 在预测器上投入大量面积。

## 预测器演进

| 世代 | 机制 | 弱点 |
|------|------|------|
| **1-bit** | 上次方向 | 循环入口/出口各错一次 |
| **2-bit 饱和** | 需两次错向才翻转 | 改善循环 |
| **局部历史 (BHT)** | 每分支独立历史 | 别名冲突 |
| **全局历史 (GShare)** | 全局分支模式 | 长历史需求 |
| **混合/TAGE** | 多预测器 + 选择器 | 现代 CPU 标配 |
| **BTB** | 缓存分支**目标地址** | 与方向预测配合 |

## 与推测执行

错误预测 → flush 流水线 + 重新取指 → 与 [Out-of-Order Execution](/concepts/out-of-order-execution.md) ROB 推测路径联动。

## AI 加速器视角

- **GPU**：warp 内分支 divergence（SIMT mask）——详见 [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md)
- **WSE/LPU**：编译器/spatial 调度 **减少或消除运行时分支** → 无需大型 BTB/TAGE
- **Deterministic 路径**：见 [Deterministic Execution](/concepts/deterministic-execution.md)

## 相关页面

- [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md) — 控制冒险来源
- [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md) — 推测与 ILP
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — 硬件推测 flush
- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — Bullseye H2P 旁路 TAGE（CBP-2025）
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — CPU 分支预测 vs Warp divergence

# Citations

[1] [raw/articles/arch-study-30d-day-11.md](raw/articles/arch-study-30d-day-11.md) — H&P Ch.3 分支预测（Day 11）
