---
type: Raw Source
title: 📰 互连网络晨报 — Day 18
source_path: /home/luke/openclawdata/workspace-research/notes/projects/interconn-study-21d/day-18.md
textbook: "Principles and Practices of Interconnection Networks (Dally & Towles) — Ch.12-13 Router Optimizations / High-Radix / CMesh"
ingested: 2026-07-13
---

# 📰 互连网络晨报 — Day 18

📅 2026-07-13（Day 18 / 21）
🎯 阶段：流控与微架构篇（Day 15-18）— **路由器微架构 II — 优化与共享**
📖 教材：*Principles and Practices of Interconnection Networks* (Dally & Towles, 2004) — Ch.12 + Ch.13

---

## 今日主题：从"5 级流水线"到"极致优化" — 路由器微架构的"工程深水区"

### 🧭 为什么今天学这个？

昨天你掌握了**标准 5 级流水线 + Crossbar + iSLIP** 的"教科书"路由器设计。但这个"标准答案"在**现代 NoC** 里**几乎从来不会**直接用——

```
WSE 的规模现实：
- 90 万 PE × 2D Mesh → ~949×949 网络
- 端到端平均跳数 ~474 跳
- 标准 5 级流水线头延迟 = 5 ns
- 端到端延迟 = 474 × 5 ns = 2370 ns ≈ 2.4 μs

→ 这个延迟对 AllReduce / 集合通信**太慢**了
→ 必须用**流水线优化**把它压到 ~1 ns/跳
```

**今日的"灵魂拷问"**：

1. **RC 必须在关键路径吗？** → Look-ahead Routing：把 RC 藏到上一拍
2. **VA 必须等 RC 完成吗？** → Speculative SA：赌 head flit 会获得 VC
3. **每个 VC 必须有独立 buffer 吗？** → Shared Buffer：N 个 VC 共享一个大 buffer
4. **路由器必须只连接 4-5 个邻居吗？** → High-Radix Router：1 个路由器连 16-64 个邻居
5. **Mesh 必须是 1 PE : 1 router 吗？** → Concentrated Mesh：1 router 服务 4 个 PE

**结论：今天的所有优化都是为"在物理约束下把延迟和成本压到极限"**——这正是 WSE 这种规模 NoC 设计的核心。

---

## 📖 阅读任务（约 80-100 分钟）

**Ch.12 高级 + Ch.13 路由器拓扑变体 + 论文**

### 必读：
1. **Ch.12.7** — Speculative Switch Allocation（投机开关分配）
2. **Ch.12.8** — Look-ahead Routing（前瞻路由）
3. **Ch.12.9** — Pipelined Bypassing（流水旁路）
4. **Ch.13.1** — Buffer Organization: Private vs Shared
5. **Ch.13.2** — Dynamic VC Allocation（动态 VC 分配）
6. **Ch.13.3** — High-Radix Routers（高基数路由器）
7. **Ch.13.4** — Concentrated Mesh（集中式 Mesh）

### 选读：
- **Kim, Dally, Abts 论文**："Adaptive Routing in High-Radix Clos Network" (2006) — 高基数网络奠基
- **Mitchell 论文**："Concentrated Mesh Router" — Concentrated Mesh 原始论文
- **Intel Teraflops 案例**："A 5-GHz Mesh Interconnect for a Teraflops Processor" (Polaris 80-core, 2007)
- **MIT Tiled 案例**："Tiled Multiprocessors" — 集中式 Mesh 实践

---

## 🔑 核心概念（必须掌握）

### 1. Speculative SA（投机开关分配）— 跳过 VA 节省 1 拍

**问题**：标准流水线 RC → VA → SA → ST → LT
- VA 必须等 RC 完成才知道用哪条 output VC
- 但 SA（开关分配）和 VA（VC 分配）**逻辑独立**——能不能并行？

**Speculative SA 思想**：
- **同时启动 VA 和 SA**
- SA **假设** head flit 会获得某个 VC（投机）
- 如果 VA 失败 → SA 的结果作废（这一拍没穿过 Crossbar，浪费 1 周期）
- 如果 VA 成功 → SA 提前 1 拍完成 ✓

```
标准流水线：   RC → VA → SA → ST → LT    （5 拍）
Speculative：  RC → SA_speculative ┐
                     VA ───────────┴→ ST → LT  （4 拍或 5 拍）
```

