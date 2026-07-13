---
type: Raw Source
title: 📰 互连网络晨报 — Day 17
source_path: /home/luke/openclawdata/workspace-research/notes/projects/interconn-study-21d/day-17.md
textbook: "Principles and Practices of Interconnection Networks (Dally & Towles) — Ch.11-12 Router Pipeline / Crossbar / Allocators"
ingested: 2026-07-13
---

# 📰 互连网络晨报 — Day 17

📅 2026-07-12（Day 17 / 21）
🎯 阶段：流控与微架构篇（Day 15-18）— **路由器微架构 I — 交叉开关与分配器**
📖 教材：*Principles and Practices of Interconnection Networks* (Dally & Towles, 2004) — Ch.11-12

---

## 今日主题：从"VC 队列"到"5 级流水线" — 路由器微架构登场

### 🧭 为什么今天学这个？

前两天我们建立了 VC + 流控的硬件基础：
- **Day 15**：wormhole 把 packet 切成 flit，沿链路逐段前进
- **Day 16**：VC 把单条物理链路切成 N 条逻辑车道

但有一个**致命问题**没解决：

```
假设一个 5 端口路由器（P0 注入 → P3 输出）：

   P0 ─┐                    ┌─ P3
   P1 ─┤                    ├─ P4
   P2 ─┤──  [???] ───────── ├─ (Local)
       │      ↑
       └──── 这一刻路由器内部在做什么？

我们需要回答：
1. flit 到了路由器后，**依次经过哪些硬件阶段**？
2. **同时有多条 flit 竞争**同一条输出端口时，谁优先？
3. Crossbar（交叉开关）**怎么物理实现**？需要多少晶体管？
```

**答案：5 级流水线 + Crossbar + 分配器**

```
P0 ─┐                                              ┌─ P3
    │    ┌────┬────┬────┬────┬────┐                │
P1 ─┼──→ │ RC │ VA │ SA │ ST │ LT │ ──→ Crossbar ──┼─ P4
    │    └────┴────┴────┴────┴────┘                │
P2 ─┘                                              └─ Local

RC: Route Compute          → 决定去哪
VA: VC Allocation          → 决定用哪条 VC（昨天学的！）
SA: Switch Allocation      → 决定何时走 Crossbar
ST: Switch Traversal       → 真的穿过 Crossbar
LT: Link Traversal         → 真的穿过链路
```

**今日三大核心问题：**

1. **5 级流水线每一级做什么？** 哪级是关键路径？
2. **Crossbar 的物理结构**是怎样的？5×5 Crossbar 需要多少 crosspoint？
3. **Switch Allocator 怎么公平调度？** Round-Robin / Matrix Arbiter / iSLIP 各有什么优劣？

---

## 📖 阅读任务（约 75-100 分钟）

**Ch.11-12 — 路由器流水线 + 交叉开关 + 分配器**

### 必读：
1. **Ch.11.1** — 路由器的基本功能：从 wormhole 流到路由器内部
2. **Ch.11.2** — 路由器的 5 级流水线（RC / VA / SA / ST / LT）
3. **Ch.11.3** — 流水线时序分析：每级的时钟开销
4. **Ch.12.1** — Crossbar（交叉开关）的结构与 crosspoint 数量
5. **Ch.12.2** — Round-Robin Arbiter（轮转仲裁器）
6. **Ch.12.3** — Matrix Arbiter（矩阵仲裁器）
7. **Ch.12.4** — iSLIP 调度算法（重要！）
8. **Ch.12.5** — Wavefront Arbiter（波形前仲裁器）

### 选读：
- **Ch.12.6** — 分配器的吞吐与公平性分析
- **McKeown 1999 iSLIP 论文**：*"The iSLIP Scheduling Algorithm for Input-Queued Switches"* — iSLIP 原始论文
- **Dally 1988 路由器流水线**：*"The J-Machine Router"*
- **MIT MIT Alewife / Intel Teraflops 路由器案例**

