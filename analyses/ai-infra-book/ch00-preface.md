---
type: Summary
title: AI Infra Book Ch.0 Preface
description: 李博杰书前言—从约束推导设计、五个数据搬移问题、十二章三部分阅读地图
tags:
- book
- methodology
- infrastructure
- architecture
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.0 前言 — 先判断再摊

来源：[《深入理解 AI Infra》前言](/entities/bojieli-ai-infra-book.md)。方法展开：[Constraint-Driven Design](/concepts/constraint-driven-ai-infra-design.md)。

## 核心判断

编程抽象上移：模型 ≈ LLM 时代的 OS，AI Infra ≈ 其体系结构。跨层工作方式：**最懂 Infra 的人做算法，最懂算法的人做数据，最懂数据的人做 Infra。** DeepSeek V4 / V4.1 CED 被当作「系统约束倒逼模型结构」的例子。

贯穿线索是**数据搬移**五问：搬什么、搬多少、搬几次、经过哪里、谁必须等它。保留数据减重算但占容量；扩大并行减本地工作但加通信。

## 十二章顺序

1. 模型与负载（1–3）→ 工作量从哪来
2. 芯片与系统（4–7）→ [加速器](/analyses/ai-infra-book/ch04-accelerators.md) 到 [超节点](/concepts/ai-infra-supernode.md) 到 [DC 网络](/analyses/ai-infra-book/ch07-datacenter-network.md)
3. 推理与训练系统（8–12）→ 请求、状态、训练、环境、端边云

作者路径：FPGA 模型并行 → AKG / 在线 softmax → [UB](/entities/unifiedbus-ub.md) 万卡互联 → 实时语音（5 s → ~500–600 ms）。

# Citations

[1] [00-前言.md](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/00-前言.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