**关键问题**：speculation 失败会怎样？
- 失败时 flit 被阻塞，Crossbar 浪费 1 周期
- 失败率 = VA 冲突率
- 通常 95%+ 命中率（高负载下也成立）

**WSE 视角**：
WSE 路由器推测**必用** Speculative SA——每跳节省 1 拍 × 474 跳 = 474 周期 ≈ 0.5 μs 延迟节省

**Pipeline diagram**（Speculative SA）：

```
Cycle 1:  flit1 → RC
Cycle 2:  flit1 → SA_spec, VA  (并行)     | flit2 → RC
Cycle 3:  flit1 → ST (如果 VA 成功)         | flit2 → SA_spec, VA
Cycle 4:  flit1 → LT                        | flit2 → ST
Cycle 5:  flit1 输出                         | flit2 → LT
                                              | flit2 输出
→ 头延迟：4 拍（vs 标准 5 拍）
→ 关键路径：max(RC, SA_spec) + ST + LT
```

### 2. Look-ahead Routing（前瞻路由）— 把 RC 藏到上一拍

**问题**：RC（路由计算）必须等 head flit 进入当前路由器后开始
- RC 延迟 2-3 FO4 → 占用了关键路径

**Look-ahead Routing 思想**：
- **当前路由器在发送 flit 到下一跳时，预先计算下一跳的路由**
- 下一跳路由器收到 flit 时，**已经有路由结果** → 跳过 RC

```
标准：      Current Router: ... → RC → VA → SA → ST → LT → wire
Look-ahead: Current Router: ... → SA → ST → LT → wire (RC 在 SA 期间并行算下一跳)
            Next Router:    ... → VA → SA → ST → LT (跳过 RC)
```

**关键**：
- RC 延迟被**完全隐藏**在 SA 之后
- 下一跳的关键路径变成：VA + SA + ST + LT（4 拍）
- **路由器延迟 5 拍 → 4 拍**（节省 25%）

**实现挑战**：
- 需要在 SA 阶段并行计算**下一跳路由**（占硬件）
- 多跳 speculative：可以看 2-3 跳的路由（再省延迟）

**WSE 视角**：
WSE 推测**至少用 1-hop look-ahead**——是 WSE 极致延迟优化的关键之一

### 3. Pipelined Bypassing（流水旁路）— 连续同方向的 flit 跳过仲裁

**问题**：连续 2 个 flit 都要从 P0 到 P3
- flit 1：完整 RC → VA → SA → ST → LT（5 拍）
- flit 2：理论上**已知**要去 P3（和 flit 1 一样），为什么还要完整走 SA？

**Bypassing 思想**：
- 如果 flit 1 刚通过 (P0 → P3)，flit 2 也去 P3 → **直接穿过 Crossbar**
- flit 2 跳过 SA（甚至跳过 RC、VA）
- 等于把流水线深度从 5 拍压到 1 拍（理想情况）

```
标准：      flit2: RC → VA → SA → ST → LT  （5 拍）
Bypassing： flit2: ... → ST → LT  （1-2 拍，前提是上一拍 grant 是同 output）
```

**关键**：
- 适用于**突发流量**（burst traffic）
- LLM 推理中的**权重广播**、**all-reduce** 高度突发
- 命中率高时平均延迟大幅下降

**WSE 视角**：
- WSE 跑 LLM 时大量**结构化流量**（broadcast、reduce）
- Bypassing 命中率**推测 >80%**——延迟减半

### 4. Shared Buffer（共享缓冲）vs Private Buffer（私有缓冲）

#### Private Buffer（默认结构）
- 每个 VC 有**独立**的 buffer（如 4 flit × 4 VCs = 16 flit buffer / port）
- 优点：VC 隔离、无动态分配开销
- 缺点：**总利用率低**（某个 VC 满时其他 VC 空闲也帮不上）

```
每个 input port 内部：
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  VC 0    │  │  VC 1    │  │  VC 2    │  │  VC 3    │
│ 4 flits  │  │ 4 flits  │  │ 4 flits  │  │ 4 flits  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
   ↑             ↑             ↑             ↑
   独立 buffer，满了就阻塞，别的 VC 帮不上
```

#### Shared Buffer（共享结构）
- 所有 VC **共享一个大 buffer**（如 16 flit / port 总容量）
- 优点：**高利用率**（空闲 VC 的 buffer 可借给忙的 VC）
- 缺点：需要**动态分配器**（多路选择器选哪个 VC 的 flit 出去）

