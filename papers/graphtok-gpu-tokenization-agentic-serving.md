---
type: Paper
title: "Taking Tokenization off the Host for Agentic LLM Serving (GraphTok)"
description: "KTH — agentic 请求前缀缓存命中后，CPU 分词成了 TTFT 最大头；GraphTok 把预分词→BPE 合并→token ID 组装整条流水线做成一张可重放 CUDA graph，逐位复现参考结果；vLLM 前缀命中下 TTFT 降 2.1–2.4×，一个 Dynamo 前端在 2 s P99 下撑 518 req/s（121k token，约 56 张 GPU 的峰时负载）"
tags:
- agentic-ai
- serving
- serving-system
- inference
- latency
- gpu
- kv-cache
- nvidia
created: 2026-10-13
updated: 2026-10-13
timestamp: '2026-10-13T00:00:00Z'
paper_author: [Mohammad Siavashi, Pascal Schwinte, Ali Banaei, Gerald Q. Maguire Jr., Marco Chiesa, Dejan Kostić]
year: 2026
arxiv: '2610.13325'
venue: arXiv preprint (cs.DC / cs.PF)
sources:
  - raw/papers/GraphTok_GPU_Tokenization_Agentic_Serving_2026.pdf
  - raw/papers/graphtok-gpu-tokenization-agentic-serving.md
---

# GraphTok：把分词搬上 GPU，解开 agentic 服务的前端瓶颈

## 一句话结论
Agentic 调用每次重发几乎不变的长上下文，前缀缓存省掉了大部分 prefill，但查缓存前必须先把整段输入分词（追加文本会改变分词结果，前缀 token 不能简单拼接）。分词因此从可忽略的 CPU 阶段变成 TTFT 的最大组成，也限制了一个前端能喂多少张 GPU。GraphTok 把完整编码流水线放进一张固定 CUDA graph 在 GPU 上执行。

## 动机（论文数字）
- TraceLab 约 4,300 个编码 agent 会话：单次调用中位数约 **119K** 缓存前缀 token、**875** 个新 token、**214** 个输出 token；**95.7%** 输入 token 来自前缀缓存。
- vLLM 0.27、单张 H100 NVL：冷缓存时分词占中位 TTFT 仅 **2%**（Llama 3.1 8B，130k token）/ **1%**（Qwen3 32B，40.5k）；前缀命中后升到 **67% / 49%**，成为最大剩余项。

## 方案
| 难点 | 做法 |
|---|---|
| 预分词是正则串行扫描 | 按分词器族把“某位置是否开启新 pre-token”写成局部谓词，并行求值后前缀和压缩成有序索引；支持 Llama 3、DeepSeek-V3 三遍规则等 |
| BPE 合并在 pre-token 内有序且数据相关 | pre-token 之间天然并行；pre-token 内并行搜索下一个最高优先级合并，只在可证明与串行等价时一次应用多个合并；按长度分桶映射到 warp |
| 不规则工作与固定 CUDA graph 冲突 | 图内处理不定长：一次捕获的图可处理容量内任意请求，无中间分配、主机同步与 host 侧调度 |
| 短输入 GPU 不占优 | 自动交给 CPU 引擎；以独立进程运行，可经 MPS 复用推理空闲的 SM |

- 在 GPT-2、Llama 3、Qwen 2.5、DeepSeek-V3、Gemma 3 上逐位复现参考 token ID；无改动接入 vLLM 与 NVIDIA Dynamo。

## 效果（仅论文数字，H100 NVL）
- 一百万 GPT-2 token 编码 **1.7–3.2 ms**（含传输）；Llama 3 上比最强 CPU 分词器 gigatoken 快 **4.7–6.0×**；在 TokTier 单请求基准上比 gigatoken 快 **2.6–3.9×**、比 TokTier 最高快 **18.1×**。
- vLLM 前缀命中：平均 TTFT 降 **2.1–2.4×**；冷缓存时仅改善 2–4%；单个无竞争请求下快速 CPU 分词器与 GraphTok 的平均 TTFT 差距在 4% 内，主要价值在前端 CPU 与容量。
- Dynamo 单前端、2 s P99：121k token 流量下 GraphTok **518 req/s**（按 BurstGPT 峰时每 GPU 9.25 req/s 折合 **56** 张 GPU），gigatoken **296**，默认分词器 **18.5**；121k–1M token 区间为 gigatoken 的 **1.75–2.5×**，gigatoken 尾延迟崩溃处 P99 最多低 **64×**。

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 前缀缓存把瓶颈推向请求前端
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — Dynamo 前端集中为整组 GPU 做分词/路由，前端容量成为扩展上限
- [Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md)、[Ask the Tool](/papers/ask-tool-progress-agent-kv-serving.md) — 同属 agentic 长前缀复用的服务侧优化
- [Heterogeneous Computing for AI Agent Inference](/papers/heterogeneous-computing-ai-agent-inference.md) — agent 负载里 CPU 侧开销上升的同类观察

## 局限与开放问题
- 评测覆盖五个生产 BPE 分词器；每个分词器族需要单独的前端规则，其他分词算法的适配论文未涉及（本页判断）。
- 分词与推理共卡时依赖 MPS/细粒度调度避免干扰；多租户下的 SM 争用未系统评估。

# Citations
- Siavashi et al., "Taking Tokenization off the Host for Agentic LLM Serving", arXiv:2610.13325, 2026. [raw](/raw/papers/graphtok-gpu-tokenization-agentic-serving.md) · [PDF](/raw/papers/GraphTok_GPU_Tokenization_Agentic_Serving_2026.pdf)
