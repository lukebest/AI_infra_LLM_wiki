---
type: Raw Source
title: 📰 体系结构晨报 — Day 25
source_path: /home/luke/openclawdata/workspace-research/notes/projects/arch-study-30d/day-25.md
textbook: "Computer Architecture: A Quantitative Approach (6th ed.) — Ch.7.1-7.5 Domain-Specific Architectures"
ingested: 2026-07-09
---

# 📰 体系结构晨报 — Day 25

📅 2026-07-08（Day 25 / 30，星期三）
🎯 阶段：并行篇（Day 23-27）
📖 教材：《计算机体系结构：量化方法》第6版 Ch.7 (7.1-7.5 — DPU/领域专用架构)

---

## 今日主题：DNN 加速器 + NPU 设计 — 把"并行"固化进硬件

### 🧭 为什么今天学这个？

**昨天我们看到 GPU 用 SIMT 做"软件版的 SIMD"——程序员写标量代码，硬件自动并行。今天我们跨过分水岭：把这种并行直接刻进芯片里。**

回顾 Day 1 的 CPU 性能公式：

```
CPU Time = IC × CPI × Clock Cycle Time
```

通用 CPU 的优化路径：
- ↓ IC（编译器优化）
- ↓ CPI（乱序、分支预测、Cache）
- ↑ Clock Rate（深流水线）

DNN 加速器走了完全不同的路——**削减通用性，换极致性能/能效**：
- ↓↓ IC（专用指令 = "卷积 + 池化 + ReLU"）
- ✓ CPI（数据流固定，几乎无控制冒险）
- ↓ Clock Rate（低频率换低功耗）

| 你的研究方向 | 与今天的关联 |
|------------|-------------|
| **NPU 核设计** | **直接命中！MAC 阵列、数据流、量化策略都是 NPU 核心设计点** |
| **WSE 架构** | WSE 的 SLA 核心本质上就是"极简版 DNN PE"——无乱序、无 Cache、单 MAC |
| **超标量 CPU 核** | 对比视角：CPU 追求通用性，NPU 抛弃通用性。今天学"为什么要抛弃" |
| **核内同步** | 数据流架构的同步机制不同于传统锁——CSL 里"到达即触发"vs Lock-Free |
| **NoC 研究** | 加速器的数据搬运模式决定 NoC 设计：脉动阵列的 NoC 就是其阵列拓扑 |

### 🎯 今天的目标

1. 理解 DNN 加速器的核心设计空间——**数据复用策略决定一切**
2. 掌握脉动阵列 (Systolic Array) 工作原理——**这是 TPU 的灵魂**
3. 用 Roofline 模型量化评估 NPU 设计——**量化方法再次登场**
4. 对比 GPU/TPU/NPU 的设计哲学差异——**从"通用 SIMD"到"专用 ASIC"**
5. **直接为你的 NPU 核设计提供参考**——**这是你的"主战场"**

---

## 📖 阅读任务（约 60-90 分钟）

**《计算机体系结构：量化方法》第6版 第 7 章 7.1-7.5 节：Domain-Specific Architectures (DPU)**

### 核心阅读（60 min）：
1. **7.1 Introduction** — 为什么需要 DSA？性能/Watt 的倒挂
2. **7.2 Guidelines for DSAs** — DSA 设计的 6 条原则
3. **7.3 Examples of DSAs** — TPU、Catapult、CGRAs 的对比
4. **7.4 Performance Metrics for DSAs** — Roofline 模型的 DSA 变体
5. **7.5 Cross-Architectural Comparisons** — CPU vs GPU vs TPU 的全面对比

### 推荐补充（30 min）：
1. **Jouppi et al. 2017 "In-Datacenter Performance Analysis of a Tensor Processing Unit"** — TPU v1 的开山论文
2. **Sze et al. 2020 "Efficient Processing of Deep Neural Networks: A Tutorial and Survey"** — 完整 DNN 加速器综述
3. **Chen et al. 2016 "Eyeriss: A Spatial Architecture for Energy-Efficient Dataflow for CNN"** — Row Stationary 数据流的代表作
4. **论文推荐**：Jouppi et al. 2023 "TPU v4: An Optically Reconfigurable Supercomputer"（可选）

