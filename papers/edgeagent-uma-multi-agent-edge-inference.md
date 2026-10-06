---
type: Paper
title: "EdgeAgent: On-Device LLM Inference for End-User Multi-Agent Systems on CPU-GPU UMA"
description: "中山大学+中国移动（ASPLOS'27）— 端侧多智能体在 Apple M4 UMA 上：零拷贝 CPU–GPU TP + SME2 kernel（vs Batch-SD 1.29×）、按可预测性动态草稿预算、工具停顿 suspend-and-yield；极端工具延迟下 makespan 1.77×"
tags:
- agentic-ai
- ai-agent
- inference
- decode
- speculative-decoding
- memory-bandwidth
- memory
- cpu
- gpu
- scheduling
- hardware
created: 2026-10-06
updated: 2026-10-06
timestamp: '2026-10-06T00:00:00Z'
paper_author: [Yuhai Long, Yuanxin Wei, Kai Wu, Jinhui Wei, Dan Huang, Jiangsu Du]
year: 2026
arxiv: '2610.03394'
venue: "ASPLOS '27"
sources:
  - raw/papers/EdgeAgent_UMA_Multi_Agent_Edge_Inference_2026.pdf
  - raw/papers/edgeagent-uma-multi-agent-edge-inference.md
---

# EdgeAgent：端侧 UMA SoC 上的多智能体 LLM 推理

## 一句话结论

端侧多智能体（编排者 + 代码/工具 worker）在 CPU–GPU 共享内存（UMA）的 SoC 上有三重浪费：decode 阶段 CPU/GPU 同时读权重会 **抢同一条内存总线**；静态投机草稿长度在难以预测的推理任务上 **白耗带宽**；工具调用停顿让 **批槽闲置**。EdgeAgent 跨层协同：零拷贝 UMA 张量并行 + SME2 micro-kernel（相对 Batch-SD **1.29×**），按实时可预测性分配草稿预算，工具停顿时挂起让出；在 [1,100] s 极端工具延迟下 makespan **1.77×**（213.1 s → 120.6 s）。

## 动机

- **UMA 内存墙**（Apple M4，120 GB/s）：小矩阵 4096×4096 时 CPU+GPU 共跑 vs GPU **1.36×**；大矩阵 4096×128256 时 GPU 已用到 >**80%** 峰值带宽，共跑仅 **0.99×**——decode 期异构 TP 几乎无收益。
- **草稿难度差异**：DeepSeek-R1-Distill-Llama-8B 上，结构化输出任务投机加速峰值 **1.69×**，推理任务在更短草稿长度即饱和后退化；而现有 SD 对整批用统一草稿长度。
- **图编译器限制**：DAG 执行器无法表达对同一共享张量的异步正交写，被迫同步 + 显式拷贝，抵消 UMA 零拷贝。
- **工具停顿**：agent 调用外部工具时其投机预算无法转给其他 agent。

## 方案

1. **UMA-aware 执行层**：改造 MLX C++ 图执行器，CPU/GPU 按输出列（N 维）切分权重做无锁零拷贝 TP；CPU 分片初始化时预打包为 SME **16×64 FP16** tile（打包耗时 M4 13–16 s、M4 Pro 6.2 s，< makespan 5%）。
2. **HAL 调度**：按实时序列可预测性为每个 agent 动态分配草稿预算（EAGLE-3）。
3. **Suspend-and-yield**：工具调用时异步驱逐停顿 agent、就地回收验证槽。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 平台 | Apple M4（32 GB，120 GB/s UMA，4P+6E CPU 含 SME2，10 核 GPU）；M4 Pro（64 GB，273 GB/s，10P+4E，20 核 GPU） |
| 纯代码生成，N=4 | 全局吞吐 **33.6 tok/s**（DeepSeek）/ **28.0 tok/s**（Llama）= **1.29×** vs Batch-SD |
| HAL 调度额外 | **1.05–1.17×** |
| 推理+代码混合 | **1.33×** vs Batch-SD |
| 工具停顿 [1,100] s，N=4（DeepSeek） | makespan **213.1 s → 120.6 s（1.77×）** |
| 零拷贝 TP（4096×14336 投影） | 稳定 ~**1.14×**；M=128 时同步开销 +0.90 ms → +0.04 ms，**1.31×** |
| SME kernel | decode 形状 **85.0 GFLOPS**（vs BNNS **4.47×**）；prefill >**90%** 的 2.3 TFLOPS，vs BNNS **3.24×** |
| 动态草稿预算 | vs 静态 **1.12×** |

## 与 wiki 的关系

- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 端侧 SoC 上 CPU+GPU 共享带宽的异构推理，和数据中心 CPU 卸载（RapidMoE）相对照
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — prefill 计算受限可聚合算力，decode 带宽受限共跑无益
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 投机解码；本文把草稿预算做成 per-agent 资源
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — agentic serving 的工具停顿/KV 驻留问题（PipeSwift、Ask the Tool 等）在端侧的版本

## 局限与开放问题

- 负载为合成 trace（LongBench/MBPP/ToolBench 按 1:2:2 混合 + log-uniform 停顿），非真实 agent 框架端到端。
- 只在 Apple M 系列（SME2）验证；Snapdragon/联发科 NPU+GPU+CPU 三方 UMA 竞争未覆盖。
- 硬件启示：端侧 agent 芯片是否需要 UMA 带宽 QoS / 分区（让 CPU 侧验证或草稿不与 GPU 抢带宽）？

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.03394) — Long et al., arXiv:2610.03394（ASPLOS '27）
[2] [raw stub](raw/papers/edgeagent-uma-multi-agent-edge-inference.md)
