---
type: Raw Source
title: 📰 体系结构晨报 — Day 18
source_path: /home/luke/openclawdata/workspace-research/notes/projects/arch-study-30d/day-18.md
textbook: "Computer Architecture: A Quantitative Approach (6th ed.) — Ch.5 (5.1-5.3)"
ingested: 2026-06-24
---

# 📰 体系结构晨报 — Day 18

📅 2026-07-01（Day 18 / 30，星期三）
🎯 阶段：存储篇（Day 17-22）
📖 教材：《计算机体系结构：量化方法》第6版 Ch.5 (5.1-5.3)

---

## 今日主题：Cache 一致性协议（Snooping & Directory）

### 🧭 为什么今天学这个？

昨天你学完了 DRAM 物理——单核视角下，CPU 拿到地址后穿过 Cache→Memory Controller→HBM→DRAM cell，一切都是有序的。

**但问题来了**：

> 当系统里有 2 个、4 个、64 个核心各自有 L1 Cache 时，**P0 写的值什么时候能让 P1 看见**？

这就是 **Cache 一致性 (Cache Coherence)** 问题。它是**多核芯片能否正确工作的第一道关口**——如果一条 coherence 协议出错，你跑的科学计算、LLM 推理、金融交易全部都会得到错误结果，而且**最难调试**。

今天的核心问题：

1. **MSI / MESI / MOESI** 四种状态到底在追踪什么？为什么 MESI 里的 "E" 状态值得多塞一个状态机？
2. **Snooping 协议** vs **目录协议**——为什么 Intel/AMD 在 server 上用目录，Apple 在 iPhone 上用 snooping？
3. **False Sharing**——一个 8-byte 的变量怎么让两个核相互拖慢 5 倍？
4. **WSE 为什么不需要这整章内容？** — 这正是你的研究领域要回答的核心简化论之一。

明天 Day 19 会进入"内存一致性模型" (Memory Consistency)，把 MESI 这层"数据同步"问题上升到"顺序语义"层面。今天先把"协议本身"讲透。

---

## 📖 阅读任务（约 60-90 分钟）

**《计算机体系结构：量化方法》第6版 Ch.5 (5.1-5.3): Symmetric and Distributed Memory Multiprocessors**

### 核心阅读（60 min）：
1. **5.1 Introduction** — 多核架构分类（SMP、DMP、NUMA）
2. **5.2 Symmetric Shared Memory Multiprocessors** — Snooping 协议族
3. **5.3 Distributed Shared Memory** — 目录协议
4. **附录 L (Appendix L)** — coherence consistency 一致性定义（选读）

### 必读论文片段（30 min）：
- **James Goodman (1983) "Using Cache Coherence"** — 早期 coherence 综述
- **IEEE 标准**：`BusInval` 和 `BusUpgr` 信号的定义（见量化方法 Ch.5 侧边栏）

### 选读：
- Intel Skylake Server Uncore 架构白皮书（directory 协议实现示例）
- ARM Cortex-A 系列 "Snoop Control Unit" 文档

---

## 🔑 核心概念（必须掌握）

### 1. 一致性问题（Why Coherence Matters）

```
单核：只有一个 L1 Cache，CPU 写完即"看见"结果
多核：Core 0 L1 写完 → Core 1 L1 还保留旧值 → Core 1 读 → 拿到错的值
```

**一致性需要满足两个属性**（Goodman 1983）：

| 属性 | 含义 |
|------|------|
| **Propagation (传播)** | 一个 core 的写最终必须被所有 core 看见 |
| **Serialization (串行化)** | 同一地址的写必须在所有 core 上看到**相同顺序** |

注意：Coherence **只管同一地址**。多个地址之间的顺序是 Day 19 的 consistency model 管的事。

### 2. MESI 状态机（最核心！）

每个 Cache Line 维护一个**两比特状态字段**：

