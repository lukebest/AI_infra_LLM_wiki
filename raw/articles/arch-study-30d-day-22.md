---
type: Raw Source
title: 📰 体系结构晨报 — Day 22
source_path: /home/luke/openclawdata/workspace-research/notes/projects/arch-study-30d/day-22.md
textbook: "Computer Architecture: A Quantitative Approach (6th ed.) — Storage Phase Summary (Day 17-21)"
ingested: 2026-07-06
---

# 📰 体系结构晨报 — Day 22

📅 2026-07-05（Day 22 / 30，星期日）
🎯 阶段：存储篇（Day 17-22）— **阶段总结日**
📖 教材：复习 Day 17-21 全部笔记 + 自补充综合材料

---

## 今日主题：存储系统全景 + 端到端延迟实战

### 🧭 为什么今天学这个？

过去 5 天我们把"存储 + 互连"分开学习：

| Day | 主题 | 解决的问题 |
|-----|------|-----------|
| 17 | DRAM + 内存墙 | "数据从哪里取？" |
| 18 | Cache 一致性 | "多核看到的数据是否一致？" |
| 19 | 同步 / Memory Ordering | "多核如何协作？" |
| 20 | SSD / NVMe / RAID | "冷数据在哪里？" |
| 21 | 互连网络 / NoC | "节点之间如何通信？" |

**但真实系统不是分章节的**——一条 load 指令要穿越：

```
CPU Core → L1 → L2 → LLC → NoC → Memory Controller → DRAM
   ↑                                                      |
   └────────── I/O / SSD ◄── DMA ◄── (写回时) ────────────┘
                    ↓
           NoC → 另一个 Core (for coherence / atomic)
```

今天的任务：**把 5 天的零件拼成一张图，并用具体数字量化"一条 load 的代价"。**

### 🎯 今天的目标（与研究连接）

你的研究方向横跨 **WSE / NoC / NPU / 同步**。第三阶段的知识是它们的共同底座。今天的端到端实战，会帮你建立一个"在心里跑模拟器"的能力——以后看到任何新架构，都能快速估算 latency / bandwidth / 瓶颈。

---

## 📖 阅读任务（约 60-90 分钟）

### 必修：复习 Day 17-21 笔记
按顺序读 `day-17.md` → `day-21.md`，每篇 15 分钟，重点看：
- **公式**（AMAT、tRCD+CL、双分带宽、t₀）
- **WSE 关联段落**（每篇都有）
- **练习题答案**（巩固理解）

### 推荐补充（30 min）：
1. **量化方法 Ch.2 小结** — 重新过一遍 memory 章节的总结图
2. **Cerebras WSE-3 白皮书** — "Memory Fabric" / "Mesh Fabric" 章节，对比传统 memory hierarchy
3. **论文精读推荐**（选 1 篇）：
   - **Balfour & Dally 2006 "Design Tradeoffs for Tiled CMP"** — 把 on-chip mesh 和传统总线做量化对比的经典论文
   - **Dally & Towles 2004 "Principles and Practices of Interconnection Networks"** Ch.1 — 互连网络的"为什么"
   - **Luczynski et al. 2024 "Near-Optimal Wafer-Scale Reduce"** — 把 WSE mesh 上的 reduce 算法和传统 NoC 对比

---

## 🔑 核心概念回顾（速查 — 不是新知识）

### 1. 端到端内存访问时间（AMAT 的层级展开）

```
AMAT = Hit_Time_L1 + MR_L1 × (Hit_Time_L2 + MR_L2 × (Hit_Time_LLC + MR_LLC × MissPenalty_DRAM))
```

**两层嵌套**的含义：
- 一旦 L1 miss，就付 L2 的访问代价（可能命中，可能继续 miss）
- 一旦 L2 miss，就付 LLC 的访问代价
- 一旦 LLC miss，就付 DRAM 的访问代价（包含 NoC + 控制器 + tRCD + tCAS + 传输）

**关键陷阱**：不要用 AMAT 算 AMAT 的"几何展开"——必须用条件概率一层层套。

