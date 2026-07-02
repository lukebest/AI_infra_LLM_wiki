---
type: Summary
title: 'A Preliminary Architecture for a Basic Data-Flow Processor'
description: Dennis & Misunas (ISCA 1975) 基本数据流处理器：decider/T-gate/merge 条件迭代、Decision Units、Instruction Cell 两级存储作活跃指令 cache
tags:
- architecture
- dataflow
- parallelism
- history
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf
---

# A Preliminary Architecture for a Basic Data-Flow Processor

**Authors:** Jack B. Dennis, David P. Misunas (MIT Project MAC) | **Venue:** 2nd Annual Symposium on Computer Architecture (ISCA), 1975 | **ACM:** [641675.642111](https://dl.acm.org/doi/10.1145/641675.642111) | **PDF:** [raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf](raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf)

## 一句话总结

在 **elementary data-flow processor**（Karp–Miller 模型、Instruction Cell + 仲裁/分发网络）上扩展 **条件与迭代**（decider、T/F-gate、merge、Decision Units），并用 **Instruction Memory + Cell Block（Association Table + Stack LRU）** 使 Instruction Cell 仅缓存活跃指令——避开 Von Neumann 并行机的切换与互连瓶颈。

## 核心贡献

1. **Basic data-flow 语言**：control token + gate/merge actor；迭代/分支数据流图（Figure 8 while 例）
2. **Basic processor**：Operation Units + **Decision Units** + Control Network；gating code 内嵌 gate 语义
3. **两级存储**：major/minor 地址 → Cell Block；retrieve/store 与 **preempt**（Stack 置换 occupied Cell）
4. **Packet 通信**：固定大小 operation/data/control packet；段间可容忍延迟
5. **路线图**：通向 Fortran 级 generalized data-flow（数组、过程、向量并行待扩展）

## 关键机制

| 机制 | 要点 |
|------|------|
| Fire 规则 | 所有输入 token 就绪且**输出弧空** |
| Merge | 多目的地写同一寄存器，非独立指令 |
| Cell 状态 | free → engaged（packet 先到）→ occupied（指令载入） |
| 置换 | Stack 选 occupied Cell → store 到 Instruction Memory → retrieve 新指令 |

## 与 wiki 交叉引用

- [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md) — 架构与 Cell Block 算法
- [Deterministic Execution](/concepts/deterministic-execution.md) — 数据驱动/编译时图执行谱系
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 非 Von Neumann 控制
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — 现代空间数据流
- [Cerebras WSE](/entities/cerebras-wse.md) — 当代数据流加速器

# Citations

[1] [raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf](raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf) — Dennis & Misunas (1975)
