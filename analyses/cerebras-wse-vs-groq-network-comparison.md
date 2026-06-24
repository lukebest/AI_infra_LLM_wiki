---
type: Analysis
title: Cerebras NoW vs Groq Switched 对比
description: WSE 2D Mesh vs Groq High-radix Switched：拓扑、规模、MoE 场景、矛盾对比
tags:
- architecture
- wse
- cerebras
- groq
- interconnect
- deterministic
timestamp: '2026-04-16T00:00:00Z'
created: 2026-04-16
sources:
- raw/articles/nvidia-groq3-lpx-blog-2026-04.md
---

# Cerebras NoW vs Groq Switched Architecture — 对比分析

> 对比两种确定性执行的 AI 加速器互联架构：WSE 2D Mesh 和 Groq Switched Network。
> Last updated: 2026-04-16

---

## 0. 背景：什么是确定性执行？

两者都追求**确定性执行**——编译器控制计算时序和数据搬运，运行时无硬件调度器介入。

| 维度 | 共同点 |
|------|--------|
| 设计目标 | 可预测的低延迟，无 jitter |
| 路由策略 | 编译时静态确定 |
| 通信模型 | 分布式内存（无共享缓存） |
| 优化目标 | Tail latency 稳定 |

但两者的**互联拓扑**选择了完全不同的路径。

---

## 1. 拓扑对比

### Cerebras WSE — 2D Mesh

```
┌─────────────────────────────────────────┐
│              Wafer                      │
│  ┌──┬──┬──┬──┬──┬──┐                  │
│  ├──┼──┼──┼──┼──┼──┤                  │
│  ├──┼──┼──┼──┼──┼──┤   每个 tile 连接  │
│  ├──┼──┼──┼──┼──┼──┤   4 个邻居        │
│  ├──┼──┼──┼──┼──┼──┤                  │
│  └──┴──┴──┴──┴──┴──┘                  │
│  Tile 直径: O(√N)                       │
│  WSE-3: ~1000+ 跳 (跨 wafer)            │
└─────────────────────────────────────────┘
```

- **拓扑**：2D rectangular mesh
- **每跳延迟**：~0.4 ns（非常快，但累积可观）
- **虚拟通道**：24 color（静态分配，互不阻塞）
- **直径**：O(√N) — 跨 wafer 最长 ~1000 跳
- **路由**：编译时 color assignment，无运行时决策

### Groq LPU — High-Radix Switched Network

```
┌──────────────────────────────────────────┐
│           Groq 3 LPX Rack                │
│                                          │
│   LPU ○──96 links──○ LPU                 │
│    │    (direct)    │                    │
│   ○───────○─────────○     每 LPU: 96 条  │
│    │                 │    112 Gbps 链路   │
│   ○────────○─────────○   直接互联，      │
│    │                 │    无中间跳点      │
│   LPU○──────────────○LPU  (通常 1-2 跳)  │
└──────────────────────────────────────────┘
```

- **拓扑**：High-radix switched network（每 LPU 96 C2C links）
- **每跳延迟**：C2C 直连，无中间跳点
- **协议**：Plesiosynchronous（消除时钟漂移）
- **直径**：常数或 O(1) — 任意 LPU 间 1-2 跳
- **路由**：编译器显式调度，无自适应路由

### 核心拓扑差异

| 维度 | WSE 2D Mesh | Groq Switched |
|------|------------|---------------|
| 拓扑类型 | 规则 mesh，低基数（4-port） | 高基数 switch（96-port） |
| 直径 | O(√N) ~ 1000+ 跳 | O(1) ~ 1-2 跳 |
| 每跳开销 | ~0.4ns × 跳数 | 接近常数（直连） |
| 全局通信 | 多跳累积延迟高 | 直连，几乎无额外延迟 |
| 局部通信 | 天然局部（1-4 跳） | 需要交换才能局部通信 |
| 路由复杂度 | 高（color × 位置分配） | 低（编译器直接调度） |

---

## 2. 规模与集成度

| 维度 | Cerebras WSE-3 | Groq 3 LPX |
|------|----------------|-----------|
| 核心/芯片数 | 900,000 PE（单 wafer） | 256 LPU |
| SRAM 总量 | 44 GB | 128 GB（256 × 500 MB） |
| Fabric 带宽 | 214 Pbit/s | 640 TB/s（scale-up） |
| 物理形态 | 单晶圆（800mm²） | 32U rack |
| 制造 | 单一 wafer=单一芯片 | 256 独立芯片互联 |
| 缺陷容忍 | 必要（defect mapping） | 芯片级独立，单芯片 yield 高 |

