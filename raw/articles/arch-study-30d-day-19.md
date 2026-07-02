---
type: Raw Source
title: 📰 体系结构晨报 — Day 19
source_path: /home/luke/openclawdata/workspace-research/notes/projects/arch-study-30d/day-19.md
textbook: "Computer Architecture: A Quantitative Approach (6th ed.) — Ch.5 (5.4-5.6)"
ingested: 2026-06-24
---

# 📰 体系结构晨报 — Day 19

📅 2026-07-02（Day 19 / 30，星期四）
🎯 阶段：存储篇（Day 17-22）
📖 教材：《计算机体系结构：量化方法》第6版 Ch.5 (5.4-5.6)

---

## 今日主题：同步与一致性进阶（Memory Consistency + 同步原语）

### 🧭 为什么今天学这个？

昨天我们讲了 **Cache Coherence**——它的作用域是**单个地址**：确保所有核看到同一地址的"最新值"。但 coherence 解决不了**多地址之间的顺序**问题。

**今天的核心问题**：

> 两个核同时跑：
> ```
> Core 0: A = 1;       // write A
>          print B;     // read  B
> Core 1: B = 1;       // write B
>          print A;     // read  A
> ```
> 在严格顺序下，不可能出现"两个核都看到对方变量 = 0"。但在弱内存模型下，**这完全可能发生**。

这就是 **Memory Consistency Model（内存一致性模型）** 解决的问题。它定义了：
1. 处理器和编译器**可以重排哪些内存操作**
2. 程序员**必须用什么指令**才能阻止重排
3. 同步原语（lock/atomic/barrier）**如何映射到硬件 fence**

**对你的研究（核内同步）而言**，今天的概念是**硬件基础**：
- 核内多线程同步（如 SMT 内 thread 间通信）需要什么 fence？
- NPU 上多个 PE 同时写同一个统计寄存器，硬件需要保证什么顺序？
- WSE 的"单一时钟域"如何天然避免 consistency 问题——代价是什么？

---

## 📖 阅读任务（约 60-90 分钟）

**《计算机体系结构：量化方法》第6版 Ch.5 (5.4-5.6): Memory Consistency + Synchronization**

### 核心阅读（60 min）：
1. **5.4 Memory Consistency Models** — SC / TSO / PSO / ARM
2. **5.5 Comparing Memory Consistency** — 各种模型的对比表
3. **5.6 Synchronization** — 原子操作、锁实现
4. **附录 L (Appendix L)** — 各种一致性模型的 formal 定义

### 必读论文片段（30 min）：
- **Adve & Gharachorloo (1996) "Shared Memory Consistency Models: A Tutorial"** — 必读中的必读
- **Sorin et al. "A Primer on Memory Consistency and Cache Coherence"** — 配套教材

### 选读：
- ARM Architecture Reference Manual §B2 (Memory ordering)
- Intel SDM Vol.3 §8.2 (Memory ordering)
- RISC-V Spec Chapter 6 (Memory Model, RVWMO)

---

## 🔑 核心概念（必须掌握）

### 1. Coherence vs Consistency（容易混淆！）

```
Coherence（昨天的内容）：
  定义：对单个地址，多核看到的值必须一致
  回答："X 的最新值是什么？"
  硬件：MESI/MOESI 实现

Consistency（今天的内容）：
  定义：对多个地址，访存的相对顺序必须满足某种规则
  回答："A=1 之后 B=2 是否一定对其他核可见？"
  硬件：Memory Fence + 访存队列约束
```

**关键洞察**：Coherence 是 per-address 的；Consistency 是 cross-address 的。一个系统可以**有完美的 coherence 但弱 consistency**。

### 2. 顺序一致性 Sequential Consistency (SC)

**Lamport (1979) 定义**：

> *系统的执行结果，等价于所有处理器操作按某种**全局全序**排列，且每个处理器的操作在该全序中保持**程序顺序 (program order)***

**核心要求**（两两组合）：
```
WR → WR  : 我写完 X，下一个写 Y 必须排在后面
WR → RD  : 我写完 X，别人读 X 必须看到我写的值
RD → WR  : 我读 X 之后才写 Y
RD → RD  : 我读 X 之后才读 Y
```

**SC 的实现代价**：
- 每次 Load/Store 都要等前序操作"在全局可见"才能执行
- 硬件开销极大：一次 Store Buffer 刷新就能 stall 一个核 50+ ns
- 现实：**没有商业处理器实现 SC**

### 3. TSO：x86 的"几乎 SC"

**Total Store Order (TSO)** — x86 (Intel/AMD) 使用的模型