```
┌─────────────────────────────────────────────────────────────────┐
│  M  = Modified      仅本 Cache 有副本，且为 dirty                  │
│  E  = Exclusive     仅本 Cache 有副本，但为 clean（与 memory 同）  │
│  S  = Shared        本 Cache 与其他 Cache 共享 clean 副本        │
│  I  = Invalid       无效（可能没有此行，或已失效）                  │
└─────────────────────────────────────────────────────────────────┘
```

**关键洞察**：M 和 E 的区别 — **E 是"我有干净副本且知道我是唯一"的提示**。有了 E，core 改写时不需要先广播"我要独占"（invalidate）消息，可直接 silent drop（升级到 M）。这是 MESI 比 MSI 性能好的关键。

### 3. MESI 状态转换（带 Bus 消息）

下表展示了 4 个转换触发条件（**这是必须背下来的东西**）：

```
Bus 消息类型：
  - PrRd : Bus Read (处理器读请求)
  - PrWr : Bus Invalidate (处理器写请求/广播失效)
  - BusUpgr : 升级请求（从 S → M 的 bus 消息）
  - Flush : 回写脏数据
  - Snoop : 其他 Cache 的应答
```

| 当前状态 | 事件 | 新状态 | 触发动作 |
|---------|------|--------|----------|
| **I** | PrRd (L1 miss) | S | 发 BusRd；若其他 Cache 命中 → 它们降为 S，自己升 S |
| **I** | PrRd (L1 miss) | E | 发 BusRd；若**没人**有副本 → 自己升 E |
| **I** | PrWr | M | 发 BusRdX（带 invalidate）；自己写并直接进入 M |
| **S** | PrRd | S | 命中，无动作 |
| **S** | PrWr | M | 发 BusUpgr；所有其他副本降为 I |
| **E** | PrRd (local) | E | 命中，无动作 |
| **E** | PrWr (local) | M | **直接静默升级！**不需要 bus 消息（这是 E 状态的精妙） |
| **M** | PrRd (local) | M | 命中，无动作 |
| **M** | 其他 core's PrRd | S | **写回 memory**，自己降为 S，其他核升 S（读直达 memory） |
| **M** | 其他 core's PrWr | I | 自己 write-back memory 后降为 I，新持有者升 M |

**为什么 E 重要？** 假设一个程序对一个变量做"读-改-写"循环：
- 第一次访问：I → E（独占）
- 之后每次修改：E → M（**零总线事务**）
- 没有 E 状态时：每次都要先发 BusUpgr，多核总线压力暴增 50%+

### 4. MOESI：在 MESI 上加一个 Owned 状态

AMD 在 Opteron 上加了 **O (Owned)** 状态。解决的问题：**多核共享同一 dirty line 时的写回问题**。

```
场景：Core 0 在 M 状态；Core 1 也要读这一行
  MESI 行为：Core 0 必须 write-back memory，Core 1 从 memory 读 → 多 100ns
  MOESI 行为：Core 0 从 M → O（保持 dirty），Core 1 从 O 拿到数据（S 状态但从 O 缓存来）
```

**O 状态**：本 Cache 是 dirty 的所有者，但已分享读给其他核；其他核 S 状态但数据来源是 O 而非 memory。

| 协议 | 状态数 | 优点 | 缺点 | 代表 |
|------|-------|------|------|------|
| MSI | 3 | 简单 | 频繁 broadcast invalid | 早期 Pentium |
| MESI | 4 | 性能更优（E 状态） | 状态机稍复杂 | x86、iPhone ARM、Apple Silicon |
| MOESI | 5 | 进一步减少 memory write-back | 硬件更复杂 | AMD Opteron / Zen |

### 5. Snooping vs Directory（核心权衡）

