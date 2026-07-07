---
type: Raw Source
title: 📰 体系结构晨报 — Day 24
source_path: /home/luke/openclawdata/workspace-research/notes/projects/arch-study-30d/day-24.md
textbook: "Computer Architecture: A Quantitative Approach (6th ed.) — Ch.4.1-4.5 Data-Level Parallelism (GPU/SIMT)"
ingested: 2026-07-07
---

# 📰 体系结构晨报 — Day 24

📅 2026-07-07（Day 24 / 30，星期二）
🎯 阶段：并行篇（Day 23-27）
📖 教材：《计算机体系结构：量化方法》第6版 Ch.4 (4.1-4.5 — 数据级并行)

---

## 今日主题：GPU 架构 — SIMT、Warp、Tensor Core

### 🧭 为什么今天学这个？

**昨天我们学了"多核复用硬件资源"（SMT + 多核）。今天学一个看似相反、实则互补的范式：把 N 个轻量级核绑在一起"步调一致地做同一件事"。**

回顾并行计算的 Flynn 分类（复习）：

```
SISD — 单指令单数据      (传统 CPU 单核)
SIMD — 单指令多数据      (向量指令、GPU)
MISD — 多指令单数据      (罕见，容错系统)
MIMD — 多指令多数据      (多核 CPU, WSE)
```

**今天主题 GPU = SIMD + 多线程 = SIMT（Single Instruction, Multiple Threads）**——这是现代 GPU 的核心抽象。

**对你研究方向的连接**：

| 你的方向 | 与今天的关联 |
|---------|-------------|
| **NPU 核设计** | NPU 的 MAC 阵列就是"硬连线 SIMD"——今天讲 SIMT，你能看到软件版和硬件版的异同 |
| **WSE 架构** | WSE 是 MIMD 极致（900K 独立 PE），GPU 是 SIMD 极致（数千线程锁步执行）——**两种相反的并行哲学** |
| **超标量 CPU 核** | CPU 的 ILP 是在小窗口内找并行（深度学习驱动），GPU 的 TLP 是在大窗口内显式并行（程序员显式标注） |
| **核内同步** | GPU 的 Warp/SM 同步是"硬件 barrier"的工业实例——比你的研究目标小一个量级，但原理相通 |

### 🎯 今天的目标（与研究连接）

1. 掌握 SIMT 执行模型——**为什么 GPU 不用更深的流水线，而是用"更宽"的 SIMD？**
2. 理解 Warp Divergence 的影响——**这是 GPU 编程的"暗坑"**
3. 量化 GPU 内存层次——**Shared Memory / Global Memory / L1/L2 的延迟差异**
4. 理解 Tensor Core 的设计哲学——**专用矩阵硬件的极致**
5. 建立"GPU vs WSE"的对比框架——**SIMD + 锁步 vs MIMD + 消息传递**

---

## 📖 阅读任务（约 60-90 分钟）

**《计算机体系结构：量化方法》第6版 第 4 章 4.1-4.5 节：Data-Level Parallelism in Vector, SIMD, and GPU Architectures**

### 核心阅读（60 min）：
1. **4.1 Introduction** — DLP 的动机、向量 vs SIMD vs GPU
2. **4.2 Vector Architecture** — 向量处理器的历史（VMIPS 例子）
3. **4.3 SIMD Instruction Set Extensions for Multimedia** — 标量 ISA 上的 SIMD 扩展（SSE, AVX, NEON）
4. **4.4 Graphics Processing Units (GPUs)** — GPU 架构总览：host + device + kernel
5. **4.5 GPU Memory Hierarchy** — GPU 的存储层次（这是今天最关键的章节）

### 推荐补充（30 min）：
1. **NVIDIA Volta Whitepaper** — Volta 架构的 SM、Warp、Tensor Core 设计
2. **NVIDIA Hopper Whitepaper** — 最新一代，理解 GPU 架构的演进（Thread Block Cluster, Distributed Shared Memory）
3. **论文推荐**：Lindholm et al. 2008 "NVIDIA Tesla: A Unified Graphics and Computing Architecture"

---

## 🔑 核心概念（带公式）

### 1. SIMT 执行模型（关键概念！）

```
CPU 视角（SIMD）：
  程序员/编译器写向量指令
  vadd v0, v1, v2   ← 单条指令，操作 16 个 32-bit 数据
  硬件自动并行

GPU 视角（SIMT）：
  程序员写标量 kernel
  每个 thread 处理一个数据元素
  硬件把 N 个 thread 打包成 Warp（典型 32 threads）
  Warp 内所有 thread 锁步执行同一条指令
```

