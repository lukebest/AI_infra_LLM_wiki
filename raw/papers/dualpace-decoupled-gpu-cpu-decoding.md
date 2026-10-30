---
type: Raw Source
title: "DualPace: Decoupled Scheduling and Cooperative GPU–CPU Decoding for LLM Serving"
source_url: https://arxiv.org/abs/2610.33501
pdf: DualPace_Decoupled_GPU_CPU_Decoding_2026.pdf
retrieved: 2026-10-30
ingested: 2026-10-30
org: Zhejiang University (Ningbo Global Innovation Center)
venue: arXiv cs.DC (2026-10)
---

# Abstract (verbatim, arXiv:2610.33501)

Large language model (LLM) serving relies on batching to improve inference throughput, but the key-value (KV) cache grows with sequence length and limits GPU-resident concurrency. CPU offloading can expand KV capacity using host memory, yet existing systems remain largely GPU-gated: CPU-resident requests make progress only when the GPU scheduler exposes suitable overlap opportunities. As a result, host memory and CPU compute cannot act as an independent serving resource, leading to bursty CPU-side progress and inflated tail inter-token latency (ITL) under load.

We present DualPace, an LLM serving runtime that turns the host into an independently scheduled decode engine. DualPace separates scheduling authority across two engines: the GPU engine executes prefills and GPU-resident decodes, while an AMX-enabled CPU engine independently batches and advances CPU-resident decodes. The engines are decoupled in scheduling but cooperative in execution: the CPU can execute a complete decode iteration locally or selectively invoke GPU Dense Assist for dense stages, while offline profiles guide hardware-specific batching and routing.

Our evaluations show that, in decode-oriented scenarios, DualPace improves serving throughput by 6.9–43.2% over NEO, a state-of-the-art open-source CPU-offloading system, and by 11.5–90.6% over vLLM, a widely used GPU serving system, while maintaining the same level of latency. DualPace also preserves NEO’s P99 time-to-first-token (TTFT) advantage over vLLM while sustaining 7.3–50.5% higher request rates than NEO at the same level of P99 ITL.

# Excerpts / key facts (from PDF)

- Authors: Kingsum Chow, KeQiang Wu, YuXuan Lin (Zhejiang University / Ningbo Global Innovation Center).
- Problem: NEO-style GPU-gated CPU offload → CPU-resident decode progresses only when GPU exposes overlap → bursty CPU progress, inflated P99 ITL.
- DualPace: GPU engine (prefill + GPU-resident decode) + AMX CPU engine (independent batching of CPU-resident decode); cooperative Dense Assist for dense stages; offline profiles for batching/routing.
- Platforms: Llama-3.1-8B on RTX 4090 + 12-core Xeon Silver 4510; Qwen3-14B on 2×H20 + 24-core Xeon Platinum 8469C; Qwen3-32B on 4×H20 + 48 CPU cores; Azure-Conv / Azure-Code traces.
- Throughput: vs NEO **+6.9–43.2%**; vs vLLM **+11.5–90.6%** (same latency level).
- Tail: same P99 ITL level, request rate vs NEO **+7.3–50.5%**; preserves NEO’s P99 TTFT advantage over vLLM.
- Mechanisms: host PagedAttention + AMX BF16 dense ops; post-attention routing for Dense Assist; CPU engine is independently scheduled (not GPU-gated).
