---
type: Concept
title: Superscalar CPU Research (2023-2026)
description: 2023-2026 超标量 CPU 顶会综述：异构旁路子系统（Constable/Bullseye/Prophet）、CVA6S+ 开源 baseline、OoO 边际饱和与 LLM memory-bound 优化；WSE/NPU 关联矩阵与核内同步 Gap
tags:
- architecture
- cpu
- superscalar
- branch-prediction
- load-elimination
- risc-v
- llm
- wse
timestamp: '2026-07-03T00:00:00Z'
created: 2026-07-03
sources:
- raw/reports/superscalar-cpu-final-report.md
- raw/reports/superscalar-cpu-report.md
- raw/reports/constable-deepdive.md
---

# Superscalar CPU Research (2023-2026)

**2023-2026 超标量 CPU 研究主线**：用**异构旁路子系统** + **软硬件协同**消除/跳过无效访问，而非传统「堆容量、挖 ILP」。LLM 推理的 memory-bound 特性把 load 消除、时序预取、前端 H2P 推到顶会中心。

**Source:** [raw/reports/superscalar-cpu-final-report.md](raw/reports/superscalar-cpu-final-report.md)（OpenClaw Scout→Analyst→Writer→Critic，综合评分 8.2-8.4/10）

## 一句话总结

Constable（ISCA'24 Best Paper）+ Bullseye + Prophet 代表「旁路主表」范式；**CVA6S+** 是可 fork 的 RISC-V 工业超标量 baseline；继续扩大 [Out-of-Order Execution](/concepts/out-of-order-execution.md) ROB/issue queue 收益已微——**前端 + 内存子系统**才是真瓶颈。

## 四大挑战

| 挑战 | 代表性缓解 | Wiki 关联 |
|------|-----------|----------|
| **内存墙** | Constable load 消除、Prophet 时序预取 | [DRAM and Memory System](/concepts/dram-memory-system.md)、[Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) |
| **前端墙** | Bullseye HIT + 双感知器旁路 TAGE | [Branch Prediction](/concepts/branch-prediction.md) |
| **能耗墙** | Constable -3.4% 动态功耗（少执行） | [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) |
| **安全墙** | Apple M1 RE、Spectre mistraining | — |

## Top 论文（arXiv 校正后）

