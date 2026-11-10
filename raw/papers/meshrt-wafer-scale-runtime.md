---
type: Raw Source
title: "MeshRT: Compile-Time Governed Wafer-Scale Runtime for Low-Latency High-Throughput Inference"
source_url: https://arxiv.org/abs/2611.08508
pdf: MeshRT_Wafer_Scale_Runtime_2026.pdf
retrieved: 2026-11-10
ingested: 2026-11-10
org: University of Edinburgh / Microsoft Research
venue: SOSP '26
---

# Abstract (verbatim gist, arXiv:2611.08508)

Wafer-scale accelerators promise ultra-low-latency AI inference, but current system stacks still carry an unsustainably high cost premium. The reason is that many current and emerging inference techniques, such as batching and MoE, introduce runtime dynamism that existing wafer-scale systems cannot support efficiently. As a result, they must choose between two unsatisfactory options: accept suboptimal latency, or preserve low latency by restricting dynamic techniques, thereby limiting the models they can support and reducing aggregate throughput. This tradeoff significantly increases the cost of low-latency serving.

We present MeshRT, the first wafer-scale system to achieve both ultra-low latency and high throughput for LLM inference. MeshRT achieves this via a novel system architecture, which we call compile-time governance of runtime dynamism. This architecture features new system abstractions and mechanisms that enable MeshRT to compile dynamic events arising from LLM inference directly into per-core schedules, enabling asynchronous and decentralized execution with low runtime overhead. Implemented on a commodity wafer-scale accelerator, MeshRT preserves ultra-low latency while improving throughput by up to 56× over the state-of-the-art system for wafer-scale accelerators. Against measured single-instance SGLang results on H200, MeshRT achieves 4.5–7.0× lower latency. Under ideal linear scaling of those GPU measurements to an approximately power-matched H200 cluster, MeshRT achieves 1.7–13.0× higher decode system throughput in the low-latency regime.

# Excerpts / key facts

- Authors: Congjie He, Le Xu, Zhan Lu, Yeqi Huang, Haocheng Xiao, Cheng Deng, Luo Mai (Edinburgh); Lingxiao Ma, Ziming Miao, Fan Yang (Microsoft Research).
- Venue: SOSP '26, September 29–October 02, 2026, Prague.
- Platform: Cerebras WSE-3 / CS-3；文中写约 900,000 PE、762×1172 2D 阵列、44 GB SRAM、21 PB/s 聚合带宽、每 PE 约 48 KB SRAM。
- 方案：compile-time governance of runtime dynamism = dynamism-aware per-core schedule synthesis + safe incremental materialization（段边界死锁无关片上重配）。
- 模型：Qwen3.5-9B、GPT-OSS-20B、Qwen3.5-35B-A3B、GPT-OSS-120B。
- vs WaferLLM 匹配配置（Fig 10 / Table 3，4K，micro-bs=1）：Qwen3.5-9B 多 40 µs（9.5%）、GPT-OSS-20B 多 25 µs（7.6%）；单用户吞吐 0.91× / 0.93×。
- vs WaferLLM 峰值系统吞吐（Table 3）：9B 6.3×、20B 32.7×、35B-A3B 28.3×、120B 55.8×（摘要作 up to 56×）。Fig 9：prefill 4.0–6.6×，decode 最高 55.8×。
- vs 单实例 SGLang@H200 延迟向 decode（Table 2a User）：9B 6.1×、20B 7.0×、35B-A3B 4.5×、120B 6.0×（摘要 4.5–7.0× lower latency）。
- 功率匹配 H200 集群投影 decode 系统吞吐（Table 2a Sys；20 H200 / CS-3，10.2 kW/DGX H200）：9B 13.0×、20B 8.2×、35B-A3B 1.7×、120B 10.6×（摘要 1.7–13.0×）。
- Table 4 decode 策略分解：流水线并行 5.5–30.1×，连续批处理 1.6–1.7×，专家并行 1.2–1.4×。
