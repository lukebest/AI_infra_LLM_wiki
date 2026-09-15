---
type: Raw Source
title: "RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems"
source_url: https://arxiv.org/abs/2609.12551
arxiv: '2609.12551'
ingested: 2026-09-15
sha256: 6234726e5509e5f393041efc038cf2a50cdb7093cd94034a8927dab8d2637a34
---

# RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems

**Authors:** Ziyue Yang, Yuting Jiang, Lei Qu, Peng Cheng
**Affiliations:** Shanghai Xingyunzhili AI Institute; Microsoft Research
**PDF:** [RoofLang_AI_Driven_LLM_Inference_Architecting_2026.pdf](RoofLang_AI_Driven_LLM_Inference_Architecting_2026.pdf)
**arXiv:** [2609.12551](https://arxiv.org/abs/2609.12551)（2026-09-11，cs.DC）

## 问题

Profiling 绑定现有软件栈，难以发现「更好架构」。需要与实现无关的工作负载表示、可验证变异空间、评估器。

## 方法要点

- RoofLang DSL：图表示 workload/硬件；placement + 语义保持变换；roofline 离散事件仿真评估。
- 模型：DeepSeek V4 Flash/Pro、GLM-5.3、Kimi K3；平台 H200/GH200/B300/GB300（仿真假设）。

## 摘录数字（仅论文给出）

- 64×GB300：V4 Flash 峰值 decode 相对 GLM-5.3 **9.6×/16.7×**（64K/1M ctx），相对 Kimi K3 **25.2×/39.5×**；V4 Pro 相对 GLM **3.5×/5.3×**，相对 Kimi **9.3×/12.4×**。
- 优化 agent 在 B300 上改进 V4 Pro 吞吐与交互性 **6.23–50.1%**（PP 重切 20.3%；DP–CP expert split 6.23%；节点内专家复制 50.1%）。
- **仿真/分析，非实测硅。**
