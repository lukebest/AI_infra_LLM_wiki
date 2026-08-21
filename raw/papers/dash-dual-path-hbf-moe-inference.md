---
type: Raw Source
title: DASH Dual-Path HBF for MoE LLM Inference
source_url: https://arxiv.org/abs/2608.14333
arxiv: '2608.14333'
ingested: 2026-08-21
sha256: 3dfdba5c55572f26ac0e7636a27f582984a227015b2141594061c708459697c6
---

# Beyond Capacity: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths

**Authors:** Seeyeon Kim, Juhyeong Jin, Joo-Young Kim（KAIST）
**PDF:** [DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf](DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf)
**arXiv:** [2608.14333](https://arxiv.org/abs/2608.14333)（2026-08-14）

## 问题

MoE 专家权重 281 GB–1.5 TB，占权重 94.1–98.8%，单卡 HBM 装不下。既有 HBF 方案走 GPU–HBM–HBF 级联，直连 GPU–HBF 闲置；NAND t_R 在路由之后暴露，decode 细粒度写撞 t_PROG。

## 方法要点

- 三条 UCIe 3.0 路径：GPU–HBM、GPU–HBF、HBM–HBF。每路径 4-module UCIe-A @64 GT/s，建模可用 1.6 TB/s/向。
- HBF 经 HBM 基座 SRAM 中继到 GPU，**不进** HBM 阵列。Direct + Relay 并发，整 expert 派给其中一条。
- 无偏置 router 把 RMSNorm 缩放提出，top-k 可在 attention 输出后立刻确定（与常规路由同序）；DeepSeek-V3 类带偏置仍走晚选择。
- Prefill KV 直写 HBF；decode KV 在 HBM 聚页再回写。权重与 KV 分 erase-block。

## 摘录数字（仅论文给出）

- 摘要代表负载：相对 RelayOnly 吞吐 **1.94×**、E2E **1.90×**。
- 五模型×四 batch 几何均值吞吐：vs RelayOnly **1.90×**、vs DirectOnly **1.84×**；E2E 降 **42.2% / 40.8%**。
- Qwen3 连续批 75% 负载 P90 E2E 相对 RelayOnly/DirectOnly 降 **53.5% / 53.3%**。
- Lookahead 在 t_R=3 μs：Qwen3/DeepSeek-V2 E2E **−3.33% / −1.99%**；32 μs 时 **−9.50% / −8.69%**。
- 事件驱动 serving 仿真 + H100 实测算子时延，非硅。
