---
type: Concept
title: CPU Pipeline Fundamentals
description: 五级流水线（IF/ID/EX/MEM/WB）、三大冒险（结构/数据/控制）、Forwarding 与分支惩罚
tags:
- architecture
- cpu
- pipeline
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-08.md
---

# CPU Pipeline Fundamentals（CPU 流水线基础）

流水线通过**指令级重叠**将理想 CPI 从多周期的 ~5 降至 **1**，是现代 GHz 处理器的根基。

## 经典五级流水线

```
指令 k:   | IF | ID | EX | MEM | WB |
指令 k+1:     | IF | ID | EX  | MEM | WB |
```

| 级 | 功能 |
|----|------|
| **IF** | 取指，PC+4 |
| **ID** | 译码、读寄存器、冒险检测 |
| **EX** | ALU、地址计算、分支决策 |
| **MEM** | Load/Store |
| **WB** | 写回寄存器 |

```
实际 CPI = 1 + 结构冒险停顿 + 数据冒险停顿 + 控制冒险停顿
```

理想加速比 ≈ 级数 n；实际 < n（冒险 + 流水线寄存器开销）。

## 三大冒险 (Hazards)

| 类型 | 原因 | 典型对策 |
|------|------|----------|
| **结构** | 硬件资源冲突 | 资源复制、stall |
| **数据 (RAW)** | 真依赖，后续需前序结果 | **Forwarding/bypass**；Load-use 仍须 1 stall |
| **控制** | 分支改变 PC | 分支预测、延迟槽、flush |

### Forwarding

将 EX/MEM 阶段结果前递到 EX 输入，消除多数 RAW stall。例外：`lw` 后立即使用仍须 stall（数据晚到）。

### 控制冒险

分支在 EX 才确定 → 错误路径指令需 flush。**分支惩罚 ≈ 错误预测次数 × (流水线深度 − 1)** → 驱动 [Branch Prediction](/concepts/branch-prediction.md) 投资。

## 与 AI 加速器的对比

- **通用 CPU**：深流水线 + 预测 + OoO 换 IPC
- **[Groq LPU](/concepts/lpu-architecture.md) / [WSE](/entities/cerebras-wse.md)**：编译器静态调度、确定性数据流，**避免分支与动态冒险**
- **[Deterministic Execution](/concepts/deterministic-execution.md)**：用编译器可见时序替代硬件推测

## 相关页面

- [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md) — 突破 CPI=1
- [ISA Design Principles](/concepts/isa-design-principles.md) — 固定长度指令利于译码
- [Branch Prediction](/concepts/branch-prediction.md) — 控制冒险对策

# Citations

[1] [raw/articles/arch-study-30d-day-08.md](raw/articles/arch-study-30d-day-08.md) — RISC-V Ch.4 流水线（Day 8）
