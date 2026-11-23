---
type: Raw Source
title: "Kameleo: In-Situ Activation-Precision Selection for Bit-Serial LLM Accelerators"
source_url: https://arxiv.org/abs/2611.25971
pdf: Kameleo_Bit_Serial_Activation_Precision_2026.pdf
retrieved: 2026-11-23
ingested: 2026-11-23
org: MICAS, KU Leuven
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.25971)

Weight-only quantization keeps the activations of large language models (LLMs) in a higher-precision format, pushing the on-chip inference cost to the activation arithmetic. Bit-serial, variable-length accelerators offer a promising path to reduce this cost by lowering activation precision while preserving model quality. They process only the mantissa bits that each layer needs. The length has to be chosen per layer and operator, and today it is chosen by offline calibration: a search driven by the perplexity of the full model on a representative dataset. The search is repeated for every model and workload, and its result degrades silently on other data. This paper presents Kameleo, an accelerator that selects the activation precision at runtime, on the accelerator, from the data it is processing. Kameleo replaces the global perplexity by a local proxy that compares the output of each GEMM at reduced and at full precision. It exploits the fact that a bit-serial datapath produces this comparison almost for free, because the reduced-precision result is an intermediate state of the full-precision computation. Two passes over the first tokens of a workload set the precision of every GEMM. On four LLMs and seven datasets, Kameleo stays within a 1% perplexity budget at a 2.11-2.34x reduction of prefill cycles on the matrix multiplication unit (MXU), close to the reduction of configurations calibrated offline on the evaluation data itself. Calibrated configurations transferred to other data, in contrast, often violate the budget. The selection hardware adds only 3.7% to the accelerator area. Kameleo thereby makes variable-length mantissas feasible in real deployments, where offline calibration for every model and workload is not.

# Excerpts / key facts

- Authors: Robin Geens, Thomas Debelle, Marian Verhelst, Chao Fang。arXiv:2611.25971，cs.AR，提交标注 19 Nov 2026。与 rising-precision VLA 加速器同属 KU Leuven MICAS。
- 模型：Llama2-13B、Llama3.1-8B、Qwen2.5-7B、Yi1.5-34B。权重 INT4（OmniQuant 初始化，无学习 clipping）。质量按 2048-token 窗口 PPL，预算相对 W4A16、满 11-bit BFP 尾数恶化 1%。
- 吞吐按 prefill MXU 周期相对 W4A16 + FP16 激活的解析计数，并用周期精确 RTL 仿真校验。WikiText2 上 Kameleo 为 2.12–2.29×；摘要给出四模型七数据集为 2.11–2.34×。
- TSMC 16 nm、250 MHz、0.75 V 综合。选择硬件使加速器面积 +3.7%、推理期 MXU 功耗 +3.5%；选择过程中 MXU 功耗 166.7 mW（相对 ANDA +50%）。
- 离线 ANDA 配置在 42 次跨数据集迁移里有 18 次超过 1% 预算，PPL 恶化最高 2.9%。Kameleo 在各数据集上自行选择，预算均满足，周期降低 2.25–2.28×。
