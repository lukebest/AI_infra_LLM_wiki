---
type: Summary
title: 'Constable: Safely Eliminating Load Instruction Execution'
description: ISCA 2024 Best Paper：likely-stable load 识别 + RMT/AMT 监控；12.4 KB/core；+5.1% perf、-3.4% 动态功耗、SMT +8.8%；与 EVES LVP 正交至 8.5%
tags:
- architecture
- cpu
- load-elimination
- isca
- power
- ooo
timestamp: '2026-07-03T00:00:00Z'
created: 2026-07-03
sources:
- raw/reports/constable-deepdive.md
---

# Constable: Improving Performance and Power Efficiency by Safely Eliminating Load Instruction Execution

**Authors:** Rahul Bera, Adithya Ranganathan, et al. (ETH Zürich + Intel PARL) | **Venue:** ISCA 2024 **Best Paper** | **arXiv:** [2406.18786](https://arxiv.org/abs/2406.18786) | **Deep-dive:** [raw/reports/constable-deepdive.md](raw/reports/constable-deepdive.md)

## 一句话总结

Constable 用 **SLD + RMT + AMT**（**12.4 KB/core**）识别并监控 **likely-stable load**，在 rename 阶段将 load **转为 register-move 并 bypass 流水**，使 **34.2%** 动态 load 中 **56.4%** global-stable 实例完全不执行——**+5.1%** 性能、**-3.4%** 动态功耗（noSMT），**+8.8%**（2-way SMT），与 LVP **正交**至 **8.5%**。

## 核心贡献

1. **消除 resource dependence**：LVP 仍执行 load；Constable 跳过 RS/AGU/L1-D（Ideal headroom **9.1%** vs LVP **4.3%**）
2. **三表协同**：SLD 识别/存储 last value；RMT 监控 reg 写；AMT 监控 store/snoop
3. **复用现有机制**：register-move elimination、LSQ disambiguation、CV-bit pinning（无全新违例硬件）
4. **Load-Inspector** 工具：分析任意 x86-64 binary 的 stable-load 比例

## 关键数字

| 指标 | 值 |
|------|-----|
| 硬件 | SLD 7.9 KB + RMT 0.4 KB + AMT 4.0 KB = **12.4 KB/core** |
| Perf (noSMT / SMT) | **+5.1%** / **+8.8%** |
| Perf + EVES | **+8.5%** / **+11.3%** |
| Dynamic power | **-3.4%** core（vs EVES **-0.2%**） |
| L1-D / RS reduction | **-26%** / **-8.8%** accesses |
| Global-stable loads | **34.2%** dynamic（max 68.3%） |
| OoO violation rate | **0.09%** eliminated loads |

## 与 wiki 交叉引用

- [Constable Load Elimination](/concepts/constable-load-elimination.md) — SLD/RMT/AMT 机制与 WSE spec
- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — 2023-2026 综述
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — rename/ROB
- [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md) — load 瓶颈
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — LLM memory-bound

# Citations

[1] [raw/reports/constable-deepdive.md](raw/reports/constable-deepdive.md) — 精读笔记（2026-07-03）
[2] Bera et al., ISCA 2024 — [arXiv:2406.18786](https://arxiv.org/abs/2406.18786)