---

## 🔑 核心概念（必须掌握）

### 1. 路由器流水线总览 — 5 级，每级 1 拍

```
P_in ─→ ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐ ─→ P_out
        │ RC │→ │ VA │→ │ SA │→ │ ST │→ │ LT │
        └────┘  └────┘  └────┘  └────┘  └────┘
         ↓       ↓       ↓       ↓       ↓
        路由    VC     开关     Crossbar  链路
        计算    分配    仲裁     穿越     穿越
         ↓
       1 拍    1 拍    1 拍    1 拍    1 拍
       ←──────── 总 5 拍延迟 ─────────→

每个周期，一个新 flit 可以进入 RC（流水线满载）
→ 吞吐量 = 1 flit/cycle/端口（理想情况）
```

**5 级流水线详解：**

#### RC (Route Compute) — 路由计算
- 输入：head flit 的 destination address
- 输出：output port + output VC ID
- 实现：组合逻辑（CAM、查找表、或简单 DOR 计算）
- **典型延迟**：2-3 个 FO4 反相器延迟

#### VA (VC Allocation) — VC 分配
- 输入：RC 的结果 + 当前空闲 VC 表
- 输出：head flit 获得一条 output VC
- 实现：两阶段仲裁器（先 request，再 grant）
- **典型延迟**：2-4 个 FO4（关键路径！）

#### SA (Switch Allocation) — 开关分配
- 输入：所有 input VC 的请求
- 输出：哪些 (input, output) 对获得 Crossbar
- 实现：iSLIP / Wavefront Arbiter
- **典型延迟**：3-6 个 FO4（**真正的关键路径**）

#### ST (Switch Traversal) — 穿越交叉开关
- 输入：SA grant
- 输出：flit 真的从 input 走到 output（穿过 Crossbar）
- 实现：Crossbar 的传输延迟
- **典型延迟**：1-2 个 FO4

#### LT (Link Traversal) — 穿越链路
- 输入：flit 从 ST 出来
- 输出：flit 到达下一个路由器的 input
- 实现：wire delay
- **典型延迟**：时钟周期的一部分（如果 wire 短，与 ST 并行）

**关键洞察**：
- **Head flit** 经过完整 5 级流水线
- **Body/Tail flit** 只经过 SA → ST → LT（3 级）→ 省 2 级延迟！
- 这就是为什么 wormhole 头部延迟高、后续 flit 流水化

**WSE 视角**：
WSE 的 fabric clock 推测 850 MHz ~ 1 GHz。每周期 ~1 ns：
- RC: 0.2 ns（2-3 FO4）
- VA: 0.3 ns（2-4 FO4）
- SA: 0.4 ns（3-6 FO4，**最长**）
- ST: 0.1 ns（穿越 Crossbar）
- LT: 与 ST 并行（片上距离短）
- 总头延迟：~1.0 ns/cycle × 5 = **5 ns 路由器延迟**

### 2. Crossbar（交叉开关）— 全连接的交换矩阵

**本质**：N 个 input + N 个 output，每个 input 可以独立连到任何 output

```
N×N Crossbar 结构（N=4）：

         P0_out  P1_out  P2_out  P3_out
         ┌────┬────┬────┬────┐
P0_in ──►│ ×  │ ×  │ ×  │ ×  │  ← crosspoint
         ├────┼────┼────┼────┤
P1_in ──►│ ×  │ ×  │ ×  │ ×  │
         ├────┼────┼────┼────┤
P2_in ──►│ ×  │ ×  │ ×  │ ×  │
         ├────┼────┼────┼────┤
P3_in ──►│ ×  │ ×  │ ×  │ ×  │
         └────┴────┴────┴────┘

共 N² 个 crosspoint
每个 crosspoint = 1 个传输门（或三态缓冲器）
```

**关键计算**：

