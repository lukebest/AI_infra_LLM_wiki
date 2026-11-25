---
type: Paper
title: "GPCPlace: 在 SM 分区 GPU 上缓解 GPC 交叉开关端口争用"
description: "港科大广州 / 清华 — 14 张 NVIDIA GPU 实测；相对 CUDA Green Contexts，各卡 112 个用例的平均加速最高 1.15×，单用例最高 2.38×，中位 STP 为 1.00×"
tags:
- architecture
- gpu
- green-context
- microarchitecture
- llm
- inference
- serving
created: 2026-11-25
updated: 2026-11-25
timestamp: '2026-11-25T00:00:00Z'
paper_author: [Ziwen Wang, Qi Luo, Kunlin Li, Changxi Liu, Dongsheng Wang, Yun Chen]
year: 2026
venue: preprint
arxiv: '2611.24458'
sources:
  - raw/papers/GPCPlace_SM_Partitioned_GPU_2026.pdf
  - raw/papers/gpcplace-sm-partitioned-gpu.md
---

# GPCPlace：按 GPC 端口争用在 spreading 与 packing 之间做选择

## 一句话结论
港科大广州与清华提出运行时 GPCPlace：在保持各负载 SM 数量不变的前提下，先在目标 GPU 上剖析共享交叉开关端口排队与打包后带宽损失，再在 CUDA 驱动里挂钩 kernel 启动并设置 TPC/SM mask。14 张覆盖 Ampere / Ada / Hopper / Blackwell 的 NVIDIA GPU 上，每卡 112 个并发用例（五次中位数）相对 CUDA Green Contexts，各卡平均加速最高 **1.15×**（Ada 四卡 **1.11×–1.15×**），单用例最高 **2.38×**，中位系统吞吐 STP 为 **1.00×**。

## 动机
为了让时延关键负载立刻有 SM 可用，CUDA Green Contexts、libsmctrl、nvtaskset 一类机制把并发负载限制到互不相交的 SM 子集。已有工作把剩余减速主要归因于共享 L2 与显存争用，于是调整 SM 数量、推迟后台 kernel，或限制后台访存。本文指出还有一层：同一 Graphics Processing Cluster（GPC）里的 SM 共用一条通往 L2 的交叉开关端口。Green Contexts 默认把负载的 SM 铺开到多个 GPC，使时延关键请求在共享端口上排在后台请求后面；把负载打进各自的 GPC 可以避开这条排队，但又会减少可用端口、限制带宽。两种放置在不同负载与不同 GPU 上互有胜负。

## 方案
GPCPlace 分三步。部署前在目标 GPU 上剖析：用 1 个 TPC 的时延关键负载，分别在单独运行、与后台分处不同 GPC、与后台共享同一 GPC 三种设置下测延迟，估计共享端口排队 (I) 以及经 L2/DRAM 的减速 (X)；再单独测量打包相对铺开的带宽损失 (L)，以及忙碌 L2 slice 上仲裁份额下降 (D)。若估计的排队超过打包损失，就把时延关键负载打进专用 GPC，否则铺开，其余 TPC 分给后台。运行时在 CUDA 驱动的 launch 回调里改 QMD 的 TPC mask，应用无需改动。各负载的 SM 数量保持不变，因而可以与已有按 SM 计数做隔离的方法叠加。NVIDIA 未公开 mask 位到物理 TPC/GPC 的映射，作者在每张目标卡上逐位关闭 mask、读硬件特殊寄存器，一次性建立该映射。

## 量化结果
平台为 Table I 中的 14 张卡：Ampere 的 A800、RTX 3060 / 3090、RTX A6000、A40；Ada 的 RTX 4080 / 4090、L4、RTX 5000 Ada；Hopper 的 H20；Blackwell 的 RTX 5070 / 5090、RTX PRO 6000、DGX Spark。时延关键负载四种：Llama-3-8B 的 8 层 Triton 或 cuBLAS GEMM，以及 FlashAttention 仅注意力 decode，均为 batch 16、上下文 2048；再加上 embedding + FFN。后台 12 种，来自已有 GPU 共享场景，包括 LLM prefill、AdamW、GEMV、vector add、encoder、大 batch decode、vector search 等。时延关键负载分配相当于 1 个或 3 个 GPC 的 TPC，并另有 4 个双后台、1-GPC 用例。对照为 Green Contexts、All Packed 与随机分配 TPC。

- 相对 Green Contexts，各卡平均加速最高 **1.15×**（Ada 四卡 **1.11×–1.15×**，Blackwell 最高 **1.07×**，四张 GDDR Ampere **1.02×–1.04×**，高带宽 HBM 的 A800 与 H20 为 **1.00×–1.01×**），单用例最高 **2.38×**。14 张卡的中位 STP 均为 **1.00×**。
- 计算请求率（SM 数 × 频率）相对内存带宽更高的卡，在 Green Contexts 下共享端口排队更重，GPCPlace 的平均收益也更大。
- All Packed 在计算密集或 L2 饱和的后台负载下会变慢，RTX 4090 上可到 Green Contexts 的 **0.58×**，RTX 5000 Ada 上为 **0.66×**。GPCPlace 相对 All Packed 在 4090 / 5000 Ada / A40 / PRO 6000 上分别最高 **1.68× / 1.52× / 1.48× / 1.34×**。
- 按后台类型：与 vector add、AdamW、GEMV 并发时，14 卡平均 **1.09×–1.27×**，最快卡上最高 **1.42×–1.90×**；与 LLM prefill、encoder、大 GEMM 或 L2 饱和的 vector search 并发时，GPCPlace 选择铺开，与 Green Contexts 对齐（**1.00×**）。
- 开销：TPC→GPC 映射在 14 张卡上均在 **3 秒**内完成；(I,X) 每个后台约 **2–3 秒**，(L,D) 每个时延关键负载不到 **1.5 秒**；运行时改 mask 给端到端 kernel launch 增加不到 **1 µs**。

## 局限与解读
- 时延关键侧是 8 层 Llama-3-8B 切片、仅注意力 decode 或 embedding+FFN，不是完整服务栈上的端到端 TTFT/TPOT。
- 放置在部署前剖析，负载组合或 GPU 变化后需要重新测量；论文未报告在线重剖析。
- HBM 数据中心卡（A800、H20）上平均收益接近 1.00×–1.01×，收益主要出现在计算请求率相对带宽更高的消费级 / 工作站卡上。
- 「up to 1.15× on average」指各卡平均加速的上限，不是把 14×112 个用例合成一个全局平均。

## 与 wiki 的关系
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — 把 GPC 交叉开关端口争用记进 SM / GPC 组织
- [SubGPU Pipelining](/papers/subgpu-pipelining-intra-gpu-spatial.md) — 同样用 Green Contexts 切 SM 池，对象是 decode 算子图的卡内空间流水
- [GC-MoE](/papers/gc-moe-green-context-expert-parallel.md) — 用 Green Contexts 拆通信与计算分区；GPCPlace 在 SM 数量不变时选择这些分区落在哪些 GPC
- [Starscream](/papers/starscream-amd-gpu-partitioning.md) — AMD 侧沿 chiplet 做卡内切分，与 NVIDIA GPC 端口争用对照

# Citations
- [arXiv:2611.24458](https://arxiv.org/abs/2611.24458) — Wang, Luo, Li, Liu, Wang, Chen
- [raw stub](/raw/papers/gpcplace-sm-partitioned-gpu.md)
- [PDF](/raw/papers/GPCPlace_SM_Partitioned_GPU_2026.pdf)
