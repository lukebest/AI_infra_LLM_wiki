---
type: Paper
title: "EAServe: Encode-Aware Disaggregated MLLM Serving"
description: "UGA 等 — PACT’26；EPD 解耦；goodput 最高 vs Dynamo 4.3×、vs vLLM 1.7×；A100 上 4.91 req/s"
tags:
- architecture
- llm
- inference
- serving
- serving-system
- disaggregated-inference
- prefill
- decode
- batching
- scheduling
- throughput
- latency
- gpu
created: 2026-09-29
updated: 2026-09-29
timestamp: '2026-09-29T00:00:00Z'
paper_author: [Kunxiong Zhu, Zhihao Shu, Hangyu Zheng, Minghai Qin, Miao Yin, Gagan Agrawal, Wei Niu]
year: 2026
arxiv: '2609.31551'
sources:
  - raw/papers/EAServe_Encode_Aware_Disaggregated_MLLM_2026.pdf
  - raw/papers/easerve-encode-aware-disaggregated-mllm.md
---

# EAServe: Encode-Aware Disaggregated Serving for MLLMs

## 一句话结论

把 MLLM 的 **Encode** 重定位为 EPD（Encode–Prefill–Decode）管线控制点：自适应微批 + 共驻 prefill 分流 + 动态 SM 分区，外加 HAS（剪枝 + TPE）搜 (alloc, B, s)；相对 NVIDIA Dynamo / vLLM 在 moderate SLO 档 goodput 最高 **4.3× / 1.7×**（PACT ’26）。

## 动机

- 文本 LLM 的 PD 解耦已成标配；MLLM 多出 **Encode**（CLIP/Whisper 等），形成三阶段 EPD。
- Dynamo 等把 Encode 当透传服务：按请求粒度、无下游流量调控；单次 encode 填不满 GPU，又因 TTFT 不敢盲目加大批，encode GPU **长期空转**，下游饥饿。
- 简单微批（B=8）能抬吞吐、降 TTFT，却会淹没 Prefill/Decode（文中 Table 1）。

对照 [Disaggregated Inference](/concepts/disaggregated-inference.md)、[Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md)、[Crossflow](/papers/crossflow-pd-elasticity-agentic.md)（文本 P/D 弹性）。

## 方案

1. **Runtime**：负载自适应 encode 微批；向共驻 prefill worker 做 rate-controlled partial offload（offload 比 s）；libsmctrl **空间 SM 分区**保共置可预期。
2. **HAS**：Stage-1 按阶段容量剖析剪掉失衡 alloc（例 7→3）；Stage-2 TPE Bayesian 精修 (alloc, B, s)。
3. **评测**：LLaVA-v1.6-34B / 视频 Qwen-32B / 音频 Ultravox-27B；8×GPU（含 A100、RTX 6000 Ada）；基线 Dynamo、vLLM、EPDServe、HydraInfer。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| Goodput vs Dynamo / vLLM（moderate tier，摘要） | 最高 **4.3×** / **1.7×** |
| Image moderate goodput | **1.93** vs vLLM 1.11 / Dynamo 0.95 req/s |
| Video / Audio moderate | **1.90** vs 1.32/0.95；**4.17** vs 2.77/0.98 req/s |
| P99 TTFT @ Λ=2（image / video vs Dynamo） | **233.8→10.8 s** / **144.8→18.0 s** |
| P99 TPOT（image / audio） | **764→72 ms** / **869→49 ms** |
| vs EPDServe / HydraInfer（LLaVA-34B, Λ=5） | Ada：**1.95** req/s（4.24× / 3.36×）；A100：**4.91**（4.86× / 3.25×） |
| Encode GPU 利用 | Dynamo &lt;10% → EAServe 持续约 **80%**（Fig.11） |

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 从文本 PD 扩到 **EPD 三池**
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — Encode 再加一轴异质性
- [Crossflow](/papers/crossflow-pd-elasticity-agentic.md) — 文本侧边界弹性；本文是 **模态入口控制**

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.31551) — Zhu et al., PACT ’26, arXiv:2609.31551
[2] [raw stub](raw/papers/easerve-encode-aware-disaggregated-mllm.md)