| Crossbar | Crosspoint 数量 | 控制线 | 总晶体管估算 |
|---------|----------------|--------|-------------|
| 4×4     | 16             | 32 (2/pt) | ~256       |
| 5×5     | **25**          | 50     | ~400        |
| 8×8     | 64             | 128    | ~1024       |
| 16×16   | 256            | 512    | ~4096       |
| 32×32   | 1024           | 2048   | ~16K        |

**WSE 应用**：
- WSE 路由器推测为 **5 端口**（N、E、S、W + Local）
- 5×5 Crossbar = **25 crosspoint**
- 每周期需仲裁哪些 (in, out) 配对 → Switch Allocator

**复杂度挑战**：
- N² 复杂度 → 大路由器成本爆炸
- 解决：分层（Benes）、分段（Clos）、或限制连接

**Crosspoint 的实现**：
- 简单传输门：2 个晶体管（NMOS + PMOS）
- 三态缓冲器：4-6 个晶体管
- 8T SRAM cell + pass transistor：~10 个晶体管

### 3. Switch Allocator — "谁能穿过 Crossbar"

**问题**：N 个 input 想同时穿过 Crossbar，但每个 output 一次只能接一个 input。如何仲裁？

```
输入：
- Input 0: 想发到 Output 2
- Input 1: 想发到 Output 2
- Input 2: 想发到 Output 0
- Input 3: 想发到 Output 1
- Input 4: 想发到 Output 0

冲突：
- Output 2: 被 Input 0 和 Input 1 竞争
- Output 0: 被 Input 2 和 Input 4 竞争
- Output 1: 只有 Input 3
- 其他 outputs: 空闲

→ 需要两阶段仲裁：
  1. Input-side arbitration：每个 input 选一个 output
  2. Output-side arbitration：每个 output 选一个 input
```

#### A. Round-Robin Arbiter（轮转仲裁器）— 最简单

**原理**：
- 每个 output 维护一个 priority pointer
- 每次 grant 后，pointer 移到下一个位置
- 公平性：O(N) 轮保证每个 input 都被服务

```
Output 0 的轮转序列：
- 优先级 [I0, I1, I2, I3, I4]
- 第 1 拍：I2 和 I4 竞争 → I2 胜 → pointer → I3
- 第 2 拍：I4 再竞争 → I4 胜 → pointer → I0
- 第 3 拍：I0 胜 → pointer → I1
- ...
```

**优缺点**：

| 维度 | 评价 |
|------|------|
| 硬件复杂度 | 低（计数器 + 比较器）|
| 公平性 | 严格（O(N) 轮）|
| 吞吐 | 中（~63% 最大匹配 vs 最优 100%）|
| 实现延迟 | 1 拍（快）|

#### B. Matrix Arbiter（矩阵仲裁器）— 并行仲裁

**原理**：
- 输入 N×N 二维 request matrix
- 每行：input 请求哪个 output
- 每列：output 收到哪些 input 的请求
- 并行解决冲突（硬件上同时处理所有行/列）

```
Request Matrix (4 inputs × 4 outputs):

       Out0  Out1  Out2  Out3
In0  [  0     0     1     0  ]
In1  [  0     0     1     0  ]
In2  [  1     0     0     0  ]
In3  [  0     1     0     0  ]

→ 解出 In0→Out2, In2→Out0, In3→Out1
→ In1 失败（与 In0 冲突 Out2）
```

**优缺点**：

| 维度 | 评价 |
|------|------|
| 硬件复杂度 | 中（O(N²) 仲裁逻辑）|
| 公平性 | 中（依赖优先级设置）|
| 吞吐 | 中-高 |
| 实现延迟 | 1-2 拍 |

#### C. iSLIP Arbiter — 工业标准，**重点掌握**