---

## 🔑 核心概念（带公式）

### 1. 量化方法：DSA 的"性能/Watt" 视角

```
通用 CPU:
  性能：1×
  功耗：1×
  性能/Watt = 1 (基准)

典型 DNN 加速器 (TPU v1):
  性能：~25-50×  (vs CPU)
  功耗：~3-4×    (vs CPU)
  性能/Watt：~10-15×  vs CPU

GPU (K80):
  性能/Watt：~3-5×  vs CPU
```

**根本原因**：通用处理器 90% 的晶体管在做"判断"（分支、依赖检查），真正做计算 (MAC) 的只占 10%。DSA 把这 90% 砍掉。

```
CPU 晶体管利用：
  Branch Predictor: ~5%
  OOO logic:       ~20%
  Cache + TLB:      ~35%
  Register File:    ~15%
  Actual MAC:       ~10%  ← 真正干活的部分
  Other (control):  ~15%

TPU 晶体管利用:
  MAC 阵列:        ~70%
  Buffer + NoC:    ~25%
  Control:         ~5%  ← 极简控制
```

### 2. Roofline 模型 for DNN 加速器

```
               Performance (Ops/Byte)
                       │
   Compute-bound       │           Memory-bound
        ▲              │              ▲
        │\             │             /│
        │ \   ┌────────┴────────┐   / │
        │  \  │                  │  /  │
        │   \ │                  │ /   │
        │    \│                  │/    │
        │     \    Ridge Point  /      │
        │      \  ─ ─ ─ ─ ─ ─ /       │
        │       \           /         │
        │        \─────────/          │
        │       /         \           │
        │      /           \          │
        │     /             \         │
        └─────┴───────────────┴───────┘
                   Bandwidth
```

**Roofline 公式**：

```
Performance = min(
    Peak_Compute,           # 计算上限 (Ops/Sec)
    Bandwidth × AI          # 带宽上限 × 算术强度
)

AI (Arithmetic Intensity) = FLOPs / Bytes
```

**Ridge Point (拐点) = Peak_Compute / Bandwidth**

- **AI > Ridge Point** → Compute-bound（优化点在阵列）
- **AI < Ridge Point** → Memory-bound（优化点在 NoC / 存储）

**典型 DNN 工作负载的 AI**：

| Kernel | AI (FLOPs/Byte) | 类别 |
|--------|----------------|------|
| GEMM (大矩阵) | 100-200 | Compute-bound |
| GEMV / 矩阵-向量 | 10-50 | 接近 Ridge Point |
| Convolution | 50-150 | Compute-bound |
| Softmax | 5-20 | Memory-bound |
| Layer Norm | 10-30 | Memory-bound |
| Attention (Q×K^T) | 50-100 | Compute-bound |
| Attention (Softmax×V) | 20-30 | Memory-bound |

### 3. 脉动阵列 (Systolic Array) — TPU 的核心

**基本思想**：让数据像心脏收缩一样在 PE 阵列里"流动"——每个 PE 计算完后，把数据**主动传给**邻居，而不是写回 memory。

```
8×8 脉动阵列（TPU 简化版，2D 示意）:

数据流方向：Weight → (从左流入，每行步进)
           Activation → (从顶部流入，每列步进)
           Partial Sum → (沿对角线累积)

    ↓ a₀  ↓ a₁  ↓ a₂  ↓ ...        ← Activation 流
   ┌────┬────┬────┬────┐
 → │PE₀₀│PE₀₁│PE₀₂│ ... │→ ─ → ─ b 部分和向右流
   ├────┼────┼────┼────┤
 → │PE₁₀│PE₁₁│PE₁₂│ ... │→
   ├────┼────┼────┼────┤
 → │PE₂₀│PE₂₁│PE₂₂│ ... │→
   └────┴────┴────┴────┘
  W ↑    W ↑   W ↑                ← Weight 预加载进每个 PE

计算: C[i,j] = Σₖ A[i,k] × B[k,j]
每个 cycle：8 个 MAC × 8 行 = 64 个 MAC 同时进行
```

