---
type: Concept
title: Instruction-Level Parallelism
description: 指令级并行 ILP：超标量 vs VLIW、真依赖与名称依赖、静态/动态多发射权衡
tags:
- architecture
- cpu
- pipeline
- parallelism
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-09.md
---

# Instruction-Level Parallelism（指令级并行）

**ILP** = 单指令流中可并行执行的指令数。超标量处理器每周期发射多条指令，突破流水线 **CPI = 1** 下限（→ **IPC > 1**）。

## 依赖类型

| 类型 | 别名 | 可否消除 |
|------|------|----------|
| **真依赖 (RAW)** | Read After Write | 不可 — 必须等待 |
| **反依赖 (WAR)** | Anti-dependence | 可 — 寄存器重命名 |
| **输出依赖 (WAW)** | Output dependence | 可 — 寄存器重命名 |

ILP 上限受 **程序依赖图** 与 **硬件资源**（功能单元、寄存器端口、发射宽度）双重约束。

## 静态 vs 动态多发射

| | VLIW/EPIC (静态) | Superscalar (动态) |
|--|------------------|-------------------|
| 调度者 | 编译器 | 硬件 |
| 硬件复杂度 | 低 | 高 |
| 编译器复杂度 | 高 | 低 |
| 代表 | Itanium | Intel Core, Apple M |
| 弱点 | Cache miss、分支不可编译时预测 | 面积/功耗 |

VLIW 未统治通用计算：**动态事件**（Cache miss、分支）使编译期调度信息不完整。

## 动态调度概述

- **保留站 (Reservation Station)** + **ROB** → [Out-of-Order Execution](/concepts/out-of-order-execution.md)
- **分支预测** → [Branch Prediction](/concepts/branch-prediction.md)
- **硬件推测** — 错误路径 flush

## 与 AI 基础设施

| 路径 | ILP 策略 |
|------|----------|
| 通用 CPU | 硬件开采 ILP，功耗高 |
| GPU | 线程级并行 (TLP) 为主，warp 内 SIMT |
| WSE/LPU | 编译器/spatial 调度，**不依赖 OoO ILP** |

## 相关页面

- [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md) — 流水线前提
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — Tomasulo 与重命名
- [Deterministic Execution](/concepts/deterministic-execution.md) — 规避动态 ILP 的范式
- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — 2024-2026 超标量顶会主线
- [Constable Load Elimination](/concepts/constable-load-elimination.md) — load 资源依赖消除

# Citations

[1] [raw/articles/arch-study-30d-day-09.md](raw/articles/arch-study-30d-day-09.md) — H&P Ch.3 ILP 入门（Day 9）
