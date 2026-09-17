---
type: Raw Source
title: "PipeSwift: Revisiting Pipeline Parallelism for Large-Scale Completion-Oriented Agentic Serving"
source_url: https://arxiv.org/abs/2609.16491
arxiv: '2609.16491'
ingested: 2026-09-17
sha256: 044ebd7d46b0c1c9e1dfb2355617a5300ecae827bbd2056365a059e038acbc04
---

# PipeSwift: Pipeline Parallelism for Completion-Oriented Agentic Serving

**Authors:** Shiju Wang, Fei Ren, Fangcheng Fu, Zhanhong Tan, Kairui Li, Jingwei Cai, Kaisheng Ma
**PDF:** [PipeSwift_Pipeline_Parallel_Agentic_Serving_2026.pdf](PipeSwift_Pipeline_Parallel_Agentic_Serving_2026.pdf)
**arXiv:** [2609.16491](https://arxiv.org/abs/2609.16491)（cs.DC；Wed 2026-09-16 列表）

## 问题

Agent 长程工作流由 completion time（JCT）主导，而非 chatbot 的 TTFT/TPOT SLO。现有 serving 按 token 级 SLO 优化，prefill 优先策略可拿到最好 TTFT/decode 吞吐，却不一定最优 JCT。

## 方法要点

- 系统探索调度区间：completion time 相对最优点可差到 **1.40×**。
- 论证 pipeline parallelism（PP）在 JCT 目标下提供更好的 prefill–decode 折中。
- PipeSwift：JCT-aware 调度层 + pipeline-integrated multi-token prediction（MTP）；SPMD 运行时。
- 评测：GLM-4.7-360B、Qwen3.5-397B；64×H800；SWE-Bench / BrowseComp 轨迹重放。

## 摘录数字（仅论文给出）

- Overall JCT：**1.21–1.45×** vs SGLang wide-EP；**1.60–2.33×** vs vLLM PP2；**1.14–1.54×** vs 开源 PD-disagg（2P2D）。
- Ablation（文内表）：相对 vLLM PP2，仅调度层 **1.31×**，再加 MTP 到更高端点。
