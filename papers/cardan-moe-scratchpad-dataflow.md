---
type: Paper
title: "CARDAN: Scratchpad 张量加速器上的多引擎 MoE 解码数据流"
description: "共享低秩/VQ 权重表示配合路由无关预取，把 Trainium3 上 MoE decode 的 HBM 读流量降低 26–50%，batch-1 加速 1.15–1.31×。"
tags:
- architecture
- accelerator
- inference
- llm
- moe
- dataflow
- memory-bandwidth
- throughput
created: 2026-09-22
updated: 2026-09-22
timestamp: '2026-09-22T00:00:00Z'
paper_author: [Bin Ma, Wenjie Fan, Dong Li]
year: 2026
arxiv: '2609.21137'
sources:
  - raw/papers/CARDAN_Multi_Engine_MoE_Scratchpad_Dataflow_2026.pdf
  - raw/papers/cardan-moe-scratchpad-dataflow.md
---

# CARDAN：Scratchpad 张量加速器上的多引擎 MoE 解码数据流

## 一句话结论

CARDAN 不是再做一个 GPU kernel，而是针对 scratchpad tensor accelerator 的软硬件数据流：用 **expert-shared low-rank/VQ 表示**把一部分权重搬运提前到 routing 前，并把 DMA、tensor、SIMD/vector/scalar engine 串成流水。在 AWS Trainium3 的五个 MoE 上，batch-1 decode 比 AWS dense BF16 megakernel 快 **1.15–1.31×**；OLMoE batch 16 达 **1.70×**。

## 动机：MoE 的权重只有路由后才知道

小 batch decode 的矩阵乘退化为 GEMV，expert 权重读取而非算力成为瓶颈。论文对 Qwen3-30B-A3B 的剖析显示，expert weight loading 占端到端层延迟 **56%**；现有流水虽能隐藏一部分，仍有 **36.8%** 暴露。相较有 cache 的 GPU，显式 scratchpad 更依赖编译器/数据流安排，权重读取与其他 engine 协同时机更关键。

## 方案

### 1. 把权重拆成共享部分与 expert-private 部分

对 gate/up projection，CARDAN 使用共享低秩 basis 与共享 VQ codebook；每个 expert 只保存低秩 coefficient 与 VQ index。共享 basis/codebook 是 routing-independent，可在 router 产出 expert ID 前搬进 scratchpad；coefficient/index 则在 routing 后搬运。down projection 保持 BF16，以控制误差。

### 2. 多 engine 流水而非单 kernel

CARDAN 把工作映射到五类硬件：DMA 搬运，tensor engine 做共享低秩投影，GpSimd/GpSimd2 解码 VQ，vector/scalar engine 做量化、索引与 elementwise。路由、shared transfer、private transfer、projection 可以跨 engine 重叠；compiler 用 stream 与 event 固化依赖关系。

### 3. 训练/系统协同

压缩后的 gate/up projection 需要 knowledge distillation 恢复精度；硬件侧采用芯片内 TP=4，并在 batch 变大时把计算切成 partial-sum 任务分配给多个 tensor engine。

## 量化结果

评测覆盖 Qwen3-30B-A3B、OLMoE-1B-7B、Granite-3.1-MoE-3B、Granite-4.0-Micro、Qwen1.5-MoE-A2.7B，运行于 AWS Trainium3：

- **性能**：batch 1 相对 AWS BF16 dense megakernel 加速 **1.15–1.31×**；OLMoE 从 batch 1 的 **1.15×** 增至 batch 16 的 **1.70×**。
- **带宽**：MoE projection 的 HBM read 降低 **26–50%**，DMA-active time 降低 **10–31%**。
- **压缩**：gate/up projection 权重压缩率 **3.92–4.92×**。
- **质量**：distillation 后五个模型的 PPL 均达到或优于各自 BF16 teacher；例如 Qwen3 从 7.85 降至 6.28（论文认为来自蒸馏正则化，不能泛化成无损压缩结论）。

## 局限与解读

- 结果只覆盖 Trainium3 与芯片内 TP=4；跨芯片 expert parallel 的网络瓶颈未进入评测。
- 提速由权重压缩、预取与多 engine 调度共同产生，论文没有给出所有因素的完全解耦消融。
- gate/up 压缩需要离线 distillation，部署成本与模型升级频率会影响收益。

这项工作的增量是把 [DNN Accelerator Systolic Dataflow](../concepts/dnn-accelerator-systolic-dataflow.md) 的片上 engine 编排扩展到动态路由 MoE，并与 [GEMM vs. GEMV](../concepts/gemm-vs-gemv.md) 的 decode 带宽瓶颈直接对接；它和 [Vortex](vortex-extreme-compression-llm-inference.md) 的共同点是预取权重，区别在于 CARDAN 先改变权重表示来制造“可在 routing 前预取”的共享部分。

# Citations

1. Ma, B., Fan, W., & Li, D. “A Multi-Engine Dataflow for MoE Decoding on Scratchpad-Based Tensor Accelerators.” arXiv:2609.21137, 2026. [arXiv](https://arxiv.org/abs/2609.21137)
2. [本地原文 PDF](../raw/papers/CARDAN_Multi_Engine_MoE_Scratchpad_Dataflow_2026.pdf)；[原始来源记录](../raw/papers/cardan-moe-scratchpad-dataflow.md)
