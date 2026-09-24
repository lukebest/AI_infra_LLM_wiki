---
type: Raw Source
title: "Decoupling Logical Masks from GPU Execution for Dynamic Block-Sparse Attention"
description: "NUS Tessera — 逻辑 mask 与物理 tile 解耦；vDiT BSA 请求最高 6.79×；720p 50-step 环 1.22–2.08×。"
timestamp: '2026-09-24T00:00:00Z'
source_url: https://arxiv.org/abs/2609.25869
arxiv: '2609.25869'
ingested: 2026-09-24
sha256: 0e00594ddc8e640f6091acf70713bcd4457f46406a710d783ee6ca84c3bcd0e4
---

# Tessera: Decoupling Logical Masks from GPU Execution for Dynamic Block-Sparse Attention

**Authors:** Shanghao Liu, Xiaoyun Yu, Wanting Li, Wenqi Jiang  
**Affiliation:** National University of Singapore  
**PDF:** [Tessera_Dynamic_Block_Sparse_Attention_2026.pdf](Tessera_Dynamic_Block_Sparse_Attention_2026.pdf)  
**arXiv:** [2609.25869](https://arxiv.org/abs/2609.25869)（2026-09-22，cs.AR）

## 问题

视频 DiT 的动态 block-sparse attention（BSA）把逻辑块几何绑死在执行策略上，难适配变化 mask 与多代 GPU；运行时特化开销可抵消执行收益。

## 方法要点

1. **物理映射层**：保留/合并/细分逻辑块 → 适配 mask 与架构的物理 tile。  
2. **任务组织层**：tile 分组调度，复用数据、暴露并行、重叠搬运。  
3. **Profile-guided regime**：离线剖析表 + 低开销在线选型；四代 NVIDIA GPU 专用 CUDA catalog。

## 摘录数字（仅论文给出）

- 2,315 真实 mask + 工业 vDiT：BSA 请求最高 **6.79×**。
- 相对基线 geomean：FlashInfer **1.85–5.11×**；FlexAttention **1.62–33.73×**；flex-block-attn **3.96×**；四平台 **1.12–6.38×**。
- HunyuanVideo 720p 五秒：attention **2.95–6.79×**；完整 50-step 扩散环 **1.22–2.08×**。
- 消融：相对 Direct 固定映射，物理映射 geomean kernel **≈1.38×**（文 1.379×）；任务组织 H100 **1.105×**。

**Working page:** [Tessera](/papers/tessera-dynamic-block-sparse-attention.md)