```
每个 input port 内部：
┌─────────────────────────────────────────────┐
│          Shared Buffer (16 flits)           │
│         ┌────┬────┬────┬────┬────┐          │
│  flit   │VC0 │VC1 │VC2 │VC0 │VC1 │   ...    │
│         └────┴────┴────┴────┴────┘          │
│  ↑      ↑      ↑      ↑      ↑              │
│  flit 可能属于不同 VC，动态分配             │
└─────────────────────────────────────────────┘
```

**关键参数对比**：

| 维度 | Private Buffer | Shared Buffer |
|------|----------------|---------------|
| 总 buffer 量 | N_VC × buf_per_VC | 单一总 buffer |
| 利用率 | 低（满 VC 阻塞，闲 VC 浪费）| 高（共享）|
| 硬件复杂度 | 低 | 高（多路选择器 + 分配器）|
| 功耗 | 高（每 VC 独立读写） | 中（共享读写）|
| 适用 | 低负载 | 高负载、突发流量 |

**WSE 视角**：
WSE 推测**混合策略**——少量 VC（2-4）私有大 buffer，剩余 capacity 共享
- 原因：WSE 上 LLM 流量突发极强（all-reduce、broadcast）

### 5. Dynamic VC Allocation（动态 VC 分配）

**问题**：每条物理链路上 N 条 VC，但是否要给每个流**静态分配**一条 VC？

**静态分配**（保守）：
- 每个 message class（请求/响应、req/reply）固定占用 1 条 VC
- 简单但利用率低

**动态分配**（激进）：
- VC 数随流量动态变化
- 流量少的 class 让出 VC 给流量大的 class
- 硬件需要**VC 状态机**

**WSE 视角**：
- LLM 推理的流量模式**非对称**（GEMM 阶段 vs attention 阶段）
- 动态 VC 分配可提升**全流量**吞吐 20-40%

### 6. High-Radix Router（高基数路由器）— 改变一切的设计哲学

**传统 NoC 路由器**（低基数）：
- 4-5 端口（4 邻居 + 1 local）
- Mesh 上 1 跳 = 1 路由器
- N 节点网络直径 ≈ √N

**高基数路由器**：
- 16-64 端口（多对多连接）
- 一次跳跃覆盖更多节点
- **直径 ∝ log_r(N)** → 跳数大幅减少

**数学对比**：
- 4-radix 路由器，1024 节点 Mesh：直径 = 2×32 = 64 跳
- 16-radix 路由器，1024 节点 Clos：直径 = log₁₆(1024) = 2.5 跳
- **延迟差距 25 倍**！

**高基数路由器的代价**：
- Crossbar：N² crosspoint
- 64 端口 → 4096 crosspoint（昂贵！）
- 现代方案：用 Clos 替代单层 Crossbar

**WSE 视角**：
- WSE 推测**仍用 4-5 radix 路由器**（因为 PE 极多，全局高基数不可能）
- 但 WSE 内部可能有**局部高基数**（如 8-radix 子网）
- 全局是 2D Mesh，局部可优化

### 7. Concentrated Mesh（集中式 Mesh）

**思想**：1 个路由器服务 4 个 PE（c=4 concentration）

```
传统 Mesh (c=1)：              Concentrated Mesh (c=4)：
                               
P - R - P - R - P - R          P P P P - R - P P P P - R
|   |   |   |   |   |           |   |   |   |   |
R - R - R - R - R - R           R - R - R - R - R
|   |   |   |   |   |           |   |   |   |   |
P - R - P - R - P - R          P P P P - R - P P P P - R
                               
router 数 = N                   router 数 = N/4
PE 数 = N                       PE 数 = N
直径 ≈ √N                       直径 ≈ √(N/4) = √N / 2
```

**关键优势**：
- 路由器数**减 4 倍**（省硬件）
- 直径**减半**（省延迟）
- 每个 PE 的端口数仍 = 1（连到本地 router）

**代价**：
- 4 个 PE **共享**一个 router 的输出带宽
- 局部拥塞可能上升

**WSE 视角**：
- WSE 推测 c=1（每个 PE 有独立 router）
- 但**未来 NoC 设计**的趋势是 c=4 或 c=8

### 8. 路由器优化的整体图景