```
TSO = SC + 允许一个特殊优化：Store Buffer
```

**关键放宽**：写操作可以"暂时藏在 Store Buffer 里"，不必立即对其他核可见。读操作可以**绕过 Store Buffer** 直接从内存读。

**TSO 允许的重排**：
```
✗ 不允许：Load → Load 重排（可能破坏 SPSC 同步）
✗ 不允许：Load → Store 重排（写必须等读完）
✗ 不允许：Store → Store 重排（写顺序必须保留）
✓ 允许：Store → Load 重排（写完不等，立即读）
```

**为什么这很重要**：在 TSO 下，"读自己的写"是 guaranteed（store buffer 对自己可见）。但**其他核读不到这个写，直到 fence/buffer flush**。

### 4. ARM / RISC-V 弱模型（最复杂）

ARM 和 RISC-V 默认采用 **weak memory model**：

**ARM 允许的几乎所有重排**（除了显式 fence）：
```
✓ Load → Load 重排
✓ Load → Store 重排
✓ Store → Store 重排
✓ Store → Load 重排
```

**实战对比**：

| 操作 | SC | TSO (x86) | ARM/RISC-V |
|------|----|---------|-----------|
| 普通 Load 后跟 Store | 必须等 | 必须等 | 可并行 |
| Store 后跟 Load | 必须等 | **可重排** | 可重排 |
| 需要 fence 阻止 | 几乎从不 | 偶尔 | **必须显式** |

**这是为什么 x86 程序员的 lock-free 代码**比 ARM 程序员写起来简单的原因——但 ARM 性能上限更高（无谓 fence 更少）。

### 5. Memory Fence / Barrier 详解

**X86 指令集**（TSO 下的 fence 需求）：
```
mfence  : 阻止所有 Load 和 Store 重排（最强）
lfence  : 阻止 Load 重排
sfence  : 阻止 Store 重排
LOCK prefix : 原子操作 + 隐含 full fence
```

**ARM 指令集**（需要更细粒度）：
```
DMB (Data Memory Barrier)  : 等待之前所有访存完成
DSB (Data Sync Barrier)    : 等所有访存完成 + 指令完成
ISB (Instruction Sync Barrier) : 刷新流水线
```

**RISC-V 指令集**（最简洁）：
```
fence rw, rw  : 阻止读写之间的重排（最常用）
fence.tso     : 类似 TSO 语义（轻量 fence）
fence.i       : 指令同步（用于自修改代码）
```

### 6. 原子操作原语：LL/SC vs CAS

**Compare-And-Swap (CAS)**：
```
int CAS(int* addr, int expected, int new) {
    atomic {
        old = *addr;
        if (old == expected) *addr = new;
        return old;
    }
}
```
**实现**：x86 `LOCK CMPXCHG` 指令，硬件锁总线/缓存行，~50ns。

**Load-Linked / Store-Conditional (LL/SC)**：
```
do {
    ll_result = LL(addr);     // Load-Linked, 标记地址
    success = SC(addr, new);  // Store-Conditional, 仅当未被打断
} while (!success);
```
**实现**：RISC-V `LR/SC`、ARM `LDREX/STREX`、Power `lwarx/stwcx`。

**对比**：

| 维度 | CAS | LL/SC |
|------|-----|-------|
| 硬件复杂度 | 中（总线锁/缓存锁） | 高（需跟踪 LL 标记） |
| ABA 问题 | **有**（值变回原值但语义已变） | **无**（条件不仅看值） |
| 失败重试 | 直接重试 | 自动重试（SC 失败不写） |
| ISA 支持 | x86 主流 | RISC 主流 |
| NPU 上的适用性 | 控制面偶尔用 | **数据流同步更友好** |

### 7. 锁实现：从 Spinlock 到 MCS

**Test-and-Set Spinlock**（最简单，性能最差）：
```
acquire:
    while (TestAndSet(&lock, 1) == 1) ;   // 自旋
release:
    lock = 0;
```
**问题**：所有等待者争抢同一个 cache line（false sharing），多核下**性能雪崩**。

**Ticket Lock**（公平，FIFO）：
```
acquire:
    my_ticket = Fetch&Add(&next_ticket, 1);
    while (my_ticket != now_serving) ;   // 等待轮到
release:
    now_serving++;
```
**优点**：公平，无饥饿。**缺点**：所有等待者还是 polling 同一 cache line。