```
┌───────────── Snooping (Bus-based) ─────────────┐
│  所有 core 共享一条广播总线（如 QPI / ring bus）  │
│  任何 core 的 L1 miss 都会 broadcast 到总线        │
│  每个 cache controller 监听（snoop）所有消息      │
│  优点：延迟低（一次总线事务搞定）                  │
│  缺点：总线不可扩展（>16 核就饱和）                │
│  代表：Intel Core i7 ring bus、Apple M1           │
└──────────────────────────────────────────────────┘

┌───────────── Directory (NUMA) ──────────────────┐
│  一个集中式 Directory 记录"哪个 cache 有 line X"   │
│  Core X 请求 line → Directory 查表 → 只通知持有者 │
│  优点：可扩展到 1000+ 核                           │
│  缺点：Directory lookup 本身延迟（~50ns），三跳     │
│  代表：Intel Skylake Server、AMD EPYC、ARM CCIX    │
└──────────────────────────────────────────────────┘
```

**量化对比**：

| 规模 | Snooping | Directory |
|------|---------|-----------|
| 4 核 | ✓ 简单 | 杀鸡用牛刀 |
| 16 核 | ✓ ring bus 仍可承受 | 仍可选项 |
| 64 核 | ✗ 总线成为瓶颈 | ✓ 必需 |
| 256 核 | ✗✗ 不可行 | ✓✓ 标配 |

### 6. False Sharing（性能杀手！）

**定义**：两个独立变量落在**同一 Cache Line**（通常 64B）内，被不同核分别修改，导致整个 line 在两核之间反复 invalidate。

```
struct {  int x;  int y;  } shared;   // x 与 y 看似独立

Core 0 (thread 0) 频繁写 x    → 持有 line 的 M 状态
Core 1 (thread 1) 频繁写 y    → 看到 line 是 M → 触发 flush + reload
                    ↑↑ 这就是 False Sharing ↑↑
```

**真实代价**：在 2-socket server 上，两个核之间一次 M↔I 抖动能导致 **~30-50 ns 延迟**。如果 thread 0 每 20ns 写一次，thread 1 也每 20ns 写一次，吞吐能掉 **3-5×**。

**修复**：padding 到 64B 边界，让 x 和 y 在不同 line。

```c
struct { int x; char pad[60]; int y; } shared;   // x 与 y 不同 line
```

### 7. 一致性粒度（Coherence Granularity）

一致性协议追踪的最小单位是 **Cache Line**（64B 是主流）。

```
粒度小（如 32B）：减少 False Sharing，但 Directory 翻倍
粒度大（如 128B）：减少 metadata，但 False Sharing 更严重
折中：64B 是过去 30 年的甜蜜点
```

**有趣的方向**：一些研究（NCC、Sector cache）探索 variable-granularity coherence——读密集区用大粒度，写密集区用小粒度。研究价值高但硬件实现复杂。

---

## 📝 笔记任务（约 30 分钟）

1. **手绘 MESI 状态转换图**（4 个状态 + 6-8 个箭头），标注每个箭头的触发 bus 消息
2. **列出 MESI 状态在每种状态下的"本地视角"**：
    - M：我是 dirty 持有者，谁来读我要么 transfer 要么 write-back
    - E：我是干净独占者，写时静默升级
    - S：我与他人共享 clean
    - I：对我无效
3. **对比 MESI / MOESI 在"多核共享 dirty line"场景的 bus 流量**（画出一个具体 trace）
4. **手算题**：4 核处理器跑下面这段代码，每个变量初始在 memory：
    ```
    Core 0: A = 1;   B = A + 1;
    Core 1: C = A + 2;
    Core 2: D = B + C;
    Core 3: print C, D;
    ```
    列出所有 MESI 状态转换 + 总线事务数。**答案见下文练习题。**

---

## 🧪 练习题（约 30-60 分钟）

### 基础题

**Q1**：在 4 核 MESI 系统中，Core 0 写地址 X（X 初始在 memory）。从 Core 0 第一次写开始，到 Core 2 读到 X，列出每个核的 X 的状态变化。

