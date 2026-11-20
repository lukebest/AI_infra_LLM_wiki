---
type: Raw Source
title: "XM-Sparse: High-Throughput Sparse-Attention LLM Serving over Scale-up Memory Pools"
source_url: https://arxiv.org/abs/2611.22280
pdf: XM_Sparse_Scale_Up_Memory_Pool_2026.pdf
retrieved: 2026-11-20
ingested: 2026-11-20
org: Netpreme / HKUST / NUS
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.22280)

Sparse attention has been increasingly adopted by production LLMs for long-context inference, yet serving systems must still retain the full KV history, making GPU HBM capacity a key limit on serving concurrency. Existing systems offload the KV cache to host memory, but suffer from the limited bandwidth of PCIe and the limited capacity of host memory. Emerging scale-up memory pools (e.g., X-Mem) relieve both limits and open new opportunities for sparse-attention offloading. In this paper, we first conduct an in-depth analysis and reveal that, even with scale-up memory pools, decode throughput remains bounded by HBM capacity, as hot KV buffers and the fully resident indexer key (K-index) cache occupy substantial HBM. Moreover, the two caches exhibit distinct access patterns. Based on these insights, we present XM-Sparse, the first sparse-attention offloading system over scale-up memory expansion. The core idea of XM-Sparse is to offload both caches aggressively while matching each with an I/O mechanism tailored to its access pattern. Specifically, for dynamically selected KV entries, XM-Sparse fuses TMA-based retrieval with attention in a tile-level pipeline to hide on-demand retrieval latency. For predictable K-index accesses, it prefetches pages via SM-efficient GPU-initiated DMA and coordinates prefetching with latency-critical operations to avoid interfering with decoding. We have implemented XM-Sparse atop SGLang, and our experiments on DeepSeek-V3.2 and GLM-5.3 with an emulated scale-up memory pool show that XM-Sparse delivers up to 4.98× and 4.52× higher decode throughput than PCIe-based ECHO and HiSparse, respectively, and up to 1.34× over a naive integration on the same platform, across 16K–1M contexts.

# Excerpts / key facts

- Authors: Yijun Sun, Xudong Liao, Zhuobin Huang, Kai Chen, Nikita Lazarev, Zhizhen Zhong（Netpreme / HKUST / NUS；Sun 与 Huang 标注为 Netpreme 实习期间完成）。arXiv:2611.22280，cs.DC / cs.LG，提交标注 17 Nov 2026。13 pages。
- 评测：八张 B300，四卡 decode、四卡作为 X-Mem VM 内存节点；超过 1 TB 的容量靠反复映射物理内存。模型 DeepSeek-V3.2（671B）与 GLM-5.3（744B），FP8，DP4+EP4。吞吐实验使用固定 15% 缺失率与 round-robin 专家路由。
- 相对 ECHO 吞吐：DeepSeek 1.72–2.50×，GLM 3.14–4.98×；相对 HiSparse：1.57–1.75× 与 2.05–4.52×；相对同平台朴素接入：1.10–1.34× 与 1.06–1.29×。