```
┌─────────────────────────────────────────────────┐
│              路由器优化技术栈                      │
├─────────────────────────────────────────────────┤
│ 延迟优化                                         │
│  - Speculative SA   (-1 拍)                     │
│  - Look-ahead Routing (-1 拍)                   │
│  - Pipelined Bypassing (-1~3 拍突发)            │
├─────────────────────────────────────────────────┤
│ 面积/功耗优化                                    │
│  - Shared Buffer    (-30% buffer 面积)          │
│  - Dynamic VC Alloc (-VC 静态开销)               │
│  - High-Radix Router (-跳数, +crosspoint 权衡)  │
│  - Concentrated Mesh (-路由器数 4 倍)            │
├─────────────────────────────────────────────────┤
│ 整体效果                                         │
│  头延迟：5 拍 → 2-3 拍（极致优化）               │
│  跳数：√N → log_r(N)（高基数）                   │
│  端到端：2370 ns → ~700 ns（节省 70%）          │
└─────────────────────────────────────────────────┘
```

---

## 🧪 练习题（约 60-90 分钟）

### 基础题

**Q1（Speculative SA 失败成本）**：WSE 路由器 5 级流水线，目标 1 GHz。
- (a) Speculative SA 把头延迟从 5 拍压到几拍？
- (b) 如果 VA 失败率 = 10%（speculation miss），平均头延迟多少？
- (c) WSE 推测 474 跳时，延迟节省多少 ns？

> **参考答案**：
> - (a) 4 拍（RC + 并行(SA_spec, VA) + ST + LT）
> - (b) 0.9 × 4 + 0.1 × 5 = 3.6 + 0.5 = **4.1 拍**（平均）
> - (c) 标准 5 × 474 = 2370 ns；Speculative 4.1 × 474 = **1943 ns**；节省 **427 ns**

**Q2（Look-ahead Routing 关键路径）**：
- (a) Look-ahead Routing 把哪一级流水线从关键路径移除？
- (b) 移除后关键路径变成什么？
- (c) 路由器延迟从 5 拍变成几拍？

> **参考答案**：
> - (a) **RC**（路由计算）
> - (b) VA + SA + ST + LT（4 拍）
> - (c) 4 拍（节省 1 拍 = 20%）

**Q3（Shared Buffer 利用率）**：
- (a) Private buffer：4 VCs × 4 flits = 16 flits / port。如果 VC 0 满、VC 1 满、VC 2 满、VC 3 空闲 50%，实际可接收的 flits？
- (b) Shared buffer：16 flits 共享。如果分配器让 1 个"满 VC"借到空闲容量，等效可接收 flits？
- (c) 利用率提升多少？

> **参考答案**：
> - (a) 满的 3 个 VC 各阻塞（无法再收 flit），空 VC3 收 2 flits → 总 14 flits 可接收
> - (b) 16 flits 全部可动态分配 → 16 flits 可接收
> - (c) (16-14)/14 = 14% 提升（低负载下小，高负载下大）

**Q4（高基数路由器跳数）**：
- (a) 1024 节点用 4-radix 路由器 Mesh，理论跳数 = ？
- (b) 用 16-radix 路由器 Clos 网络，理论跳数 = ？
- (c) 假设路由器延迟 5 ns/跳，端到端延迟差距？

> **参考答案**：
> - (a) 32×32 Mesh，直径 = 62 跳
> - (b) Clos 树 3 级 = 3 跳
> - (c) 4-radix 310 ns vs 16-radix 15 ns → **快 20 倍**

**Q5（Concentrated Mesh 直径）**：
- (a) N=1024 节点，c=1 Mesh 直径？
- (b) N=1024 节点，c=4 Concentrated Mesh 直径？
- (c) 节省比例？

> **参考答案**：
> - (a) 32×32 Mesh = 62 跳
> - (b) 16×16 Concentrated Mesh = 30 跳
> - (c) (62-30)/62 = **52% 节省**

### 进阶题（与研究关联）

**Q6（WSE 路由器微架构反向推测）**：基于 WSE 的 90 万 PE 规模，推测其路由器微架构的 5 个最可能选择：

> **参考答案**：
> 1. **Speculative SA**：必用（474 跳，每跳 1 拍都宝贵）
> 2. **Look-ahead Routing**：必用（1 跳 look-ahead，节省 1 拍/跳）
> 3. **混合 Buffer**：4-8 VCs per port，前 2-3 私有 + 余量共享
> 4. **Crossbar + iSLIP**：5×5 crossbar + 2-3 轮 iSLIP
> 5. **c=1 Concentrated Mesh**（每个 PE 独立路由器，但 router pipeline 优化极致）