**为什么"脉动"？**
- **每个数据被复用 N 次**（N = 阵列维度）
- 不需要每完成一个 MAC 就写回 memory
- **计算吞吐 = 1 MAC/cycle/PE，但数据访存降到 1/N**

**关键特性**：
- 所有 PE **同步执行**（single clock domain inside the array）
- 控制极简（不需要乱序、不需要分支预测）
- 数据流和权重流方向**正交**——这是创造高复用的关键

### 4. 数据复用策略对比（重要！）

DNN 加速器的核心设计抉择：**数据怎么复用？**

| 策略 | 复用对象 | 数据流 | 代表 | 优点 | 缺点 |
|------|---------|-------|------|------|------|
| **Weight Stationary (WS)** | 权重 (Filter) | 权重预加载到 PE，feature map 流过 | TPU (原始) | 最小化权重访存 | 中间结果累加复杂 |
| **Output Stationary (OS)** | 输出 | 每个 PE 累加自己的输出值 | NVDLA | 简单，无需 partial sum 路由 | 权重/输入访存高 |
| **Row Stationary (RS)** | 行 (1D 卷积) | 把 1D 卷积映射到 PE 行 | Eyeriss | 卷积效率高 | 控制复杂 |

**数据搬运量对比**（假设 C×F=F×F 卷积，N=N 个输出 channel）：

```
理论最小数据搬运（任意策略）：
  Load weights:   C × F × F × 4 bytes (一次)
  Load inputs:    1 batch × 1 (从 memory load 一次，PE 间复用 F×F 次)
  Store outputs:  C (写出一次)

TPU 实际 (Weight Stationary)：
  ≈ 接近最优，因为权重一次加载后复用 N 次
```

**对你的 NPU 设计的启示**：
- **小 batch** → Weight Stationary 划算（权重占比大）
- **大 batch** → Output Stationary 划算（输入占比大）
- **不规则 kernel** → Row Stationary 划算（如深度可分离卷积）

### 5. 单个 MAC 单元的设计（PE 级别）

```
典型 PE 结构（TPU 风格）：
  ┌─────────────────────────────┐
  │  Weight Register (32-bit)   │ ← 静态，加载一次
  │  Activation Register (8-bit)│ ← 动态，每 cycle 流过
  │  MAC:   out = w × a + acc   │
  │  Accumulator (32-bit)        │ ← 累加到 right neighbor
  └─────────────────────────────┘

数据流:
  cycle 1:  load w, a; acc = a × w
  cycle 2:  acc = a × w + prev_acc
  ...
  cycle N:  最终结果向右移出
```

**为什么是 8-bit activation × 32-bit weight 累加？**
- 输入低精度化：内存带宽减少 4×
- 累加高精度化：避免精度损失（这是 **混合精度 (Mixed Precision)** 的核心）
- **对你的 NPU 启示** —— 直接关系到 Day 5 学的 BF16/INT8 选择

### 6. Roofline 评估 TPU v1（练习题预告）

**TPU v1 规格**：
- 65,536 个 INT8 MAC（65536 = 256×256）
- 频率 700 MHz
- 片上 SRAM：24 MB
- 内存带宽：34 GB/s（DDR3）

**计算**：

