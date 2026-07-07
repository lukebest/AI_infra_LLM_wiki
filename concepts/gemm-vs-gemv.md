---
type: Concept
title: GEMM vs GEMV in LLM Inference
description: 矩阵乘 vs 矩阵-向量乘：算子形状、算术强度（AI）、Roofline 类别、Prefill/Decode 对应关系；GEMM compute-bound（AI~1000），GEMV bandwidth-bound（AI~2）；H100 decode <1% 峰值 FLOPS，理论时间 vs 实际时间差 100×
tags:
- gemm
- gemv
- arithmetic-intensity
- roofline
- compute-bound
- bandwidth-bound
- prefill
- decode
- matmul
- kernel
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- concepts/prefill-decode-divergence.md
- concepts/waferllm-system.md
- concepts/flashdecoding-plus-plus.md
- raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf
---

# GEMM vs GEMV in LLM Inference

**GEMM (General Matrix Multiply)** 和 **GEMV (General Matrix-Vector Multiply)** 是 LLM 推理中两个最基本、但**行为天差地别**的算子。理解它们的差异是理解 [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md)、[WaferLLM System](/concepts/waferllm-system.md) 和 [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md) 的基础。

## 1. 数学定义

| | GEMM | GEMV |
|---|------|------|
| 算子 | C = A × B | y = A × x |
| 输入维度 | A: M×K, B: K×N | A: M×N, x: N |
| 输出维度 | C: M×N | y: M |
| 内部累加次数 | 每个 C_ij 累加 **K** 次 | 每个 y_i 累加 **N** 次 |
| 计算量 | **O(M·N·K)** | **O(M·N)** |
| **关键差异** | K 是"复用维度"（reusable dim）| 无复用维度 |

**GEMM 中 K 维度的"复用"**：A 的同一行 (A_i*) 被用来计算 C 的**整行**；B 的同一列 (B_*j) 被用来计算 C 的**整列**。**同一份数据被用 K 次**。

**GEMV 没有 K 维度**：x 加载一次，用 N 次（每次一个 y_i）；**没有 K 维的复用**。

## 2. 算术强度（Arithmetic Intensity）

**算术强度 AI = FLOPs / Bytes loaded**（单位：FLOPs/byte），是判断 kernel 类型的核心指标。

### GEMM 的 AI

```
Y = X @ W  (X: B×d, W: d×F, Y: B×F)
- FLOPs = 2·B·d·F
- Bytes loaded (W 读 1 次, X 读 1 次) = B·d + d·F (FP16: 乘 2)
- AI = 2·B·d·F / (2·(B·d + d·F)) ≈ B (当 d ≫ B, F)
```

| Batch B | AI (FLOPs/byte) | 类别 |
|---------|----------------|------|
| B=512 (prefill 中 prompt) | **~500** | **compute-bound** |
| B=64 | ~64 | compute-bound |
| B=8 (decode 中 batch) | **~8** | 临界（接近 ridge point）|
| B=1 (decode 单 token) | **~1** | **bandwidth-bound** |

### GEMV 的 AI（**几乎永远是 ~2**）

```
y = W @ x  (W: M×N, x: N)
- FLOPs = 2·M·N
- Bytes loaded = M·N + N (W 读 1 次)
- AI = 2·M·N / (M·N + N) ≈ 2
```

**GEMV 无论矩阵多大，AI 几乎恒为 2**。这是它的"诅咒"——**永远 bandwidth-bound**。

### Roofline 一图说清楚

H100 算力 ~989 TFLOPS (FP16) ÷ 内存带宽 ~3.35 TB/s = **ridge point ~295 FLOPs/byte**

| Kernel | AI | Roofline 位置 | 实际性能 |
|--------|-----|------------|---------|
| GEMM B=512 | ~500 | 远离 ridge，**compute-bound** | **~70% peak FLOPS**（tensor core 吃饱）|
| GEMM B=8 | ~8 | 接近 ridge | ~10-20% peak FLOPS |
| **GEMV B=1** | ~2 | **深陷 bandwidth-bound** | **<1% peak FLOPS**（~10 TFLOPS 等效）|

> 💡 **H100 跑 GEMV 时实际算力利用率 < 1%**：硬件设计为 989 TFLOPS，但 GEMV 实际只能跑 ~10 TFLOPS 的"等效"算力。这就是 LLM decode "看似简单却跑不快"的根本原因。

## 3. 为什么 Prefill = GEMM，Decode = GEMV

### Prefill 阶段

