---
type: Paper
title: "SPLASH: HBF×稀疏注意力协同的长上下文推理"
description: "NUS — HBM+HBF 虚拟化 KV，稀疏注意力适配 HBF page/plane；100 ms TPOT 下每 GPU decode 吞吐相对基线 3.5–11.4×。"
tags:
- architecture
- hbf
- hbm
- kv-cache
- llm
- inference
- serving
- attention
- sparse
- memory-bandwidth
- packaging
- memory
created: 2026-09-23
updated: 2026-09-23
timestamp: '2026-09-23T00:00:00Z'
paper_author: [Aditya Anirudh Jonnalagadda, Agasthi Haputhanthri, Pranav Dangi, Rohan Juneja, Wenshuo Yue, Aritra Bagchi, Bin Gao, Tulika Mitra]
year: 2026
arxiv: '2609.23816'
sources:
  - raw/papers/SPLASH_Sparse_Attention_High_Bandwidth_Flash_2026.pdf
  - raw/papers/splash-sparse-attention-hbf.md
---

# SPLASH：稀疏注意力与 High-Bandwidth Flash 协同

## 一句话结论

SPLASH 把长上下文 KV 虚拟化到 **带宽相近的 HBM+HBF 层次**，并把稀疏注意力改成 HBF 友好的 **page 对齐 / 扫描隐藏 / plane 均衡**。在 100 ms 每 token 延迟目标下，每 GPU decode 吞吐相对评测基线 **3.5×–11.4×**，精度相对 dense 在 **4%** 内。

## 动机

HBM 带宽够但容量不够；host/CXL/SSD 容量够但带宽约低两个数量级。HBF 提供 TB 级容量与接近 HBM 的读带宽，但写寿命差、读以 flash page 为单位、靠数千 plane 聚合带宽——稀疏注意力若不协同设计会读废带宽。

## 方案

- **层次虚拟化**：新 KV 进 HBM，旧页迁 HBF，选中页经同一接口回读，对软件呈现一块逻辑内存。
- **稀疏×物理**：选择与注意力扫描按 page 对齐，隐藏页内扫描成本，并平衡 plane 并行。
- 容量动机：Qwen3-235B-A22B、64×1M 上下文约 **12.9 TB** KV（约填满 68 颗 B200 HBM）。

## 量化结果（十五组模型×上下文，100 ms p50 TPOT）

相对各系统自身满足 100 ms 前沿的配置，SPLASH 几何均值吞吐：

| 基线 | SPLASH / 基线 |
|------|----------------|
| HBM-only | **11.4×** |
| H3 | **9.3×** |
| FlashAccel-CLI | **6.4×** |
| FlashAccel-CSI | **5.8×** |
| LongSight-HBF | **3.5×** |

摘要汇总区间即为 **3.5×–11.4×**；长上下文套件精度相对 dense **within 4%**。

## 局限与解读

与 [HBFlex](hbflex-flexible-memory-hbf-llm.md)（主张去掉 HBM、全 HBF 服务动态 KV）对照：SPLASH 保留 HBM 作热层，重点是稀疏读路径与 HBF 物理属性对齐。与 [Trillion MoE HBF](trillion-param-moe-hbf-memory-provisioning.md)、[Fathom](fathom-sparse-decoding-offloaded-kv.md) 同属 [End-to-End Memory Data Path](../concepts/end-to-end-memory-data-path.md) 上的 HBF/卸荷叙事。

# Citations

1. Jonnalagadda et al. “SPLASH: Co-Designing Sparse Attention with High-Bandwidth Flash for Efficient Long-Context Inference.” arXiv:2609.23816, 2026. [arXiv](https://arxiv.org/abs/2609.23816)
2. [本地原文 PDF](../raw/papers/SPLASH_Sparse_Attention_High_Bandwidth_Flash_2026.pdf)；[原始来源记录](../raw/papers/splash-sparse-attention-hbf.md)