```
Peak Compute = 65536 MAC × 700 MHz × 2 (1 MAC = 2 FLOP)
             = 91.8 TFLOPS (INT8)
             ≈ 46 TFLOPS (FP32 equivalent, 因为 1×INT8 = 0.5×FP32)

Bandwidth = 34 GB/s

Ridge Point = 91.8 / 34 ≈ 2700 FLOPs/Byte (INT8)
             ≈ 1350 FLOPs/Byte (FP32 equivalent)

对比 CPU:
  CPU Ridge Point ≈ 10 FLOPs/Byte
  TPU Ridge Point ≈ 2700 FLOPs/Byte
  → TPU 的"compute 区域"比 CPU 大 270 倍！
```

**对你的 NPU 设计的指导**：
- 如果你的 NPU 目标 workload AI < 100 → memory-bound，要堆带宽
- 如果 AI > 1000 → compute-bound，要堆 PE 数
- Ridge Point 是 NPU 的"设计锚点"

### 7. TPU vs GPU vs CPU 设计哲学对比

| 维度 | CPU | GPU | TPU |
|------|-----|-----|-----|
| **代表 ISA** | x86, ARM, RISC-V | NVIDIA PTX, AMD GC | TPU ISA |
| **核心数** | 4-128 | 100-200 (SM) | 1-4 (超大阵列) |
| **单核心"算力"** | 高 | 中 | 低 (单 MAC) |
| **单芯片总算力** | ~1 TFLOPS | ~50-1000 TFLOPS | ~100-400 TFLOPS |
| **编程模型** | 串行代码 | kernel | 编译成数据流 |
| **控制硬件** | 完整 | 简化 | 极简（核心是无控制状态机）|
| **数据复用** | 靠 Cache | 靠 Shared Memory | 靠数据流 |
| **适用 workload** | 串行 + 分支 | 数据并行 + 规整 | 大规模矩阵 |
| **性能/Watt** | 1× | 3-5× | 10-15× |

### 8. CSA (Cerebras SLA) —— 你的研究直接对照

```
WSE-3 SLA (Sparse Linear Algebra) Core:
  ┌──────────────────────────────┐
  │  3× FMAC (FP16 MAC + 累加) │
  │  ~50KB local SRAM            │
  │  4 路消息 NoC（上下左右）   │
  │  Flex Sched (硬件调度器)     │
  │  单时钟域                    │
  └──────────────────────────────┘

TPU PE 单元:
  ┌──────────────────────────────┐
  │  1× MAC (8-bit × 32-bit)    │
  │  ~32 字节 Register           │
  │  无 NoC (固定阵列连线)       │
  │  无 scheduler (固定数据流)    │
  └──────────────────────────────┘
```

**关键差异**：

| 维度 | SLA | TPU PE |
|------|-----|--------|
| **核大小** | 大（独立 CPU-like） | 小（1 MAC） |
| **核与核连接** | 通用 NoC | 硬连线 mesh |
| **编译器责任** | 高（placement 优化） | 低（编译器映射到固定阵列） |
| **灵活性** | 高（任何 DAG） | 低（只优化矩阵乘） |
| **数据复用** | 通过 SRAM + NoC | 通过 systolic flow |

**给你的 NPU 设计的关键启示**：
- TPU 思路 = 极致专用（NPU-as-ASIC）
- WSE SLA 思路 = 通用 PE（NPU-as-MIMD-core）
- **你的 NPU 核在哪条路上？**——这取决于目标 workload 的稳定性
  - 如果只跑推理 → TPU 路线（脉动阵列）
  - 如果跑训练 + 推理 + 控制 → WSE 路线（更通用 PE）

### 9. CGRA (Coarse-Grained Reconfigurable Array) — 第三个极端

```
CGRA = TPU 的可配置版本：
  ┌──────┬──────┬──────┬──────┐
  │  ALU │  ALU │  ALU │  ALU │   ← 这些 ALU 之间
  ├──────┼──────┼──────┼──────┤      的连线可以配置
  │  ALU │  ALU │  ALU │  ALU │
  ├──────┼──────┼──────┼──────┤
  │ Reg  │ Reg  │ Reg  │ Reg  │
  └──────┴──────┴──────┴──────┘
       ↑  ↑  ↑  ↑
    每个 ALU 可以是 +, ×, MAC, 比较等
    每个 Reg 可以配置 (双 buffer, FIFO)
    连线在每次编译时重新配置
```