**MCS Lock**（最优解！John Mellor-Crummey & Michael Scott, 1991）：
```
acquire:
    my_node->next = NULL;
    predecessor = Swap(&lock, my_node);  // 原子交换
    if (predecessor == NULL) return;       // 我是第一个
    my_node->locked = 1;
    predecessor->next = my_node;           // 排队
    while (my_node->locked) ;              // 自旋本地变量

release:
    if (my_node->next == NULL) {
        if (CAS(&lock, my_node, NULL)) return;
        while (my_node->next == NULL) ;   // 等后继出现
    }
    my_node->next->locked = 0;             // 直接唤醒后继
    my_node->next = NULL;
```

**关键创新**：每个等待者自旋**自己的本地变量**，不争抢全局 cache line。**100 核下性能比 Ticket Lock 高 10×**。

| 锁 | Cache Line 争抢 | 公平性 | 复杂度 | 适用规模 |
|----|----------------|--------|--------|---------|
| TAS Spinlock | 极严重 | 否 | 极简 | 4 核以下 |
| Ticket Lock | 严重 | 是 | 简单 | 16 核以下 |
| MCS Lock | **无** | 是 | 中等 | 100+ 核 |

---

## 📝 笔记任务（约 30 分钟）

1. **手画 SC / TSO / ARM 三种模型的"允许重排矩阵"**（4×4 表格：Load-Load, Load-Store, Store-Load, Store-Store）
2. **手写一个 Lock-Free Queue**（基于 CAS），并标注每行的 memory ordering 要求
3. **对比下面这段代码在 x86 (TSO) 和 ARM 上的正确性差异**：
    ```c
    // Thread 1
    flag = 1;       // 写
    while (!ready) ; // 读

    // Thread 2
    ready = 1;       // 写
    while (flag != 1) ; // 读
    // 期望: Thread 1 能读到 ready==1
    ```
4. **计算 NPU 同步开销**：假设 NPU 有 64 个 PE，每个 PE 写 1 个字节到共享统计寄存器：
    - 用 LL/SC 实现需要多少次总线事务？
    - 用 MCS 锁呢？
    - 用纯消息传递（write to mailbox）呢？

---

## 🧪 练习题（约 30-60 分钟）

### 基础题

**Q1**：下面哪个操作组合在 x86 (TSO) 下**不需要 fence** 就能保证正确？
```c
// 选项 A
x = 1;       // write
y = *p;      // read  → 可能比 x 的写更早对其他核可见？

// 选项 B
y = *p;      // read
x = 1;       // write → 读完后才写

// 选项 C
x = 1;       // write
x = 2;       // write → 顺序对其他核也保留？
```

> 答：
> - **A**：需要 fence。TSO 允许 Store→Load 重排，其他核可能先看到 `y=*p` 再看到 `x=1`。
> - **B**：不需要。TSO **禁止** Load→Store 重排。
> - **C**：不需要。TSO **禁止** Store→Store 重排，x=1 一定在 x=2 之前对所有核可见。

**Q2**：Mellor-Crummey & Scott 1991 年提出 MCS Lock 时，主要解决了什么问题？量化对比 ticket lock。

> 答：
> - **问题**：Ticket Lock 在 N 核上扩展性差。N 个等待者**全部 polling 同一 cache line**（`now_serving`），每次 cache line invalidate 触发 O(N) 次 snoop。
> - **MCS 创新**：每个等待者自旋**本地变量** `my_node->locked`，只在 predecessor 显式唤醒时修改。
> - **量化对比**（32 核机器实测）：
>   - Ticket Lock：N 核同时 lock 时，每秒 invalidate ~3M 次，吞吐 ~2M ops/s
>   - MCS Lock：每秒 invalidate ~3K 次，吞吐 ~25M ops/s
>   - **吞吐提升 ~12×**，cache line 争抢降低 **1000×**

**Q3**：LL/SC 比 CAS 好在哪？给一个 CAS 出错的例子。

> 答：**ABA 问题**。
> ```
> Thread 1:              Thread 2:
>   old = top (A)          pop()      // top 变成 B
>   ... (被抢占)           push(A)     // top 又变成 A
>   CAS(top, A, new)
>   // CAS 成功！但链表已经被 Thread 2 改过
>   // 破坏链表不变量
> ```
> LL/SC 的解决：`SC` 失败当**该地址被任何写访问过**（不只是值变化），所以 Thread 2 那个 pop 会让 Thread 1 的 SC 失败。

**Q4**：在 RISC-V 上实现自旋锁，哪种写法**不需要 fence**？
```c
// 选项 A: 用 atomic_flag
while (atomic_flag_test_and_set(&lock)) ;   // 调用 LR/SC

// 选项 B: 用普通变量 + fence
while (lock) ;
```

