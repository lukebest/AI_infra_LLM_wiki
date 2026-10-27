---
type: Raw Source
title: "TranSAGE: Automating Spatial Accelerator Generation for Large-Scale Transformer Models"
source_url: https://arxiv.org/abs/2610.32279
pdf: TranSAGE_Spatial_Accelerator_Generation_ASPLOS2027.pdf
retrieved: 2026-10-27
org: Shanghai Jiao Tong University; South China University of Technology
venue: ASPLOS 2027 (accepted), arXiv cs.AR
---

# Abstract (verbatim, arXiv:2610.32279)

Large-scale Transformers have achieved remarkable success across NLP, computer vision, and robotics, but their growing computational and memory demands challenge efficient inference. Spatial accelerators offer advantages in on-chip bandwidth and energy efficiency, yet designing them for large models remains costly and time-consuming. Existing accelerator generators typically focus on single-operation support, overlooking the benefits of multi-operation pipelining, which limits throughput and energy efficiency. We propose TranSAGE, a compiler-based framework that jointly optimizes scheduling for large-scale Transformers under multi-operation pipelining and generates corresponding accelerator implementations. Our approach integrates a design space exploration (DSE) engine with multi-operation dataflow optimization and a dynamic programming-based graph partitioning algorithm to efficiently identify pipeline-friendly operation clusters and their optimal dataflow parameters. We further design spatial architecture primitives and lowering passes to automatically generate efficient RTL implementations. Evaluations on four representative LLMs demonstrate that TranSAGE achieves up to 2.41x higher throughput and 13.04x higher energy efficiency than commercial GPU/NPU baselines. Compared with state-of-the-art accelerator generators, TranSAGE achieves up to 11.33x higher throughput and 6.07x higher energy efficiency.

# Excerpts / key facts (from PDF)

- MLIR-based: PyTorch → Torch-MLIR → Linalg; DSE over fusion (DP graph partitioning minimizing EDP, cutIndex backtracking) + intra-cluster dataflow (L2 tiling / L1 unroll+order, dimension-relation network).
- Spatial architecture primitives (SAPs) for arithmetic, storage (DataNode), routing (Decompose/Compose/Mux/Demux); per-cluster binary in dispatch table; RTL from primitive templates.
- Workloads: Llama3-8B, Qwen3-8B, Gemma-7B, Llama3-70B, Qwen3-235B-A22B. Baselines: Orin NX, A100, Ascend 910B3 (measured, PyTorch/Torch-NPU); Gemmini-OS/WS, LEGO (Timeloop+Accelergy).
- TranSAGE at 1 GHz, 45 nm model; energy scaled via DeepScaleTool to 8 nm / 7 nm for comparison.
- vs GPU/NPU prefill avg throughput 2.05× / 1.65× / 1.42× (Orin NX / A100 / 910B3); decode 2.41× / 1.62× / 2.12×. Energy efficiency prefill 1.78× / 3.46× / 3.69×; decode 3.65× / 8.57× / 13.04×.
- vs generators prefill: edge 1.58× / 2.22× / 1.82× (Gemmini-OS / WS / LEGO), server 4.14× / 3.28× / 5.50×; decode edge 3.13× / 1.46× / 1.46×, server 11.33× / 3.37× / 3.37×.
- BF16 utilization up to 96.15% (edge) / 90.20% (server) on prefill; decode 3.16% / 3.05% (memory-bandwidth bound).
- Reconfiguration area overhead ≤0.11%; DSE with max cluster size 6 finishes within tens of minutes (near-linear vs exponential full search).
- Limitations: resources fixed after generation; single-chip only (no communication-aware multi-chip DSE).
