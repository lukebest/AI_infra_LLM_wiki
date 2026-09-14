---
type: Summary
title: AI Infra Book Ch.2 Model Architecture
description: 第2章模型架构—权重/注意力/KV 公式、GQA vs MLA、MoE 专家读取、混合注意力状态
tags:
- book
- transformer
- llm
- moe
- kv-cache
- attention
- memory
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.2 模型架构

把 Ch.1 的 \(M,F,R\) 展开成可代入的矩阵尺寸与状态寿命。对接 [Prefill/Decode Divergence](/concepts/prefill-decode-divergence.md)、[FlashAttention](/concepts/flashattention.md)。

## 机制（先判断再摊）

- **Prefill vs decode**：prefill 一次处理已有输入；decode 每步一个新 token，复用 KV。状态驻留时间 × 调用次数 = 读量。
- **注意力状态**：MQA / GQA 靠共享 KV 头减每 token 字节；MLA 缓存上投影前的潜变量，交接字节可再降（Ch.9 用同一公式算 PD 传输）。
- **MoE**：总专家权重大，每 token 只读 \(K\) 个专家。批内活跃专家期望 \(E[1-(1-K/E)^M]\)（后在 Ch.6/9 复用）。计算量由分派次数决定，读取量由**不同**专家数决定——均匀 64 token×8/128 专家几乎读完全部专家权重。
- **混合注意力 / 线性注意力**：每 token 存多少、每步 decode 读多少要分开列（窗口、压缩、递推状态）。

## 设计规则

从加速器容量**先扣**服务状态与工作区，再看剩下能装多大模型。结构选择（GQA、稀疏、专家粒度）本身就是 Infra 效率旋钮。新条件只改其中一项：加 batch、加上下文、加 \(E\) 或 \(K\)，分别进不同公式。

V4 / V4.1 贯穿：局部窗口 + 压缩 + 稀疏选择，压长上下文状态；V4.1 Flash 的 Engram 表是只读大表，放置见 [Ch.6](/analyses/ai-infra-book/ch06-supernode.md)。

# Citations

[1] [Ch.2](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/02-模型架构.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