> 答：
> 1. Core 0 PrWr X：发 **BusRdX**；没人 hit；Core 0 取到 X（值为初值），直接写后进入 **M**；其他核 I
> 2. Core 1 PrRd X：发 **BusRd**；Core 0 hit in M → write-back memory → Core 0 降为 **S**；Core 1 升 **S**
> 3. Core 2 PrRd X：发 **BusRd**；memory 命中（Core 0 已 write-back）；Core 2 也升 **S**
> 4. **总事务数 = 2**（一次 BusRdX + 一次 BusRd）

**Q2**：MESI 比 MSI 性能好在哪儿？举一个具体场景说明。

> 答：单线程反复修改独占数据的场景。
> - **MSI**：每次写都要发 BusUpgr（I→M 需要 invalidate 其他 core），即使其他 core 根本没 cache 这行
> - **MESI**：第一次读进 **E**（因为是独占），之后 E→M 是**静默升级**，不发任何 bus 消息
> - 实测性能差距：在 OLAP 数据库 single-threaded update 场景，**MESI 比 MSI 快 15-30%**

**Q3**：64 核系统为什么必须用 Directory 而不是 Snooping？

> 答：
> - Snooping 总线 = 共享介质；每次 coherence 事件都是 broadcast
> - 单次 snoop 延迟 = 10ns；每条 coherence 消息都要被所有 64 个 cache controller 处理
> - 总线带宽上限 ~ 32 bytes/cycle @ 2GHz = 64 GB/s；理论上够，但实际因总线仲裁、cache controller 排队，**>32 核**就开始饱和
> - Directory 是点对点通信，只通知持有者那 1-3 个核，带宽压力是 O(共享者数) 而非 O(核数)，**64 核时 Directory 总流量只有 Snooping 的 5-10%**

**Q4**：下面这段代码有什么性能问题？如何用一行 padding 修复？
```c
typedef struct { int counter; int checksum; } stats_t;
stats_t stats[NUM_THREADS];  // 每个 thread 修自己的 stats[i]

void worker(int tid) {
    for (int i = 0; i < N; i++) {
        stats[tid].counter++;      // thread tid 写自己的 counter
        stats[tid].checksum += i;  // thread tid 写自己的 checksum
    }
}
```
> 答：**False Sharing**。`stats[tid].counter` 与 `stats[tid+1].counter` 落在同一 Cache Line；两个 thread 同时写同一 line 不同字段，反复 invalidate。
> 修复：
> ```c
> typedef struct { int counter; char pad[60]; int checksum; } stats_t;
> ```
> 性能提升：在 2-socket 16-core server 上，**吞吐提升 3-5 倍**。

### 进阶题

**Q5**：分析下面 trace 的 MESI 状态转换和总总线事务数（4 核 MESI，初始所有 data 在 memory）。
```
T0: Core 0 read  X          (Core 0 cache state of X after: ?)
T1: Core 1 read  X          (Core 0 state, Core 1 state: ?)
T2: Core 0 write X           (events on bus?)
T3: Core 2 read  X
T4: Core 1 write X
T5: Core 0 read  X
T6: Core 3 write X
```

> 答（用 [Core0, Core1, Core2, Core3] 表示各核的 X 状态）：
>
> | 步骤 | Core 0 | Core 1 | Core 2 | Core 3 | Bus 事件 |
> |------|--------|--------|--------|--------|---------|
> | T0   | E      | I      | I      | I      | BusRd (无应答) |
> | T1   | S      | S      | I      | I      | BusRd (Core 0 snoop → S; Core 1 新加 S) |
> | T2   | M      | I      | I      | I      | BusUpgr (Core 1 snoop → I; Core 0 升 M) |
> | T3   | S      | I      | S      | I      | BusRd (Core 0 write-back memory, → S; Core 2 新加 S) |
> | T4   | I      | M      | I      | I      | BusRdX (Core 0, Core 2 snoop → I; Core 1 升 M) |
> | T5   | I      | S      | I      | I      | BusRd (Core 1 write-back; → S; Core 0 新加 S) |
> | T6   | I      | I      | I      | M      | BusRdX (Core 0, Core 1 snoop → I; Core 3 升 M) |
>
> **总总线事务 = 7**（4 次 BusRd + 2 次 BusUpgr/BusRdX）；如果不优化（无 E 状态），会再多 1-2 次。