### 2. 内存墙（Memory Wall）的量化

Wulf & McKee 1995 提出的"每 1.5 年内存访问时间仅下降 5%"，而 CPU 频率每年增长 40%。结果是：

```
Memory_Wall_Gap = (CPU_Clock) / (Memory_Access)   — 单调增长
```

**解药**（按时间顺序）：
1. Cache 层次（L1/L2/L3，1985-2000）
2. 大页（Huge Pages，减少 TLB miss）
3. 内存压缩 / 预取（Prefetching）
4. HBM / 3D-stacked DRAM（2014-，带宽解药而非延迟解药）
5. **存内计算 / 近数据计算**（PIM，2019-，彻底重构数据移动方向）
6. **WSE 式方案**（2020-，消除 off-chip 访问，把所有数据放在 on-chip SRAM）

### 3. 一致性协议的存在感判断（决策树）

```
是否需要 MESI / 目录协议？
├── 共享内存？ ← 否则不需要
│   ├── 多核共享地址空间？
│   │   ├── 共享数据？ ← 否则不需要
│   │   │   └── 多核同时读写？ ← 否则 read-only 也不需要
│   │   │       → 需要 MESI / 目录
```

**WSE**：每 PE 有独立 SRAM + 私有地址空间 + 通过 NoC 显式传递消息 → **整个决策树的"否则"分支** → 一致性协议完全不需要。

### 4. NoC 在存储路径中的位置

传统 CPU 的 load 指令可能走两条路：

```
路 A（同 die 内）：LLC → Memory Controller (本地) → DRAM → 回 LLC → Core
路 B（跨 die 共享）：LLC ↔ NoC ↔ 远端 LLC（一致性协议介入）→ 远端 Core
```

**WSE**：只有路 A（且路径都是 on-chip SRAM），但 NoC 必须超快（21 PB/s 总带宽）。

### 5. 同步原语的成本（按数量级排序）

```
Memory Fence:    ~50-200 ns   （x86 MFENCE，跨核）
Atomic CAS:      ~20-100 ns   （L1 命中时；NUMA 下可能 ~500 ns）
Lock acquire:    ~50-500 ns   （无竞争 vs 强竞争）
Barrier:         ~1-10 μs     （取决于核数）
分布式 Lock:     ~10-100 μs   （跨机器）
WSE 同步:        ~1-10 ns     （单时钟域 + 短链路，硬件 barrier 指令）
```

**规律**：跨域越远、竞争越激烈，成本越高。WSE 的"同步优势"来源于单一时钟域 + on-chip 距离。

---

## 🧪 实战练习（必做 — 重点题目）

### 练习 1：端到端 AMAT 计算（基础题，10 min）

给定参数（来自教科书典型值）：

| 级别 | Hit Time | Miss Rate (单独) |
|------|----------|----------------|
| L1 | 1 cycle | 5% |
| L2 | 10 cycles | 3%（在 L1 miss 条件下） |
| L3 (LLC) | 40 cycles | 30%（在 L2 miss 条件下） |
| DRAM | 200 cycles | — |

**任务**：
1. 计算平均内存访问时间 AMAT（单位：cycles）
2. 如果主频 3 GHz，把 AMAT 换算成 ns
3. 解析：哪一级对 AMAT 的贡献最大？占比多少？

**答案**：

```
AMAT = L1_HitTime + MR_L1 × (L2_HitTime + MR_L2 × (LLC_HitTime + MR_LLC × DRAM_Penalty))

代入：
AMAT = 1 + 0.05 × (10 + 0.03 × (40 + 0.30 × 200))
     = 1 + 0.05 × (10 + 0.03 × (40 + 60))
     = 1 + 0.05 × (10 + 0.03 × 100)
     = 1 + 0.05 × (10 + 3)
     = 1 + 0.05 × 13
     = 1 + 0.65
     = 1.65 cycles

主频 3 GHz → AMAT = 1.65 / 3 = 0.55 ns
```

**贡献分解**：