**原理**（McKeown 1999）：
- 三步迭代，最多 N 轮达到最大匹配
- 每轮：request → grant → accept → 更新 priority
- **关键**：priority pointer 在 grant 后才更新（vs 传统 Round-Robin 在 accept 后更新）

```
iSLIP 单轮：

1. Request: 所有 input 向所有 output 发请求
2. Grant: 每个 output 选择 priority pointer 指向的最高优先级 request
3. Accept: 每个 input 选择 priority pointer 指向的最高优先级 grant
4. Update: 只更新**已成功 grant** 的 output 的 pointer

→ 这种"延迟更新"是 iSLIP 公平性的关键
```

**iSLIP 的关键性质**：

1. **1 轮**：吞吐可达 ~63%（vs 最优 100%）
2. **2 轮**：吞吐可达 ~88%
3. **3+ 轮**：吞吐 ~98%，接近最优
4. **无饥饿**（no starvation）：O(N²) 轮保证每个 input 被服务至少一次

**优缺点**：

| 维度 | 评价 |
|------|------|
| 硬件复杂度 | 中（类似 Round-Robin，但迭代逻辑稍复杂）|
| 公平性 | 高（pointer 延迟更新是关键）|
| 吞吐 | **高**（2-3 轮后 ~90%+）|
| 实现延迟 | 多轮（2-4 拍，但可流水化）|

**WSE 推测**：iSLIP 是 WSE switch allocator 的强候选（高吞吐 + 工业验证）。

#### D. Wavefront / Wavefront-Decision Arbiter

**原理**：
- 类似 iSLIP，但并行决策（一次完成所有 grant/accept）
- 适合高速流水线

### 4. 路由器 5 级流水线的时序分析

**理想情况**（每级 1 拍）：
```
周期 1: flit 1 在 RC
周期 2: flit 1 在 VA，flit 2 在 RC
周期 3: flit 1 在 SA，flit 2 在 VA，flit 3 在 RC
周期 4: flit 1 在 ST，flit 2 在 SA，...
周期 5: flit 1 在 LT，flit 2 在 ST，...
周期 6: flit 1 输出，flit 2 在 LT，...
```

**关键路径限制**：
- 通常 RC + VA + SA 在同一拍完成（组合逻辑）
- ST + LT 在下一拍完成（传输）
- 总延迟：5 拍 / 周期 = 5 ns（@ 1 GHz）

**Head vs Body flit 的流水线差异**：
- **Head flit**：5 级全部经过（决定路由）
- **Body flit**：跳过 RC 和 VA → 3 级
- **Tail flit**：同 body + 释放 VC

**WSE 推测延迟分解**（@ 1 GHz fabric clock）：
- Router 头延迟：~5 ns
- 链路延迟（短）：~1 ns
- 端到端 8 跳：~50 ns（典型数据报延迟）

### 5. Crossbar vs 其他交换结构

| 结构 | Crosspoint | 阻塞 | 复杂度 |
|------|-----------|------|-------|
| **Crossbar** | N² | 无内部阻塞（Crossbar 本身） | O(N²) |
| **Clos Network** | 3×(N×2k) | 严格非阻塞 | O(N^(3/2)) |
| **Benes Network** | ~N×logN | 可重排非阻塞 | O(N log N) |
| **Butterfly** | N×logN | 内部阻塞 | O(N log N) |

**为什么 NoC 选 Crossbar**：
- N 小（5-8 端口）：N² 成本可控
- 无内部阻塞（Crossbar 天然非阻塞）
- 控制简单

**为什么 HPC 选 Clos/Fat Tree**：
- N 大（64-128 端口）：N² 不可接受
- 需 Clos 的 O(N^(3/2)) 优势

### 6. 路由器微架构的演化

```
1980s (CM-5): 简单 crossbar + store-and-forward
1990s (TMC CM-5, MIT J-Machine): wormhole + 1-cycle 路由器
2000s (Intel Teraflops): 5-级流水线 + 4-VC + iSLIP
2010s (MIT Tile, Intel SCC): mesh + speculative SA
2020s (WSE): 推测 advanced 流水线 + 高基数 + 多 VC
```