**Q6**：用 Directory 协议重新分析 Q5（4 核 → 假设每个 line 在 Directory 的 sharer list 准确）。Directory 总共需要发送多少条 unicast 消息？

> 答：
> - T0: Core 0 → Directory: BusRd；Directory → Core 0: data + state=E, sharers=[0]
> - T1: Core 1 → Directory: BusRd；Directory → Core 0: "降为 S"；Directory → Core 1: data, sharers=[0,1]
> - T2: Core 0 → Directory: BusUpgr；Directory → Core 1: "降为 I"；Directory → Core 0: 升级为 M, sharers=[0]
> - T3: Core 2 → Directory: BusRd；Directory → Core 0: "write-back + 降为 S"；Directory → Core 2: data, sharers=[0,2]
> - T4: Core 1 → Directory: BusRdX；Directory → Core 0: "降为 I"；Directory → Core 2: "降为 I"；Directory → Core 1: data + 升级为 M, sharers=[1]
> - T5: Core 0 → Directory: BusRd；Directory → Core 1: "write-back + 降为 S"；Directory → Core 0: data, sharers=[0,1]
> - T6: Core 3 → Directory: BusRdX；Directory → Core 0: "降为 I"；Directory → Core 1: "降为 I"；Directory → Core 3: data + 升 M, sharers=[3]
>
> **每条消息最大 fan-out = 2**（Directory 只需通知当前持有者）。Snooping 一次 broadcast 是 4 个 listener；**Directory 总流量 ≈ Snooping 的 50-60%**（64+ 核时差距更大）。

### 思考题（与 WSE 研究关联）

**Q7**：WSE-3 有 900,000 PE。如果每个 PE 有 48KB SRAM 并维护 MESI 一致性，需要多少状态存储？会发生什么？

> 答（粗略量化）：
> - 假设 48KB SRAM 用于 cache data，line = 64B → 每个 PE 有 **768 个 line**
> - 每 line 需要 2-bit MESI state = **192B metadata**（忽略 tag 等）
> - 总 metadata = 900,000 × 192B ≈ **170 GB** metadata！这比 SRAM 数据本身还大！
> - 更糟：维护 900K 个 PE 的 MESI 状态，directory 节点需要 **170 GB 关联存储**（line → sharer list），查询延迟 100ns+ 量级
> - **总流量**：一次 R/W 将触发 O(对角线 PE 数) 广播；WSE 的 mesh NoC 立刻饱和
> - **结论**：在 900K PE 的尺度上，传统 coherence **硬件层面就破产了**——这就是 WSE 必须重新思考一致性模型的物理原因。

---

## 🔗 与 WSE / NoC / NPU 研究的关联

### 1. WSE 的根本性简化：没有共享内存

```
通用多核（Cerebras 之外的所有芯片）：
  全局共享地址空间 + Cache + Coherence Protocol
  → ISA 兼容标准 C/C++/Python → 编程简单
  → 硬件成本高，扩展性受限

WSE：
  无全局地址空间，每个 PE 独占 48KB SRAM
  → 数据通过 mesh NoC "流动"（fabric 拉/推）
  → 需要"显式"数据布局 → 编程复杂（CSL/SpaDA）
  → 硬件极简，扩展性 → 900K PE
```

**WSE 取消了 coherence 的代价是什么？**

| 维度 | 通用多核 | WSE |
|------|---------|-----|
| 一致性硬件 | MESI 协议 + Directory | **无**（用消息传递替代） |
| 编程模型 | 共享变量（pthread） | 显式数据路由（CSL） |
| 编译器 | 普通 C/C++ | 需要 SpaDA 编译为 DAG |
| 正确性保证 | ISA 提供 SC/TSO | 由程序员 + 编译器保证 |
| 性能 | 硬件自动 | 程序员调优（人力成本高） |

