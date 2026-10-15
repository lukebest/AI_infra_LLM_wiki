---
type: Raw Source
title: "FORGE: Procedural Weight Generation for Sparse MoE Inference"
source_url: https://arxiv.org/abs/2610.16890
pdf: FORGE_Procedural_Weight_Generation_Sparse_MoE_2026.pdf
retrieved: 2026-10-15
org: University of Wisconsin-Madison / NVIDIA / Korea University
venue: ASPLOS 2027 (arXiv cs.AR)
---

# Abstract (verbatim, arXiv:2610.16890)

We introduce FORGE (Fast On-chip Rotor Generation for Experts), a procedural weight generation system for Sparse Mixture-of-Experts (MoE) inference. Rather than storing and loading every expert weight tensor from HBM, we show how a compact accelerator inside each Streaming Multiprocessor can regenerate them on-the-fly from $O(\log^2 d)$ rotor parameters per projection. Per replaced layer, gigabytes of stored expert weights are approximated with under a megabyte of seeds. This addresses the dual memory bottleneck of autoregressive Sparse MoE decode, where per-expert FFN operations are HBM-bandwidth-bound at small routed-token counts and the aggregate expert footprint forces multi-node Expert Parallelism (EP) with all-to-all traffic. We realize the approach as the Rotor Generation Unit (RGU), a fixed-function datapath that generates FFN weight tiles without competing with Tensor Core execution. With 30% of the MoE FFN layers replaced across five Sparse MoE models, we estimate 1.3-2.8x higher system throughput at matched GPU count and 1.10-1.15x lower per-user decode latency at short context. In exchange, downstream accuracy on three model families falls below that of the same model fine-tuned without rotor replacement, and the replacement ratio controls this tradeoff. FORGE also expands KV cache capacity by 1.2-2.6x. It is agnostic to the bit width at which weights are stored, so it can compose with quantization. The RGU is fully implemented/verified in SystemVerilog at ~0.9% SM area overhead (0.032 mm^2/SM, 7nm).

# Excerpts (from arXiv PDF v1)

- §1 / Table 1: MoE parameters are 94–98% of total footprint across five target MoEs at FP8; seed per replaced layer 594 KB (DeepSeek-v3.2), 509 KB (GLM-5), 276 KB (Qwen3-235B), 221 KB (Qwen3-30B), 776 KB (Qwen3-Coder-Next); compression 19,065× / 19,065× / 8,738× / 2,731× / 2,081×.
- §2.2: at B=32 on DeepSeek-v3.2 (K=8, E=256) each expert sees one token; cuBLASLt FP8 per-expert projections on H100 reach 50% SM compute utilization only at b_expert ≈ 512 (DeepSeek-v3.2/GLM-5 UpGate) or ≈ 4,096 (Qwen3-30B), i.e. serving batch B ≈ 16,384 / 65,536 tokens.
- §2.3: rotor projection uses a 3-stage pipeline (din→c chunks, m=2 rotor maps, c→dout chunks), n = floor(log2(min(din,dout))) ∈ {9,10,11}; each chunk has C(n,2) learned angles.
- Table 2: software SIMT generation alone is 25.8–45.1× slower than the full baseline expert GEMM; 76–149× more instructions; bank conflicts rise by two to five orders of magnitude.
- §4: RGU = Supertile Address Generator (0.5 KB Base ROM, 9 KB Mapping ROM, Schedule ROM from offline max matching over bank-conflict graph), 4-bank 1R1W Supertile SRAM 28.875 KB (FP8), 0.43 KB parameter buffer, dual 64-wide PE lanes, 2-cycle pair throughput; Output Streamer applies Phase-XOR swizzle into SMEM.
- Table 4 (per-MoE-FFN kernel speedup vs cuBLASLt FP8 on H100, 8 / 16 tok/expert): DeepSeek-v3.2 2.33×/1.29×; GLM-5 2.47×/1.40×; Qwen3-235B 3.23×/1.67×; Qwen3-30B 2.28×/1.13×; Qwen3-Coder-Next 2.34×/1.19×. Qwen3-235B per-expert latency 14.58 µs → 4.52 µs; DeepSeek-v3.2 23.48 µs → 10.06 µs.
- Table 5 (full-model decode speedup, B=1, r=0.3, T=4K/32K/128K): 1.10–1.15× at 4K, 1.07–1.11× at 128K.
- §5.4: at r=0.3 minimum-fit GPU count for DeepSeek-v3.2 and GLM-5 drops from 10/11 to 7/8, fitting in one NVLink node.
- §5.5: freed weight HBM = 28–29% of total parameter memory; U_max 1.2–2.6× at T=4096, 1.1–3.5× at T=131072; system throughput 1.3–2.8× (r=0.3), 2.0–6.1× at r=0.7 (accuracy not evaluated, what-if).
- Table 6 (ASAP7 7 nm): logic 0.017 mm², SRAM 0.015 mm², total 0.032 mm²/SM (~0.9% of 3.475 mm² SM); 1.80 GHz; logic power 35.9 mW; ~4.2 mm² and ~5.1 W across 132 SMs (0.5% die, 0.7% of 700 W TDP).
- Table 7 (r=0.3, WikiText ppl / ARC-C / HellaSwag): Qwen3-30B Baseline+LoRA 6.53/55.72/60.88 vs FORGE 7.65/51.36/57.10; ERNIE-21B 5.93/58.96/62.50 vs 7.16/57.25/59.30; Qwen3-Coder-Next 5.99/61.86/63.99 vs 6.88/60.41/60.52.
- §5.8 limitations: baseline measured, design simulated; decode/throughput via analytical simulator (validated within 7.6% MAE in prior work), no SM contention/occupancy effects; synthesis covers RGU alone, excludes SM wiring; predictive 7 nm vs commercial 4 nm baseline.