**关键洞察**：WSE 的 900K 核心是"小核心高密度"，Groq 的 256 LPU 是"大核心高算力"。WSE 用大规模并行换取简单核心；Groq 用可扩展的 LPU 互联换取算力。

---

## 3. 编程模型

### WSE: CSL (Cerebras Software Layer) — 数据流编程

```
CSL Program → 编译时 → Static dataflow graph
  ↓
运行时：PE 间通过 2D mesh 传递 tokens
  ↓
特点：
- 数据流图在编译时完全展开
- 每个 PE 的角色（source/sink/route）在编译时固定
- 通信模式高度局部化
- 缺陷映射：编译时感知
```

- **调度**：编译时全部分配
- **通信**：点对点通过 mesh，无共享内存
- **并行粒度**：细粒度（PE 级别，900K 并行）

### Groq: Compiler Spatial Scheduling — 编译器空间调度

```
Neural Network → 编译器 → Static instruction schedule
  ↓
每条向量（320 bytes）经过 MXM/VXM/SXM 处理
  ↓
数据在 LPU 间通过 C2C 直接路由
```

- **调度**：编译器生成每条向量的精确路由
- **通信**：显式 C2C transfer，编译器编排
- **并行粒度**：粗粒度（LPU 级别，256 并行）

### 编程复杂度对比

| 维度 | WSE CSL | Groq Compiler |
|------|---------|---------------|
| 编程抽象 | 数据流图 | 神经网络 → 编译器 |
| 用户可见度 | 高（需感知 mesh topology） | 低（编译器自动处理） |
| 调度复杂度 | 极高（900K PE + 24 color） | 高（256 LPU × 96 links） |
| 编译时间 | 可能很长（color routing 求解） | 可控（静态调度） |
| 调试难度 | 高（静态路由难调试） | 中（编译器错误可读） |

---

## 4. 通信模式与开销

### WSE Mesh 的通信开销

```
问题：全局 AllReduce 在 2D mesh 上的开销

Token 从 L1 到 L1000：
  L1 → L2 → L3 → ... → L1000
  每跳 ~0.4ns，总计 ~400ns

中间跳点被占用：
  L500 同时在传 L1→L2 和 L999→L1000 的流量
  → 有效带宽 < 理论带宽
```

- **优势**：局部通信极快（1-4 跳，<2ns）
- **劣势**：全局通信代价高；过境流量浪费带宽

### Groq Switch 的通信开销

```
M2N Token dispatch：
  Attention LPU → [直接 C2C] → Expert LPU
  几乎无跳数，latency ~ O(1)

Ping-pong pipeline 中：
  Attention 计算时，Expert 空闲？
  → 被 micro-batch 的通信 overlap 覆盖
```

- **优势**：全局通信几乎无额外延迟（直连）
- **劣势**：单 LPU 的 96 链路是固定资源，全速通信时链路饱和

### 通信库

| 维度 | WSE | Groq |
|------|-----|------|
| 通信原语 | 24-color static routing | M2N/N2M dispatch |
| 协议 | 晶圆内同步 | Plesiosynchronous C2C |
| 通信库优化 | CS-2（支持 AllReduce） | 自定义 C2C lib |
| 瓶颈 | color routing 冲突 | C2C 链路饱和 |

---

## 5. MoE 场景分析

### WSE 处理 MoE

**优势**：
- 900K 细粒度 PE，每个 expert 可以映射到多个 PE
- 片上 44 GB SRAM，足够存一个 expert 的全部权重（小的 expert）
- 确定性路由保证 expert 切换的稳定延迟

**劣势**：
- MoE 的 token dispatch（top-k expert routing）需要 All-to-All：每个 token 要被路由到对应 expert 所在的 tile
- **跨 wafer 的 All-to-All 在 2D mesh 上是噩梦**：每个 token 可能走 100+ 跳
- Expert 数量增加（如 64 expert）→ dispatch 通信量指数增加

### Groq 处理 MoE

**优势**：
- **与 MegaScale-Infer 的 disaggregation 天生契合**：
  - Attention LPU → M2N dispatch → Expert LPU
  - 1-2 跳直连，dispatch 延迟极低
- Ping-pong pipeline overlap 通信和计算
- M2N 通信库专门优化 token dispatch

**劣势**：
- 每个 Expert LPU 存一个 expert → expert 数量 = LPU 数量限制
- 如果 expert 很大（如 7B 参数），单 LPU 的 500 MB SRAM 不够

### 关键对比：MoE Expert Routing

| 维度 | WSE 2D Mesh | Groq Switched |
|------|------------|---------------|
| Token dispatch 路径 | 多跳 mesh 路由 | 1-2 跳直连 |
| 路由开销 | O(√N) hop × 跳数 | O(1) hop |
| Expert 内存限制 | SRAM 小，expert 必须小 | SRAM 大（500MB），expert 可较大 |
| 扩展 expert 数 | 天然支持（PE 多） | 受 LPU 数限制 |
| 通信库支持 | CS-2 AllReduce | M2N 专用库 |

