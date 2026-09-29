---
type: Paper
title: "DynBranch: Speculative Subgraph Reuse for Agentic Serving"
description: "NUS — Qwen3-32B@4×H200；相对最强基线均值延迟最高 −32%；相对无复用底 −46–66%"
tags:
- architecture
- llm
- inference
- serving
- serving-system
- agentic-ai
- ai-agent
- kv-cache
- scheduling
- latency
- throughput
- speculative-decoding
created: 2026-09-29
updated: 2026-09-29
timestamp: '2026-09-29T00:00:00Z'
paper_author: [Junyi Shen, Noppanat Wadlom, Zhengyuan Su, Yao Lu]
year: 2026
arxiv: '2609.31047'
sources:
  - raw/papers/DynBranch_Speculative_Subgraph_Agentic_2026.pdf
  - raw/papers/dynbranch-speculative-subgraph-agentic.md
---

# DynBranch: Speculative Subgraph Reuse for Dynamic Agentic LLM Serving

## 一句话结论

在 **branch-resolution barrier**（下游子图要等模型/用户决议才开跑）上，用模板坐标让未决议分支可寻址：决议窗口内投机 fill + 跨请求精确新鲜复用 + 负载定价准入；Qwen3-32B @ 4×H200 上相对各负载最强先验系统均值延迟最高 **−32%**，相对无复用底 **−46–66%**。

## 动机

- Agentic 工作流运行时决定路径；测量显示 **45–57%** 端到端延迟是模型输出后才串行的下游时间。
- 纯缓存：复用键要决议后才知；纯请求内投机：不跨请求共享子图结果；前缀 KV 与 dataflow 调度都不联合解决「决议前启动 + 跨请求复用 + 按负载定价」。

对照 [PipeSwift](/papers/pipeswift-pipeline-parallel-agentic-serving.md)、[Ask the Tool](/papers/ask-tool-progress-agent-kv-serving.md)、[Crossflow](/papers/crossflow-pd-elasticity-agentic.md)。

## 方案

1. **C1 共享子图复用**：记录子 DAG + 输入 + 外部读；精确匹配且读仍新鲜才消费；写失效。
2. **C2 决议前 fill**：工作流模板提供决策点坐标；候选子图在分辨率窗口跑；错误预测不可见、不改结果。
3. **C3 负载定价准入**：两级控制器按 decode/KV 占用抬高价格，期望收益超过价格才生成/执行 fill。
4. **部署边界**：挂在 model-API（SGLang/vLLM）与 harness 之间，不改引擎。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 32B/4×H200 vs 各负载最强外部基线（低负载） | 均值延迟 **−14–32%** |
| 高负载 Routing/Sub-Agent/HCI / ReAct | **−15–31%** / **−6.2%** |
| vs 无复用底 | **−46–66%** |
| p99 vs 无复用底（Routing/ReAct/Sub-Agent） | 高负载 **−11–33%**；低负载 **−19–36%** |
| C2 vs 仅 C1（高负载） | Sub-Agent **−30%**、HCI **−35%**、Routing **−8.6%** |
| Qwen3-8B@4×4090 vs 最强基线 / 无复用底 | **−6.9–37.6%** / **−29.6–54.6%** |
| Fanout K=0→3（4 workers） | 均值 **18.2→15.2 s**；每请求投机 GPU 秒 **+19.8**；丢弃份额 **20%→33%** |

## 与 wiki 的关系

- [PipeSwift](/papers/pipeswift-pipeline-parallel-agentic-serving.md) — JCT/PP；本文是 **分支决议窗口投机**
- [Ask the Tool](/papers/ask-tool-progress-agent-kv-serving.md) — 工具等待期 KV；本文是 **子图结果复用**
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 服务编排层正交补丁

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.31047) — Shen et al., NUS, arXiv:2609.31047
[2] [raw stub](raw/papers/dynbranch-speculative-subgraph-agentic.md)