**代表**：Plasticine, Sambanova RDU, Versal AI Edge

**对你研究的启示**：CGRA 介于"硬编码（TPU）"和"通用（WSE）"之间——是编译时灵活性最优解。

---

## 🧪 练习题（约 60 分钟）

### 基础题

**Q1：脉动阵列的数据搬运优化**

某 16×16 脉动阵列，权重和输入均为 FP16（2 bytes）。
- **不用脉动阵列**（每次 MAC 后写回 memory）：128×128 矩阵乘需要多少次访存？
- **用脉动阵列**：需要多少次访存？
- 计算加速比（仅访存节省带来的）。

> **答**：
>
> **不用脉动**（假设 1 MAC 后写回）：
>   总 MAC 数 = 16³ = 4096
>   每个 MAC 后写回 1 个 partial sum = 4096 次写
>   每个权重读 16 次 = 16²×16 = 4096 次读
>   每个输入读 16 次 = 16³ = 4096 次读
>   总访存 = 4096 + 4096 + 4096 = 12,288 次访存
>
> **用脉动阵列**（一次加载，多次复用）：
>   权重：加载 16²×2 = 512 bytes（一次，复用 16 次）
>   输入：加载 16²×2 = 512 bytes（一次，复用 16 次）
>   输出：写出 16²×2 = 512 bytes（一次）
>   总访存 = 1536 bytes（假设每次读写都是 16-bit 基本单位）
>
> **加速比 ≈ 12288 / 1536 = 8×**
>
> **结论**：脉动阵列对 16×16 的 GEMM 节省 8× 数据搬运。**阵列越大，节省越多**（对 256×256 是 256×）。
>
> **对你的 NPU 设计的启示**：PE 阵列越大，data reuse 越好，但要权衡良率/频率。

### 进阶题

**Q2：Roofline 模型分析 NPU 设计**

你的 NPU 设计目标：
- 32×32 = 1024 个 FP16 MAC
- 频率 1 GHz
- SRAM: 1 MB（片上）
- DRAM: 16 GB/s 带宽（HBM-lite）

某目标 workload：1×1 卷积，AI = 50 FLOPs/Byte。
- **计算**：
  1. Peak Compute
  2. 内存带宽上限
  3. Ridge Point
  4. 实测性能 30 TFLOPS 时是哪个 bound？效率多少？

> **答**：
>
> Peak Compute = 1024 MAC × 1 GHz × 2 = 2.048 TFLOPS (FP16)
>
> 内存带宽上限 = Bandwidth × AI = 16 GB/s × 50 = 800 GFLOPS = 0.8 TFLOPS
>
> Ridge Point = 2.048 / 0.016 = 128 FLOPs/Byte
>
> AI = 50 < 128 = Ridge Point → **memory-bound**
>
> 实际性能上限 = min(2.048, 0.8) = 0.8 TFLOPS
>
> 实测 30 TFLOPS 不可能达到，超过 memory-bound 上限 0.8 TFLOPS。
>
> **结论**：这个 NPU 对 1×1 卷积是 **memory-bound**，DRAM 带宽是瓶颈。要么堆 HBM、要么用更高 AI 的算子（如 im2col）。
>
> **对你的 NPU 设计**：
> - 切记 **用 Roofline 反向约束你的 NPU 设计**！
> - 不能孤立看 PE 数，要看工作负载的 AI 和目标系统的 Bandwidth
> - 跑 MLPerf inference（典型 AI = 50-100），Ridge Point 在 100-300 范围最优

### 思考题（与 WSE/NoC/NPU 研究的关联）

**Q3：Cerebras SLA 核心 vs TPU PE 本质对比**