```
输入：N 个 prompt token (B = N, e.g. 512-8192)
- QKV projection: X[B×d] @ W[d×3d] → QKV[B×3d]   ← GEMM
- Attention: Q[B×d] @ K^T[d×B] → S[B×B]           ← GEMM
- Softmax + Attn: S[B×B] @ V[B×d] → O[B×d]        ← GEMM
- FFN: X[B×d] @ W1[d×4d] → H[B×4d]                ← GEMM
```

**B = prompt length N（数百到数千）** → AI 数百到数千 → **compute-bound**，tensor cores 满载。

### Decode 阶段

```
输入：1 个新 token (B=1)
- QKV projection: x[1×d] @ W[d×3d] → qkv[1×3d]   ← **GEMV**
- Attention: q[1×d] @ K^T[d×N] → s[1×N]           ← **GEMV**
- Attn: s[1×N] @ V[N×d] → o[1×d]                  ← **GEMV**
- FFN: x[1×d] @ W1[d×4d] → h[1×4d]                ← **GEMV**
```

**B = 1** → AI ≈ 2 → **memory-bandwidth-bound**，99% 时间在等 HBM 读权重。

### 一个 LLaMA-7B 具体数字对比（d=4096, F=11008 FFN）

| 阶段 | 输入 | FLOPs | 读 Bytes (FP16) | AI | 类别 |
|------|------|-------|---------------|-----|------|
| **Prefill (B=512)** | X: 512×4096 | 4.6 × 10¹⁰ | ~95 MB | **484** | compute |
| **Decode (B=1)** | x: 1×4096 | 9.0 × 10⁷ | **~90 MB** | **1.0** | **bandwidth** |

**算术强度差 ~500 倍**。同一矩阵乘法 W，在 prefill 是 compute-bound、在 decode 是 bandwidth-bound。

## 4. 执行时间与功耗的实际差异

### 4.1 时间差异（理论 vs 实际）

**理论计算时间**（假设利用率 100%）：

| 阶段 | FLOPs | H100 FP16 算力 | 理论时间 |
|------|-------|---------------|---------|
| Prefill (B=512, 1 layer FFN) | 4.6×10¹⁰ | 989 TFLOPS | 0.046 ms |
| Decode (B=1, 1 layer FFN) | 9×10⁷ | 989 TFLOPS | 0.091 μs |

**实际时间**（考虑硬件瓶颈）：

| 阶段 | 实际时间 | 限制因素 | tensor core 利用率 |
|------|---------|---------|------------------|
| Prefill (B=512) | ~0.05-0.1 ms | compute | ~70% |
| **Decode (B=1)** | **~5-10 ms** | **HBM 3.35 TB/s 带宽** | **<1%** |

**decode 比 prefill 慢 ~100× 不是因为 FLOPS**——FLOPS decode 比 prefill 小 500 倍，但 prefill 跑 0.1 ms、decode 跑 5 ms，**实际 decode 慢 50×**。**根因是 7B 权重 = 14 GB FP16，HBM 带宽 3.35 TB/s → 至少 4.2 ms 读一遍**。

### 4.2 功耗差异（隐藏但关键）

**H100 整卡 ~700W TDP**，但内部功耗分布：

| 组件 | Prefill 功耗 | Decode 功耗 |
|------|-------------|------------|
| Tensor cores | ~300W（满载）| ~3W（<1% 利用率，但漏电 ~3W）|
| HBM3e | ~10-20W | ~10-20W（**仍在跑带宽**）|
| 其他（PCIe, NVLink, control）| ~50W | ~50W |

**decode 期间 HBM 是"满载跑带宽"的状态**——读 14 GB 权重花了 5 ms，**HBM 在这 5 ms 内全速工作，功耗跟 prefill 一样**。但 tensor cores 闲置 → **每 token 能效比 prefill 差 50-100×**。

### 4.3 一个直觉

| | Prefill | Decode |
|---|---------|--------|
| 类比 | 工厂批量生产 (production line 满载) | 顾客单件定制 (产能闲置) |
| tensor core 利用率 | 70% | <1% |
| 等待什么 | 几乎不等待 | 99% 时间等 HBM |
| 实际算力 | 989 TFLOPS | ~10 TFLOPS 等效 |
| 单 token 成本 | 低（能效高）| 高（能效低 50-100×）|
| 优化方向 | 算力大、并行高 | 内存大、带宽高 |

## 5. 加速器视角的差异

### 5.1 传统 GPU（H100 / MI300X）

