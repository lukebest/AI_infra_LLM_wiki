---
type: Paper
title: "Starscream: Reimagining LLM Sharding on AMD Instinct GPUs with GPU Partitioning"
description: "AMD Research — 在 MI300X/MI355X 分区上沿正交维做卡内切分；相对不感知 chiplet 的基线，注意力最高 4×，融合 GEMM 1.43×"
tags:
- amd
- gpu
- chiplet
- numa
- inference
- attention
- kernel
- llm
- parallelism
- interconnect
created: 2026-11-16
updated: 2026-11-16
timestamp: '2026-11-16T00:00:00Z'
paper_author: [Sumanth Gudaparthi, Smeet Chheda, Ganesh Dasika]
year: 2026
venue: arXiv preprint
arxiv: '2611.15951'
sources:
  - raw/papers/Starscream_AMD_GPU_Partitioning_2026.pdf
  - raw/papers/starscream-amd-gpu-partitioning.md
---

# Starscream：在 AMD Instinct 分区 GPU 上重做 LLM 切分

## 一句话结论
AMD Research 观察到，把为均匀 GPU 拓扑设计的一维切分直接套到 MI300X / MI355X 的分区模式上，会出现 KV 复制、GEMM 算术强度下降、以及扁平集合通信把跨裸片流量放大。Starscream 在现有跨 GPU 切分之外，再沿一条正交维做卡内切分：保住 kernel 形状、去掉多余复制、并按 NUMA 做分层集合通信。在 MI300X（CPX/NPS4 vs SPX/NPS1）与 MI355X（DPX/NPS2 vs SPX/NPS1）上，相对不感知 chiplet 的基线，注意力最高 **4×**，融合 GEMM **1.43×**。作者把这些数字写成保守下界。

## 动机
MI300X 把八个 XCD 做成一张物理 GPU，并提供分区能力（文中写 QPX 为 4 路，CPX 为按 XCD 的 8 路），再配上 NPS4 之类的 NUMA 域。这样可以缩短启动、让访问更靠近本地 HBM。现有框架（vLLM、Megatron 等）往往把切出来的逻辑 GPU 当成更多彼此独立的设备，把原来的一维切分再摊薄，于是出现三类问题：注意力 KV 在各 XCD 上复制，大 batch 会先把显存吃光（Fig. 8 里只有朴素切分出现 OOM）；GEMM 的算术强度下降；扁平集合通信让跨裸片移动从 3·M·N 升到 7·M·N，大约 **2.3×**。

## 方案
三条原则：保住 kernel 形状、消除内存冗余、压低通信开销。张量并行是一条实例化路径，作者认为同样的原则可以接到其他切分策略上。

具体做法包括：decode 注意力按序列长度把 KV 均匀铺到各 NUMA 域，避免热点与复制；把 all-reduce 拆成卡内 reduce-scatter、卡间对等 XCD 的 all-reduce、再卡内 all-gather，并把输出直接写到目标 NUMA，与计算重叠；还可以通过交换 GEMM+reduce-scatter 与 all-gather+GEMM 做 2D 切分，改善 tile 形状。

实现：自注意力基于 vLLM 的 Triton unified-attention（vLLM-v1）与 HIP paged-attention（vLLM-v0）；GEMM 用 Triton 上的 Stream-K；计算-通信融合走 PyTorch symmetric memory。作者写计划在录用后开源。评测形状来自 GPT-OSS-120B、Llama3-70B、Llama3-405B（注意力：上下文 16K–128K，batch 1–1024）以及 200 多个 GQA/MoE GEMM 与集合通信形状。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 注意力（decode） | 相对 chiplet-oblivious 基线最高 **4×**（NUMA 感知的 paged-attention）；作者声明为未再为 CPX 调 workgroup / flash-attention 分段的保守下界 | 摘要 / 正文 §V-B / 结论 |
| 融合 GEMM | 最高 **1.43×**（含跨 XCD 的对等映射） | 摘要 / 结论 |
| Llama3-405B FC2，all-gather+GEMM vs SPX/NPS1 | 低时延区（batch 1–16）最高 **1.41×**；吞吐区（batch 32–2048）约 **1.08×**；batch >2048 时单 XCD 的 L2（FP16、MI300X）不够用，收益下降 | Fig. 10 / §V-C |
| 朴素分区切分 | 持续低于 SPX/NPS1，且随 batch 增大因 KV 复制先 OOM；SPX 与 Starscream 在这些点上仍能继续跑 | Fig. 8 |

大 batch 下 SPX 自己也会把访问铺得更均匀，与 Starscream 的差距会收窄；与此同时 IOD 之间的 USR 链路开始争用。Starscream 靠少走 USR、按阶段选择移动 query 还是 KV 头来维持优势。

## 与 wiki 的关系
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — 已记录 MI350X 上 8 XCD 的移植代价；本篇把分区（CPX/DPX）当成一等执行模式，重做注意力与 GEMM 的切分
- [AMD Scheduling Data to Compute](/papers/amd-scheduling-data-to-compute-tdm-sdma.md) — 同一厂商栈上用 TDM/SDMA 把数据送到计算；本篇处理的是卡内 NUMA 与逻辑设备
- [Meta × AMD MI350X](/papers/meta-amd-mi350x-training-codesign.md) — 训练侧的 XCD 一致性与 swizzle；本篇是推理切分
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 把集合通信拆成「卡内分层 + 卡间对等 XCD」

## 开放问题
- 4× / 1.43× 是「最高」值，正文没有给出所有模型与 batch 的完整均值表；注意力数字明确写了未做 CPX 专用调参。
- 实现计划开源，本轮页面撰写时还没有公开仓库地址。
- 原则声称可推广到其他切分与未来架构，正文的完整实例是张量并行。
- 评测在单卡分区与节点内形状上展开，跨节点规模下的分层集合还需要更多端到端服务数字。

# Citations
- [arXiv:2611.15951](https://arxiv.org/abs/2611.15951) — Gudaparthi, Chheda, Dasika（AMD Research and Advanced Development）
- [raw stub](/raw/papers/starscream-amd-gpu-partitioning.md)
- [PDF](/raw/papers/Starscream_AMD_GPU_Partitioning_2026.pdf)