**WSE 的可能优化**（基于其规模 900K PE）：
- **Speculative SA**：跳过 VA 直接做 SA（节省 1 拍）
- **Look-ahead routing**：RC 与上一级 SA 并行（隐藏 RC 延迟）
- **Pipeline bypassing**：连续同 output 端口的 flit 跳过 SA
- **High-radix router**：减少跳数（每跳 ~5 ns × 5 跳 = 25 ns vs 3 跳高基数 = 15 ns）

---

## 🧪 练习题（约 60-90 分钟）

### 基础题

**Q1（5 端口路由器流水线）**：画出一个 5 端口路由器（WSE 推测拓扑）的完整流水线时序图。标注：
- 5 个端口（P0-P4）
- 5 级流水线（RC/VA/SA/ST/LT）
- 一个 head flit 从 P0 进入 → 路由到 P3 的完整路径
- 同时有 body flit 跟随的情况

> **参考答案**：
> ```
> Cycle 1: flit 1(head) → RC | (P1-P4 idle)
> Cycle 2: flit 1 → VA | flit 2(body) → RC
> Cycle 3: flit 1 → SA | flit 2 → VA (skipped RC) | flit 3(body) → RC
> Cycle 4: flit 1 → ST | flit 2 → SA | flit 3 → VA
> Cycle 5: flit 1 → LT | flit 2 → ST | flit 3 → SA
> Cycle 6: flit 1 输出 (P3) | flit 2 → LT | flit 3 → ST
> ```

**Q2（5×5 Crossbar crosspoint 计算）**：一个 5 端口路由器（4 个网络端口 + 1 个本地端口）的 Crossbar：
- (a) 需要多少个 crosspoint？
- (b) 如果用传输门（2 晶体管/crosspoint），共多少晶体管？
- (c) 如果改用 8T SRAM cell（10 晶体管/crosspoint）作为配置寄存器，总成本？

> **参考答案**：
> - (a) 5² = **25 crosspoint**
> - (b) 25 × 2 = 50 晶体管
> - (c) 25 × 10 = 250 晶体管

**Q3（Round-Robin 公平性验证）**：一个 4 输入 / 4 输出 Crossbar。Input 0 持续请求 Output 0，Input 1 持续请求 Output 1。问：
- (a) Round-Robin 仲裁器如何在两个 input 之间分配 Crossbar 周期？
- (b) Input 2 突然请求 Output 0，需要等待多久才能被服务？
- (c) 这个延迟是否符合"无饥饿"原则？

> **参考答案**：
> - (a) 50/50（Input 0 和 Input 1 各自占一半周期）
> - (b) 最多 3 拍（O(N) 轮）
> - (c) 是，O(N) 等待是严格无饥饿

**Q4（iSLIP 单轮 grant/accept）**：Request matrix 如下：
```
       Out0  Out1  Out2  Out3
In0  [  1     0     1     0  ]
In1  [  0     1     0     1  ]
In2  [  1     1     0     0  ]
In3  [  0     0     1     1  ]
```
假设所有 priority pointer 初始为 0（指向 In0）：
- (a) 第 1 轮 grant 阶段：每个 Output 选哪个 Input？
- (b) 第 1 轮 accept 阶段：每个 Input 接受哪个 Output 的 grant？
- (c) 第 1 轮后，哪些 Output 的 pointer 更新？

> **参考答案**：
> - (a) Out0→In0（pointer 0），Out1→In2（pointer 0），Out2→In0（pointer 0），Out3→In1（pointer 0）
> - (b) In0→Out0，In2→Out1，In1→Out3
> - (c) Out0/Out1/Out3 更新（被 grant 的），Out2 未被 grant 不更新

### 进阶题（与研究关联）