> 答：**A**。`atomic_flag_test_and_set` 是 C11 原子操作，编译器+硬件**自动插入必要的 fence**。
> B 不行：编译器会把 `lock = 0` 缓存在寄存器里，**优化掉了写**——这叫 "compiler reordering"，比 CPU reordering 更难发现。必须用 `volatile` 或 atomic 类型。

### 进阶题

**Q5**：分析下面 lock-free counter 的正确性（多核 x86 + ARM 都要分析）：
```c
std::atomic<int> counter(0);

// Thread 1, 2, ..., N
void inc() {
    int old = counter.load(std::memory_order_relaxed);
    while (!counter.compare_exchange_weak(old, old + 1,
            std::memory_order_relaxed,
            std::memory_order_relaxed)) ;
}
```

> 答：
> - **x86 (TSO)**：counter 是对齐的 4-byte，原子读写天然安全。即使 relaxed 不插入 fence，硬件保证 `LOCK CMPXCHG` 原子性。**正确。**
> - **ARM (weak)**：`CMPXCHG` 在 ARM 上是 LL/SC 序列，relaxed 模式下允许前后读写重排，但因为每个 `CAS` 本身是 RMW 原子，CAS 之间不需要顺序。**正确。**
> - **为什么 relaxed 安全**：因为 counter 只有一个变量，coherence 保证一致性；CAS 失败时自动重读新值；不需要 cross-variable ordering。**这是 relaxed 的标准用例。**

**Q6**：某 NPU 有 64 个 PE 同时写同一个 32-bit 统计计数器。用以下三种方式实现，各需要多少次"总线事务"？（假设每个总线事务 = 一次 cache line transfer，~10 ns）
- A：每个 PE 用 CAS 重试
- B：每个 PE 用 LL/SC 重试
- C：所有 PE 把数据写到同一个 SRAM 地址（无锁）

> 答：
> - **A (CAS)**：64 PE 串行化。CAS 失败的 PE 需要 retry；假设均匀分布，平均每个 PE 重试 2 次 → 总事务 = 64 × 2 = **128 次**，延迟 ~1280 ns
> - **B (LL/SC)**：与 A 类似但失败的概率更高（因为 SC 对任何写敏感），平均重试 3 次 → 总事务 ≈ 64 × 3 = **192 次**，延迟 ~1920 ns
> - **C (无锁写)**：如果硬件支持"atomic OR/FETCH_ADD"，一次广播就够了 → 总事务 = **1 次 broadcast**，延迟 ~10 ns
> - **结论**：NPU 上统计计数应该用 **fetch-and-add 硬件原语**，而不是软件 CAS。这是 NPU ISA 设计的关键决策。

### 思考题（与 WSE 研究关联）

**Q7**：WSE 的 mesh NoC 有 900K PE。如果要让所有 PE 同步一个 barrier（等所有 PE 到达），需要多少跳 / 多少时间？和 MCS Lock 比怎么样？

> 答（粗略量化）：
> - **Hardware Barrier**：WSE 的 fabric 有专门的 barrier 信号线（参考 Cerebras 论文）。最坏情况：信号穿越对角线 ~670 hop × 1 ns/hop = **670 ns**
> - **软件 MCS Lock**：900K PE 排队，平均等待者 = 450K。每个等待者自旋自己的本地变量（mesh 局部变量）→ 无 cache line 争抢。但**每个 PE 都要等前 450K 个 PE 完成 lock/unlock**，每次 lock/unlock 在 mesh 上传消息至少 2 hop ≈ 2 ns，**总时间 ~900K × 2 ns ≈ 1.8 ms**
> - **硬件 Barrier vs MCS**：**快 2700 倍**
> - **启示**：在 WSE 这种规模下，**所有软件同步原语都破产了**。必须用硬件 barrier/signal。这是 Luke 核内同步研究的关键 insight：**当核数超过 ~10K，硬件 barrier 是唯一选择**。

---

## 🔗 与 WSE / NoC / NPU 研究的关联

### 1. WSE 的"单时钟域"天然实现 SC

WSE-3 的 900K PE 在**同一时钟域**下同步运行（参考 Cerebras 公开资料）。这意味着：

```
优势：
  • 一次 Store 立即对所有 PE 可见（无 store buffer 延迟）
  • 没有 TSO/ARM 弱序问题
  • 一致性模型 = 顺序一致性 (SC)

代价：
  • 时钟频率被最长路径限制（~1 GHz 而非 5 GHz）
  • 工艺波动会限制良率（一个慢点全部要降频）
  • 物理上无法做大（光速延迟开始成为问题）
```

