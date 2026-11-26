---
type: Raw Source
title: "ANOR: Scaling Sparse Attention with a GPU–PNM Computing Hierarchy"
source_url: https://arxiv.org/abs/2611.30417
pdf: ANOR_GPU_PNM_Sparse_Attention_2026.pdf
retrieved: 2026-11-26
ingested: 2026-11-26
org: KAIST / SK hynix / Penn State
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.30417)

Serving long-context LLMs requires keeping the full KV cache because later sparse-attention steps may select other entries. Processing-near-memory (PNM) devices attached through CXL can hold the full cache and compute attention where it resides. Prior GPU–PNM systems are PNM-centric; existing CXL-PNM devices provide far less memory bandwidth than GPU HBM, so the PNM becomes the bottleneck and the GPU sits idle.

ANOR is a GPU–PNM joint acceleration system that computes most of the attention on the GPU from a cache of recently selected entries and processes only the misses on the PNM. GPU cache updates are decoupled from current-step execution. A bounded cache-update policy limits updates to the point where later-step hit ratio saturates. An Early Streaming Buffer (ESB) captures KV data during PNM attention and streams it to the GPU. An adaptive cache-factor mechanism adjusts GPU cache size based on serving load. Across two models and three long-context agentic workloads, ANOR improves decode throughput by 2.3× over HiSparse and 2.0× over a PNM baseline on average.

# Excerpts / key facts

- Authors: Hyunsu Ye, Hyunmin Choi, Jaehong Cho, Jaeseo Lee（KAIST）；Hyeongseok Gwak, Joohee Lee, Donguk Moon, Woosuk Chung, Hoshik Kim（SK hynix）；Kiwan Maeng（Penn State）；Jongse Park（KAIST）。arXiv:2611.30417，cs.AR，Tue 24 Nov 2026 公告。
- 评估是 LLMServingSim 建模：Qwen3-4B-Thinking 用一张 H100 NVL，Qwen3-30B-A3B-Thinking 用两张；GPU kernel 在 H100 NVL 上剖析，PNM 时延按 M2NDP 配置推导，主机开销在 Intel Xeon 6520P 上测量。四个 CXL-PNM 器件为模型（各四通道 DDR5-6400、200 GB/s、512 GB，合计 2 TB 池），不是硅片实测。
- 负载：SWE-chat、Open-SWE、OpenResearcher；系统评估回放 SeerAttention-R 轨迹，Top-2K。
- 离线最大 batch、cache factor 固定 1.0、三负载平均：相对 HiSparse，4B / 30B 吞吐 2.6× / 2.1×；相对 PNM 基线 2.3× / 1.7×。摘要再对两模型平均为相对 HiSparse 2.3×、相对 PNM 基线 2.0×。
- 在线 SWE-chat、20 requests/s：相对最好基线，4B 的 P50 / P99 完成延迟 2.7× / 2.8×，30B 为 3.3× / 2.2×；排队峰值低 2.1× / 6.6×，到达停止后队列早 115 s / 43 s 排空。
- 硬件开销（CACTI 22 nm 再投影到 7 nm）：每只 PNM 器件新增 2.01 mm²、动态功耗 186 mW，四只合计 8.04 mm²、0.74 W；默认 8 MiB ESB、30% 更新比例。
