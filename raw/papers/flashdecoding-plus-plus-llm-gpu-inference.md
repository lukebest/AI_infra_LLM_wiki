---
source_url: https://arxiv.org/abs/2311.01282
ingested: 2026-06-24
sha256: c1428ddf443c20041b647c8a30e3ebb3f247e7c0debd3f4cb18c147848aaf599
---

# FlashDecoding++: Faster LLM Inference on GPUs (arXiv 2024)

**Authors:** Ke Hong, Guohao Dai, Jiaming Xu, Qiuli Mao, Xiuhong Li, Jun Liu, Kangdi Chen, Yuhan Dong, Yu Wang — Tsinghua, SJTU, PKU, Infinigence-AI

**Venue:** arXiv:2311.01282v4, Jan 2024

## Three bottlenecks in LLM inference

1. **Synchronized partial softmax** — FlashAttention/FlashDecoding tile attention; cross-tile max update → **~18.8%** attention overhead (Llama2-7B, A100, seq=1024)
2. **Flat GEMM under-utilization** — decode phase M≪64; cuBLAS/CUTLASS pad M to 64 → **>50%** wasted compute
3. **Static dataflow** — single Tensor Core path suboptimal for GEMV vs flat GEMM vs large GEMM → up to **50.25%** loss

## Technique 1: Asynchronized softmax + unified max φ

- Softmax scale factor can be any ϕ ∈ R (not only max); choose ϕ from empirical xi range (>99.99% xi within bounds for Llama2)
- Partial tiles compute ⟨softmax(x), v⟩ numerator/denominator independently; no sync between partial softmax updates
- Overflow/out-of-range → fallback to synchronized partial softmax (FlashDecoding)
- OPT-6.7B excluded (wide xi range)

## Technique 2: Flat GEMM + double buffering

- Pad M to **8** (Tensor Core native) not 64
- Small N: parallelism-bound → tune BN for SM count (~128–256 blocks)
- Large N: memory-bound → **double buffering** in shared memory (load next tile while compute current)

## Technique 3: Heuristic dataflow

Per LLM only **4 [N,K] shapes** (K/Q/V proj, O proj, FFN1, FFN2). Three impls:
- **ImplA:** FastGEMV (CUDA Core) — best for small M
- **ImplB:** flat GEMM (Section 4) — Tensor Core
- **ImplC:** CUTLASS — large M prefill GEMM

Offline profile inflection points M1 (A vs B), M2 (B vs C) per [N,K]; runtime lookup table.

## Chip / eval setup

- NVIDIA: A100 80GB, RTX 3090; AMD: MI210, RX 7900 XTX
- Models: Llama2-7B/13B, OPT-6.7B, ChatGLM2-6B
- Baselines: HF, vLLM, DeepSpeed, TensorRT-LLM, OpenPPL, FlashAttention2/FlashDecoding

## Results (decode unless noted)

| vs baseline | Speedup |
|-------------|---------|
| Hugging Face (NVIDIA) | up to **4.86×** |
| Hugging Face (AMD MI210) | up to **3.93×** |
| FlashDecoding (A100 avg) | **1.37×** |
| vLLM / DeepSpeed / TRT-LLM / OpenPPL / FlashDecoding (avg) | 1.24× / 1.44× / 1.13× / 1.24× / 1.21× |
| HF prefill | up to **1.40×** |

Figure 1 claim: batch=1, input 1K → up to **92×** faster first token vs HF on A100 (marketing chart; decode each-token also large gains).

## Relation

- Builds on FlashAttention [18,19], FlashDecoding [13]
- Complements serving systems (vLLM KV paging) — kernel-level decode optimization
- Prefill still GEMM-heavy; decode = flat GEMM/GEMV + attention (see [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md))
