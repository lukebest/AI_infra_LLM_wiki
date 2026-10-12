---
type: Paper
title: "Expert Coupling in MoE Pretraining: Reducing All-to-All Overhead with Correlated Placement and Token Shuffling"
description: "Zyphra — MoE 预训练早期路由已呈专家共现与跨层相关；相关专家同卡放置 + 下一层预测的 token 洗牌，MI300X 上 all-to-all 1.16–2.63×、step 最高 1.41×，不改路由与参数"
tags:
- moe
- expert-parallelism
- training
- collective
- communication
- amd
- distributed
created: 2026-10-12
updated: 2026-10-12
timestamp: '2026-10-12T00:00:00Z'
paper_author: [Radha Gulhane, Quentin Anthony, Beren Millidge]
year: 2026
arxiv: '2610.09372'
venue: arXiv preprint (cs.CL/cs.DC)
sources:
  - raw/papers/Expert_Coupling_MoE_Pretraining_AllToAll_2026.pdf
  - raw/papers/expert-coupling-moe-pretraining-all-to-all.md
---

# Expert Coupling：利用专家共现压缩 MoE 预训练 all-to-all

## 一句话结论
预训练早期路由器就学会了相关的选择模式：层内少数专家对被大量 token 同时选中，上一层选的专家能预测下一层。把常一起被选的专家放同一 GPU，并在 attention 后的 reduce-scatter 里顺手把 token 挪到"下一层专家所在 GPU"，就能把大量分发留在本卡，路由决策和参数都不变。

## 动机
- 每节点 8×AMD MI300X，EP32 时 all-to-all 占训练 step **45%**（top-2）/ **60%**（top-6）。
- top-2 下层内 **0.8%** 的专家对被 **42%** 的 token 同时选中。

## 方案
- **相关专家放置**：共现频繁的专家放同卡；配合"每 token 每 GPU 只发一次"的 dispatcher，最多去掉 **58%** 分发行。
- **Token 洗牌**：序列并行把 token 切到 EP 组内时，在 attention 之后的 reduce-scatter 中把 token 送到预测持有其下一层专家的 GPU；单节点本卡命中率 **12.5% → 59%**。
- 实现于 Megatron-LM。

## 效果（仅论文数字）
| 场景 | 数字 |
|---|---|
| EP8–64，top-2/top-6 | all-to-all 时间 **1.16–2.63×** 缩短 |
| 端到端 step | 最高 **1.41×** |

## 与 wiki 的关系
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP all-to-all 的数据局部性优化
- [RailWave](/papers/railwave-ep-rail-incast-scheduling.md) — 同处理 EP 通信，RailWave 调度流量，本文直接减少流量
- [Zepp](/papers/zepp-distributed-moe-serving-relaxed-balance.md) — 推理侧同样用"副本放置 + 本地优先"减少跨节点 token

## 局限与开放问题
- 共现模式随训练漂移，需要多久重放置一次、迁移成本多大，论文覆盖有限。
- 平台为 MI300X；在 NVL72 等大 scale-up 域里节点内外带宽比不同，收益比例会变。

# Citations
- Gulhane, Anthony, Millidge, arXiv:2610.09372, 2026. [raw](/raw/papers/expert-coupling-moe-pretraining-all-to-all.md)
