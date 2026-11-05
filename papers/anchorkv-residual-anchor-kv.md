---
type: Paper
title: "AnchorKV: Lossless KV Reconstruction from Layer-Sparse Residual Anchors"
description: "西南交大 — 残差锚点无损重建 KV；cascade 最高 16.3×，32k 可再激活容量 5.78–54.0× full-KV"
tags:
- kv-cache
- inference
- serving
- llm
- compression
- memory
- attention
created: 2026-11-05
updated: 2026-11-05
timestamp: '2026-11-05T00:00:00Z'
paper_author: [Hao Li, Jiashu Zhang, Kaleem Ullah Qasim, Heying Zhang]
year: 2026
venue: arXiv
arxiv: '2611.00117'
sources:
  - raw/papers/AnchorKV_Residual_Anchor_KV_Reconstruction_2026.pdf
  - raw/papers/anchorkv-residual-anchor-kv.md
---

# AnchorKV：层稀疏残差锚点的无损 KV 重建

## 一句话结论
按层缓存 residual 再投影 KV 在 MHA 上省内存，但在 GQA 等现代结构上 𝜌layer=𝑑/(2𝑛𝑘𝑣 𝑑head) 可落在 **0.50–3.50**，𝑠=1 反而更费。AnchorKV 把「每层 residual」到「整网单向量 checkpoint」连成可配置间距 𝑠 的 storage–replay 谱；break-even 𝑠⋆=⌊𝜌layer⌋+1 只依赖 config。Cascade 重放把复杂度从 𝑂(𝐿𝑠) 降到 𝑂(𝐿)（24 层 Qwen2.5：**276→23**）；4k 上下文 cascade 相对 naive 最高 **16.3×**；32k 最深间距八模型可再激活会话容量 **5.78–54.0×** full-KV，且 bit-exact。

## 动机
- 有损驱逐/量化改输出；无损 residual 路线的内存优势依赖架构。
- 𝑠=1（activation checkpoint）与 𝑠=𝐿（KV-Direct）两端已知，中间工作点与放置规则缺谱系化。
- 交错滑窗注意力的重建需求非均匀，均匀间距不是最优。

## 方案
1. **Break-even 规则**：由 config 算 𝜌layer 与首个省存间距 𝑠⋆。
2. **Cascade replay**：段内共享中间 residual，把块执行从 𝑂(𝐿𝑠) 收到 𝑂(𝐿)。
3. **精确 DP 放置**：交错滑窗等非均匀需求下最小化 cascade 代价。
4. **后端**：CPU / CUDA / Ascend NPU；fp32/bf16；六架构族、十二 checkpoint 验证 bit-exact。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 𝜌layer 跨族跨度 | **0.50–3.50** |
| Cascade vs naive（4k，最高） | **16.3×**（九模型另报 **7.17–16.25×**） |
| 24 层 Qwen2.5 块执行 | **276→23** |
| 32k 最深间距可再激活容量 | **5.78–54.0×** full-KV |
| Bit-exact | max \|ΔK\|=max\|ΔV\|=**0** |
| Gemma-3-1B DP 放置 | 重放 18→0；中位 **60.64→5.52 ms** |

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 页式 KV 驻留；AnchorKV 用残差锚点换可再激活容量，保持无损
- [RISK-KV](/papers/risk-kv-selective-reconstruction.md) — 跨层重建可省略历史 KV（有损边界不同）；AnchorKV 钉 bit-exact
- [ZipFusion](/papers/zipfusion-lossless-kv-attention-fusion.md) — 无损压缩态直接喂 attention；AnchorKV 无损重建路径走 residual replay
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 会话级「驻留 vs 再激活」容量交易

## 开放问题
- 与生产前缀缓存 / PD 解耦全局池的调度接口（何时 cascade、何时保留全 KV）仍待系统化。
- 超深模型与投机解码叠加时的 cascade 延迟尾部分布需更多后端实测。

# Citations
- [arXiv:2611.00117](https://arxiv.org/abs/2611.00117) — Li, Zhang, Qasim, Zhang, Southwest Jiaotong University, 2026
- [raw stub](/raw/papers/anchorkv-residual-anchor-kv.md)