```
L1 Hit 的贡献（永远付）：1.0 cycle      (60.6%)
L1 Miss → L2 Hit：0.05 × 10 = 0.5 cycle (30.3%)
L1 Miss → L2 Miss → LLC Hit：0.05 × 0.03 × 40 = 0.06 cycle (3.6%)
L1 Miss → L2 Miss → LLC Miss → DRAM：0.05 × 0.03 × 0.30 × 200 = 0.09 cycle (5.5%)

合计 = 1.65 cycles ✓
```

**关键观察**：
- **L1 命中本身（60.6%）是 AMAT 的主导** → 优化 L1 hit rate 的回报最大
- **DRAM 访问虽然慢，但占比仅 5.5%** → 因为 LLC 截掉了 70% 的请求
- 如果把 LLC miss rate 翻倍到 60%，AMAT 变为 1.85 cycles（+12%）

### 练习 2：AMAT 敏感性分析（进阶，15 min）

基于练习 1 的系统，分别分析以下优化对 AMAT 的影响：

1. **优化 A**：L2 miss rate 从 30% 降到 15%
2. **优化 B**：L1 hit time 从 1 cycle 降到 0.5 cycle（流水线加深）
3. **优化 C**：DRAM 延迟从 200 cycle 降到 100 cycle（用 HBM 替代 DDR）

哪个优化收益最大？

**答案**：

```
基线 AMAT = 1.65 cycles

优化 A（L2 MR: 0.30 → 0.15）：
  AMAT_A = 1 + 0.05 × (10 + 0.03 × (40 + 0.15 × 200))
         = 1 + 0.05 × (10 + 0.03 × 70)
         = 1 + 0.05 × (10 + 2.1)
         = 1 + 0.05 × 12.1
         = 1.605 cycles
  收益 = 1.65 - 1.605 = 0.045 cycles (-2.7%)

优化 B（L1 HT: 1 → 0.5）：
  AMAT_B = 0.5 + 0.05 × (10 + 0.03 × (40 + 0.30 × 200))
         = 0.5 + 0.05 × (10 + 0.03 × 100)
         = 0.5 + 0.05 × 13
         = 0.5 + 0.65
         = 1.15 cycles
  收益 = 1.65 - 1.15 = 0.5 cycles (-30.3%)  ★ 最大

优化 C（DRAM: 200 → 100）：
  AMAT_C = 1 + 0.05 × (10 + 0.03 × (40 + 0.30 × 100))
         = 1 + 0.05 × (10 + 0.03 × 70)
         = 1 + 0.05 × (10 + 2.1)
         = 1.605 cycles
  收益 = 1.65 - 1.605 = 0.045 cycles (-2.7%)
```

**结论**：优化 B（降低 L1 命中时间）收益最大，因为 **L1 每次访问都付 hit time**。优化 A 和 C 看似"更深"，但因 MR 小，乘下来贡献有限。

**关键洞察（与 WSE 研究关联）**：
- 这就是为什么超标量核要把 L1 做得极小（32 KB）但极快（1-2 cycle）—— hit rate 不靠大，靠预测 + prefetch
- HBM 替代 DDR 的营销常强调"带宽翻倍"，但**延迟减半的 AMAT 收益其实很小**（除非 LLC miss rate 已经很高）

### 练习 3：WSE vs 传统 CPU 的延迟对比（研究关联，20 min）

**场景**：训练一个 LLM，每一步需要访问 100 GB 权重矩阵。

| 架构 | 数据位置 | 单次访问延迟 | 带宽 |
|------|---------|------------|------|
| 传统 H100 + HBM3 | HBM（片外） | ~400 ns | 3 TB/s |
| Cerebras WSE-3 | on-chip SRAM | ~10 ns（估算） | 21 PB/s |

**任务**：
1. 假设 100 GB 权重需要访问 N 次才能完成一次 forward+backward，N=10。计算两种架构的总访问时间。
2. 如果用 Mesh 上的平均跳数（50 跳）反推单跳延迟，WSE 总延迟应该是多少？

**答案**：

