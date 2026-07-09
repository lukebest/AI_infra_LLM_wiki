---
type: Concept
title: DNN Accelerator Systolic Dataflow
description: H&P Ch.7 DSA：脉动阵列、WS/OS/RS 数据复用、Roofline for NPU、TPU vs GPU vs WSE SLA；晶体管从控制迁到 MAC
tags:
- accelerator
- dnn
- systolic
- dataflow
- tpu
- npu
- roofline
- dsa
timestamp: '2026-07-09T00:00:00Z'
created: 2026-07-09
sources:
- raw/articles/arch-study-30d-day-25.md
---

# DNN Accelerator Systolic Dataflow（DNN 加速器与脉动数据流）

arch-study **并行篇 Day 25**：H&P Ch.7.1–7.5 **Domain-Specific Architectures**——把 Day 24 [GPU SIMT](/concepts/gpu-simt-architecture.md) 的「软件 SIMD」再推一步：**把并行刻进 MAC 阵列**。核心命题：**数据复用策略决定一切**；脉动阵列是 TPU 的灵魂。

**Source:** [raw/articles/arch-study-30d-day-25.md](raw/articles/arch-study-30d-day-25.md)

## 为何需要 DSA

通用 CPU 优化路径：↓IC / ↓CPI / ↑Clock。DNN 加速器换路：

| | 通用 CPU | 典型 DNN 加速器 (TPU v1) |
|--|----------|--------------------------|
| 性能 | 1× | ~25–50× |
| 功耗 | 1× | ~3–4× |
| **性能/Watt** | 1× | **~10–15×** |
| GPU (K80) 对照 | — | ~3–5× vs CPU |

**晶体管叙事**：CPU ~90% 做「判断」（分支、依赖、Cache）；真正 MAC ~10%。TPU 把控制砍到 ~5%，**MAC 阵列 ~70%** + Buffer/NoC ~25%。见 [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md)。

## Roofline for DNN / NPU

```
Performance = min(Peak_Compute, Bandwidth × AI)
AI = FLOPs / Bytes
Ridge Point = Peak_Compute / Bandwidth
```

- **AI > Ridge** → compute-bound（堆 PE）
- **AI < Ridge** → memory-bound（堆带宽 / NoC）

| Kernel | 典型 AI (FLOPs/Byte) | 类别 |
|--------|----------------------|------|
| 大 GEMM | 100–200 | Compute-bound |
| Convolution | 50–150 | Compute-bound |
| Attention Q×Kᵀ | 50–100 | Compute-bound |
| GEMV | 10–50 | 近 Ridge |
| Softmax / LayerNorm | 5–30 | Memory-bound |

算子级 AI 与 Prefill/Decode 对应见 [GEMM vs GEMV](/concepts/gemm-vs-gemv.md)。

### TPU v1 锚点（练习）

- 65,536 INT8 MAC（256×256）、700 MHz、34 GB/s DDR3
- Peak ≈ **91.8 TOPS INT8**；Ridge ≈ **2700 FLOPs/Byte (INT8)**（CPU Ridge ~10 → TPU「compute 区」大 ~270×）

**NPU 设计锚点**：目标 workload AI 与 Ridge 对齐——MLPerf 推理典型 AI 50–100 时，Ridge 落在 100–300 往往更平衡。

## 脉动阵列 (Systolic Array)

数据像「心跳」在 PE 间流动：算完**主动传给邻居**，而非每 MAC 写回 memory。

```
Activation ↓ 列步进；Weight 预载于 PE；Partial Sum → 行/对角累积
C[i,j] = Σₖ A[i,k] × B[k,j]
吞吐 ≈ 1 MAC/cycle/PE；访存相对朴素实现可降到 ~1/N（N=阵列边长）
```

**关键特性**：单时钟域同步；控制极简（无 OoO/BP）；权重流与激活流**正交** → 高复用。

**访存直觉（16×16 FP16 GEMM）**：朴素每 MAC 写回 ≈ 12k 次访存；脉动一次加载复用 ≈ **~8×** 访存节省；**阵列越大，复用越好**（256×256 量级可达 ~256×），但受良率/频率约束。

