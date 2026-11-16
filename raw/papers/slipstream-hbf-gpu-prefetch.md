---
type: Raw Source
title: "SlipStream: Enabling HBF for GPU Systems by Mitigating the Latency and SRAM Overheads"
source_url: https://arxiv.org/abs/2611.14776
pdf: SlipStream_HBF_GPU_Prefetch_HPCA2027.pdf
retrieved: 2026-11-16
ingested: 2026-11-16
org: Georgia Tech / NVIDIA Research / Stanford University
venue: HPCA 2027
---

# Abstract (verbatim gist, arXiv:2611.14776)

Large language model (LLM) inference demands ever more memory capacity for larger models and batch sizes. High-Bandwidth Flash (HBF) replaces the DRAM dies of HBM with NAND flash and provides up to 16x the capacity at comparable read bandwidth. However, HBF can incur a read latency of nearly 20 μs, 20x that of HBM, so on-demand HBF accesses slow inference by up to 12.8x. Conventional cache-line prefetchers require 20x more in-flight tracking state to cover this latency. Tensor-streaming designs, such as H3, follow virtual-address order as opposed to kernel-demand order, and therefore need hundreds of megabytes of buffering. We propose SlipStream, a software-hardware co-designed prefetcher that turns prefetching into a demand-paced producer-consumer pipeline. In software, SlipStream profiles the repeatable weight-page demand order of data-independent LLM kernels and inserts a staging warp that replays this order with non-blocking STAGE instructions. In hardware, the staging warp acts as the producer and the work warps as consumers. Our key insight is to retire each STAGE tracking entry only when demand first accesses the page, as opposed to when the page returns from HBF. Demand thus paces staging and bounds how far staging leads consumption. SlipStream tracks 4 KB pages instead of cache lines and allocates buffer slots only when pages return, which decouples the buffer size from outstanding traffic. Across seven dense models spanning 16-800 GB, SlipStream with a 40 MB staging buffer achieves 92.4% of the performance of an ideal HBF with HBM-like latency. H3 achieves only 43.1%, even with a 320 MB buffer. The buffer sizing of SlipStream is independent of HBF latency and workload. SlipStream with 16 MB buffer, 20x smaller than that of H3, performs within 4% of SlipStream-40MB. SlipStream also supports Mixture-of-Experts models and reaches 91.2% of ideal performance (40 MB buffer).

# Excerpts / key facts

- Authors: Anish Saxena、Hritvik Taneja（Georgia Tech），Christos Kozyrakis（NVIDIA Research & Stanford University），Aamer Jaleel（NVIDIA Research）。To appear in HPCA 2027。arXiv:2611.14776，cs.AR，2026-11-13 公告。PDF 15 页。
- 仿真栈：Accel-Sim v1.3 + Ramulator2。基线配置（Table III）：L2 **40 MB**，HBM/HBF 峰值读带宽各 **2 TB/s**，容量 80 GB / 1280 GB，页 **4 KB**，HBF 请求到返回延迟 **20 µs**。
- 七个稠密 FP16 模型、batch 64：Llama-8B、Mistral-24B、Qwen2.5-32B、DeepSeek-67B、Llama-70B、Qwen2.5-72B、Llama-405B（更大模型因 FP16 权重可达 800 GB 量级，评估中使用 INT4 等压缩路径）。另有 MoE：TensorRT-LLM 持久 MoE kernel，Qwen3-30B 与 Qwen3-235B（w13 与 w2 GEMM 融合）；batch 8/64 时平均激活 31 与 87 / 128 专家。
- 硅上开销（staging warp，无 HBF）：A100（108 SM）、H100（132 SM）、Blackwell RTX PRO 6000（188 SM）上，七个模型端到端 decode 开销 **0.76–2.96%**，几何均值分别为 **2.1% / 2.4% / 1.2%**。离线 profiling 约 40 分钟（大模型可分层抽样，如 Llama-70B 的 20/80 层）。
- 稠密模型主结果（相对理想 HBF，即同等容量但延迟像 HBM）：40 MB 缓冲平均 **92.4%**（逐模型 78.0–107.2%；Llama-70B 与 Qwen2.5-72B 超过理想 HBF）。16 MB 平均 **88.8%**（74.1–102.7%），相对 40 MB 只差 **4.0%**。H3 在 40 MB 只有理想性能的 **10.6%**（减速 4.8–11.5×，接近按需取数）；即便 320 MB 也只有 **43.1%**。40 MB 时 SlipStream 持续 HBF 读带宽为峰值的 **49.2–81.2%**（归一到 2 TB/s）。
- MoE：40 MB 达到理想 HBF 的 **91.2%**，16 MB 为 **87.3%**（几何均值），无丢页或缓冲缺失。随 batch/模型变大变好：Qwen3-30B batch 8 为 **83.7%**，Qwen3-235B batch 64 为 **97.1%**。
- 系统对照（讨论段）：Llama-70B 在四张 HBM GPU 上已能放下权重并留出 KV，SlipStream 把吞吐提到 **1.17×**。Llama-405B 需要十六张 HBM GPU 才放得下一份副本，八张 HBF GPU 就够；十六张带 SlipStream 的 HBF GPU 因此给出 **2.27×** 吞吐、**0.52×** 每 token 能量、**0.23×** EDP。按需序的 H3 在 Llama-405B 上 TPOT 602 ms，是纯 HBM 服务的 **10×**，吞吐只有 **0.55×**。
- CACTI 22 nm：SlipStream 在 GPU 裸片上增加的结构约 0.39 mm²，相当于 826 mm² 的 GA100 裸片的 **0.02%**。H3-320MB 在 22 nm 占 **42.7%**（若按 H3 所设 3 nm bitcell 公式为 12.7% / 10.7%）。在测得的 49.2–81.2% HBF 利用率下，SlipStream 大约加 **24.5–32.0 W**（相对装 HBF 后的系统功率 **3.7–4.9%**）；H3-320MB 加 **18–22%**。
- 关键机制：按 kernel 需求顺序（而非虚地址顺序）replay；STAGE 表项在需求首次访问该页时才退役，让需求给预取定速；按 4 KB 页跟踪，页返回时才分配缓冲槽，从而把缓冲大小与在途流量解开。
