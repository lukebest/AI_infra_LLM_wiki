---
type: Raw Source
title: "L2C2: Enhancing Large-scale Chiplets for Agent Long-Context LLM Inference with Sparse and Distributed Attention"
source_url: https://arxiv.org/abs/2611.33691
pdf: L2C2_Chiplet_Sparse_Distributed_Attention_2026.pdf
retrieved: 2026-11-27
ingested: 2026-11-27
org: Peking University
venue: ICCAD 2026
---

# Abstract (verbatim gist, arXiv:2611.33691)

Long-context inference is a rising demand for LLMs, especially for agent applications. Sparse attention (SpAt) and chiplet technology are promising solutions to reduce computations and scale hardware performance. However, deploying SpAt on distributed chiplets necessitates context parallelism for workload partitioning, introducing complex distributed attention. In this work, we present L2C2, a system optimization for distributed SpAt in long-context inference. During the partial-prefill stage, we propose a novel Split-Comm Attention mechanism that leverages the high-bandwidth interconnect of chiplets to trade communication overhead for reduced memory access. We combine it with conventional Ring Attention to form a Bi-Mode method that adapts to varying input sequence lengths. During the decoding stage, we analyze the cause of memory access imbalance and address it by static interleaved token assignment. Dynamic agile cache balancing is also proposed to adapt to SpAt skewness. Evaluations show our optimization can achieve 1.45× and 1.53× speedup in partial-prefill and decoding with SpAt on large-scale chiplets.

# Excerpts / key facts

- Authors: Kanbo Bai, Zhonghua Mu, Hongze Zhou, Tianyu Jia。北京大学。arXiv:2611.33691，cs.AR，Thu 26 Nov 2026 公告，ICCAD 2026。
- 评估：ASTRA-sim + NS3 + Ramulator 2.0 + Timeloop；稀疏选择来自运行时轨迹。默认 MCM 为 8×8 die、HP=8、CP=8；每 die 为 20 mm × 20 mm、600 TFLOPS FP8、20 MB 缓冲 + 两只 2 TB/s HBM3，逻辑芯粒每边双向 NoI 1 TB/s。32 GPU 对照使总资源对齐，每卡为单个 die 的两倍；GPU-NVL72 每卡配置与 GPU-basic 相同，不是官方 NVL72 规格。Llama 3.1 405B，FSA 稀疏，块长 64，稀疏比 0.85，batch 8。
- 部分 prefill P=512k、N=512 时 MCM 上 Split-Comm 相对 Ring Attention 1.45×；N=256 时 KV 访问最多降到 5.49×。N=64k、P=4k 时 Split-Comm 即使在 MCM 上也损失 35% 效率。
- 交织分配把平均 KV 访问方差从 2.775 降到 0.48，MCM decode 1.34×。与敏捷均衡合在一起，MCM / GPU-basic / GPU-NVL72 平均 decode 为 1.53× / 1.32× / 1.36×。CP=H-TP=8 时 H-TP 的 decode 吞吐只有 CP 的 35.7%。