**关键洞察**：
- SIMD 是"指令级"并行（ISA 暴露），SIMT 是"线程级"并行（ISA 隐藏）
- 程序员写 SIMT 感觉是 MIMD（每个 thread 独立分支），但硬件执行是 SIMD（锁步）
- **这是 GPU 能让"标量程序员"自动获得 SIMD 性能的秘密**

### 2. GPU 硬件结构（NVIDIA 术语）

```
┌─────────────── GPU ───────────────┐
│  ┌─── SM (Streaming Multiprocessor) ───┐
│  │  ┌─── Warp Scheduler ──┐            │
│  │  │                     │            │
│  │  ├─ Warp 0 (32 threads)             │
│  │  ├─ Warp 1 (32 threads)             │
│  │  ├─ Warp 2 (32 threads)             │
│  │  ├─ Warp 3 (32 threads)             │
│  │  ...                                │
│  │  ├─ Warp N-1 (32 threads)           │
│  │                                     │
│  │  ┌─ Dispatch Unit ─┐                │
│  │  │ 32-wide SIMD     │                │
│  │  │ Functional Units │ (INT/FP/Tensor)│
│  │  └──────────────────┘                │
│  │                                     │
│  │  Registers: 256KB (64K × 32-bit)    │
│  │  Shared Memory: 128 KB              │
│  │  L1 Cache: ~128 KB                  │
│  └─────────────────────────────────────┘
│  ...  (数十个 SM 组成整个 GPU)        │
│                                       │
│  L2 Cache: ~6 MB (跨 SM 共享)         │
│  HBM: 80 GB (e.g. H100)               │
└───────────────────────────────────────┘

典型规模 (H100):
  132 SMs
  64 warps/SM × 32 threads = 2048 threads/SM
  132 × 2048 = 270,336 threads 总数
```

### 3. SIMT 性能公式

```
理想情况 (无 divergence):
  Speedup_SIMT = N_lanes
  一次 Warp 指令完成 32 个 thread 的工作

有 divergence 的情况:
  Speedup = N_lanes / (Σ_path_length)
  例：if-else 分支，Warp 内 50% 走 then、50% 走 else
  → 实际执行时间 = 1 (then) + 1 (else) = 2 cycles
  → 有效 Speedup = 32/2 = 16× (而非 32×)
```

**Warp 调度隐藏延迟**：
```
零延迟内存访问时间 = L
Warp 数 / SM = W
总吞吐量 = W × N_lanes / L   (cycles 内的总 work)

W 越大，零延迟访问越长的内存也能被"藏起来"。
NVIDIA 通常要求 W ≥ 4 才能达到接近峰值的利用率。
```

### 4. Warp Divergence（性能杀手！）

```
代码:
  if (thread_id < 16) {
      a = b + c;      // 路径 A
  } else {
      a = b * c;      // 路径 B
  }

硬件执行 (Warp = 32 threads):
  Cycle 1:  路径 A 活跃 (16 threads)，路径 B 闲置 (16 threads)
  Cycle 2:  路径 B 活跃 (16 threads)，路径 A 闲置 (16 threads)
  
  总时间 = 2 cycles
  有效利用率 = 50%
  损失 = 16 threads × 1 cycle 的"空转"
```

**Warp Divergence 的来源**：
- 条件分支（if-else, switch）
- 循环边界（如 `for (i = tid; i < N; i += blockDim)` 最后一个 block）
- 间接寻址（数据相关指针）

**Warp Divergence 的代价**：
```
每个分支路径都要"独立执行"
  时间代价：路径数倍
  寄存器代价：每条路径都需要保存所有 lanes 的活跃寄存器
```

### 5. GPU 内存层次（关键！）

| 层次 | 容量 (H100) | 带宽 / 延迟 | 作用域 |
|------|------------|------------|--------|
| **Register** | 256 KB/SM | ~0 cycles | 单 thread |
| **Shared Memory** | 128 KB/SM | ~20 cycles, ~10 TB/s/SM | Block 内所有 thread |
| **L1 Cache** | 128 KB/SM (与 SM 共用) | ~30 cycles | SM 内 |
| **L2 Cache** | 50 MB (全 GPU) | ~200 cycles, ~5 TB/s | 所有 SM |
| **HBM** | 80 GB | ~500 cycles, 3 TB/s | 所有 SM |

**关键比例**：
- Register vs HBM：**延迟差 ~500×，带宽差 ~1000×**
- 这是为什么 GPU 编程要"小心内存"——一次 HBM 访问能执行 500 条 FP32 指令
- **Roofline 拐点 (Ridge Point)** 决定了是 compute-bound 还是 memory-bound