```
总访问数据量 = 100 GB × 10 = 1 TB

传统 H100:
  1 TB / 3 TB/s = 0.33 s = 333 ms
  （纯数据传输；实际还要算上 kernel 启动 + 控制开销，可能 1-2 s）

WSE-3 (片上 SRAM):
  1 TB / 21 PB/s = 47.6 μs
  （纯数据传输；包括 NoC 通信）

加速比 = 333 ms / 47.6 μs ≈ 7000×  (单算数据传输)

反推 WSE 单跳延迟：
  假设 100 GB 权重被铺到 ~1M PE 上，每 PE 平均需跳 50 跳到目标位置
  t₀ = t_r × D + P/B
  取 P = 4 KB（一次传输 4096 个 FP16），B = 11.5 GB/s/port
  t_r = 1 ns（单时钟域，1 GHz 等效）
  
  t₀ = 1 ns × 50 + 4096 / (11.5×10⁹) 
     = 50 ns + 0.36 ns 
     ≈ 50 ns ✓
```

**注意**：以上是粗略估算，真实场景更复杂（数据布局、PE 利用率、通信 vs 计算 overlap 等）。但量级对了——WSE 的内存墙不是"缓解"，是"消除"。

### 练习 4：知识地图自检（概念题，10 min）

在不看笔记的情况下，尝试写出"端到端数据路径"的完整流程：

```
应用层:  user program (matrix multiply)
            ↓
编译器:  instruction stream (RISC-V / x86 / WSE assembly)
            ↓
处理器:  IF → ID → EX (ALU / FPU / LSU) → MEM → WB
            ↓  (LSU)
L1 Cache:  32 KB, 4-way, 1 cycle
            ↓ (miss)
L2 Cache:  256 KB-1 MB, 8-way, 10 cycles
            ↓ (miss)
LLC:       8-32 MB, 16-way, 40 cycles
            ↓ (miss)
NoC:       cross-bar or ring or mesh, 10-50 ns
            ↓
Memory Controller:  DDR / HBM / GDDR, command scheduler
            ↓
DRAM:      tRCD + tCAS + burst, ~100 ns total
            ↓ (写回时)
SSD / NVMe:  10-100 μs (冷数据)
```

**你的任务**：
1. 在每个环节标上**典型延迟**（含单位）
2. 标出**这条路径上 WSE 的简化**（哪些环节被去掉了？哪些被合并了？）
3. 把这张图复制到 `formulas.md` 的末尾作为"全景参考"

**思考**：
- WSE 把 L1/L2/L3/DRAM 都替换成 on-chip SRAM —— **没有"miss"概念**
- 没有 NoC 跨 die 的"长距离"问题 —— 所有通信都在片内
- 没有 SSD 的冷热数据问题 —— 数据完全驻留在 SRAM 中（但容量受限）

### 练习 5（选做，开放题）：WSE 容量瓶颈分析

**问题**：WSE-3 有 900K PE × 48 KB SRAM ≈ 43 GB on-chip SRAM。这听起来很大，但单个 LLM 训练权重就超过这个量级。如何解决？

**提示**：
- 权重流式加载（streaming）
- 模型并行（每个 PE 只放部分权重）
- 权重 offload 到外部 DRAM / SSD，通过 NoC 的边缘节点访问
- Cerebras MemoryX 系统的设计

**建议作业**：用 1-2 句话写出你的看法，和传统 GPU + HBM + NVMe 方案对比优劣。

---

## 🔗 与 WSE/NoC 研究的关联

### 1. WSE 是"消除存储墙"的极端尝试

```
传统 CPU 存储路径 (约 100+ ns 到 DRAM):
  Core → L1 → L2 → LLC → NoC → MC → DRAM

WSE 存储路径 (约 10 ns):
  Core → on-chip SRAM (NoC 把数据送过来，本地访问)
```

**这是 Day 17 学到的"内存墙"的彻底重构方案**——不是让数据移动得更快，而是**让所有数据已经在 on-chip**。

### 2. 一致性协议的"存在感决策树"用在 WSE 上

```
WSE:
  - 是否共享内存？ → 否（消息传递）
  - 是否需要 MESI？ → 否（每 PE 私有 SRAM）
  - 是否有 cache coherence？ → 否
  - 是否有同步原语？ → 是，但实现极简（单时钟域 + 短消息）
```

