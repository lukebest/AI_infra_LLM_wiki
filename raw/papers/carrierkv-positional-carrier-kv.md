---
type: Raw Source
title: "CarrierKV: An Edge LLM Accelerator with Positional Carrier Decomposition for Low-Bit KV Cache"
source_url: https://arxiv.org/abs/2611.26857
pdf: CarrierKV_Positional_Carrier_Decomposition_2026.pdf
retrieved: 2026-11-24
ingested: 2026-11-24
org: Brown University; Google Research
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.26857)

Long-context decoding on edge devices is limited by DRAM, because every generated token reads the whole, growing KV cache. 4-bit block-scaled formats such as NVFP4 reduce this traffic but degrade accuracy: on Qwen3-4B, NVFP4 lowers 32K RULER (seven tasks) from 92.6 to 79.4, and a Hadamard rotation lowers it further to 57.7. We observe that most of the key energy is a positional carrier, one per-head vector that rotary position embedding (RoPE) rotates with position. In NVFP4, it sets the shared scale of most key blocks and lowers the signal-to-quantization-noise ratio of the content by about 5 dB, nearly one bit, yet it depends only on that vector and the position. We therefore introduce positional carrier decomposition, which removes the carrier before RoPE and stores only the content residual. We design a KV path that rotates and quantizes keys only after this removal and computes each attention score directly on the 4-bit code. We also design a positional phase engine that regenerates the carrier's score term for one key per cycle. At the same cache size as NVFP4, CarrierKV raises 32K RULER on Qwen3-4B from 79.4 to 91.1 and lowers the 32K PG19 perplexity increase of NVFP4 by 1.8 to 5.9 times on four models, outperforming SageAttention and P3-LLM on all four. Its loss also stays nearly flat as the cache grows, while that of NVFP4 rises. In a 22 nm FDSOI process at 600 MHz, CarrierKV's hardware increases the area of the NVFP4 accelerator by 2.9% and the energy of a 20K-token reasoning request on Qwen3-4B by 0.12% at the same decode latency. On Qwen3-4B at 32K, CarrierKV has a better RULER score than FP8 keys (91.1 against 89.3) and uses 13.7% less energy per token. The decomposition also lowers the 32K perplexity increase of 3-bit TurboQuant keys on Qwen3-4B from 69.7 to 0.76.

# Excerpts / key facts

- Authors: Junyi Luo, Xinting Jiang, Ruichen Qi, Quan Cheng, Mehdi Saligane（Brown University）；Gregory Kielian（Google Research）。arXiv:2611.26857，cs.AR，提交标注 19 Nov 2026。
- 准确率在四张 H100 上用软件模拟加速器格式；面积为 22 nm FDSOI、0.8 V、600 MHz 综合；时延与能量为 SCALE-Sim v3 + Ramulator 2.1（LPDDR5-6400 x64）。
- Qwen3-4B 32K RULER：BF16 92.6，NVFP4 79.4，SageAttention 86.9，P3-LLM 75.1，CarrierKV 91.1；面积 4.945→5.087 mm²（+2.9%），20K token 请求 86.595→86.700 mJ/token（+0.12%）。
