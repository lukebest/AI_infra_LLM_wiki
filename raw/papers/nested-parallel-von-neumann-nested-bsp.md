---
type: Raw Source
title: "Nested Parallel von Neumann Architecture and Nested BSP"
source_url: https://arxiv.org/abs/2609.16787
arxiv: '2609.16787'
ingested: 2026-09-17
sha256: 2fe5d6c9805510be56ad940474ed4a0be3e4647857a73c396c2cf571537ec42b
---

# Nested Parallel von Neumann Architecture and Nested BSP

**Author:** Heng Liao（Huawei Technologies）
**PDF:** [Nested_Parallel_von_Neumann_Nested_BSP_2026.pdf](Nested_Parallel_von_Neumann_Nested_BSP_2026.pdf)
**arXiv:** [2609.16787](https://arxiv.org/abs/2609.16787)（cs.DC/cs.AR；Wed 2026-09-16 列表）

## 问题

十万到百万处理器规模下，如何仍是「一台计算机」而非松散集群：反对 master/slave 与「多机联网≈更大一台机」的外推。

## 方法要点

- **Nested BSP**：经典 BSP 递归嵌套；每层并行工作→屏障→交换汇聚；硬约束为每层节点 **peer**。
- **Nested Parallel von Neumann Architecture**：从 package→board→rack→SuperNode→data hall→autonomous zone 的硬件嵌套；端到端 **Unified Bus**（memory-semantic、peer equality：physically sparse, logically tight）。
- 与华为 **τ Scaling law** 配对：τ 折叠时间，架构折叠并行层次。
- 文称 Huawei SuperNode 设计以 Nested BSP 为理论根基。

## 摘录数字

论述/架构论文，无独立吞吐/面积基准；定量效果指向既有 τ 芯片与 UB 体系叙述。
