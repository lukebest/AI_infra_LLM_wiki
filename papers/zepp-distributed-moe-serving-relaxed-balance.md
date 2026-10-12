---
type: Paper
title: "Zepp: Accelerating Distributed MoE Serving under Relaxed Balance Constraints"
description: "UCSD/ETH — 把均衡当约束、以跨节点通信为目标：GPU 约束下副本放置 + NIC 约束下 split/merge 流 + 计算分片重叠；MoE 层 vs 7 个系统最高 6.68×，vs 最快基线最高 2.78×（几何均值 1.86×）"
tags:
- moe
- expert-parallelism
- serving
- inference
- communication
- scheduling
- distributed
created: 2026-10-12
updated: 2026-10-12
timestamp: '2026-10-12T00:00:00Z'
paper_author: [Chang Chen, Xinwei Qiang, Tiancheng Chen, Zhongkai Yu, Xiang Fang, Yufei Ding, et al.]
year: 2026
arxiv: '2610.11158'
venue: arXiv preprint (cs.DC)
sources:
  - raw/papers/Zepp_Distributed_MoE_Serving_Relaxed_Balance_2026.pdf
  - raw/papers/zepp-distributed-moe-serving-relaxed-balance.md
---

# Zepp：把负载均衡当约束的分布式 MoE 推理

## 一句话结论
EP 推理里为均衡某一维（计算/通信/显存）引入的操作本身就贵或不均衡。Zepp 改为直接最小化瓶颈的跨节点通信，只对 GPU 和 NIC 施加简化的均衡约束，分放置、路由、执行三层逐步优化。

## 方案
- **放置**：GPU 约束下跨节点放专家副本，使每个新副本扩大节点级覆盖；路由优先本地副本，剩余请求合并到更少远端节点。
- **路由/流整形**：NIC 约束下用 split 与 merge 原语重塑流；共享输入跨节点只发一次。
- **执行**：切分并调度专家计算以重叠通信；每次迭代联合协调计算、token 通信与专家权重迁移以适应动态负载。

## 效果（仅论文数字）
| 对比 | 数字 |
|---|---|
| vs A2AV+GEMM | **2.10–6.68×** |
| vs 最快竞争基线（7 个系统） | 最高 **2.78×**，几何均值 **1.86×**（端到端 MoE 层） |
| 平台 | 4 节点 16 GPU（每 GPU 配一 NIC），A100/H100 配置；模型含 Qwen3-235B 等 |

## 与 wiki 的关系
- [Expert Coupling](/papers/expert-coupling-moe-pretraining-all-to-all.md) — 训练侧同类"相关放置减少跨卡 token"
- [MegaFlux](/papers/megaflux-skew-resilient-moe-megakernels.md) — kernel 内热专家复制；Zepp 在集群层做副本与 NIC 级流整形
- [AFORE](/papers/afore-afd-expert-reconfiguration.md) — 同样动态重配专家，面向 AFD 架构

## 局限与开放问题
- 规模 16 GPU，较大 EP（数百卡、NVL72 域）下 NIC 约束模型是否仍简单有效待验证。
- 指标是 MoE 层时间，端到端 TTFT/TPOT 与 SLO 影响需看完整系统。

# Citations
- Chen et al., "Zepp", arXiv:2610.11158, 2026. [raw](/raw/papers/zepp-distributed-moe-serving-relaxed-balance.md)
