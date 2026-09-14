---
type: Summary
title: AI Infra Book Ch.4 Accelerators
description: 第4章加速器—Roofline 时间模型、存储层次、封装互联、NVIDIA/昇腾/Apple/TPU/Groq/WSE
tags:
- book
- accelerator
- gpu
- hbm
- memory-bandwidth
- architecture
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.4 加速器架构

对接 [GPU SIMT](/concepts/gpu-simt-architecture.md)、[DNN Systolic](/concepts/dnn-accelerator-systolic-dataflow.md)、[Cerebras WSE](/entities/cerebras-wse.md)、[LPU](/concepts/lpu-architecture.md)。

## 核心预算

矩阵乘：算 \(2MNK\) FLOPs，读数由复用与层次决定。面积/功耗/封装限制片上 SRAM vs 片外 HBM 配比。时间模型（后文超节点式 6-2 同源）：

\[
T_{\mathrm{op}}=\max(F/P,\,V/B_{\mathrm{HBM}}).
\]

容量、带宽、延迟三者限制不同问题：装不下、供不上、启动/往返主导小消息。

## 机制

- **计算单元**：矩阵单元吃规则 GEMM；向量/控制做 softmax、RMSNorm、路由。低精度改计算量、数据量与转换开销（Ch.10 再写 FP8 分块 scale）。
- **存储层次**：HBM vs 统一内存（Apple）；缓存 / 片上缓冲 / 寄存器。异步搬移 + 双缓冲掩盖读。
- **多芯片**：封装内算力–内存–连接；CPU↔加速器；加速器↔加速器（为 Ch.6 超节点铺路）。

## 架构演进（书中判断）

- **NVIDIA**：矩阵吞吐、精度、数据路径（TMA 等）分别贡献；不要把代际加速全算成 FLOP/s。
- **昇腾**：从 CNN 卷积展开到 Transformer 的矩阵–向量交接。
- **Apple**：大统一内存换「能跑多大模型」，不是峰值 decode。
- **TPU / Groq / Graphcore / Cerebras**：固定数据流或 SRAM-first；Ch.6.7.4 用 ROM 晶圆对照——权重离开 HBM 后，单用户速度改由集合通信决定。WSE-3 片上 SRAM **44 GB** 被用来排除「权重放 SRAM」的 V4.1 方案。

## 设计规则

用同一模型比较候选加速器：先容量，再 Roofline，再测 kernel 效率（书后文常取峰值 40–50%）。时间与能耗两本账：带宽决定一步多快，pJ/bit × 复用决定焦耳，功率上限压频率。

# Citations

[1] [Ch.4](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/04-加速器架构.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