**Q5（路由器关键路径分析）**：假设你设计一个 WSE 路由器，频率目标 1 GHz。
- (a) 如果 FO4 延迟 = 25 ps，5 级流水线每级最多多少 FO4？
- (b) 已知 SA 需要 6 FO4（iSLIP），ST 需要 2 FO4。如果 SA 和 ST 在同一拍会怎样？
- (c) 如何重新切分流水线来满足时序？

> **参考答案**：
> - (a) 1000 ps / 25 ps = 40 FO4/拍
> - (b) 6 + 2 = 8 FO4 → 完全可行（远小于 40 FO4 上限）
> - (c) 可以合并更多逻辑（如 speculative SA 跳过 VA）

**Q6（WSE Switch Allocator 反推）**：基于今天内容，做 4 个推测：
- (a) WSE Switch Allocator 最可能用哪种算法？（iSLIP vs Round-Robin vs Wavefront）
- (b) 5 端口路由器的 SA 仲裁器需要多少比较器？
- (c) SA 在哪一级流水线？是关键路径吗？
- (d) WSE 如何通过 speculative SA 优化 SA 延迟？

> **推测答案**：
> - (a) iSLIP（工业标准 + 高吞吐）
> - (b) 5 outputs × 5 inputs = 25 比较器（理论上，更少因为 conflict detection）
> - (c) SA 是第 3 级，**是关键路径**（6+ FO4）
> - (d) Speculative SA：head flit 同时启动 SA 和 VA，谁先完成用谁的结果

**Q7（Crossbar 变体选择）**：给定应用场景：
- (a) 4 端口 Mesh 路由器（最常见 NoC）
- (b) 8 端口集中式 Mesh 路由器（CMP，集中 4 个核）
- (c) 16 端口 Fat Tree 边缘交换机
- (d) 64 端口 HPC 核心交换机
为每个场景选择 Crossbar 类型（直接 Crossbar / 分段 Clos / Benes），并解释。

> **参考答案**：
> - (a) 4×4 = 16 crosspoint → 直接 Crossbar
> - (b) 8×8 = 64 crosspoint → 直接 Crossbar（仍可接受）
> - (c) 16×16 = 256 crosspoint → 临界，可考虑分段
> - (d) 64×64 = 4096 crosspoint → 必须 Clos 或 Benes

**Q8（流水线吞吐 vs 延迟）**：5 级流水线 vs 1 级组合逻辑：
- (a) 哪种延迟更低？（单 flit）
- (b) 哪种吞吐更高？（流水线满载）
- (c) WSE 路由器为什么必须用流水线？

> **参考答案**：
> - (a) 1 级组合延迟 = RC+VA+SA+ST+LT = 40 FO4，5 级流水 = 5 拍 × 8 FO4/拍 = 40 FO4（相同）
> - (b) 流水：1 flit/cycle/端口；组合：1 flit/(40 FO4)
> - (c) 频率 + 吞吐约束。流水线是高速 NoC 的唯一选择

---

## 📝 笔记任务（约 30-45 分钟）

在 `day-17.md` 末尾记录：

1. **5 级流水线时序图**（自画）：
   ```
   Cycle:  1    2    3    4    5    6
   flit1: RC   VA   SA   ST   LT  out
   flit2:     RC   VA   SA   ST   LT
   flit3:          RC   VA   SA   ST
   ```

2. **5×5 Crossbar 物理结构图**（25 个 crosspoint）

3. **三种 Arbiter 对比表**：
   | Arbiter | 公平性 | 吞吐 | 复杂度 |
   |---------|--------|------|--------|
   | Round-Robin | 高 | 中 | 低 |
   | Matrix | 中 | 中 | 中 |
   | iSLIP | 高 | 高 | 中 |

4. **WSE 路由器推测清单**：
   - 5 端口（4 网络 + 1 local）
   - 5 级流水线
   - 25 crosspoint Crossbar
   - iSLIP switch allocator
   - 推测频率 850 MHz ~ 1 GHz