**带宽密度对比**：

| 系统 | 总带宽 | 带宽密度 |
|------|-------|---------|
| H100 HBM | 3 TB/s | 0.05 TB/s/cm² |
| WSE-3 SRAM | 21 PB/s | 100+ TB/s/cm² |
| Cerebras MemoryX (DRAM) | 20 PB/s (峰值) | 外部 |
| LPDDR5 (Apple M2) | 100 GB/s | 0.01 TB/s/cm² |

**WSE 比 H100 片上带宽高 7000×**——这是数据流架构的根本优势。

### 6. Tensor Core（专用矩阵硬件）

```
传统 CUDA Core:    一个 cycle 一次 FMA (a*b+c)
Tensor Core:       一个 cycle 一次 4×4 矩阵 FMA (16 次 FMA)

例：Hopper FP16 Tensor Core
  - 1024 次 FMA / cycle / SM
  - 132 SMs × 1024 = 135,168 FMA/cycle
  - @ 1.7 GHz = 459 TFLOPS (FP16)
  - vs FP32 CUDA Core: ~50 TFLOPS
  - 加速比 ~9×
```

**Tensor Core 数据流**：

```
输入：4×4 矩阵 A 和 B (FP16)
累加：4×4 矩阵 C (FP32)
计算：D = A × B + C  (16×16=256 个 FMA)

一个 Tensor Core 指令 = 1 个周期完成
传统方式需要 256 个 FMA 指令 = 256 个周期
```

**对你的 NPU 研究的启示**：
- Tensor Core = "硬连线 SIMD" 的极致
- NPU 核的 MAC 阵列（Day 25 会学）= 类似的思路：把数据流固化在硬件上
- 区别：Tensor Core 处理小矩阵（4×4, 8×8），NPU 处理大矩阵（128×128, 256×256）
- 共同设计哲学：**用空间换时间，用专用换灵活**

### 7. GPU vs CPU 设计哲学对比

| 维度 | CPU | GPU |
|------|-----|-----|
| **核心数** | 4-128 (重) | 数千到数十万 (轻) |
| **单核性能** | 高 (乱序 + 分支预测 + Cache) | 低 (在序 + SIMD) |
| **线程数** | 1-2 (SMT) | 数十万 (轻量 thread) |
| **上下文切换** | 昂贵 (μs) | 廉价 (1 cycle) |
| **分支优化** | 分支预测 (硬件) | 避免 divergence (软件) |
| **内存模型** | 复杂 (Cache 一致性) | 简单 (弱一致) |
| **适用场景** | 控制流密集 | 数据并行 |
| **编程模型** | 低级 (C/asm) | kernel + grid/block |

**黄金法则**：
- **Latency-bound 工作**：用 CPU（大 cache + 乱序）
- **Throughput-bound 工作**：用 GPU（高并行 + 高带宽）
- **Mix**：用 APU/Heterogeneous（如 Apple Silicon, Intel CPU + GPU）

---

## 🧪 练习题（约 60 分钟）

### 基础题

**Q1：SIMT 加速比计算**

某 GPU 拥有 32-wide Warp。运行一段 100 条 SIMT 指令的程序：
- 90 条无 divergence
- 10 条有 4-way divergence（每条指令走 4 条不同路径，每路径平均 16 threads 活跃）

求：(a) 理想加速比；(b) 实际加速比。

> **答**：
> 理想：100 × 32 = 3200 thread-cycles
> 实际：
>   无 divergence: 90 × 32 = 2880
>   有 divergence: 10 × (4 × 32) = 1280 (每条 4 倍时间)
>   实际总 = 2880 + 1280 = 4160 thread-cycles
> 实际加速比 = 3200 / 4160 ≈ 0.77×
> **结论**：divergence 让 GPU 反而比 CPU 慢！这是 GPU 编程最大的坑。

**Q2：Warp 调度延迟隐藏**

某 GPU 每个 SM 有 64 个 Warp，内存访问延迟 400 cycles。问：
- 零开销执行时，每个 Warp 至少需要多少 cycle 来隐藏延迟？
- 如果实际应用只有 32 个 Warp/SM，吞吐损失多少？

> **答**：
> 完全隐藏延迟 = 内存延迟 / Warp 数 ≥ 1
>   400 / 64 ≈ 6.25 cycles/Warp （每个 Warp 平均只有 6 cycles 时间片）
> 实际：400 / 32 = 12.5 cycles/Warp
> 吞吐损失：cycle 利用率 = 12.5 / 400 = 3.1%（虽然很低但不是 0）
> **结论**：Occupancy（每 SM 的 Warp 数）直接影响 GPU 性能。