| 论文 | 会议 | 核心数字 | arXiv/DOI |
|------|------|---------|-----------|
| **Constable** | ISCA 2024 **Best Paper** | +5.1% perf / -3.4% 动态功耗 / SMT +8.8% | [2406.18786](https://arxiv.org/abs/2406.18786) |
| **CVA6S+** | arXiv 2025 | +43.5% IPC vs 标量 CVA6；+10.9% vs CVA6S；+9.30% 面积 | [2505.03762](https://arxiv.org/abs/2505.03762) |
| **Bullseye** | CBP-2025 | 187 KB 总预算；MPKI **3.4045** | [2506.06773](https://arxiv.org/abs/2506.06773) |
| **Prophet** | ISCA 2025 | +14.23% vs Triangel | [2506.15985](https://arxiv.org/abs/2506.15985) |
| **AVM-BTB** ⚠️ | ISCA 2024 | [未深分析 — 全文不可达] | DOI [推测] 10.1145/3695053.3730996 |
| Apple M1 RE | arXiv 2025-02 | RE 类；非主线 | [2502.10719](https://arxiv.org/abs/2502.10719) |

### Bullseye（H2P 旁路 TAGE）

159 KB TAGE-SC-L + **28 KB H2P 子系统**（HIT 表 + 双感知器）；H2P PC 停止污染 TAGE 更新。直接扩展 [Branch Prediction](/concepts/branch-prediction.md) 中 TAGE 工业基线。

### Constable（load 消除）— 精读

动态识别 **likely-stable load**；详见 [Constable Load Elimination](/concepts/constable-load-elimination.md)（[精读笔记](raw/reports/constable-deepdive.md)：SLD/RMT/AMT **12.4 KB**、+5.1% / -3.4% 功耗、Ideal headroom 9.1%）。

### CVA6S+（开源工业核）

改进 BP + 寄存器重命名 + 操作数转发 + **HPDCache**（+74.1% L1 带宽）。与 [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md) / [Out-of-Order Execution](/concepts/out-of-order-execution.md) 教科书结构对应，且 RTL 可 fork（OpenHW `cva6s`）。

## 五条跨论文 Insight

| # | 性质 | 要点 |
|---|------|------|
| 1 | 🔀 组合 | 旁路子系统解决主表退化（Constable/Bullseye/Prophet 同范式） |
| 2 | 🔁 复用 | CVA6S+（开源 RTL）+ Apple M1 RE（工业参数校准）双轨 |
| 3 | 🔀 组合 | 内存 + 前端瓶颈；OoO 深度边际饱和（Zen 5：6-wide + 大 prefetch） |
| 4 | 💡 提案 | LLM memory-bound 复兴 → WSE 上 LLM 推理核专用 ISA |
| 5 | 💡 提案 | 微架构透明度作差异化（vs [Cerebras WSE](/entities/cerebras-wse.md) 黑盒路线） |

## WSE / LLM 关联

| 方向 | 关键复用 |
|------|---------|
| **WSE 控制核** | Constable likely-stable；Bullseye 28 KB H2P；**WSE-aware Constabulary**（跳过远程 mesh 访问） |
| **LLM 推理** | Constable → KV cache 规律访问；Prophet profile-guided → KV 预取 |
| **NPU** | HPDCache 数据供给；Prophet hints → weight reuse |
| **核内同步** | ⚠️ **Gap**：6 篇均无 LR/SC/AMO 优化；Constable 思路**未必适用**（coherence 失败模式 ≠ load）→ 见 [Memory Consistency Model](/concepts/memory-consistency-model.md) |

与 [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) 对照：WSE PE **无**传统 BP/OoO——本综述主要指导**片上控制核**或 **host 侧**超标量设计，而非 WSE 数据流 PE 本身。

## 设计启示（spec 级）

保守 OoO（例：**4-wide**，ROB ≤ 256）+ **激进前端**（大 BTB/BP + Prophet-style 预取）+ **高带宽 L1**（HPDCache 思路）——当前文献 + 工业（Zen 5）组合的性价比最高点。

## 研究 Gap

1. **核内同步**：无直接顶会论文；Constable 迁移有 4 点负面论证
2. **WSE 多核共享前端**：现有论文假设单芯片有限核数
3. **AVM-BTB**：多租户 BTB 对 WSE mesh BPU 共享——数字 [待验证]
4. **AI 训练侧**微架构瓶颈：文献偏 inference / 传统 workload

## 优先行动

1. 精读 Constable Section 5+7（2-3 h）→ 微架构 checklist — 见 [Constable Load Elimination](/concepts/constable-load-elimination.md)
2. `git clone openhwgroup/cva6s` + HPDCache + gem5 baseline（1-2 周）
3. 获取 ISCA 2024 AVM-BTB proceedings
4. gem5 profile LR/SC 失败模式 → 核内同步 proposal

## 相关页面

- [Branch Prediction](/concepts/branch-prediction.md) — TAGE/BTB、Bullseye H2P
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — ROB/重命名；深度边际饱和
- [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md) — Superscalar vs VLIW
- [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md) — 分支惩罚与流水线
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — LLM memory-bound
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — LR/SC Gap 上下文
- [Cerebras WSE](/entities/cerebras-wse.md) — 对比：无 BP/OoO vs 控制核需求
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — SLA vs Golden Cove
- [summaries/superscalar-cpu-research-2023-2026.md](/summaries/superscalar-cpu-research-2023-2026.md) — 报告 digest
- [Constable Load Elimination](/concepts/constable-load-elimination.md) — ISCA'24 Best Paper 精读

# Citations

[1] [raw/reports/superscalar-cpu-final-report.md](raw/reports/superscalar-cpu-final-report.md) — 最终汇总（2026-07-03）
[2] [raw/reports/superscalar-cpu-report.md](raw/reports/superscalar-cpu-report.md) — 结构化综述 v2（~2400 字）
[3] [raw/reports/constable-deepdive.md](raw/reports/constable-deepdive.md) — Constable 精读
