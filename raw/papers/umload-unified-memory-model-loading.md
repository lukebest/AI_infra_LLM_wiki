---
type: Raw Source
title: "UMLoad: Fast On-Demand Model Loading on Unified Memory Architecture"
source_url: https://arxiv.org/abs/2611.04253
pdf: UMLoad_Unified_Memory_Model_Loading_2026.pdf
retrieved: 2026-11-06
ingested: 2026-11-06
org: Shanghai Jiao Tong University IPADS
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.04253)

On-demand model loading dominates response latency for interactive on-device AI, yet unified memory architectures (UMAs)—now common on edge devices—should make it cheap by placing weights in memory the GPU already sees. However, frameworks still use the loading flow built for discrete GPUs, leaving significant inefficiencies. This paper presents UMLoad, a system-level model-loading accelerator that decouples a framework’s logical allocations from their physical page backing. UMLoad uses on-demand reconstruction to eliminate the weight copy while preserving copy independence, and GPU-assisted page zeroing to accelerate runtime allocation while preserving its security guarantee. Implemented on Intel, AMD, and NVIDIA UMA platforms and evaluated with llama.cpp, PyTorch, and vLLM across six models, UMLoad reduces average loading time by 36.6%–71.9% over vanilla and 19.9%–62.7% over pipelined loaders, and cuts mean LLM-routing time to first token (TTFT) by 51.3%–59.3% and model-backed tool completion latency by 10.2%–31.6%.

# Excerpts / key facts

- Authors: Zimeng Wang, Jinrong Yang, Rong Chen (SJTU IPADS).
- On-demand reconstruction + GPU-assisted page zeroing。
- Platforms: Intel/AMD/NVIDIA UMA；llama.cpp, PyTorch, vLLM；六模型。
- 装载：vs vanilla **−36.6%–71.9%**；vs pipelined **−19.9%–62.7%**。
- 路由 TTFT **−51.3%–59.3%**；工具完成 **−10.2%–31.6%**。
