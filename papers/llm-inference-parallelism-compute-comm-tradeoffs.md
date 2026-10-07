---
type: Paper
title: "Characterizing Parallelism Strategies in LLM Inference: Fundamental Compute-Communication Trade-offs"
description: "Dell CTO 办公室 — TP/PP/Hybrid 推理的统一解析模型（计算+集体通信+点对点+流水线气泡）；8×A100 NVLink 实测：prefill TP8 约 40% TTFT 在 NCCL，PP 更优；decode TP 消除气泡更优；有效带宽 prefill ~250 GB/s、decode ~150 GB/s（理论 600 GB/s）"
tags:
- inference
- parallelism
- prefill
- decode
- latency
- collective
- allreduce
- communication
- gpu
- nvidia
created: 2026-10-07
updated: 2026-10-07
timestamp: '2026-10-07T00:00:00Z'
paper_author: [Javad Mirzaei, Jeebak Mitra]
year: 2026
arxiv: '2610.05305'
venue: arXiv preprint
sources:
  - raw/papers/LLM_Inference_Parallelism_Compute_Comm_Tradeoffs_2026.pdf
  - raw/papers/llm-inference-parallelism-compute-comm-tradeoffs.md
---

# LLM 推理并行策略：计算–通信–气泡三分账

## 一句话结论

把分布式推理延迟拆成 **计算 + TP 集体通信 + PP 点对点通信 + 流水线气泡** 四项并给出解析式，解释为什么 **prefill 偏向 PP**（大消息、TP 每层两次 AllReduce 的同步代价高）而 **decode 偏向 TP**（S=1 时 PP 的填充/排空气泡占主导）。在 8×A100 NVLink 上，即便 TP8，decode 实测有效带宽也只有约 150 GB/s（理论 600 GB/s 的 25%），说明 TP decode 是 **延迟受限而非带宽受限**。

## 动机

- 现有并行选择多靠经验扫描，换模型/序列长度/硬件结论就不成立；多数系统 prefill 和 decode 用同一并行配置。
- Megatron TP 每层两次激活同步、每个生成 token 都要做；作者 profiling 显示通信可占 decode 端到端 **30–40%**。

## 方案

- 用 α–β 模型刻画 TP 集体通信（α 为启动/同步，β 为有效 NVLink 带宽），PP 点对点通信，以及自回归下的流水线利用率/气泡；参数化为模型结构、序列长度、批大小、GPU 数与互连拓扑。
- 验证：Qwen2.5-14B/32B-Instruct，8×A100 SXM4 80 GB，NVLink（600 GB/s 双向聚合）。

## 效果（仅论文数字）

| 观测 | 数字 |
|------|------|
| prefill 有效 NVLink 带宽 | 饱和在 ~**250 GB/s**（理论 ~600 GB/s）；TP 度越高利用率越高 |
| decode 有效带宽 | 饱和在 ~**150 GB/s**（约理论 **25%**） |
| TP 扩展下的 TTFT | TP1→8 TTFT 下降，但高 TP 时通信占 TTFT 近 **40%** |
| prefill：TP8 vs PP8 | TP8 TTFT 近 **40%** 在 NCCL；PP8 通信占比很小 → prefill 选 PP |
| decode：PP8 vs TP8 | PP8 通信最少但 ITL 最高（气泡）；TP8 NCCL 最多但 ITL 最低 → decode 选 TP |

## 与 wiki 的关系

- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — 前者给 DP→TP 的规模切换点，本文给 TP↔PP 随阶段切换的机理
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — 为 PD 分离下各自选并行度提供解析依据
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 推理侧小消息 AllReduce 的 α 主导问题；与 [Purlin](/papers/purlin-collectives-orchestration-datapath.md) 降同步开销的方向一致
- [NVLink/NVSwitch](/concepts/nvlink-nvswitch-scale-up-fabric.md) — scale-up 链路"名义带宽"与实测有效带宽的落差

## 局限与开放问题

- 只有 8×A100 单机、稠密 Qwen2.5；未覆盖 MoE/EP、跨节点、H100/B200 NVSwitch 世代。文中未给出模型误差的汇总数字。
- 开放问题：既然 decode 是 α 主导，硬件侧更该优化集体通信的启动/同步延迟（in-switch reduction、GPU 发起通信）而非链路带宽。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.05305) — Mirzaei & Mitra, arXiv:2610.05305
[2] [raw stub](raw/papers/llm-inference-parallelism-compute-comm-tradeoffs.md)
