---
type: Concept
title: Constable Load Elimination
description: ISCA 2024 Best Paper：SLD/RMT/AMT 识别 likely-stable load 并跳过执行；12.4 KB/core、+5.1% perf、-3.4% 动态功耗、SMT +8.8%；与 LVP 正交
tags:
- architecture
- cpu
- load-elimination
- ooo
- power
- llm
- isca
timestamp: '2026-07-03T00:00:00Z'
created: 2026-07-03
sources:
- raw/reports/constable-deepdive.md
---

# Constable Load Elimination

**Constable**（Bera et al., ISCA 2024 **Best Paper**）通过 **likely-stable load 识别 + source register / memory 监控**，在 load 依赖未变时**完全不执行 load**（不占 RS、AGU、L1-D 端口），而非 [Out-of-Order Execution](/concepts/out-of-order-execution.md) 中 LVP 式「仍执行再验证」。

**Authors:** Rahul Bera, Adithya Ranganathan, et al. (ETH + Intel PARL) | **arXiv:** [2406.18786](https://arxiv.org/abs/2406.18786) | **Tool:** [Load-Inspector](https://github.com/CMU-SAFARI/Load-Inspector)

**Source:** [raw/reports/constable-deepdive.md](raw/reports/constable-deepdive.md)（精读笔记）

## 核心条件

两次同一静态 load 动态实例取相同值 **iff**：

```
Condition 1: I₁→I₂ 间无 source register 写  → 地址不变
Condition 2: I₁→I₂ 间无 store/snoop 访问该地址 → 值不变
```

**34.2%** 动态 load 为 **global-stable**（整 workload 同址同值）；编译器 -O3 仍无法消除。

## 四步机制

| 步 | 动作 | 硬件 |
|----|------|------|
| **Identify** | 非消除 load 完成时比较 (last_addr, last_val)；match → confidence++，else /=2；≥30 → likely-stable | **SLD** |
| **Arm** | likely-stable 在 writeback：RMT 插 source reg、AMT 插 phys addr、SLD 设 can_eliminate=1 | RMT + AMT |
| **Eliminate** | rename 阶段转为 3-operand register-move，源=xPRF last value，bypass 后续流水 | SLD + xPRF |
| **Invalidate** | reg 写 / store / snoop / context switch → reset can_eliminate | RMT + AMT |

## 硬件表（Golden Cove 6-wide baseline）

| 结构 | 大小 | 要点 |
|------|------|------|
| **SLD** | **7.9 KB** | 32×16 ways；tag+addr+val+conf+can_eliminate；**3R/2W** |
| **RMT** | **0.4 KB** | 监控 architectural reg 写；**2R/6W** |
| **AMT** | **4.0 KB** | 32×8 ways；监控 store/snoop；**1R/1W** |
| **xPRF** | 32 entries | last-fetched value（论文不计入 Constable 面积） |
| **合计** | **12.4 KB/core** | |

端口数由 workload 分布反推（rename group 平均 **1.93 loads**；98.3% ≤2）。

## vs LVP (EVES)

| | LVP | Constable |
|---|-----|-----------|
| 消除 | 数据依赖（仍执行 load 验证） | 数据 + **资源**依赖 |
| Ideal headroom | **4.3%** | **9.1%** |
| 实测 | 4.7% | **5.1%**（noSMT） |
| 动态功耗 | -0.2% | **-3.4%** |
| 组合 | — | **8.5%**（正交） |

**Headroom 洞察**：4.3%→9.1% 的 **4.8%** 差距 = resource dependence 的真实代价；Constable 实现 **56%** of ideal。

## 实验结果（摘要）

| 指标 | 值 |
|------|-----|
| 性能 (noSMT) | **+5.1%** avg，**+31.2%** max |
| 性能 (2-way SMT) | **+8.8%**（RS/L1-D 端口更稀缺） |
| 动态功耗 | **-3.4%** core；L1-D **-9.1%**；RS **-5.1%** |
| L1-D 访问减少 | **-26%** avg |
| RS 分配减少 | **-8.8%** avg |
| Load 消除覆盖 | **23.5%**（Constable）；**56.4%** of global-stable |
| OoO 违例 | **0.09%** eliminated loads（复用现有 LSQ disambiguation） |
| Multi-core | **CV-bit pinning** in coherence directory |

**Workload 分解**：stack-relative 贡献 **2.6%** perf（50% of benefit）→ 控制流主导代码收益最大。

## OoO 与一致性

- **OoO store-load 违例**：store 地址生成后 AMT reset；年轻 eliminated load 由既有 memory disambiguation flush（**0.09%**）
- **Multi-core stale**：eliminated load 时 **pin CV-bit**；远端写 → snoop → AMT reset
- **Wrong path**：不恢复 SLD（0.2% 影响）

## WSE / LLM 复用

| 场景 | 预期 |
|------|------|
| **WSE 控制核 (4-wide)** | 表缩至 ~**6 KB**；2R/2W SLD、2R/4W RMT |
| **LLM KV cache** | 高 stability → likely-stable 可能 **>50%** |
| **NPU weight tile** | 不依赖 OoO；SLD 思路可移植 |
| **LR/SC Gap** | Constable **不直接适用** → [Memory Consistency Model](/concepts/memory-consistency-model.md) |

**WSE-aware 扩展**：跳过远程 mesh 访问而非本地 load → 见 [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md)。

## 局限

- **43.6%** global-stable 未消除：source reg 写 (23.3%)、silent store (14.1%)、表满/phase (6.2%)
- **30/90 workload**：EVES > Constable（random/crypto 数据）
- xPRF、CV-bit pinning 工业部署需额外验证

## 相关页面

- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — 综述上下文
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — rename/ROB/LSQ
- [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md) — load 双重瓶颈
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — memory-bound decode
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — CV-bit / snoop
- [papers/constable-load-elimination.md](/papers/constable-load-elimination.md) — 论文摘要页

# Citations

[1] [raw/reports/constable-deepdive.md](raw/reports/constable-deepdive.md) — Constable 精读（2026-07-03）
[2] Bera et al., ISCA 2024 — [arXiv:2406.18786](https://arxiv.org/abs/2406.18786)
