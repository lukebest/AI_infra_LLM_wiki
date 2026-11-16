---
type: Raw Source
title: "Starscream: Reimagining LLM Sharding on AMD Instinct GPUs with GPU Partitioning"
source_url: https://arxiv.org/abs/2611.15951
pdf: Starscream_AMD_GPU_Partitioning_2026.pdf
retrieved: 2026-11-16
ingested: 2026-11-16
org: AMD Research and Advanced Development
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.15951)

As GPU accelerators grow larger to meet rising compute demands, they exhibit increasingly pronounced non-uniform memory access (NUMA) characteristics that challenge existing LLM frameworks. Chiplet-based architectures provide a practical path to larger GPUs while mitigating manufacturing yield constraints. Modern GPUs such as AMD Instinct MI300X employs such a multi-die design, and further offer GPU partitioning capabilities, partitioning a single physical GPU into multiple logical devices with NUMA-aware memory domains, promising faster kernel launches, and reduced memory access latencies with improved locality. However, current parallelization strategies, designed for homogeneous GPU topologies, when applied under partitioning, extend its unidimensional sharding causing significant performance degradation. Three bottlenecks emerge: (1) memory redundancy; (2) arithmetic intensity collapse; (3) communication overhead from flat collectives. We present Starscream, a rethinking of LLM sharding for the chiplet era. Rather than stretching inter-GPU sharding thinner, Starscream adds intra-GPU sharding along an orthogonal dimension, grounded in three foundational principles: kernel shape preservation, memory redundancy elimination, and communication overhead minimization. These principles form the basis for extending any sharding strategy into the partitioning regime. We demonstrate their effectiveness using tensor parallelism as a case study. On AMD MI300X and MI355X, exploiting partitioning capabilities yields up to 4x speedup for attention and 1.43x for fused GEMMs compared to chiplet-oblivious baselines, demonstrating the effectiveness of chiplet-aware designs. Starscream's principles generalize across sharding strategies and future architectures.

# Excerpts / key facts

- Authors: Sumanth Gudaparthi、Smeet Chheda、Ganesh Dasika，AMD Research and Advanced Development。arXiv:2611.15951，cs.DC / cs.AR，2026-11-11 提交、2026-11-13 作为交叉列表出现在 cs.AR。PDF 13 页。摘要与 PDF 均未标注会议。作者写计划在录用后开源实现。
- 硬件：MI300X 上对比 CPX/NPS4 与基线 SPX/NPS1；MI355X 上对比 DPX/NPS2 与 SPX/NPS1。MI300X 为八个 XCD 的多裸片设计，SPX 把整卡看成一台设备，CPX 可按 XCD 切成最多 8 个逻辑 GPU，并与 NPS4 的 NUMA 域对齐。
- 实现：自注意力基于 vLLM 的 Triton unified-attention（vLLM-v1）与 HIP paged-attention（vLLM-v0）；GEMM 用 Triton 上的 Stream-K；计算-通信融合走 PyTorch symmetric memory。
- 负载：decode 自注意力用 GPT-OSS-120B、Llama3-70B、Llama3-405B，上下文 16K–128K、batch 1–1024。GEMM 与集合通信用 200 多个来自上述模型及其他 SOTA GQA/MoE 的形状。
- 朴素把现有一维切分套到分区上会遇到：KV 在各 XCD 上复制（容量与带宽浪费，大 batch 还会 OOM，Fig. 8 中只有朴素切分出现红叉）、GEMM 算术强度塌缩、扁平集合通信把跨裸片流量放大（文中举例 8 卡 MI300X 节点上 GPU 间数据移动从 3·M·N 升到 7·M·N，约 **2.3×**）。
- 方案：在现有跨 GPU 切分之外，再沿正交维做卡内切分。注意力按序列长度把 KV 均匀铺到各 NUMA 域；集合通信按 NUMA 做分层（卡内 reduce-scatter / all-gather + 卡间对等 XCD 的 all-reduce），并把输出直接写到目标 NUMA，与计算重叠。还可通过交换 GEMM+reduce-scatter 与 all-gather+GEMM 做 2D 切分，改善 tile 形状与算术强度。
- 效果：摘要与结论写，在 MI300X / MI355X 上相对不感知 chiplet 的基线，注意力最高 **4×**，融合 GEMM **1.43×**。正文 Fig. 9 的 GEMM+卡内集合：低时延区（batch 1–16）Llama3-405B FC2 的 all-gather+GEMM 最高 **1.41×**；吞吐区（batch 32–2048）差距收到约 **1.08×**；batch >2048 时单 XCD 的 L2（FP16、MI300X）不够用，收益下降。作者声明注意力数字是保守下界：把 SPX 上最好的 kernel 配置移植到 CPX，没有为 CPX 再调 workgroup 与 flash-attention 分段。
- 作者强调 4× / 1.43× 是分区能力被用起来之后、相对 chiplet-oblivious 基线（含把分区当更多独立 GPU 的朴素切分）的加速；SPX 在大 batch 会改善热点，但又会撞上 IOD 之间的 USR 链路争用。
