---
type: Paper
title: "PipeSwift: Pipeline Parallelism for Completion-Oriented Agentic Serving"
description: 清华等 — JCT-aware PP+MTP；360B+ MoE×64 H800；JCT vs SGLang EP 1.21–1.45×、vs vLLM PP2 1.60–2.33×、vs PD-disagg 1.14–1.54×
tags:
- agentic-ai
- ai-agent
- serving
- serving-system
- disaggregated-inference
- moe
- llm
- inference
- prefill
- decode
- scheduling
- parallelism
- pipeline
- speculative-decoding
- throughput
- latency
- architecture
timestamp: '2026-09-17T00:00:00Z'
created: 2026-09-17
updated: 2026-09-17
sources:
- raw/papers/PipeSwift_Pipeline_Parallel_Agentic_Serving_2026.pdf
- raw/papers/pipeswift-pipeline-parallel-agentic-serving.md
---

# PipeSwift: Revisiting Pipeline Parallelism for Large-Scale Completion-Oriented Agentic Serving

**Authors:** Shiju Wang, Fei Ren, Fangcheng Fu, Zhanhong Tan, Kairui Li, Jingwei Cai, Kaisheng Ma
**Affiliation:**（文内；Kaisheng Ma 组等）
**arXiv:** [2609.16491](https://arxiv.org/abs/2609.16491)（2026-09-15，cs.DC；Wed 9/16 列表）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.16491)

相对 chatbot 的 TTFT/TPOT SLO，agent 长程工作流以 **job completion time（JCT）** 为主目标。PipeSwift 证明 **prefill 优先≠最优 JCT**，并在大规模 MoE 上复活 **pipeline parallelism（PP）** 与 **pipeline-integrated MTP**。

## 动机

- Coding / web-search / research agent：每轮模型输出决定后续工具与环境转移，用户感知的是整条轨迹完成时间。
- Prefill-prioritized 调度可拿最好 TTFT 与 decode 吞吐，但文内调度空间探索显示 completion time 可差到 **1.40×**，最优点不在两端。
- 既有 wide-EP（DeepSeek-V3 式）与开源 PP（vLLM PP 缺 MTP/灵活调度；SGLang PP 评测模型跑不通）未按 JCT 共设计。

## 方案

1. **JCT-aware 调度层**：编排 prefill/decode 波次与 micro-batch；管线 flush 后重划 decode micro-batch。
2. **Pipeline-integrated MTP**：verify–extend–draft 环嵌入 PP 各级；末级少分 backbone 层以容纳 MTP/采样开销（相对 SGLang 的 draft–verify–extend）。
3. **SPMD 运行时**：各 stage 本地决定 NCCL P2P 与 micro-batch，避免中心调度器逐步交换。
4. 评测：确定性重放 SWE-Bench / BrowseComp；**GLM-4.7-360B**、**Qwen3.5-397B**；**64×H800-80GB**。

## 效果（仅论文数字）

| 对照 | Overall JCT 加速 |
|------|------------------|
| vs SGLang wide-EP | **1.21–1.45×**（峰值并发可达 **1.86×** vs 无 prefill-delay EP16） |
| vs vLLM PP2 | **1.60–2.33×** |
| vs 开源 PD-disagg（2P2D，128 GPU） | **1.14–1.54×** |
| Ablation vs vLLM PP2 | 仅调度层 **1.31×**（40.35→30.73 min）；再加 MTP 到高端点 |

**口径：** 系统/serving 论文；JCT 为批次墙钟完成时间，勿与单流 tok/s 横比。2P2D 基线用 128 GPU（64P+64D），同任务对比需读正文。

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — **PP 共置** vs PD 解耦在 **agentic JCT** 下的再评估；对照 [PDD](/papers/pdd-cross-datacenter-prefill-decode-disaggregation.md) 的跨 DC PD
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — JCT 由 prefill/decode 效率平衡决定
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — MoE EP/all-to-all 与 PP stage 通信对照
- [UNISON](/papers/unison-near-memory-scheduler-llm-agents.md) — agent 会话 KV 硬件调度 vs 本文 serving 并行策略
- [RoofLang](/papers/rooflang-ai-driven-llm-inference-architecting.md) — agent 负载建模另一侧

## 开放问题

1. 开源 PD 栈补齐 MTP 与动态调度后，2P2D 差距是否收窄。
2. 更长工具等待 / 更高 turn 数下 PP bubble 与 KV 增长如何交互。
3. 与硬件侧 agent 内存路径（UNISON 等）的联合设计未展开。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.16491) — Wang et al., arXiv:2609.16491
[2] [raw/papers/pipeswift-pipeline-parallel-agentic-serving.md](raw/papers/pipeswift-pipeline-parallel-agentic-serving.md) — ingest stub