---

## 6. 矛盾分析法视角

用矛盾分析法看两者：

### 共同主要矛盾

> **确定性 vs 灵活性** — 这是两者的共同主要矛盾

两种架构都选择了**确定性**（编译器静态调度），代价是：
- WSE：color routing 复杂度随核心数指数增长
- Groq：编译器需要精确建模 256 LPU + 96 links 的所有时序

### 差异化矛盾

| 矛盾 | WSE | Groq |
|------|-----|------|
| 拓扑均匀性 vs 通信异构 | **主要矛盾**（mesh vs All-to-All） | 次要矛盾（switched 直连缓解） |
| 编译器复杂性 vs 可扩展性 | 激化（WSE-3 已严重） | 中等（256 LPU 可控） |
| 细粒度并行 vs 同步开销 | 激化（900K PE 同步极复杂） | 缓解（粗粒度 LPU） |
| 内存容量 vs 模型规模 | 激化（44GB 太小） | 缓解（128GB 更大） |

### 矛盾转化预判

**WSE 的矛盾转化**：
- 如果 MoE 成为主流，WSE 的 mesh All-to-All 会成为瓶颈
- Color routing 的组合爆炸会在 WSE-4（更大 wafer）时失控
- **可能的转化方向**：引入层次化 mesh 或光互联

**Groq 的矛盾转化**：
- 确定性执行在 agentic AI 动态场景下会受限
- 256 LPU 的规模在万亿参数模型时可能不够
- **可能的转化方向**：扩展 LPU 数 + 异构（Vera Rubin + LPX）

---

## 7. 总结对比表

| 维度 | Cerebras WSE | Groq 3 LPX |
|------|-------------|------------|
| **拓扑** | 2D Mesh（低基数 4-port） | High-radix Switch（96-port） |
| **直径** | O(√N) ~ 1000+ 跳 | O(1) ~ 1-2 跳 |
| **核心数** | 900K 简单 PE | 256 复杂 LPU |
| **片上 SRAM** | 44 GB | 128 GB（256 × 500 MB） |
| **确定性机制** | 24-color 静态路由 | Plesiosynchronous C2C |
| **编程模型** | CSL 数据流 | 编译器静态调度 |
| **编译器复杂度** | 极高（color × 900K） | 高（96 links × 256） |
| **MoE dispatch** | 多跳 All-to-All，代价高 | M2N 直连，代价低 |
| **适用场景** | 极大 dense 模型，训练 | MoE 推理，agentic AI |
| **规模扩展** | 受 wafer 尺寸限制 | 可扩展 LPU 数 |
| **缺陷容忍** | 必须（defect mapping） | 芯片级独立，更易 |
| **主要优势** | 超大规模并行，局部通信快 | 直连低延迟，MoE 友好 |
| **主要劣势** | 全局通信代价高，编译复杂 | 规模受 LPU 数限制 |

---

## 8. 核心洞察

1. **拓扑选择是根本**：2D mesh 天然适合局部通信，高-radix switch 天然适合全局通信。MoE 的 expert routing 是全局 All-to-All → **switched topology 天然优于 mesh**。

2. **确定性执行的边界**：两者的确定性在训练和大 batch 推理时是优势；在 agentic AI（动态 batching、speculative decoding）时，灵活性可能更重要。

3. **规模 vs 复杂度的权衡**：WSE 选择了"单系统最大化"（整个 wafer 是一个芯片），代价是编译器复杂度和缺陷容忍挑战。Groq 选择了"可组合扩展"（256 LPU 可互联成更大系统），代价是芯片间通信的开销。

4. **融合趋势**：未来的 AI 加速器可能同时需要两者——WSE 风格的超大规模并行 + Groq 风格的高带宽直连互联。

---

## 相关页面
- [Cerebras Wse](/entities/cerebras-wse.md) — WSE 实体
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — Groq LPX 实体
- [Wse Nom Contradiction Analysis](/analyses/wse-nom-contradiction-analysis.md) — WSE NoW 矛盾分析（更深入）
- [Deterministic Execution](/concepts/deterministic-execution.md) — 确定性执行概念
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构推理（与 MegaScale-Infer 的关联）
- [Megascale Infer 2504.02263](/papers/megascale-infer-2504.02263.md) — MegaScale-Infer（Groq 天然适合此场景）

# Citations

[1] [raw/articles/nvidia-groq3-lpx-blog-2026-04.md](raw/articles/nvidia-groq3-lpx-blog-2026-04.md)
