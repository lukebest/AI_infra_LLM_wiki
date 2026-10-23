---
type: Raw Source
title: "HAWK: Heterogeneity-Aware KV Cache Transfer for Efficient GPU-NPU Phase-Disaggregated LLM Inference"
source_url: https://arxiv.org/abs/2610.29873
pdf: HAWK_GPU_NPU_Heterogeneous_KV_Transfer_2026.pdf
retrieved: 2026-10-23
org: Georgia Tech; ETRI
venue: arXiv cs.AR / cs.DC (2026-10)
---

# Abstract (verbatim, arXiv:2610.29873)

Large language model (LLM) inference exhibits distinct computational characteristics across its two phases: prefill is compute-intensive, whereas decode is more memory-bound. As a result, AI accelerators achieve varying levels of efficiency across the two phases. GPUs are well suited to prefill, but are often underutilized during decode. By contrast, NPUs can utilize their compute resources more effectively during decode. Motivated by this observation, we explore a heterogeneous architecture that integrates GPUs and NPUs, mapping prefill to GPUs and decode to NPUs to achieve high performance and efficiency. However, realizing such heterogeneous integration is challenging because LLM phase disaggregation requires KV cache transfer from prefill to decode—that is, from GPUs to NPUs—which is complicated by differences in inter-device communication mechanisms and KV cache tensor layouts.

To address this, we propose HAWK, a transfer mechanism that enables rapid KV cache transfer across heterogeneous devices. HAWK establishes a remote direct memory access (RDMA) path for direct cross-device transfers while handling inter-device tensor layout discrepancies as part of the transfer process. In particular, HAWK allocates tensor-layout-aware RDMA buffers on the NPU side to match the target tensor layout. Leveraging these buffers, HAWK orchestrates data transfer from a conventional contiguous GPU RDMA buffer to the corresponding NPU buffers, allowing transferred tensors to be consumed directly without additional data rearrangement while maintaining transfer efficiency. We implement and evaluate HAWK on a system built with commercially available GPUs and NPUs, demonstrating performance within 7.88% of a GPU-only system under the same SLO constraints while achieving up to 1.26× higher power efficiency and 1.72× higher cost efficiency.

# Excerpts / key facts (from arXiv HTML)

- Table 1 (Llama 3.1 70B, 512 in / 128 out, BS=32, 4 devices TP=4): A100 prefill 133.16 vs p150a 52.74 tok/t_prefill (2.52×); decode 15.27 vs 13.17 (1.16×); NPU decode power efficiency 107.20 vs GPU 77.11 (1.39×); cost efficiency 2.35 vs 0.40 (5.88×).
- HAWK: common Linux RDMA path (GPU peermem + NPU peer memory client); transfer-aware tensor transform on GPU; per-DRAM-channel layout-aware RDMA buffers on NPU; Mooncake Transfer Engine v0.3.6; vLLM 0.10.0 + Tenstorrent stack.
- Eval: 4×A100 PCIe prefill + 4×Tenstorrent p150a decode; 200 Gbps HDR IB; Llama 3.1 70B TP=4.
- Transfer: HAWK up to 27.69× faster than naive host-staged; latency within 0.65% of GPU-to-GPU RDMA; GN-HAWK latency drops to 14.69% of GN-Host at 1280 MB.
- Online serving (90% SLO): Chatbot / Summarization request-rate gap vs GG-Direct 2.90% / 5.90% (TTFT); SLO attainment request-rate gap Summarization 7.69%; decode throughput gap ≤7.88% (Summarization) / 0.48% (Chatbot).
- Efficiency vs GG-Direct (Table 8): power 1.26× / 1.15×; cost 1.72× / 1.61× (Chatbot / Summarization).
- vs H100 decode GGH-Direct (Table 9): throughput within 6.53%; power 1.03×; cost up to 2.76×.