WSE-3 SLA 核心本质上是一个"极简 CPU + 大量 SRAM + NoC"，可以独立调度。
TPU PE 本质上是"1 个 MAC + 寄存器 + 邻居硬连线"，只能随大阵列同步。

**问题**：从硬件复杂度、能效、可编程性三个维度，对比 SLA 和 TPU PE 哪个"NPU 性"更强？
如果你的 NPU 核要做"可重构 AI 加速器"，应该借鉴哪个？

提示：
- 硬件复杂度（晶体管数 / gate-equivalent）
- 能效（TOPS/W）
- 可编程性（能跑什么 DAG / kernel）
- 编译器成熟度

> **答（提示方向）**：
>
> **硬件复杂度**：
> - SLA ≈ 50,000 gates (含 Flex Sched, NoC, SRAM 控制器)
> - TPU PE ≈ 1,000 gates (1 个 MAC + register + 流接口)
> - **TPU PE 简单 50×**
>
> **能效**：
> - SLA: ~10-20 TOPS/W（因为有 NoC + 控制 + 本地 SRAM 寻址）
> - TPU PE (在阵列中): ~30-50 TOPS/W（极简，数据流固定）
> - **TPU 阵列能效高 2-3×**
>
> **可编程性**：
> - SLA：高（任何 DAG 都能跑）
> - TPU PE：低（只跑二维脉动阵列算法）
> - **SLA 灵活度高 10-100×**
>
> **编译器**：
> - SLA → 复杂编译器（SME/CSE），需要解决 placement / routing 优化（NP-hard）
> - TPU → 相对简单（XLA 把矩阵乘映射到阵列）
> - **TPU 编译器成熟度更高**
>
> **结论**：
> - TPU 是 **极致专用**——快、省、但只能跑一类算法
> - SLA 是 **领域半专用**——更灵活、更通用、能跑更多 kernel
> - **对你的 NPU 设计的启示**：选择哪个取决于你的目标场景
>   - 如果只跑推理 + 矩阵乘 → **TPU 路线**（脉动阵列）
>   - 如果要跑训练 + 控制 + 通信 + 矩阵乘 → **SLA 路线**（灵活 PE）
>   - 如果是不确定未来 → **CGRA 路线**（Plasticine, Sambanova）

**Q4：脉动阵列的 NoC 视角（与你的研究方向）**

脉动阵列的"邻居硬连线"本质上是一个**专用 NoC**——固定 mesh 拓扑、固定路由、无拥塞（因为数据流已编排）。

对比传统 NoC：
- 传统 NoC：灵活路由、自适应、支持任意流量模式
- 脉动阵列 NoC：固定路由、确定性、数据流已编排

你的研究方向：NoC 路由算法。

**问题**：脉动阵列的 NoC 设计经验如何迁移到通用 NoC？哪些能借鉴，哪些不能？

> **答（提示方向）**：
>
> **能借鉴的**：
> 1. **确定性路由 (Determinism)**：DOR 在通用 NoC 也常用，借鉴脉络相同
> 2. **避免拥塞靠设计而非运行时**：脉动阵列在编译时就算好流量，通用 NoC 应学习"通过 PE placement 优化"
> 3. **数据流预编排**：Systolic dataflow 是"compile-time placement"，可用在你 NoC 的 traffic-aware scheduling
>
> **不能直接借鉴的**：
> 1. **脉动阵列无拥塞是因为流量固定**：通用 NoC 处理不规则流量，无法避免拥塞
> 2. **脉动阵列无死锁是因为数据流单向**：通用 NoC 需双向流动，必须有虚通道等机制
> 3. **脉动阵列同步是 single clock**：通用 NoC 是全局异步，需要更高层次的同步
>
> **你的研究启示**：
> - 把"compile-time optimization"思想引入 NoC 设计——**Software-Defined NoC**
> - 这正是 WSE CSL 编译器做的事情——SME 把 DAG 当 placement 优化，把"运行时不确定"换成"编译时确定"
> - 你可以研究：**在传统多核 NoC 中，如何把"动态路由"换成"预编排路由"以降低运行时复杂度**

