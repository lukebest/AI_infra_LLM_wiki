---
type: Paper
title: "Tessera: Logical Mask ↔ Physical Tile for Dynamic BSA"
description: "NUS — 解耦逻辑 mask 与 GPU 执行；vDiT BSA 最高 6.79×；720p 50-step 环 1.22–2.08×"
tags:
- architecture
- gpu
- attention
- sparse
- llm
- inference
- serving
- throughput
created: 2026-09-24
updated: 2026-09-24
timestamp: '2026-09-24T00:00:00Z'
paper_author: [Shanghao Liu, Xiaoyun Yu, Wanting Li, Wenqi Jiang]
year: 2026
arxiv: '2609.25869'
sources:
  - raw/papers/Tessera_Dynamic_Block_Sparse_Attention_2026.pdf
  - raw/papers/tessera-dynamic-block-sparse-attention.md
---

# Tessera: Decoupling Logical Masks from GPU Execution for Dynamic Block-Sparse Attention

## 一句话结论

Tessera 把 BSA 的**逻辑 mask**与 **GPU 物理 tile/任务组织**解耦，并用剖析表低开销选型：在 2,315 真实 mask 与工业视频 DiT 上，BSA 请求最高 **6.79×**；HunyuanVideo 720p 的 50-step 环 **1.22–2.08×**。

## 动机

- 视频 DiT 注意力占墙钟大部分；BSA 用逻辑块 mask 降算力，但 mask 随请求/头/层/去噪步变化。
- 固定内核绑死逻辑几何 → 跨 mask/GPU 次优；编译式特化 → 准备开销吃掉收益。

## 方案

1. **物理映射**：Direct / 合并 / 细分逻辑块 → 物理 tile。
2. **任务组织**：tile 成任务，复用、并行、重叠搬运。
3. **Regime 表**：离线剖析桶 → 在线查表；四代 NVIDIA 本地 CUDA catalog。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| BSA 请求最高加速 | **6.79×** |
| vs FlashInfer / FlexAttention / flex-block-attn | geomean **1.85–5.11×** / **1.62–33.73×** / **3.96×** |
| 四平台 vs 基线 | **1.12–6.38×** |
| HunyuanVideo 720p：attention / 50-step 环 | **2.95–6.79×** / **1.22–2.08×** |
| 消融：映射 / 组织 | vs Direct **≈1.38×**；H100 组织 **1.105×** |

**口径：** 视频 DiT BSA runtime（非 LLM 文本服务）；工作负载与 [SPLASH](/papers/splash-sparse-attention-hbf.md) 的 LLM 稀疏×HBF 正交。

## 与 wiki 的关系

- [FlashAttention-3](/concepts/flashattention-3.md) / [GPU SIMT](/concepts/gpu-simt-architecture.md) — 稠密/稀疏执行层对照
- [SPLASH](/papers/splash-sparse-attention-hbf.md) — LLM 稀疏×内存层次；本文是 **GPU runtime×动态 mask**
- [Vortex](/papers/vortex-extreme-compression-llm-inference.md) — 稀疏/压缩推理加速器侧对照

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.25869) — Liu et al., NUS, arXiv:2609.25869
[2] [raw stub](raw/papers/tessera-dynamic-block-sparse-attention.md)
