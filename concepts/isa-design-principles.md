---
type: Concept
title: ISA Design Principles
description: 指令集设计原则：Load/Store、RISC-V 编码、CISC vs RISC 历史教训、寄存器与条件码权衡
tags:
- architecture
- cpu
- compiler
- programming-model
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/articles/arch-study-30d-day-03.md
- raw/articles/arch-study-30d-day-04.md
---

# ISA Design Principles（指令集设计原则）

**ISA** 是软硬件唯一契约；**微架构** 是 ISA 的具体硬件实现（可换而不改程序语义）。

## Load/Store 架构

RISC-V / ARM / MIPS 采用 **Register-Register + Load/Store**：

- 运算只操作寄存器；访存仅通过 `lw`/`sw`
- 简化 ALU 与译码；内存地址计算与运算分离

对比 CISC（x86）任意指令可访存 → 译码复杂，现代 x86 内部仍 **μop 翻译为 RISC 风格**执行。

## RISC-V 指令编码

固定 **32 位**，五种格式 R/I/S/B/U/J：

- opcode 总在低 7 位 → 并行译码
- 寄存器字段位置固定 → 流水化解码
- **x0 = 0** 硬连线：清零/移动无需专用指令

## CISC vs RISC 对比

| 维度 | CISC (x86) | RISC (RISC-V/ARM) |
|------|-----------|-------------------|
| 指令长度 | 可变 1–15 B | 固定 4 B（RVC 压缩除外） |
| 寻址模式 | 20+ | Load/Store + 偏移 |
| 寄存器 | 16 (x86-64) | 32 |
| 解码 | 复杂 | 简单并行 |

**历史结论**：RISC 赢性能；CISC 靠生态存活。NPU/加速器领域专用 ISA（如 WSE CSL、TPU 指令）借鉴 **极简 + 编译器可见** 的 RISC 哲学。

## 寄存器数量权衡

- 太少 → spill/reload，增 IC 与内存流量
- 太多 → 编码 bit 增加、上下文切换开销
- **32 个 GPR** 为广泛采用的甜点（x86-64 的 16 个为历史包袱）

## 条件码 vs 条件移动

- **条件码 (flags)**：cmp + 条件分支，简单但引入隐式依赖
- **条件移动 (cmov)**：predicated 写回，减少分支但增寄存器压力

OoO CPU 用 **寄存器重命名 + 分支预测** 掩盖条件码成本；[Deterministic Execution](/concepts/deterministic-execution.md) / 数据流架构则倾向 **显式依赖、无隐式 flags**。

## 相关页面

- [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md) — ISA 如何影响流水线友好性
- [Deterministic Execution](/concepts/deterministic-execution.md) — 专用 SLA vs 通用 RISC
- [LPU Architecture](/concepts/lpu-architecture.md) — 编译器调度替代复杂 ISA

# Citations

[1] [raw/articles/arch-study-30d-day-03.md](raw/articles/arch-study-30d-day-03.md) — RISC-V Ch.2（Day 3）
[2] [raw/articles/arch-study-30d-day-04.md](raw/articles/arch-study-30d-day-04.md) — H&P Appendix A ISA 对比（Day 4）
