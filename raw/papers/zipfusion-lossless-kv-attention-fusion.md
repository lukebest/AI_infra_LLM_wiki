---
type: Raw Source
title: "ZipFusion: Fusing Lossless KV Decompression with Attention for Efficient LLM Decoding"
source_url: https://arxiv.org/abs/2610.33719
pdf: ZipFusion_Lossless_KV_Attention_Fusion_2026.pdf
retrieved: 2026-10-28
ingested: 2026-10-28
org: The Chinese University of Hong Kong; Unaffiliated
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.33719)

The key-value (KV) cache places growing demands on GPU memory capacity and bandwidth as large language models serve longer contexts and more concurrent requests. Its footprint limits concurrency, while repeated KV reads during attention can make decoding memory-bandwidth bound. Prior lossless KV cache compression methods reduce transfers between devices but restore the uncompressed KV cache in GPU memory before attention. They therefore leave these repeated KV reads unchanged and require additional work and memory for decompression. We present ZipFusion, which enables attention to consume the losslessly compressed KV cache directly. ZipFusion co-designs the compression format and attention kernel to reduce the bytes read from GPU memory during attention. The kernel reconstructs the original values directly in registers using simple bit operations, avoiding a separate decompression pass and easing the memory-bandwidth bound. ZipFusion also reassigns memory freed by compression across layers to store additional KV cache. Its memory manager reserves space for ongoing generation and makes the remaining capacity available to new requests. We implement ZipFusion on the top of FlashInfer and integrate it with SGLang. On an NVIDIA H100, ZipFusion achieves about 1.25× speedup over FlashInfer in decode attention. With 8K context, it improves model decode throughput by up to 26.3% over uncompressed SGLang under the same GPU memory budget. At each method's largest supported batch, it also delivers up to 2.76× the throughput of the best-performing lossless KV cache compression baseline.

# Excerpts / key facts (from PDF)

- Authors: Yuetao Chen, Peng Wang, Hong Xu (CUHK / Unaffiliated).
- Stack: FlashInfer 0.6.12 attention + SGLang KV manager; CUDA Graphs; 16-token KV pages; H100 80 GB HBM3, CUDA 13.0, PyTorch 2.11.0.
- Models: Llama 3.1 8B Instruct, Qwen3-8B; BF16 KV; workloads 8192 input / 256 output tokens.
- Baselines: uncompressed SGLang+FlashInfer; IBP, SplitZip, nvCOMP LZ4 (each decompresses layer KV into GPU buffer before FlashInfer).
- Instrument: SplitZip/IBP/LZ4 decompression is 32.7–73.8% of instrumented decode time (batch 32, 2048 input).
- Decode attention: 1.23–1.25× vs FlashInfer (18.5–20.2% lower latency); e.g. 8K ctx batch 64 Llama 704.6→562.7 µs.
- Framework throughput @ batch 32: ZipFusion 2044 tok/s Llama / 1882 Qwen (+15.3% / +15.2% vs SGLang); vs SplitZip 2.51× / 2.57×.
- Max batch under mem fraction 0.8: Llama 46→57, Qwen 40→50; max-batch throughput +26.3% Llama / +25.8% Qwen vs uncompressed SGLang; up to 2.76× (Llama) / 2.61× (Qwen) vs best lossless baseline; absolute ~2453 / 2042 tok/s (~1.26× SGLang).
- Format: lossless BF16 exponent-block encoding; reconstruct in registers via bit ops; no uncompressed KV copy kept for attention.