- **Prefill**：HBM 大（80-192 GB），tensor core 满载，**GEMM 是甜点**
- **Decode**：tensor core 闲置，靠 HBM 带宽撑 → **GROQ/WSE/TPU 这类 memory-centric 架构天然占优**

### 5.2 Groq LPU（deterministic pipeline）

- 230 MB SRAM **装下**小模型权重
- Decode 时权重在 SRAM 里**不被搬运**，**没有 HBM bandwidth 限制**
- 算力虽然小，但 decode 延迟稳定 sub-ms → **LLM serving 优势明显**

### 5.3 Cerebras WSE / WaferLLM

- 44 GB SRAM 装下大模型
- **Prefill**：MeshGEMM（2-hop cyclic shift）解决 GEMM 通信
- **Decode**：MeshGEMV（K-tree allreduce）解决 GEMV 在 mesh-NoC 上的 allreduce
- 论文承认 decode **5× underutilization**，**本质是 GEMV 在 mesh 上通信密集 + K=2 硬编码**

### 5.4 数据流架构（SambaNova SN40L, FPGA LoopLynx）

- 都面临 GEMV **dataflow 流水线在串行 decode 上不连续**的问题
- 解决思路：
  - SN40L：**编译器全自动融合** 数百 op
  - LoopLynx：**hybrid spatial-temporal** + state-machine scheduler
  - TileLoom（Tenstorrent）：**MLIR spatiotemporal dataflow planning**

## 6. 编译器优化空间（Direction 2 视角）

**GEMV 的"特殊性"决定它是 compiler 的主要战场**：

1. **Routing-aware placement**（Gap 5 of [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md)）
   - GEMV 没有 K 维复用 → **每个输出 y_i 都要 broadcast W 的不同行**
   - 在 mesh-NoC 上，**placement 决定哪些 y_i 共享哪些 W**
   - 编译器可做 routing budget-aware placement

2. **K-tree allreduce auto-search**（Gap 3）
   - K=2 硬编码 → 不同 (N, R) 应该有不同最优 K
   - 编译器 cost model 自动搜 K

3. **Persistent kernel + 2D KV shift**（Gap 1, 4）
   - 48KB SRAM 装不下 GEMV 的 working set → persistent kernel 减少重载
   - GQA head 维度不均 → 2D shift

4. **Flat GEMM with M-pad heuristic**（[FlashDecoding++](/concepts/flashdecoding-plus-plus.md) 思路）
   - 中等 batch（B=8）时是 GEMV 还是 GEMM 并不明显
   - 编译器 runtime heuristic 决定走哪条 kernel

5. **Speculative decode / multi-token decode**
   - [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) 等：把"多步 GEMV"变成"少步 GEMM"——直接绕过 GEMV 的 bandwidth 限制

## 7. 一句话总结

> **GEMM 是 LLM 的"算力代表"**（Prefill、训练），**GEMV 是 LLM 的"带宽代表"**（Decode、推理）。LLM 推理 99% 时间在 GEMV，**所以"加速 LLM 推理"本质上是"加速 GEMV 在现代加速器上的执行"** —— 这就是所有 LLM serving 系统优化（vLLM / FlashDecoding++ / WaferLLM / Groq）的核心战场。

## 相关页面

- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 两阶段资源正交的本质原因
- [WaferLLM System](/concepts/waferllm-system.md) — MeshGEMV + K-tree allreduce
- [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md) — GEMV 在编译器视角的 6 个 open problem
- [FlashDecoding++](/concepts/flashdecoding-plus-plus.md) — GPU 上的 flat GEMM/GEMV hybrid kernel
- [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md) — GEMM 的分布式算法谱系（Cannon/SUMMA）
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — MoE 推理的 single-kernel 融合
- [DRAM and Memory System](/concepts/dram-memory-system.md) — HBM 带宽与 memory wall
- [Roofline Model](/concepts/architecture-benchmark-methodology.md) — Roofline 模型基础
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 用算法层减少 GEMV 步数
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 上 GEMV 的 82× vs A100
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — Tenstorrent 上 dataflow 编译

# Citations

[1] [raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf](raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf) — Hong et al., arXiv:2311.01282 (2024) — flat GEMM/GEMV hybrid 思路
[2] [concepts/prefill-decode-divergence.md](concepts/prefill-decode-divergence.md) — Prefill/Decode 资源分歧核心数据
[3] [concepts/waferllm-system.md](concepts/waferllm-system.md) — MeshGEMV 在 WSE 上的实现
