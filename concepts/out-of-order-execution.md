---
type: Concept
title: Out-of-Order Execution
description: 乱序执行：Tomasulo 算法、保留站、ROB 顺序提交、寄存器重命名与指令窗口 IPC 收益递减
tags:
- architecture
- cpu
- pipeline
- scheduling
timestamp: '2026-10-19T00:00:00Z'
created: 2026-06-24
updated: 2026-10-28
sources:
- raw/articles/arch-study-30d-day-10.md
- raw/articles/arch-study-30d-day-12.md
- raw/articles/arch-study-30d-day-19.md
- raw/reports/superscalar-cpu-report.md
- raw/reports/constable-deepdive.md
---

# Out-of-Order Execution（乱序执行）

**动机**：就绪指令不必等待前序慢指令（如长延迟 MUL）。通过 **乱序执行、顺序提交** 在保持精确异常语义下开采 ILP。

## Tomasulo 算法（1967–至今）

三大组件：

```
保留站 (RS)  ← 等待操作数，监听 CDB 广播
寄存器重命名  ← Qi 字段指向 RS 或已就绪
CDB (Common Data Bus) ← 结果广播到所有 RS
```

流程：**Issue → Execute → Write Result**；提交仍经 **ROB (Reorder Buffer)** 按程序序。

## 寄存器重命名

消除 WAR/WAW **名称依赖**：物理寄存器池 >> 架构寄存器；每条写分配新物理寄存器。现代 CPU（Intel/AMD/Apple）核心机制。

## 指令窗口与 IPC 递减

```
指令窗口 ≈ ROB + Issue Queue
```

Palacharla et al. (1997) 量化结论：**窗口 64–128 后 IPC 收益急剧递减**。

| 窗口增大 | 代价 |
|----------|------|
| IPC ↑ | Wakeup/Select 延迟 ↑、面积/功耗 ↑ |

**Wakeup 延迟**：完成指令唤醒等待者的时间  
**Select 延迟**：从就绪队列选出可发射指令的时间

→ 窗口不能无限大；这是 **暗硅/功耗墙** 在 OoO 上的体现。

## 硬件推测

OoO + [Branch Prediction](/concepts/branch-prediction.md)：在分支结果前发射后续指令；错误则 flush ROB 中推测路径。

## Memory Fence

Fence 进入 ROB 后设 **Barrier bit**，排空 Store Buffer 并 stall 后续 store，直到屏障前指令 retire。多核路径经 coherence/NoC 排空 Invalidate Queue——详见 [Memory Fence and Barrier](/concepts/memory-fence-barrier.md)、[Memory Consistency Model](/concepts/memory-consistency-model.md)（TSO Store→Load 重排）。

## 与 AI 加速器

OoO 是 **通用 CPU 高 IPC 的灵魂**，也是 **功耗与面积的主要来源**。[Cerebras WSE](/entities/cerebras-wse.md)、[Groq LPU](/concepts/lpu-architecture.md) 选择 **无 OoO、编译器确定性调度**——用可预测性换能效与规模（见 [Deterministic Execution](/concepts/deterministic-execution.md)）。

## 相关页面

- [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md) — ILP 与依赖
- [Branch Prediction](/concepts/branch-prediction.md) — 控制推测
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — Store Buffer 与 TSO
- [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) — ROB/SBUF 排空与 coherence
- [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — 暗硅与功耗墙
- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — ROB/issue queue 边际饱和；Constable 跳过 load
- [Constable Load Elimination](/concepts/constable-load-elimination.md) — likely-stable load 消除（ISCA'24 Best）

## 2026-10-13 补充：乱序核里接入软件管理存储

[CacheFlex](/papers/cacheflex-l2-scratchpad-scalable-vector.md) 给 Cortex-A710 风格核（128 ROB、32 LQ/48 SQ）加一套 SPM LSQ：常规内存↔SPM 的桥接指令同时进两套 LSQ，各域独立保证 RAW/WAW，WAR 交给 ROB 顺序提交；桥接指令像缓冲 store 一样提交即释放 ROB 项。说明向量宽度上去后，访存瓶颈也可以通过 ISA + LSQ 协同，而不只靠加深 ROB/LSQ 掩盖延迟。另见 [Memory Hierarchy & Cache](/concepts/memory-hierarchy-cache.md)。

## 2026-10-19 补充：ROB 不再是瓶颈的情形

[CTMA](/papers/causal-top-down-microarchitecture-analysis.md)：cactuBSSN_r 在扭曲数据拓扑下短循环密集、误预测频繁，压缩 ROB 份额几乎无损（~9–10%），瓶颈转到前端填充率；规则拓扑时同一操作损失 ~23%（Intel）。见 [Branch Prediction](/concepts/branch-prediction.md)。

## 2026-10-28 补充：搜 OoO 参数也要 Pareto 反馈

[PaFeDSE](/papers/pafedse-pareto-feedback-microarch-dse.md) 把微架构 DSE 里的「选点」做成 hit/miss 闭环：代理不只估 CPI/功耗/面积，还估会不会抬超体积；对反复 miss 的局部用图记忆惩罚。SPEC CPU 2017 上相对 MoDSE 最高少 **49.0%** 仿真达目标 HV。


# Citations

[1] [raw/articles/arch-study-30d-day-10.md](raw/articles/arch-study-30d-day-10.md) — Tomasulo 算法（Day 10）
[2] [raw/articles/arch-study-30d-day-12.md](raw/articles/arch-study-30d-day-12.md) — 指令窗口量化（Day 12）
[3] [raw/articles/arch-study-30d-day-19.md](raw/articles/arch-study-30d-day-19.md) — Store Buffer / TSO（Day 19）
[CacheFlex] [arXiv:2610.12940](https://arxiv.org/abs/2610.12940)
[CTMA] [arXiv:2610.21387](https://arxiv.org/abs/2610.21387)
[PaFeDSE] [arXiv:2610.34838](https://arxiv.org/abs/2610.34838)