**对 Luke 的启示**：WSE 的设计哲学是**用硬件一致性换软件简洁性**。但代价是放弃频率、放弃工艺弹性、放弃规模化。

### 2. 弱一致性在 NPU 上的应用

NPU 通常做 **dataflow / systolic computation**——大量 PE 沿数据流推进，不需要全局共享变量。

```
典型 NPU 工作流：
  input → PE[0] → PE[1] → PE[2] → ... → PE[63] → output
                                          ↑
                              不需要 coherence
                              不需要 consistency
                              只需要 data 按时到达
```

**但 NPU 也有需要同步的地方**：
- **Reduction**：64 个 PE 的 partial sum 加起来 → 需要 barrier + reduce
- **Control plane**：所有 PE 同步等待 dispatch 指令 → 需要 barrier
- **Statistics**：每个 PE 写自己的 cycle count → 不需要原子

**Luke 的研究机会**：**为 NPU 设计专用的轻量级同步原语**——既不像通用 coherence 那么重，也不像纯消息传递那么慢。理想方案：
- Hardware Barrier（专用信号线）
- Mesh-aware Reduce（拓扑感知的 reduce 算法）
- Fetch-and-Add Counter（专用原子单元）

### 3. MCS Lock vs WSE Fabric 的拓扑对比

```
MCS Lock 在 cache-coherent 多核：
  • 自旋本地变量（cache line 在 L1）
  • 等待者分布在全核 → L1 hit 高
  • 但 cache line 跨核传递有 snoop 开销
  • 适合：16-64 核、cache-coherent、x86

WSE 的同步原语：
  • 自旋本地 SRAM 地址（48KB per PE）
  • 信号通过 mesh 传递，无 cache coherence
  • 每个 PE 自旋纯本地，无跨 PE 同步压力
  • 适合：100K+ PE、no-coherence、dataflow
```

**结论**：你的"核内同步"研究如果是针对 **small-scale NPU（< 64 PE 数组）**，借鉴 MCS Lock；如果是针对 **wafer-scale array**，需要完全不同的硬件原语。

### 4. 一个具体的 NPU 同步原语设计建议

针对你研究的 NPU 核（假设每核 = 4×4 SLA 阵列，多核之间用 mesh）：

```c
// 假设的 NPU 原子指令集扩展
npu_atomic_barrier(mask_t pe_mask);     // 等待指定 PE 集合都到达
npu_atomic_reduce_sum(addr, value);     // mesh-aware tree reduce
npu_atomic_fetch_add(counter_addr, 1);  // 专用硬件计数器
npu_fence_row();                        // 阻止同一行 PE 之间的重排
npu_fence_mesh();                       // 全局 fence（最重）
```

**设计要点**：
- **npu_atomic_barrier** 利用 mesh 的 row/column 总线，O(sqrt(N)) 而非 O(N) 时间
- **npu_atomic_reduce_sum** 用蝶形网络拓扑，log2(N) 步
- **npu_atomic_fetch_add** 用专用硬件单元，不占用 cache line

**这正是 Luke 的研究机会**——把通用同步原语**重新设计**成 NPU 友好的版本。

---

## 🔗 明日预告

**Day 20：存储系统 + I/O**
- 磁盘/SSD 物理原理（Flash cell、FTL、磨损均衡）
- RAID 0/1/5/6 性能对比
- NVMe 协议栈与延迟分解
- I/O 路径全栈分析（用户态 → 内核 → 驱动 → PCIe → SSD）

**承上启下**：今天学了"内存级别"的同步和一致性，明天进入"存储级别"的 I/O 系统——AI 训练数据加载会成为 Day 27 分布式训练的基础。

---

## 💡 今日感悟位

> *一致性模型的本质是什么？是"硬件和软件之间的契约"——硬件说我会乱排某些访存，软件说我会用 fence 保证关键顺序。x86 TSO 的契约对程序员友好（少写 fence），ARM/RV 的契约对性能友好（少 stall）。Luke 的 NPU 研究要选哪个？答案是：**根据 NPU 工作负载特性自创一份契约**——把"什么需要顺序、什么可以重排"从 ISA 层面讲清楚。这比"通用 CPU 的弱序 + fence"高一个抽象层次。*

---

*Day 19 / 30. 第三阶段（存储篇）第三天。今天你掌握了"内存一致性"这把瑞士军刀——SC/TSO/ARM 三种模型、Memory Fence、原子原语、锁实现。下一步是把视野扩展到外存 I/O，看清楚 AI 训练系统的完整数据路径。*