---

## 🔗 与 WSE/NoC/NPU 研究的关联

### 1. 量化分析：NPU 设计的"性能/面积/功耗"三角

```
NPU 设计核心权衡：
                                    
        Performance
            ▲
           /│\
          / │ \
         /  │  \      ← 三者互相牵制！
        /   │   \
       /    │    \
      /  ★  │    \    
     /      │     \
    ┌───────┴──────┐
  Area        Energy
```

**你的 NPU 核研究**：今天的练习题 Q2 的 Roofline 方法可用于：
1. 评估你的核设计是否 balance
2. 找到瓶颈（compute / memory / interconnect）
3. 指导 PE 阵列大小选择

### 2. 脉动阵列 vs 脉动 NoC

```
传统 NPU NoC (脉动 mesh):
  - 固定拓扑: 8×8 或 16×16 mesh
  - 数据流: weight/activation/psum 三向流动
  - 路由: 硬连线，无虚通道
  
研究 NoC 的方向 (你):
  - 拓扑可重构？
  - 流量自适应路由？
  - 编译时路由优化？
  - 与脉动数组不同的设计点？
```

**给你一个研究机会**：
- **"Demand-Aware Mesh NoC for LLM Inference"** ——结合 Day 27 的 LLM 通信模式
- 问题：LLM inference 的 traffic pattern（attention 阶段 all-to-all vs MLP 阶段 all-reduce）是否能用 reconfigurable NoC 优化？
- 这是 ISCA/MICRO 热门 topic，与 WSE 的脉动 NoC 形成对比

### 3. TPU 的"硬件 SIMD" 给你的设计灵感

```
传统超算 (Day 24 GPU):
  程序员负责把矩阵乘分解成 32-wide warp
  → 软件管理的 SIMD
  
TPU:
  脉动阵列的硬件自动管理 SIMD
  → 硬件管理的 SIMD
  → 程序员只看到 "矩阵乘" 这个抽象

启示: 你的 NPU 核在最外层应该提供"高级 API"——
  不要让程序员看到 1024 个独立 PE
  而应该提供: GEMM, Conv, Attention 这类"算子级 API"
```

**这是 ISA 设计的黄金法则**：
- 对用户暴露的抽象 = 高级操作（GEMM、Conv、Attention）
- 对硬件暴露的细节 = PE 调度、片上数据流、片外访存
- **你的研究机会**：为 NPU 设计合适的"中间层抽象"

### 4. CGRA 作为 TPU + 通用 CPU 的中间方案

```
| 通用 CPU |-----| CGRA |-----| TPU |
   灵活      编译时    运行时
            灵活      固定
            ↓
    适合：多变算法、固定算子、专用算子
```

**你未来的研究方向可能性**：
- **方向 A**：基于 WSE 的灵活 PE + 编译时优化（SME 路线）
- **方向 B**：基于 TPU 的脉动阵列 + 高级编译器（XLA 路线）
- **方向 C**：基于 CGRA 的中间方案 + 可重构编译器（Plasticine 路线）
- **方向 D**：NoC + NPU 协同设计（HW/SW Co-design）

### 5. Cerebras WSE 的 SLA 是"PE-as-MIMD-CPU"

```
SLA 核:
  - 1 个 PE = 1 个微 CPU (3 MAC + NoC + SRAM)
  - 整个芯片 = 900K PE = "超多核阵列"
  - 本质 = 把"CPU 核 + 内存 + NoC"组合做一个 PE
  - 与 NPU 的根本区别: NPU 把"CPU 逻辑"换成"MAC 数组"

你的 NPU 核可能的设计:
  - 不要全盘搬 "CPU 逻辑" 或 "纯 MAC"
  - 考虑混合：通用核（控制）+ 专用 MAC 阵列（计算）
  - 这正是 Day 19 "核内同步" 研究的实际应用场景！
```