**Q7（优化组合效果）**：WSE 路由器从标准 5 拍优化到几拍？需列出 3 个组合优化及效果。

> **参考答案**：
> - **标准**：5 拍/跳 × 474 跳 = 2370 ns
> - **+ Speculative SA**：-1 拍 → 4 拍 → 1896 ns
> - **+ Look-ahead Routing**：-1 拍 → 3 拍 → 1422 ns
> - **+ Bypassing (50% 命中)**：-1 拍 → 2 拍 → 948 ns
> - **+ 链路并行 (pipeline forwarding)**：基本 0
> - **+ 距离优化**（局部高基数）：-30% 跳数
> - **最终**：~700-1000 ns（节省 60-70%）

**Q8（路由器微架构研究趋势）**：基于今天内容，列出 NoC 路由器研究的 4 个前沿方向：

> **参考答案**：
> 1. **硅光子集成**（photonic NoC router）：光交叉开关替代电 crossbar
> 2. **近似计算路由器**（approximate router）：降精度换性能
> 3. **3D 堆叠路由器**（3D-stacked router）：垂直方向加维度
> 4. **存算一体路由器**（in-memory router）：路由 + 缓冲融合
> 5. **可重构路由器**（reconfigurable router）：按应用动态调流水线深度

**Q9（Concentrated Mesh 拥塞分析）**：
- (a) c=4 Concentrated Mesh 中，4 个 PE 共享 1 个 router 出口带宽。假设每个 PE 注入 0.3 flits/cycle，router 出口带宽 1 flit/cycle，会发生什么？
- (b) 拥塞率多少？
- (c) 与 c=1 Mesh 相比（每 PE 独立出口）拥塞差异？

> **参考答案**：
> - (a) 4 PE × 0.3 = 1.2 flits/cycle 需求 vs 1 flit/cycle 出口 → **过载 20%**
> - (b) 拥塞 = max(0, 1.2-1) / 1 = 20% 时延
> - (c) c=1：每 PE 出口独立 1 flit/cycle，0.3 远低于 1 → **不拥塞**
> - 结论：c=4 在重负载下拥塞，c=1 轻负载下**更稳**

**Q10（动态 VC 分配的场景）**：
- (a) 哪种流量模式最适合动态 VC 分配？
- (b) 哪种流量模式最不适合？
- (c) LLM 推理的哪个阶段（prefill vs decode）更适合动态 VC？

> **参考答案**：
> - (a) 突发流量（如 all-reduce、broadcast）—— 闲 VC 借给忙 VC
> - (b) 均匀流量（uniform random）—— 静态分配已足够
> - (c) **Decode 阶段**（小 batch、大量 token 间依赖通信）—— 突发更强

---

## 📝 笔记任务（约 30-45 分钟）

在 `day-18.md` 末尾记录：

1. **Speculative SA 时序图**（自画）：
   ```
   Cycle:  1    2    3    4    5
   flit1: RC   SA_spec/VA → ST → LT  (4 拍)
                 ↑ 并行
   ```

2. **Look-ahead Routing 流水线对比**：
   ```
   标准:    RC → VA → SA → ST → LT
   Look-ahead: ... → VA → SA → ST → LT  (RC 在上一跳并行)
   ```

3. **Private vs Shared Buffer 对比表**：

| 维度 | Private | Shared |
|------|---------|--------|
| 利用率 | 低 | 高 |
| 复杂度 | 低 | 高 |
| 适用 | 低负载 | 高负载/突发 |

4. **高基数 vs 低基数 路由器对比表**：

| 维度 | 低基数 (4-5) | 高基数 (16-64) |
|------|--------------|----------------|
| 跳数 | 多（√N）| 少（log_r(N)）|
| 单 router 复杂度 | 低 | 高（crosspoint 爆炸）|
| 适合 | 大规模 NoC (WSE) | HPC 交换芯片 |

5. **WSE 路由器微架构推测清单（Day 17 + Day 18 综合）**：
   - 5 端口（4 网络 + 1 local）
   - **Speculative SA** ✅
   - **Look-ahead Routing** ✅
   - **混合 Buffer**（private + shared）
   - **iSLIP switch allocator**
   - 推测频率 850 MHz ~ 1 GHz
   - 推测头延迟：**3-4 拍**（极致优化后）