**架构简化 = 功耗降低 + 频率提升 + 面积留给 PE**。这是 WSE 900K PE 的根本原因之一。

### 3. NoC 在存储路径中的角色：从"瓶颈"到"加速器"

传统 NoC 是 L3 ↔ Memory Controller 之间的瓶颈（cross-bar、ring bus 都有限）。
WSE 的 2D Mesh 是 **数据搬运的并行通道**——21 PB/s 的总带宽相当于 7000 张 H100 同时工作的内存带宽。

**对你的 NoC 研究的启示**：
- 不只是设计"NoC"，而是设计"内存系统的骨架"
- NoC 的延迟、带宽、拓扑直接影响所有存储层的性能
- 未来 NoC 设计的核心问题：**如何让 on-chip SRAM 的高带宽被有效利用**

### 4. 同步原语的硬件实现

你的"核内同步"研究方向 = 设计**单时钟域内 + on-chip 距离**的高效同步原语。

```
传统多核同步:  ~μs 量级（跨 socket、跨 NUMA）
WSE 同步:      ~ns 量级（单时钟域 + NoC 短消息）

挑战：
  - 同步延迟如何进一步降低？
  - 同步原子性如何保证（NoC 中消息丢失？乱序？）
  - 同步原语如何与编程模型（CSL / SpaDA）配合？
```

---

## 📊 阶段总结：第三阶段（Day 17-22）知识地图

```
                冷数据                              热数据
                  │                                   │
                  ▼                                   ▼
              SSD/NVMe ──── DMA ──── DRAM ──── Cache ──── Core
              (10-100μs)    (1μs)   (100ns)   (1-40c)    (1c)
                                            │
                                            │ NoC
                                            ▼
                                        远端 Core/LLC
                                        (跨 die: 50-100ns)
```

```
WSE 的简化版（去掉所有 off-chip）:

              on-chip SRAM (distributed, 43 GB total)
                       │
                       │ 2D Mesh NoC (~50ns, 21 PB/s)
                       ▼
                   SLA Core (~900K PE)
                   
  全部在 ~50 ns 内完成，无 off-chip 访问
```

---

## 🔗 明日预告

**Day 23：多核架构 + 多线程（SMT）**
- 进入**第四阶段（并行篇 Day 23-27）**
- 多核 vs 多线程：为什么 SMT 仍是标配？
- Amdahl 定律在多核扩展性上的极限
- NUCA（非均匀缓存访问）—— 多核下的存储层次新挑战
- 与 WSE 的对比：WSE 算"超多核 + 单线程"还是"超多核 + 多线程"？

**承上启下**：今天把第三阶段的存储 + 互连拼成完整图景。明天开始学**如何在多核上调度任务**——Amdahl 定律会再次出现，但这次是在"多核扩展性"语境下。同时 NUCA 会告诉我们：**即使有 Cache，访问延迟也不是均匀的**——这是 WSE 的"分布式 SRAM 也是 NUMA"问题的预演。

---

## 💡 今日感悟位

> *第三阶段结束。从 DRAM 到 SSD，从 MESI 到 MCS Lock，从 Ring 到 Mesh——所有这些"传统架构的复杂性"，在 WSE 上要么被消除、要么被简化。这不是偶然，而是**架构哲学的体现**：Cerebras 选择了一条"把所有资源都给计算"的极简路线，把所有复杂的一致性、缓存、同步问题交给软件 (SME) 显式管理。明天开始学多核时，要带着这个视角问：**多核的复杂度哪些是必要的？哪些是历史包袱？如果让你从零设计，你会保留哪些？***

---

*Day 22 / 30. 第三阶段（存储篇）结束。今天你把 5 天的零件拼成了一张图：一条 load 指令的全路径 + AMAT 的端到端计算 + WSE 的简化哲学。明天进入第四阶段（并行篇），从多核 SMT 开始——会回到 Amdahl 定律，但这次是在"多核扩展性"语境下。*