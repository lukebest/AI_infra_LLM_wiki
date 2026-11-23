---
type: Raw Source
title: "Rethinking KV Caching for LLM Decode: Free-Space Optical KV Regeneration for Reduction of Memory Traffic"
source_url: https://arxiv.org/abs/2611.19279
pdf: OptiDecode_FSO_KV_Regeneration_2026.pdf
retrieved: 2026-11-23
ingested: 2026-11-23
org: National University of Singapore; Lumai Ltd.
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.19279)

Long-context large language model (LLM) decoding repeatedly reads the historical key-value (KV) cache, making multi-head attention (MHA) memory-bandwidth-bound. Caching layer-input activations instead halves historical-cache storage and traffic, but requires regenerating KV from each cached activation. On digital accelerators such as GPUs, this regeneration takes far longer than fetching the activation from HBM. The KV regeneration overhead outweighs the savings from reduced memory traffic, shifting decode attention from a memory bottleneck to a compute bottleneck. We present OptiDecode, a hybrid optoelectronic decode-attention accelerator that regenerates historical KV using free-space optics and computes attention digitally. Projection weights remain resident on optical tiles, exploiting reuse across historical tokens for high-throughput optical regeneration. Scaling to large models introduces two challenges. First, distributing weights across tiles requires sending the same activations to every head group, while each readout die produces only partial KV. Activation replay shares one set of electrical-to-optical converters across head groups without costly broadcast. In-situ attention avoids transferring partial KV from readout dies to reducers by computing on them locally and exchanging only partial scores, probabilities, and partial outputs. Second, processing an activation chunk through all dependent stages takes longer than one activation-fetch interval. Chunk pipelining overlaps successive chunks so that OptiDecode sustains the HBM activation-fetch rate. OptiDecode demonstrates 1.92-1.99x decode-attention speedup over an ideal GPU KV-read baseline at equal peak HBM bandwidth (A100-B200), for 32K-token contexts across evaluated 30B-175B MHA models, approaching the 2x upper bound from halving historical memory traffic.

# Excerpts / key facts

- Authors: Aritra Bagchi, Bin Gao, Weng-Fai Wong, Tulika Mitra（National University of Singapore）；James Spall, Jakub Pietrak（Lumai Ltd.）。arXiv:2611.19279，cs.AR / cs.ET，提交标注 14 Nov 2026。
- 主对照是理想 GPU KV 读取基线：按峰值 HBM 带宽流式读取 2Ndb 字节 INT8 历史 KV，注意力计算全部被隐藏。默认 batch 1。目标模型为 ≥30B 的稠密 MHA（d≥7,168）。
- Fig. 11：30B 及以上模型在 32K token、A100–B200 四档等带宽下达到 1.92–1.99×；128K 时约 1.98× 或更高。OPT-175B 在 B200、1K token 时 batch 1 为 1.07×，batch 8 为 1.80×。
- Fig. 13（OPT-175B，32K，batch 1）：OptiDecode 注意力相对实测 GPU 注意力为 1.99–3.30×，整层相对 GPU roofline 为 1.18×（此处计入权重加载，FFN 按 GPU roofline）。
- 能量为参数化一阶模型。相对 TDP 基线，8 / 4.8 / 2.04 TB/s 下为 3.31 / 3.37 / 3.66 µJ per historical token per layer，分别低于 Blackwell Ultra / H200 SXM / A100 SXM 估计值 23% / 6% / 24%；相对 NVML 实测再低 37–43%。