### 进阶题

**Q3：Roofline 模型 + Tensor Core**

H100 规格（简化）：
- FP32 peak: 50 TFLOPS
- FP16 Tensor Core peak: 450 TFLOPS
- HBM 带宽: 3 TB/s
- L2 带宽: 5 TB/s

某 GEMM kernel 实际达到：
- FP32: 35 TFLOPS
- FP16+Tensor Core: 380 TFLOPS
- 算术强度 (AI): 100 FLOPs/Byte (FP32), 200 FLOPs/Byte (FP16+TC)

判断每种情况是 compute-bound 还是 memory-bound。

> **答**：
> Roofline 拐点 (Ridge Point)：
>   FP32: 50 / 3 = 16.7 FLOPs/Byte (HBM-bound 上限)
>         50 / 5 = 10 FLOPs/Byte (L2-bound 上限)
>   FP16+TC: 450 / 3 = 150 FLOPs/Byte
>
> FP32 (AI=100):
>   Ridge point = 16.7 (HBM), 我们 AI=100 > 16.7 → Compute-bound
>   实测 35/50 = 70% peak (合理)
>
> FP16+TC (AI=200):
>   Ridge point = 150, 我们 AI=200 > 150 → Compute-bound
>   实测 380/450 = 84% peak (优秀)
>
> **结论**：两种都是 compute-bound，TC 的更高 AI 让它更接近峰值。
> **对你的 NPU 研究**：低精度 + 高 AI = 性能优势。

### 思考题（与 WSE 研究关联）

**Q4：GPU vs WSE 的根本差异**

GPU（H100）有 ~270K 线程（轻量、SIMT 锁步）。
WSE-3 有 ~900K PE（独立、MIMD 异步）。

为什么 WSE 的 PE 数可以比 GPU 的线程数多 3×？是工艺优势还是架构优势？

从以下角度分析：
1. 每"线程"占用的硬件资源（寄存器、调度器）
2. 时钟频率
3. 通信模型（共享 vs 消息传递）
4. 编程模型对硬件可见性的影响

> **答（提示方向）**：
> 1. **硬件资源占用**：
>    - GPU 线程：~256 bytes (寄存器) + 调度器 (Warp Scheduler) 共享
>    - WSE PE：~50KB SRAM + 独立调度器（Flex）
>    - **GPU 更"轻"——所以单芯片内可以塞更多"线程"**
> 2. **时钟频率**：
>    - GPU: 1.5-2 GHz (高频率，需要复杂流水线)
>    - WSE: ~500 MHz (低频率，单时钟域，链路短)
>    - **WSE 用低频率换大面积的同步性**
> 3. **通信模型**：
>    - GPU: 共享内存 + 一致性协议 (复杂)
>    - WSE: 消息传递 + NoC (简单)
>    - **GPU 适合"所有 thread 都能访问同一份数据"的场景**
>    - **WSE 适合"每个 PE 拥有自己的数据"的场景**
> 4. **编程模型**：
>    - GPU: kernel 函数（隐式并行）
>    - WSE: 数据流图（显式 placement）
>    - **WSE 把 placement 的责任交给编译器，硬件可以更简单**
>
> **根本结论**：
> - GPU = "通用 SIMD 引擎"——灵活但复杂
> - WSE = "专用 MIMD 网格"——专用但极简
> - 两者都是 Moore 定律终结后的"用面积换性能"的不同解法

---

## 🔗 与 WSE/NoC/NPU 研究的关联

### 1. SIMT 思维 vs 数据流思维

```
GPU 思维 (SIMT):
  - "所有 lane 做同一件事"
  - 适合：矩阵乘、卷积、规约
  - 性能杀手：divergence、不规则访存

WSE 思维 (MIMD + Dataflow):
  - "每个 PE 做自己被分配的事"
  - 适合：不规则 DAG、稀疏计算、控制流密集
  - 性能杀手：通信不均衡、placement 差
```

**给你的启示**：你的 NPU 核应该用哪种模型？
- **如果是 MAC 阵列** → SIMT/SIMD（用 Tensor Core 思路）
- **如果是调度 + 运算混合** → MIMD（用 WSE 思路）
- **如果是 NPU 的控制器核** → 传统超标量（用 Day 10 思路）

### 2. Shared Memory ↔ WSE 的 NoC 局部通信

