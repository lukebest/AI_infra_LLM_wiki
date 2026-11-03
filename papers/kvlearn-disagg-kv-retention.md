---
type: Paper
title: "KVLearn: Learning KV Cache Retention in Disaggregated Serving"
description: "UCLA/Columbia SYSTOR'26 — PRP+CARS+ATC 代价感知 keep/admit；TTFT 最高 −56%/−38%/−33% vs No-Cache/LRU-Pool/Mooncake；跨节点 KV 传输最高 −53%；MM-Session 吞吐约在 oracle 5% 内"
tags:
- inference
- kv-cache
- serving-system
- disaggregated-inference
- prefill
- decode
- latency
- throughput
- llm
- prefix-cache
- memory
created: 2026-11-03
updated: 2026-11-03
timestamp: '2026-11-03T00:00:00Z'
paper_author: [Dong Liu, Yanxuan Yu, Eric Jiang, Shu Wang, Ying Nian Wu]
year: 2026
venue: SYSTOR '26
arxiv: '2610.28637'
sources:
  - raw/papers/KVLearn_Disagg_KV_Retention_2026.pdf
  - raw/papers/kvlearn-disagg-kv-retention.md
---

# KVLearn：解耦服务中的学习式 KV 保留

## 一句话结论
解耦 P/D 后，miss 同时付出 **prefill 重算 + 跨节点传输**，admit 本身也要占池带宽；经典 LRU 不再刻画真实代价。KVLearn 用 **PRP（复用概率）+ CARS（代价感知保留分）+ ATC（闭环阈值）** 做 keep/admit。端到端 TTFT 相对 No-Cache 最高 **−56%**、相对 LRU-Pool **−38%**、相对 Mooncake 风格 **−33%**；跨节点 KV 传输相对 LRU-Pool 最高 **−53%**；MM-Session 吞吐约在 oracle **~5%** 内。

## 动机
- DistServe / Splitwise / Mooncake 把 prefill 与 decode 拆到不同节点池后，KV 在计算与消费之间隔着网络；miss 成本不再是「同卡重算」。
- 多模态前缀（图像/视频 token）KV 体量大、重算贵，但复用不均匀；一律全留或全丢都会浪费内存与带宽。

## 方案
1. **PRP**：用结构与时间特征（前缀长度、模态、radix 深度、会话元数据、访问近因/频次等）在线估计复用概率，不碰模型权重。
2. **CARS**：把复用概率换算成 keep/admit 信号，计入每块重算、传输与存储代价。
3. **ATC**：按命中率与内存压力闭环调节准入阈值。
4. **部署与负载**：接入全局解耦拓扑；文本 + 多模态会话；代码 https://github.com/FastLM/KVLearn。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| TTFT vs No-Cache | 最高 **−56%** |
| TTFT vs LRU-Pool | 最高 **−38%** |
| TTFT vs Mooncake-style | 最高 **−33%** |
| 跨节点 KV 传输量 vs LRU-Pool | 最高 **−53%** |
| MM-Session 吞吐 vs oracle | 约在 **~5%** 内 |

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 直接作用在 P/D 之间的全局 KV 池 admit/evict
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — miss 代价拆成重算与传输两段，与 PD 资源分歧同构
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 页/块级保留决策叠在页式 KV 之上
- [FlatCake](/papers/flatcake-flat-kvcache-storage.md) — 同属解耦侧 KV 层；FlatCake 管扁平介质放置，KVLearn 管学习式保留策略

## 开放问题
- 阈值与代价模型依赖织物带宽与池容量标定；跨厂商互联与多租户干扰未展开。
- 与稀疏 attention / 选择性重建（如 RISK-KV）叠加时的联合策略未报告。

# Citations
- [arXiv:2610.28637](https://arxiv.org/abs/2610.28637) — Liu et al., SYSTOR '26
- [raw stub](/raw/papers/kvlearn-disagg-kv-retention.md)
