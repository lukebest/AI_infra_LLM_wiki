---
type: Paper
title: "Meta × AMD: End-to-End Co-Design for AI Training on MI350X"
description: "Meta/AMD MICRO'26 — 首份超大规模厂商 AMD GPU 生产训练报告：模型-硬件协同（吃满 1.6× HBM）、Origami 解析 GEMM 选型（93%）、agent 化 kernel 移植；直接移植基线上端到端最高 1.5×，十个生产模型几何均值 101.2% of B200"
tags:
- gpu
- amd
- meta
- nvidia
- training
- training-system
- recommendation
- kernel
- collective
- chiplet
- hbm
- agentic-ai
- power
created: 2026-10-19
updated: 2026-10-19
timestamp: '2026-10-19T00:00:00Z'
paper_author: [Haoyu Zhang, Arshad Rahman, Adnan Aziz, "...", Ajit Mathews, Chunqiang Tang]
year: 2026
venue: MICRO 2026
arxiv: '2610.22230'
sources:
  - raw/papers/Meta_AMD_MI350X_Training_CoDesign_MICRO26.pdf
  - raw/papers/meta-amd-mi350x-training-codesign.md
---

# Meta × AMD：MI350X 上的端到端训练协同设计

## 一句话结论
Meta 把 DLRM 生产训练搬到数万张 MI350X 上，方法论有三条：按新硬件的长处改模型和训练配方；用解析模型零预热挑 GEMM tile；把 kernel 调优经验写成 agent 工作流。十个生产模型端到端吞吐几何均值达到 B200 的 **101.2%**，相对直接移植基线最高 **1.5×**。

## 动机
- DLRM 形态杂：kernel 碎、矩阵形状不规则、访存不规则，NVIDIA 专属优化积累深，直接 hipify 性能差。
- 硬件差异实打实：wavefront 64 线程 vs warp 32；MI350X 8 个 XCD chiplet、无 TMA；B200 单 SM LDS 更大、scale-up 900 vs 538 GB/s。
- MI350X 的结构性长处是 HBM：288 GB vs 180 GB（**1.6×**）。

| 规格（Meta 部署） | MI350X | B200 |
|---|---|---|
| CU/SM | 256（8 XCD × 32） | 148（2 die） |
| BF16 dense | 2300 TFLOPS | 2250 TFLOPS |
| HBM | 288 GB / 8 TB/s | 180 GB / 8 TB/s |
| scale-up（单向） | 538 GB/s | 900 GB/s |
| 功耗/散热 | 1000 W 风冷 | 750 W 风冷 |

## 方案
1. **模型-硬件协同**：用多出的 HBM 加大 batch、关掉部分 activation checkpointing、加长序列/放大 hidden/扩 embedding 表；整体训练提速 **20%**，NE 改善 >**0.1%**。
2. **Origami 解析 GEMM 模型**：tile 计算时延 = 矩阵指令数 × 指令时延；按工作组共享建模 L2/LLC 命中率，扩展到多 chiplet（XCD 感知 workgroup ID swizzle，把相邻输出 tile 放同一 XCD）。微秒级给出 tile 配置，相对穷举 autotune 达到 **93%**。
3. **Agent 化 kernel 工作流**：把 occupancy hint、PID swizzle、MFMA 指令配置、专用硬件指令等经验编码为 skill；手写与编译器生成 kernel 上 **1.6–2×**；缺 ROCm 等价库时由 agent 生成 shim。
4. **通信与功耗**：RCCL 用 LL64 替代 LL128（128 B 写在 AMD 64 B cache line 上会拆开），AllGather/ReduceScatter **2×**、AllReduce **1.2–1.4×**；整体从「比 NCCL 慢 2×」拉到「差 10–15%」。OAM 允许 20 µs 内 2.0× TBP、20 ms 内 1.1× TBP 的瞬时功耗冲高，调控制环后合成 GEMM 负载最高 **1.33×**。

## 效果（论文数字）
- GDPA kernel：GeLU 快速数学 + occupancy + MFMA + PID swizzle，前向 1.47 → **0.59 ms**（58.4 → 145.9 TFLOP/s，2.5×），反向 3.67 → **2.17 ms**。
- HSTU kernel：前向 **3.22×**；按序列长度平均，MI350X 优化后比 B200 前向快 **1.22×**、反向快 **1.80×**。
- 原子操作：多 chiplet 原子需跨 XCD 一致性，高争用下 MI350X 可比 B200 慢 >**10×**；shared memory 树形归约在 20% 违例率下提速 **4.34×**，反超 B200 **1.75×**。
- 大 HBM：好友推荐模型 2×/4×/6× batch 提速 **26%/46%/51%**；GPT 模型在 B200 上必须激进 AC 才放得下，吞吐落后 **1.35×**。
- B200 仍占优处：GEMM，MI350X 时延高 **1.3–1.7×**（TF32 用 3 次 BF16 GEMM 仿真）。

## 核内非线性细节
GDPA 里的 GeLU：Triton 默认 tanh 近似在 AMD 上展开成 2σ(2x)−1，多一次 sigmoid 与额外算术；改为直接用 sigmoid 形式 GeLU，配合 `fast_expf`/`fast_dividef` 映射到单条硬件指令。另用 `tl.rsqrt()` 替代 libdevice 调用。见 [核内非线性运算加速](/concepts/in-core-nonlinear-operator-acceleration.md)。

## 与 wiki 的关系
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — wavefront 64、无 TMA 时浅流水（num_stages≈2）更优、多 chiplet 原子一致性
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — LL64 协议、Direct AllGather、P2P batching（128 GPU AllToAll −40%）
- [API-level memory model（rocSHMEM）](/papers/api-level-memory-model-multi-gpu-communication.md) — 同属 AMD 多 GPU 通信栈打磨
- [HC2026 AMD MI455X](/papers/hc2026-amd-instinct-mi455x.md)、[HC2026 Meta MTIA 400](/papers/hc2026-meta-mtia-400.md) — Meta 异构机群的另外两条腿

## 开放问题
- LLM 训练（>2,000 卡）结果作者留作后续；DLRM 结论能否平移到稠密 Transformer 尚未给数。
- GEMM 差距（TF32 无原生支持、hipBLAS 不规则形状成熟度）仍待硬件/库补齐。
- Agent 工作流成功率与回归风险的量化不充分。

# Citations
- Zhang et al., "Architecting for Hardware Diversity: Meta's End-to-End Co-Design for High-Performance AI Training on AMD GPUs", MICRO 2026, arXiv:2610.22230. [raw](/raw/papers/meta-amd-mi350x-training-codesign.md) · [PDF](/raw/papers/Meta_AMD_MI350X_Training_CoDesign_MICRO26.pdf)