6. ❓ **标注你不理解的概念**

---

## 🎯 阶段自测（微架构篇 Day 15-18 综合校验）

在进入 Day 19（系统设计）前，先确认核心问题：

1. **Speculative SA 节省了哪一级流水线？**（提示：把 SA 和 VA 并行）
2. **Look-ahead Routing 把哪一级从关键路径移除？**（提示：路由计算）
3. **Shared Buffer 相比 Private Buffer 的核心优势？**（提示：高利用率）
4. **高基数路由器相比低基数，核心权衡是什么？**（提示：跳数 vs crosspoint）
5. **Concentrated Mesh 中 c=4 的含义？**（提示：1 router 服务 4 PE）
6. **WSE 路由器从 5 拍优化到几拍？哪 3 个优化贡献最大？**

能用自己的话回答这 6 个问题吗？

---

## 🔗 明日预告

**Day 19：系统设计 + 网络接口**

- 端到端原则 (End-to-End Argument)
- 网络服务模型（消息传递 / 共享内存）
- 拥塞管理（源头/目的地/网络内）
- 拥塞控制（开环 vs 闭环）
- Max-Min Fairness
- 流量控制 vs 拥塞控制的区别
- **NI（Network Interface）设计**

**Day 19 会用到今天的概念**：今天学的路由器优化是"网络内"的；明天学"网络边缘"的 NI——把"包"翻译成"消息"，把"网络"接到"应用"。

---

## 💡 今日感悟位

> 留给你写一句话总结今天的收获。
>
> 我的起点洞察：**路由器微架构优化是"用硬件复杂度换性能"的极致演绎**。
> - Speculative SA 用 1 周期风险换 1 周期延迟节省
> - Look-ahead Routing 用 1 个并行单元换 1 周期延迟节省
> - Bypassing 用控制逻辑换突发延迟减半
> - Shared Buffer 用分配器换 buffer 利用率
> - High-Radix 用 crosspoint 爆炸换跳数对数化
> - Concentrated Mesh 用共享出口带宽换路由器数减少
>
> **没有免费的午餐**——每个优化都有代价。但当你面对 90 万 PE 的 WSE 时，每 1 拍延迟都是真金白银：1 拍 × 90 万 = 不可忽略。这就是为什么 NoC 是体系结构研究的"硬骨头"——它既受物理约束（晶体管、线宽、功耗），又被应用需求（LLM、集合通信）倒逼。今天你看到的"看似聪明的小技巧"背后，是 30 年（1990s 至今）的工程经验 + 研究创新。

---

## 📚 推荐补充阅读

1. **Dally 论文**："Virtual-Channel Flow Control" (1992) — VC 原始论文
2. **iSLIP 论文**：McKeown, *"The iSLIP Scheduling Algorithm"* (1999)
3. **High-Radix Clos 论文**：Kim, Dally, Abts, *"Adaptive Routing in High-Radix Clos Network"* (2006)
4. **Concentrated Mesh 论文**：Mitchell, "The Concentrated Mesh"
5. **Intel Teraflops 论文**：Hoskote et al., *"A 5-GHz Mesh Interconnect for a Teraflops Processor"* (2007) — 工业案例
6. **Cerebras WSE 白皮书**（推测）：fabric architecture、router pipeline 推测
7. **BookSim 2.0 仿真器**：模拟路由器流水线 + 各种优化

---

## 📊 21 天进度追踪

| 阶段 | 天数 | 已完成 | 当前 |
|------|------|--------|------|
| 基础篇 | Day 1-4 | ✅✅✅✅ | |
| 拓扑篇 | Day 5-10 | ✅✅✅✅✅✅ | |
| 路由篇 | Day 11-14 | ✅✅✅✅ | |
| **流控篇** | **Day 15-18** | **✅✅✅✅** | **🔥 Day 18（最后一天）** |
| 应用篇 | Day 19-21 | | |

**整体进度**：Day 18 / 21 = **86% 完成** 🎯

---

*这是 21 天学习计划的第 18 天。昨天你进入了路由器微架构的"标准设计"，今天你学完了它的"优化变体"——从 Speculative SA 到 High-Radix Router，你已经看到了 NoC 工程师是如何在"面积、功耗、延迟"三角中走钢丝。明天开始你将走出路由器，进入"系统视角"——看 NI、看拥塞控制、看端到端原则，这是把 NoC 接到真实系统的关键一步。*
