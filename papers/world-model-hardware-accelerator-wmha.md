---
type: Paper
title: "The World Model Hardware Accelerator (WMHA)"
description: 独立研究 — DiT/世界模型 VLIW 加速器；MSE×23、2.37e8 零失败；sky130 综合 68.4 mm²；调度重构 1.484×
tags:
- accelerator
- architecture
- pipeline
- attention
- inference
- llm
- agentic-ai
- dataflow
- isa
- sram
- hardware
timestamp: '2026-09-17T00:00:00Z'
created: 2026-09-17
updated: 2026-09-17
sources:
- raw/papers/World_Model_Hardware_Accelerator_WMHA_2026.pdf
- raw/papers/world-model-hardware-accelerator-wmha.md
---

# The World Model Hardware Accelerator (WMHA)

**Author:** Shashank Chaurasia
**Affiliation:** Independent / self-funded（文内声明）
**arXiv:** [2609.16244](https://arxiv.org/abs/2609.16244)（2026-09-14，cs.AR）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.16244)

面向 **diffusion transformer / 世界模型** 推理：每去噪步是完整序列前向、形状编译期已知，串行维仅是步数。WMHA 用 **VLIW + weight-stationary 阵列 + online-softmax** 做成 latency-first 加速器，并走通 sky130 开源物理流与 **语义验收门**（真实去噪轨迹 MSE）。

## 动机

自回归 decode 的 token 递推不适用于 DiT：步内可全并行调度；若每步回 host 做 modulation/guidance，互连吃掉 latency。世界模型/机器人/视频生成等 agentic 感知–行动环需要短步延迟。

## 方案

- **256-bit VLIW**：四引擎槽（array / VPU / DMA LD / DMA ST）+ wait mask；控制开销文内测 **9 cycles/字**。
- **16×16 dual-dot** weight-stationary；**FP8 E4M3 / BF16**，FP32 累加。
- **Single-pass online-softmax** attention；skewed software pipeline 保 K/V 驻留。
- **UVM** 对 double-precision replay；验收：元素失败=0 + 轨迹 MSE 相对噪声至少 **÷10**。
- 物理：sky130；五引擎 routed+parasitic；全芯片 synthesis-only（host P&R 天花板）。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 语义门 | MSE 压低因子 **23**（两配置）；**2.37×10⁸** 元素零失败 |
| 仅重排指令调度 | ≥2 引擎并发 **1.83%→44.66%** cycles；加速 **1.484×** |
| 全芯片综合 | **5.77 M** cells、**68.355 mm²**（无 dense SRAM macro） |
| PE cell | **0.05 mm²**；post-route 例 PE **153.4 MHz / 8.03 mW**，epilogue **76.7 MHz / 172 mW** |

**口径：** 开源 PDK、存储综合为 flop，面积/频率勿直接对标先进节点商用 NPU；DiT/视频/机器人形状基准，非 LLM decode。

## 与 wiki 的关系

- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 阵列数据流对照（本文 dual-dot + VLIW）
- [FlashAttention-3](/concepts/flashattention-3.md) — online-softmax 族谱对照
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — 步内静态形状 vs decode GEMV
- [UNISON](/papers/unison-near-memory-scheduler-llm-agents.md) / [PipeSwift](/papers/pipeswift-pipeline-parallel-agentic-serving.md) — agentic 栈另一侧（KV/serving vs 世界模型算子）

## 开放问题

1. 有 compiled memory 的先进节点上，68 mm² 中存储主导项如何收缩。
2. 与自回归 LLM 同片异构时，VLIW 静态调度是否仍成立。
3. 多步采样与 CFG 批处理的片上 residency 上限。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.16244) — Chaurasia, arXiv:2609.16244
[2] [raw/papers/world-model-hardware-accelerator-wmha.md](raw/papers/world-model-hardware-accelerator-wmha.md) — ingest stub
