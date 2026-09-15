---
type: Paper
title: "RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems"
description: 行云智理/MSR — DSL+roofline 仿真驱动架构搜索；V4 系峰值 decode 相对对照 3.5–39.5×；B300 agent +6.23–50.1%
tags:
- inference
- serving-system
- llm
- decode
- prefill
- kv-cache
- moe
- deepseek
- nvidia
- architecture
- optimization
- parallelism
- throughput
- latency
- batching
- distributed
- scale-up
timestamp: '2026-09-15T00:00:00Z'
created: 2026-09-15
updated: 2026-09-15
sources:
- raw/papers/RoofLang_AI_Driven_LLM_Inference_Architecting_2026.pdf
- raw/papers/rooflang-ai-driven-llm-inference-architecting.md
---

# RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems

**Authors:** Ziyue Yang*, Yuting Jiang, Lei Qu, Peng Cheng（*通讯）
**Affiliation:** Shanghai Xingyunzhili Artificial Intelligence Institute；Microsoft Research
**arXiv:** [2609.12551](https://arxiv.org/abs/2609.12551)（2026-09-11，cs.DC）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.12551)
**Code/site:** https://github.com/yzygitzh/rooflang ；https://yzygitzh.github.io/rooflang

相对纯 profiling 调参（被现有栈能力绑定），RoofLang 提供 **与实现无关** 的 workload 图 + 可验证架构动作 + roofline 离散事件评估，让 agent 在「换并行/放置/图变换」层搜索。价值在 **架构发现数字**，不只是 DSL 工具本身。

## 动机

现有 AI 优化多盯 kernel/编译/框架配置，反馈来自 profiling——搜不到「当前栈实现不了」的更好系统架构。要闭环需要：通用 workload 表示、可验证变异空间、少受软件实现噪声干扰的评估器。

## 方案

**RoofLang DSL。** 工作负载与硬件建成图；**placement 原语** + **语义保持变换**（表 1–2）；评估器用 roofline 离散事件仿真暴露算力/内存/网络/依赖/争用/寿命/容量成本。

**评测模型（表 3–4）。** DeepSeek V4 Flash（284B-A13B，CSA+HCA）、V4 Pro（1.6T-A49B）、GLM-5.3、Kimi K3；V4 系 KV 为 **FP8 main + FP4 index**。硬件假设 H200 / GH200 / B300 / GB300（表 5；NVLink scale-up）。**仿真，非硅实测。**

## 效果（仅论文数字）

**模型级峰值 decode（64×GB300）。** 64K / 1M 上下文：V4 Flash 相对 GLM-5.3 **9.6× / 16.7×**，相对 Kimi K3 **25.2× / 39.5×**；V4 Pro 相对 GLM **3.5× / 5.3×**，相对 Kimi **9.3× / 12.4×**。文称差距主要来自紧凑 KV → 更大可持续 batch、更低每 token 内存流量（表 7–8：如 64K 上 Flash per-decode-token KV 读 **0.192 GiB** vs 更大模型显著更高）。摘要归纳 DeepSeek V4 系可达对照模型 **3.5–39.5×** 峰值 decode 吞吐。

**Agent 架构改进（DeepSeek V4 Pro @ B300）。** 吞吐与交互性同时提升 **6.23–50.1%**：例如 decode-64K / 256 GPU / B=4096 / EP=PP=16 的代价感知 PP 重切 **+20.3%**；prefill-8K / 8 GPU 上 DP–CP expert split 去本地 Gather–Scatter **+6.23%**；prefill-1M / 16 GPU 节点内专家复制改走节点内 NVLink **+50.1%**。

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — RoofLang 搜索空间含并行/放置；与 PD/EP 机柜拆分同层问题，但是 **仿真探索**
- [DeepSeek-V4](/entities/deepseek-v4.md) — 文中 CSA+HCA 与紧凑 KV 精度配置是吞吐差距主因之一
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) / [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — decode 峰值由每 token 内存流量主导的分析呼应
- [NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 节点内复制换 IB 路由的案例依赖 SU 域

## 开放问题

1. 评估器是 roofline DES，不是真实 serving 栈；选出的架构仍需 kernel/框架落地验证。
2. 模型/硬件规格取自公开配置与假设表，跨代 SKU 数字会漂。
3. Agent 改进幅度高度依赖初始图与约束；不可当通用加速承诺。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.12551) — Yang/Jiang/Qu/Cheng, arXiv:2609.12551
[2] [raw/papers/rooflang-ai-driven-llm-inference-architecting.md](raw/papers/rooflang-ai-driven-llm-inference-architecting.md) — 结构化摘录
