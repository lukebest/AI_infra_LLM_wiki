---
type: Raw Source
title: 深入理解 AI Infra：量化分析与系统设计（李博杰）
authors:
- 李博杰
license: Apache-2.0
language: zh
source_url: https://github.com/bojieli/ai-infra-book
online_url: https://bojieli.github.io/ai-infra-book/
pdf_url: https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf
ingested: 2026-09-14
---

# 《深入理解 AI Infra》— 源 stub

开源教材（Apache-2.0）。作者李博杰；方法是 **从约束推导设计**，反复追问数据搬移的五个问题：搬什么、搬多少、搬几次、经过哪里、谁必须等它。

**不要把全书正文拷进本 stub。** 工作层摘要见 [实体](/entities/bojieli-ai-infra-book.md) 与 [章节页](/analyses/ai-infra-book/ch01-intro.md)。

## 链接

| 项 | URL |
|----|-----|
| 仓库 | https://github.com/bojieli/ai-infra-book |
| 在线 | https://bojieli.github.io/ai-infra-book/ |
| PDF（公开 release） | https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf |
| 许可 | Apache-2.0 |

入库只拉 `manuscripts/*.md`（及 `manuscripts/README.md`、`calculations/README.md` 索引），**未 clone Git LFS**（`archive/`、experiments 二进制、配图二进制不入库）。

## 章节清单

| 章 | 手稿 | GitHub |
|----|------|--------|
| 前言 | `manuscripts/00-前言.md` | [00-前言.md](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/00-前言.md) |
| 1 初识 AI Infra | `manuscripts/01-初识 AI Infra.md` | [01](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/01-初识%20AI%20Infra.md) |
| 2 模型架构 | `manuscripts/02-模型架构.md` | [02](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/02-模型架构.md) |
| 3 推理与训练负载 | `manuscripts/03-推理与训练负载.md` | [03](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/03-推理与训练负载.md) |
| 4 加速器架构 | `manuscripts/04-加速器架构.md` | [04](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/04-加速器架构.md) |
| 5 算子与运行时 | `manuscripts/05-算子与运行时.md` | [05](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/05-算子与运行时.md) |
| 6 超节点 | `manuscripts/06-超节点.md` | [06](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/06-超节点.md) |
| 7 数据中心网络 | `manuscripts/07-数据中心网络.md` | [07](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/07-数据中心网络.md) |
| 8 推理优化 | `manuscripts/08-推理优化.md` | [08](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/08-推理优化.md) |
| 9 分布式推理 | `manuscripts/09-分布式推理.md` | [09](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/09-分布式推理.md) |
| 10 训练系统 | `manuscripts/10-训练系统.md` | [10](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/10-训练系统.md) |
| 11 资源调度与运行环境 | `manuscripts/11-资源调度与运行环境.md` | [11](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/11-资源调度与运行环境.md) |
| 12 端边云协同 | `manuscripts/12-端边云协同.md` | [12](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/12-端边云协同.md) |

## 结构（三部分）

1. **模型与负载**（Ch.1–3）：数量级、模型资源公式、到达过程与训练/RL 负载。
2. **芯片与系统**（Ch.4–7）：加速器、算子/运行时、[超节点](/concepts/ai-infra-supernode.md)、数据中心网络。
3. **推理与训练系统**（Ch.8–12）：单实例优化、分布式推理、训练、调度、端边云。

贯穿案例：Qwen3 系列、DeepSeek V4 / V4.1 Flash、HGX H100、Unified Bus / CloudMatrix384。作者经历覆盖 AKG、UB、KV-Direct。

# Citations

[1] [bojieli/ai-infra-book](https://github.com/bojieli/ai-infra-book) — Apache-2.0
[2] [AI-Infra-Book.pdf](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [Online book](https://bojieli.github.io/ai-infra-book/)
