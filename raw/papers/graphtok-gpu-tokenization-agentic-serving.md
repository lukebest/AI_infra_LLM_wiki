---
type: Raw Source
title: "Taking Tokenization off the Host for Agentic LLM Serving (GraphTok)"
source_url: https://arxiv.org/abs/2610.13325
pdf: GraphTok_GPU_Tokenization_Agentic_Serving_2026.pdf
retrieved: 2026-10-13
org: KTH Royal Institute of Technology
venue: arXiv preprint (cs.DC)
---

# Abstract (verbatim, arXiv:2610.13325)

Agentic workloads resend long contexts that barely change between calls. Prefix caching now skips most of their prefill, yet every request must still be tokenized in full before the cache can even be consulted. Tokenization, a CPU stage long treated as negligible, becomes the largest part of time-to-first-token (TTFT), and a frontend that tokenizes for a whole GPU fleet limits how many GPUs it can feed. We present GraphTok, a GPU tokenizer that runs the entire encoding pipeline, from pre-tokenization through byte-pair encoding (BPE) merging to token-ID assembly, as one replayable CUDA graph. GraphTok reproduces the reference token IDs bit-for-bit on GPT-2, Llama 3, Qwen 2.5, DeepSeek-V3, and Gemma 3, hands short inputs to a CPU engine where the GPU cannot win, and plugs into unmodified vLLM and NVIDIA Dynamo. GraphTok encodes one million GPT-2 tokens in 1.7-3.2 ms including data transfers, and on Llama 3 it is 4.7-6.0x faster than gigatoken, the strongest CPU tokenizer. On TokTier's own single-request benchmark, it is 2.6-3.9x faster than gigatoken and up to 18.1x faster than TokTier. In vLLM with a cached prefix, it lowers mean TTFT by 2.1-2.4x. The largest gain is capacity. Within a 2 s P99 target, one Dynamo frontend with GraphTok sustains 518 requests/s of 121k-token traffic, the busiest-hour load of 56 GPUs, against 296 with gigatoken and 18.5 with the default tokenizer. Across 121k to one million tokens, this is 1.75-2.5x the load gigatoken sustains, with a P99 up to 64x lower where gigatoken's tail breaks.