## 数据复用三策略

| 策略 | 驻留对象 | 代表 | 优点 | 缺点 |
|------|----------|------|------|------|
| **Weight Stationary (WS)** | Filter/权重 | TPU（经典） | 权重访存最小 | psum 路由复杂 |
| **Output Stationary (OS)** | 输出累加 | NVDLA | 实现简单 | 权重/输入访存高 |
| **Row Stationary (RS)** | 1D 卷积行 | [Eyeriss](/concepts/eyeriss-accelerator.md) | 卷积复用好 | 控制复杂 |

**选型启发**：小 batch → WS；大 batch → OS；不规则/深度可分离 → RS。可重构 (dataflow, layout) 见 [FEATHER](/concepts/feather-accelerator.md)。

## PE 级混合精度

典型 TPU 风格 PE：Weight reg（可 32b）× Activation（常 8b）+ 宽 Accumulator。**低精度输入减带宽，高精度累加保数值**——与 [Numeric Formats](/concepts/numeric-formats-ai-hardware.md) 的 INT8/BF16 选择直接相关。

## CPU vs GPU vs TPU 哲学

| 维度 | CPU | GPU | TPU |
|------|-----|-----|-----|
| 并行形态 | 少核高 IPC | SIMT 宽 | 超大 MAC 阵列 |
| 数据复用 | Cache | Shared Memory | **数据流** |
| 控制 | 完整 OoO/BP | 简化 | **极简** |
| 编程 | 串行+线程 | Kernel | 编译成数据流 |
| 性能/Watt | 1× | 3–5× | **10–15×** |

GPU Tensor Core = 小矩阵×多实例；脉动阵列 = 大网格×少实例——共同：**空间换时间、专用换灵活**（[GPU SIMT](/concepts/gpu-simt-architecture.md)）。

## WSE SLA vs TPU PE

| 维度 | [WSE](/entities/cerebras-wse.md) SLA | TPU PE |
|------|--------------------------------------|--------|
| 粒度 | 微 CPU（多 MAC + SRAM + NoC） | 1 MAC + 寄存器 |
| 互连 | 通用 2-D mesh NoC | 硬连线阵列 |
| 灵活性 | 任意 DAG | 矩阵乘为主 |
| 编译器 | Placement/routing 重 | XLA 映射阵列 |
| 能效倾向 | 中（含 NoC/控制） | 阵列内更高 |

- **只跑推理矩阵乘** → TPU/脉动路线  
- **训练+控制+通信** → WSE/MIMD PE 路线  
- **中间态** → [Plasticine](/concepts/plasticine-accelerator.md) 等 **CGRA**（编译时重构连线）

## NoC 视角：脉动能借鉴什么

脉动「邻居硬连线」= **专用 NoC**：固定拓扑、确定性路由、流量编译期编排 → 无运行时拥塞。

| 可借鉴 | 不可照搬 |
|--------|----------|
| 确定性路由（DOR） | 不规则流量下的零拥塞假设 |
| 编译期 placement 减冲突 | 单向数据流 → 无死锁 |
| Software-Defined / 预编排路由 | 单时钟域同步 |

见 [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md)、[Mesh and Torus Topology](/concepts/mesh-torus-topology.md)。晶圆级量化综合见 [WSE Quantitative Architecture Analysis](/concepts/wse-quantitative-architecture-analysis.md)（Day 26）。

## 相关页面

- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — Day 24 软件 SIMD
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 砍通用性换能效
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — RS dataflow 流片基线
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — CGRA 中间路线
- [FEATHER Accelerator](/concepts/feather-accelerator.md) — 可重构 dataflow-layout
- [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md) — AI / Roofline
- [Cerebras WSE](/entities/cerebras-wse.md) — SLA vs 脉动 PE
- [WaferLLM System](/concepts/waferllm-system.md) — 晶圆级 LLM 算子映射

# Citations

[1] [raw/articles/arch-study-30d-day-25.md](raw/articles/arch-study-30d-day-25.md) — H&P Ch.7.1–7.5 DSA（Day 25）
