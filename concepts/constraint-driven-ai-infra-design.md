---
type: Concept
title: Constraint-Driven AI Infra Design
description: 李博杰书中的「从约束推导设计」：容量/算力/带宽/延迟四类数字 + 五个数据搬移问题 + MFU/MBU 对极限
tags:
- methodology
- book
- architecture
- infrastructure
- formal-analysis
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Constraint-Driven AI Infra Design（从约束推导设计）

来自 [《深入理解 AI Infra》](/entities/bojieli-ai-infra-book.md) 前言与第 1 章。与本 wiki 的 [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) / [Architecture Paper Reading](/concepts/architecture-paper-reading-methodology.md) 同族：先算物理下界，再解释实测差距。

## 四类数字

任务要保存 \(M\)、算 \(F\) FLOPs、经某接口读写 \(R\)。加速器提供容量 \(M_{\mathrm{cap}}\)、吞吐 \(\Pi\)、带宽 \(\beta\)：

\[
M\le M_{\mathrm{cap}},\qquad T_{\mathrm{compute}}=F/\Pi,\qquad T_{\mathrm{memory}}=R/\beta.
\]

容量决定能否同时放下（权重 + 状态 + 工作区须**相加**）；后两项是时间下界。峰值下界 = 硬件物理极限。

| 比值 | 定义 | 上界 |
|------|------|------|
| **MFU** | \(F/(\Pi T)\) | 1 |
| **MBU** | \(R/(\beta T)\) | 1 |

书中反复用同一判据：下界与实测之差，不是**模型漏项**（忘了 KV、通信、重算），就是**可去掉的系统开销**（逐 kernel launch、就绪偏差）。

## 五个数据搬移问题

从片上 SRAM 到超节点到端边云，都问：

1. **搬什么** — 权重 / KV / 激活 / 梯度 / 通知
2. **搬多少** — 字节；精度与表示（GQA vs MLA）直接改这个数
3. **搬几次** — 复用次数 \(r\) 决定远程读 vs 搬回本地
4. **经过哪里** — HBM、NVLink、NIC、Clos 上联、WAN
5. **谁必须等它** — 依赖边；集体通信从最慢 rank 的就绪时刻开始

对应本 wiki：[End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)、[Interconnection Design Space](/concepts/interconnection-network-design-space.md)。

## 设计顺序（书中反复出现）

1. 容量：\(W_i+K_i+A_i+U_i\le C_i\)（逐卡，不是集群总和）。
2. Roofline：\(T_{\mathrm{op}}=\max(F/P,\,V/B)\)。
3. 通信：算法字节 × 割集带宽 + 轮次 \(\alpha\)；小消息看启动，大消息看持续带宽。
4. 重叠与关键路径：能藏进计算的通信不再决定步时间。
5. 测量修正排名；差距小于噪声则两方案都留。

**先判断再摊**：先排除装不下或超 SLO 的方案，再在可行集里比延迟 / 吞吐 / 按时成本。

## 常见漏项（书中点名 LLM/芯片估算）

- 只算权重读，忘了 decode 读 KV。
- 算了读时间，没加工作区，显存其实放不下。
- 用峰值 FLOP/s，没查带宽能否供数。
- 把工作均分到多卡，漏卡间通信与就绪偏差。
- 报了很高吞吐，没加串行依赖与往返。

# Citations

[1] [前言](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/00-前言.md)
[2] [Ch.1](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/01-初识%20AI%20Infra.md)
[3] [PDF release](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[4] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
