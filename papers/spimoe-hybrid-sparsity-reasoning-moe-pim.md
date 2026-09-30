---
type: Paper
title: "SPIMOE: Hybrid Sparse Reasoning MoE on Heterogeneous PIM"
description: "北航 — ICCAD’26；SRAM-PIM+HBM-PIM；vs A100 端到端最高 8.35×（Qwen3-30B-A3B, b=8,s=256）；MoE FFN vs PIMoE 最高 3.33×"
tags:
- architecture
- accelerator
- llm
- inference
- moe
- attention
- sparse
- kv-cache
- pim
- hbm
- sram
- noc
- reasoning
- throughput
- latency
- memory
created: 2026-09-30
updated: 2026-09-30
timestamp: '2026-09-30T00:00:00Z'
paper_author: [Rubing Yang, Cenlin Duan, Yingjie Qi, Xiaolin He, Xiao Ma, Jianlei Yang]
year: 2026
arxiv: '2609.34612'
sources:
  - raw/papers/SPIMOE_Hybrid_Sparsity_Reasoning_MoE_PIM_2026.pdf
  - raw/papers/spimoe-hybrid-sparsity-reasoning-moe-pim.md
---

# SPIMOE: 推理 MoE 的异构 PIM 混合稀疏协同

## 一句话结论

把长推理 MoE 的 **Attention / Expert-FFN** 拆到 **SRAM-PIM + HBM-PIM**，并用自适应专家路由、block-sparse attention 与物理 KV 淘汰做混合稀疏；相对 A100 端到端最高 **8.35×**，MoE FFN 相对 PIMoE 最高 **3.33×**（ICCAD ’26）。

## 动机

- CoT 长推理使负载从 FFN 主导转向 **attention / KV 主导**；MoE 动态路由又带来不规则专家访问。
- 既有 PIM 工作多单独优化 MoE 或 attention，缺 **Attention–FFN 解耦 + 推理感知稀疏** 的端到端协同。

对照 [CARDAN](/papers/cardan-moe-scratchpad-dataflow.md)、[Weave](/papers/weave-dynamic-sm-moe-overlap.md)、[End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)、[DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md)。

## 方案

1. **算法**：自适应专家路由（含 cognitive expert boost / phase-depth 剪枝）；block-sparse attention；按 last-used 的物理 KV block 淘汰。
2. **硬件**：32× SRAM-PIM 核（Attention，800 MHz）+ 4× HBM-PIM 模块（QKV/FFN，bank PU 400 MHz）；2.5D interposer；**4×8 NoC** mesh（256-bit/flit @800 MHz）。
3. **映射**：静态专家映射（共激活 clique）+ 动态子批调度，使 Attention 与 MoE 路径流水重叠。
4. **评测**：Qwen3-30B-A3B、Phi-mini-MoE-instruct；基线 A100-80GB 与 PIMoE；系统级仿真（含扩展 DRAMsim3 / 12 nm 综合）。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 端到端 vs A100（b=8, seq=256） | Qwen3-30B-A3B **8.35×**；Phi-mini-MoE **7.08×** |
| 端到端 vs A100（seq length 2K，摘要/贡献） | 最高 **6.27×** |
| MoE FFN vs PIMoE | 最高 **3.33×**（Switch-Large-128 上随配置 **3.33×–2.03×**） |
| 精度 | 摘要：推理精度与 full-attention 基线可比 |

## 与 wiki 的关系

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — PIM 近存路径 vs HBM/HBF 分层
- [CARDAN](/papers/cardan-moe-scratchpad-dataflow.md) / [Weave](/papers/weave-dynamic-sm-moe-overlap.md) — GPU/DSA MoE；本文是 **异构 PIM**
- [MeshKV](/papers/meshkv-noc-kv-cache-fabric.md) — 片上 KV NoC；本文 NoC 服务 **Attention↔HBM-PIM**

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.34612) — Yang et al., ICCAD ’26, arXiv:2609.34612
[2] [raw stub](raw/papers/spimoe-hybrid-sparsity-reasoning-moe-pim.md)
