---
type: Concept
title: Basic Data-Flow Processor
description: Dennis & Misunas (1975) 基本数据流处理器：token/actor 图、Instruction Cell + 仲裁/分发网络、decider/T-gate/merge 条件与迭代、Cell Block 两级存储作活跃指令 cache
tags:
- architecture
- dataflow
- parallelism
- history
- deterministic
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf
---

# Basic Data-Flow Processor（基本数据流处理器）

Jack B. Dennis 与 David P. Misunas（MIT Project MAC, 1975）在 **elementary data-flow processor** 之上提出 **basic data-flow processor**：执行带 **条件与迭代** 的数据流程序（Dennis & Fosseen 模型），并引入 **Instruction Cell 作活跃指令 cache** 的两级存储——避免 Von Neumann 式 **processor switching** 与 **processor/memory 互连** 瓶颈。这是现代 [Deterministic Execution](/concepts/deterministic-execution.md) / 空间数据流（[SpaDA](/concepts/spada-programming-language.md)、[Cerebras WSE](/entities/cerebras-wse.md)）的重要历史源头。

## 数据流执行模型

**数据驱动（data-driven）**：每条指令/actor 在**所有操作数 token 就绪**时 enable，无需独立控制信号。

| 元素 | 语义 |
|------|------|
| **Operator** | 消费输入 token → 计算 → 输出 token |
| **Link** | 复制 token 到多个目的地 |
| **约束** | operator/link **仅当所有输出弧无 token 时** 才可 fire（避免重复发射） |

与 Von Neumann（PC + 顺序控制）对比：并行度由程序图结构自然暴露，而非 [Out-of-Order Execution](/concepts/out-of-order-execution.md) 动态发现。

## Elementary Processor（前代）

Karp–Miller 初等数据流语言：有向图，节点为 operator 或 link，arc 上传 token。

```
Memory (Instruction Cells) ──operation packet──→ Arbitration Network ──→ Operation Units
Operation Units ──data packet──→ Distribution Network ──→ Memory operand registers
```

| 组件 | 功能 |
|------|------|
| **Instruction Cell** | 3 寄存器：instruction + 2 operands；齐备则 enable |
| **Arbitration Network** | 多 Cell 竞争 → round-robin 仲裁 → Switch 按 opcode 选 Operation Unit |
| **Distribution Network** | 按目的地址把 result data packet 路由回 Memory |
| **Operation Units** | 流水线 ALU；destination 地址随结果走 identity pipeline |

固定大小 packet 通信；各段可容忍传输延迟而不降低硬件利用率——**speed-independent 异步模块** 设计（[6][7]）。

## Basic 语言扩展

在 elementary 的 data link + operator 上增加 **control link** 与 **control token**（true/false）：

| Actor | 功能 |
|-------|------|
| **Decider** | 谓词 → 产生 control token |
| **Boolean operator** | 组合多个 control token |
| **T-gate / F-gate** | control 为 true/false 时通过/吸收 data token |
| **Merge** | 按 control 从 true/false 输入选一路输出 |

**Gate/Merge 不单独占 Instruction Cell**：gate 语义编入 operator/decider 的 **gating code**；merge 由 **Distribution Network 多目的地写同一寄存器**「免费」实现。

### 迭代示例（while y < x）

Figure 8：decider 测 `y < x`；true 时 T-gate 把 x、新 y、n+1 经 merge 回环；false 时 F-gate 输出最终 y、n 并恢复初态。

## Basic Processor 组织

在 elementary 上增加 **Decision Units** + **Control Network**（control packet 路由）。

**Instruction Cell 格式**（6 类）：operator / decider / Boolean / control distribution / data forwarding 等；每 operand register 含 **gating code**（none / true / false / cons）与 data/control **receiver**（value flag + gate flag）。

**Control packet 形式**：
- `{gate, true|false, <addr>}` — 在目的寄存器做 gating
- `{value, true|false, <addr>}` — 提供 Boolean 操作数

## 两级存储：Instruction Cell 作 Cache

Basic 程序节点 **fire 频率不均**（分支/迭代使子图活跃或静默）→ 不宜每指令永久占 Cell。

| 层级 | 角色 |
|------|------|
| **Instruction Cells（Cell Block）** | 活跃指令的工作集 cache |
| **Instruction Memory（辅存）** | 每地址 3 字一组存完整 Cell 内容 |

**地址划分**：major address → **Cell Block**（Distribution/Control 网络按 major 选块）；minor address → 块内 Cell。

**Cell Block 内**：
- **Association Table**：`{minor_addr, status}` — free / engaged / occupied
- **Stack**：occupied Cell 的 **LRU 置换候选序**

**Procedure 1**（data/control packet 到达）：
1. 查 Association Table；无 entry 则分配 free Cell，或 **Stack 顶 occupied Cell 被 preempt**（store 回 Instruction Memory）
2. 发 `{n, retrieve}` 取指令（若 engaged）
3. 更新 operand register（Fig. 12 状态机）
4. 三 register 均 enable → 发 operation/decision packet，Cell 复位 operand，Stack 将该 Cell 移为 **最后置换候选**

**Procedure 2**（instruction packet 从 Memory 返回）：engaged → occupied，若已 enable 则立即发射。

论文愿景：Instruction Memory 可 **并发** 处理大量 store/retrieve（类似当代 I/O 子系统）。

## 与当代 wiki 主题

| 主题 | 1975 basic DF | 现代实例 |
|------|---------------|----------|
| 控制 vs 数据 | 显式 control token + gate | 编译时静态 [Color](/concepts/cerebras-color-mechanism.md) / async task |
| 并行发现 | 图结构静态暴露 | WSE 数据流 wavelet；非 OoO 动态 ILP |
| 存储层次 | Cell = 活跃指令 cache | PE 48KB SRAM + 编译 placement |
| 互连 | Arbitration + Distribution 网络 | [Mesh NoC](/concepts/mesh-torus-topology.md)、[Collective-Capable NoC](/concepts/collective-capable-noc.md) |

未实现部分（论文 Conclusion）：数组、过程并发激活、向量并行——通向 Fortran 级 generalized data-flow（Dennis [4]）。

## 相关页面

- [Deterministic Execution](/concepts/deterministic-execution.md) — 编译时确定的数据流/空间执行
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 无 Von Neumann 隐式控制
- [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md) — Von Neumann 顺序控制对比
- [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md) — 动态 ILP vs 静态数据流并行
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — 现代空间数据流语言
- [Cerebras WSE](/entities/cerebras-wse.md) — 晶圆级数据流加速器

# Citations

[1] [raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf](raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf) — Dennis & Misunas, ISCA 1975 (ACM 641675.642111)