5. ❓ **标注你不理解的概念**

---

## 🎯 阶段自测（微架构篇 Day 17 校验）

在进入 Day 18（路由器优化）前，先确认核心问题：

1. **5 级流水线的名称和功能？**（提示：RC/VA/SA/ST/LT）
2. **5×5 Crossbar 需要多少 crosspoint？**（提示：N²）
3. **iSLIP 比 Round-Robin 的核心优势是什么？**（提示：延迟更新 pointer）
4. **Head flit 和 Body flit 经过的流水线级数差异？**（提示：5 vs 3）
5. **为什么 Crossbar 在 NoC 中主导，但 HPC 用 Clos？**（提示：N 大小）

能用自己的话回答这 5 个问题吗？

---

## 🔗 明日预告

**Day 18：路由器微架构 II — 优化与共享**

- Speculative SA（投机开关分配）
- Look-ahead Routing（前瞻路由计算）
- Bypassing（流水旁路）
- 共享缓冲（Shared Buffer）vs 私有缓冲（Private Buffer）
- 动态 VC 分配
- 高基数路由器（High-Radix Router）
- Concentrated Mesh（集中式 Mesh）
- **WSE NoC 路由器微架构的优化空间**

**Day 18 会用到今天的概念**：所有这些优化都是围绕"减少 SA/ST 的关键路径延迟"或"提高缓冲利用率"展开。

---

## 💡 今日感悟位

> 留给你写一句话总结今天的收获。
>
> 我的起点洞察：**路由器微架构是 NoC 的"心脏外科手术"**。5 级流水线 + Crossbar + iSLIP 看似只是几个硬件组件，但它们共同决定了：
> - **延迟**（5 级流水 × 1 ns = 5 ns 头延迟）
> - **吞吐**（1 flit/cycle/端口 = 满载）
> - **公平性**（iSLIP 的延迟更新 pointer）
> 这也是为什么 **"路由器微架构是 NoC 论文的高频主题"**——它既是工程的极限挑战，也是研究的开放问题。今天你看到了"看似简单的硬件组件"如何组合成一个**复杂的优化系统**，这就是体系结构研究的乐趣。

---

## 📚 推荐补充阅读

1. **iSLIP 原始论文**：McKeown, *"The iSLIP Scheduling Algorithm for Input-Queued Switches"* (1999) — 必读经典
2. **Dally 1988 J-Machine**：*"The J-Machine Router"* — 早期 wormhole 路由器
3. **Modern Router Case Studies**：
   - Intel Teraflops (Polaris) 80-core Mesh Router
   - MIT Alewife 路由器
   - Tilera TILE-Gx 路由器
4. **Cerebras WSE 公开材料**：fabric architecture、router pipeline（推测）
5. **BookSim 仿真器**：Stanford BookSim 模拟路由器流水线

---

## 📊 21 天进度追踪

| 阶段 | 天数 | 已完成 | 当前 |
|------|------|--------|------|
| 基础篇 | Day 1-4 | ✅✅✅✅ | |
| 拓扑篇 | Day 5-10 | ✅✅✅✅✅✅ | |
| 路由篇 | Day 11-14 | ✅✅✅✅ | |
| **流控篇** | **Day 15-18** | **✅✅✅** | **🔥 Day 17** |
| 应用篇 | Day 19-21 | | |

**整体进度**：Day 17 / 21 = **81% 完成** 🎯

---

*这是 21 天学习计划的第 17 天。昨天你掌握了 VC 的"逻辑车道"概念，今天你进入了路由器内部——看到了 5 级流水线 + Crossbar + iSLIP 是如何把 VC、wormhole、死锁避免这些抽象概念**转化为实际硬件**。明天你将看到这些硬件的优化变体，进入路由器微架构的"深度优化"世界。*