```
GPU 的 Shared Memory:
  - 128 KB / SM
  - Block 内所有 thread 共享
  - 访问延迟: ~20 cycles
  - 带宽: ~10 TB/s/SM
  - 本质: 程序员管理的 L1 Cache

WSE 的 NoC 邻居通信:
  - 4 个最近邻居 PE（上下左右）
  - 消息延迟: ~1-2 跳 = 1-2 cycles
  - 带宽: ~21 PB/s 总带宽
  - 本质: 硬件保证的"零延迟"通信
```

**关键差异**：
- GPU Shared Memory 是**软件管理的**（显式 __shared__ 声明）
- WSE 邻居通信是**硬件管理的**（消息路由自动）
- **对你的 NoC 研究**：NoC 的"局部优化"对应 GPU 的 Shared Memory 优化

### 3. Warp Divergence ↔ WSE 的 Place-and-route

| 问题 | GPU | WSE |
|------|-----|-----|
| 性能不均的根源 | Warp Divergence | 不平衡的 PE 工作量 |
| 解决方式 | 重构代码（避免分支） | 编译器 placement 优化 |
| 责任方 | 程序员 / 编译器 | 编译器 (SME) |
| 评估指标 | Occupancy、Divergence Rate | PE 利用率、通信均衡 |

**给你的研究方向（NoC 路由算法）的启示**：
- GPU 避免 divergence 的方式 = 重新组织 thread block
- WSE 优化通信的方式 = 重新放置 PE 任务
- **核心思想都是"把相互依赖的任务放在物理上接近的位置"**

### 4. Tensor Core ↔ 你的 NPU MAC 阵列

```
Tensor Core (Hopper):
  - 4×4 矩阵 FMA
  - 1024 FMA/cycle/SM
  - 128 SMs × 1024 = 131K FMA/cycle

典型 NPU MAC 阵列:
  - 128×128 阵列
  - 16384 MAC/cycle (16384 FMA = 32768 FLOP)
  - 单核
```

**架构差异**：
- Tensor Core **小**（4×4），**多**（1024 个/SM），**通用**（任意矩阵）
- NPU MAC 阵列 **大**（128×128），**少**（1 个/NPU），**专用**（卷积/MatMul）

**对 NPU 设计的启示**：
- 大阵列 → 更高吞吐，但灵活性差
- 小阵列 → 更灵活，但需要更多编排
- **平衡点**：64×64 或 128×128 是当前主流

---

## 📊 阶段进度（Day 24 / 30）

```
✓ Day 23: 多核 + SMT         (核的"数量"和"复用")
▶ Day 24: GPU 架构 (SIMT)     (核的"专用化")         ← 今天
→ Day 25: DNN 加速器 + NPU    (核的"领域定制")
→ Day 26: Wafer-Scale 专题    (核的"极限扩展")
→ Day 27: 并行计算 + 分布式   (跨机器的"协作")
```

**承上启下**：今天我们看到了 SIMT 如何让"成百上千的轻量线程"协同工作。明天看一个更极端的版本——**把这种并行直接固化到硬件里**：DNN 加速器 + NPU 设计。从 GPU 的"软件 SIMD"到 NPU 的"硬件 SIMD"，**专用化的下一步**。

---

## 🔗 明日预告

**Day 25：DNN 加速器 + NPU 设计**
- 脉动阵列 (Systolic Array)：Google TPU 的核心架构
- 数据复用策略 (Weight Stationary / Output Stationary / Row Stationary)
- Roofline 模型评估加速器设计
- 与今天的对比：GPU 是"软件 SIMD"，TPU 是"硬件 SIMD"
- **直接对应你的 NPU 核研究方向**——这是你的"主战场"

---

## 💡 今日感悟位

> *GPU 把"并行"做到了极致，但用了一个巧妙的抽象——SIMT：让程序员写标量代码，硬件自动做 SIMD。这种"软件可见 vs 硬件并行"的桥接，正是体系结构设计的精髓。但 WSE 走了相反的路：让硬件极简，把复杂性完全推给编译器。两条路都成功，告诉我们：**没有"最好的架构"，只有"最适合的权衡"**。明天学 TPU 时，会看到这种权衡的另一个极端——把"软件 SIMD"也固化成硬件脉动阵列。*

---

*Day 24 / 30. GPU 让我们看到 SIMT 如何把"标量程序员"解放出来——但代价是 Warp Divergence、Occupancy、内存层次这些"暗坑"。WSE 的设计哲学是反向的：把一切固化在硬件里，用专用换性能。明天学 TPU，会发现 DNN 加速器走到了 GPU 和 WSE 之间的某个位置——是"软件 SIMD 做得不够极致"还是"硬件 SIMD 做得不够灵活"？看你怎么理解。*