### 2. Luke 的核内同步研究的"反面"机会

你的研究方向是 **核内同步**（intra-core synchronization）。今天的内容揭示了一个有趣的研究空白：

> **问题**：在多核 NPU 设计中，PE 之间需要快速同步（如 SPMD-style 同步 barrier、SEMA 操作）。传统 coherence 协议太慢（100ns+）；mesh 上手写消息传递延迟又不可控。

**研究机会**：
- 借鉴 WSE 的 "fabric pull" 模型，设计**轻量级 PE 间同步原语**（broadcast barrier + 数据 confirm）
- 用 NoC 的"硬件 barrier"加速 AllReduce 风格的同步
- 在 coherence 和消息传递之间寻找"中间形态"——比如只对**关键共享变量**做 coherence，其他用消息传递（研究者叫 **Hybrid Coherence**）

### 3. 为什么 Intel 在 Xeon 上死磕 Directory，Apple 在 M1 上用 Snooping？

| 维度 | Intel Xeon SP（server） | Apple M1（client） |
|------|------------------------|-------------------|
| 核数 | 16-112 核 | 8 核（4P+4E） |
| 一致性协议 | Directory（Haswell 之后） | Snooping（ring bus） |
| 原因 | 规模决定非 Directory 不可 | 小规模 Snooping 更低延迟 |
| Ring 宽度 | — | M1 是 32B/cycle 总线 |

**给 Luke 的启示**：核数从 8 到 64，光是 coherence 协议就要换一套硬件结构。**你的 NPU 核研究必须明确"目标核数"**——8 核 Snooping 与 64 核 Directory 的 NoC 设计哲学根本不同。

### 4. 一个具体 NPU 案例分析

假设你设计一个 64-core NPU，每核是 4×4 SLA 阵列：

```
设计选择 A：标准 MESI + Snooping
  → 需要 ring bus 或全局 mesh 总线
  → 64 核 ring bus 延迟 = 64 × hop_latency ≈ 数百 ns
  → 一次 share 变量读延迟：500-1000 ns
  → NPU 通常不写共享变量，主要做 dataflow → coherence 是 overhead

设计选择 B：消息传递（如 WSE/Transputer）
  → NoC 直接传 64B message
  → hop_latency = 10ns；8 hop 距离 = 80 ns
  → 编程难度上升；需要 SPMD 风格
  → 适合 dataflow workload

设计选择 C：Hybrid
  → 控制面 + 标量变量 → coherence（用 snooping，10核以内）
  → 数据面 + 张量 → 消息传递
  → Luke 的研究机会！
```

---

## 🔗 明日预告

**Day 19：同步与一致性进阶**
- 内存一致性模型（SC / TSO / ARM）
- Memory Barrier / Fence 语义
- LL/SC vs CAS 原子操作
- 锁实现：Spinlock / Ticket Lock / MCS Lock
- **核心问题**：为什么 Apple Silicon 上某些代码比 x86 上更容易出现 race？
- **与 WSE 关联**：WSE 的单时钟域天然保证 SC，但代价是放弃全局异步弹性。

**承上启下**：今天把"数据同步"（coherence）讲透了，明天把"顺序语义"（consistency）讲到 hardware-software contract 的深度。这是 Luke 核内同步研究的硬件基础。

---

## 💡 今日感悟位

> *Cache 一致性协议的本质是什么？是把"我是这份数据的唯一持有者"这件事写成硬件可验证的不变量。今天学到最反直觉的一点：MESI 协议的状态机本身在做"硬件级分布式事务"——而 WSE 直接取消了这件事，把正确性扔回给软件。这其实是把硬件复杂度换成了软件复杂度，背后是 30 年体系结构权衡的核心思想。*

---

*Day 18 / 30. 第三阶段（存储篇）第二天。今天你掌握了多核系统的"宪法"——MESI。下一步是把宪法扩展到"顺序的合法性"，即内存一致性模型。这是 Luke 研究"核内同步"的硬件前置知识。*