### 6. 直接关联到 WSE-3 性能分析

WSE-3 总算力 ≈ 900K PE × 3 MAC × 0.5 GHz × 2 ≈ 2.7 POPS (FP16 AI workload)

```
TPU v4 单芯片 ≈ 275 TFLOPS
WSE-3 单芯片 ≈ 2.7 POPS = 2700 TFLOPS
→ WSE-3 在 FP16 AI 工作负载下算力是 TPU v4 的 ~10×
```

但 WSE-3 没有巨大 HBM（只有 20 PB/s SRAM + MemoryX DRAM），所以 Ridge Point 也不同：

```
WSE-3:
  Peak Compute (FP16) ≈ 2700 TFLOPS
  SRAM Bandwidth ≈ 21 PB/s
  Ridge Point (using SRAM) ≈ 0.128 FLOPs/Byte
  → 几乎所有 AI workload 都在 compute-bound 区域！
  → 这是 WSE 比 GPU/TPU 强大的根本原因（高带宽）
```

---

## 📊 阶段进度（Day 25 / 30）

```
✓ Day 23: 多核 + SMT          (并行的"通用"形式)
✓ Day 24: GPU SIMT            (并行的"软件 SIMD")
▶ Day 25: DNN 加速器 + NPU    (并行的"硬件 SIMD")    ← 今天 + 你的研究主战场
→ Day 26: Wafer-Scale 专题    (并行的"极限扩展")
→ Day 27: 并行计算 + 分布式   (跨芯片的"协作")
```

**承上启下**：今天我们把"并行"做到了硬件里。明天（Day 26）我们将看到一个极端——把这种并行扩展到整片晶圆尺度的 WSE。

---

## 🔗 明日预告

**Day 26：Wafer-Scale 架构专题**
- WSE-1/2/3 三代架构对比
- 2D Mesh NoC 设计哲学
- 容错机制 (Route-around + Fail-in-place)
- 数据流编程模型 (CSL/SpaDA)
- 片上 vs 片外互连的巨大差异
- **直接基于你的 reports/ 目录下的 wafer-scale-engine-2026/ 分析**

---

## 💡 今日感悟位

> *DNN 加速器教会我一件事：**通用性是奢侈品**。CPU 和 GPU 把它当作默认假设，DNN 加速器敢于扔掉它——这就是"性能/Watt"提升 10×+ 的代价。但通用性不是一切，看 WSE 的 SLA 核：它选择了另一个极端，把"通用 PE" × "海量集成"，同样获得了高性能。两条路都成功，因为它们各自匹配了不同 workload 的不规则性。今天的练习题 Q4 给了我一个启示：脉动阵列的"compile-time 数据流编排"思想，可能可以用在我的 NoC 研究里——把运行时的不确定性转化为编译时的确定性。这是软件定义网络（SDN）的体系结构版本。*

---

## 📚 推荐补充阅读

1. **Jouppi et al. 2017 "In-Datacenter Performance Analysis of a Tensor Processing Unit"** — TPU v1 的开山之作（ISCA 2017）
2. **Sze et al. 2020 "Efficient Processing of Deep Neural Networks"** — 完整 DNN 加速器教程（Proc. IEEE）
3. **Chen et al. 2016 "Eyeriss: A Spatial Architecture for Energy-Efficient Dataflow for CNN"** — Row Stationary 数据流（ISCA 2016）
4. **Jouppi et al. 2023 "TPU v4"** — 光学互连的可重构超算（ISCA 2023）

---

*Day 25 / 30. DNN 加速器让我们看到——**把简单做到极致，就是一种艺术**。TPU 的脉动阵列、Google TPU 的诞生、Cerebras WSE 的反方向探索，都证明了一件事：**体系结构不是非此即彼的选择题，而是参数空间的连续探索**。今天学的是"硬件 SIMD"，明天学"硬件 SIMD × 晶圆级"——把 1 个芯片扩成 1 个 wafer。*
