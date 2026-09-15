---
type: Raw Source
title: "Vortex: Bridging Extreme Compression and Efficient LLM Inference"
source_url: https://arxiv.org/abs/2609.12208
arxiv: '2609.12208'
ingested: 2026-09-15
sha256: fdb357851063daac3025f20237d91956c25323970adc63ce55f14934abcf7296
---

# Vortex: Bridging Extreme Compression and Efficient LLM Inference

**Authors:** Haoxuan Shan, Cong Guo, Bowen Duan, Chiyue Wei, Feng Cheng, Yuzhe Fu, Yintao He, Hai "Helen" Li, Yiran Chen
**Affiliations:** Duke University
**PDF:** [Vortex_Extreme_Compression_LLM_Inference_2026.pdf](Vortex_Extreme_Compression_LLM_Inference_2026.pdf)
**arXiv:** [2609.12208](https://arxiv.org/abs/2609.12208)（2026-09-10，cs.AR）

## 问题

VQ（codebook）+ 输入依赖稀疏在脉动阵列上难落地：码本查找冲突、dequant 开销；细粒度稀疏与 batched VQ 粒度错位。

## 方法要点

- 兼容脉动阵列的 **bi-flow**：Lookup-First (LUF) 适合 prefill（M≥16）；Multiply-First (MUF) 适合 decode（M<16）。
- 增量单元：LUU（码本查找）、QAU（运行时 KV 量化）、SPU（codebook-wise 上下文稀疏）。
- 算法：AQLM 风格 VQ（评测主配置 n=2, v=8, b=8）+ CQ 风格 KV 量化 + codebook-wise 稀疏阈值。

## 摘录数字（仅论文给出）

- 相对 SOTA 加速器端到端：**8.03×–23.7×** 加速、**5.68×–12.5×** 能耗降低。
- vs 常规脉动阵列平均 **22.4×** 加速 / **9.75×** 能耗；vs FIGLUT **8.03×**。
- 消融：权重量化 **11.33×** → +注意力量化至 **18.8×** → +稀疏至 **22.4×**。
- 芯片面积 **2.10 mm²**；相对 SA/ANT/FIGNA 面积效率 **11.9× / 10.1× / 4.42×**（文内场景）。
- 几何均值加速 **17.6×**、能耗降低 **7.39×**（相对 SA，跨模型）。
