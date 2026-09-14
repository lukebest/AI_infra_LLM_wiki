---
type: Summary
title: AI Infra Book Ch.3 Workloads
description: 第3章推理与训练负载—到达过程、Agent 驻留、6ND 训练、RL 阶段配比
tags:
- book
- inference
- training
- serving
- agentic-ai
- llm
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.3 推理与训练负载

单次请求工作量（Ch.2）加上**何时到达**和**步骤依赖**。对接 [Inference Capacity Trap](/concepts/inference-capacity-trap.md)、[Heterogeneous Inference](/concepts/heterogeneous-inference.md)。

## 预算 / 机制

- **持续到达**：平均值估资源；短时积压与 KV 驻留暴露平均值看不到的压力。工具等待时计算可停，状态仍占显存（Ch.9 把 10 s 等待 × 1.125 GiB KV 写成 GiB·s）。
- **Agent / 多轮**：前缀增长、分支、工具等待、失败重试都要累加工作量与驻留。
- **训练**：前向+反向+更新；\(6ND\) 量级到逐项矩阵。预训练 / 中训 / SFT 改的是数据与可训练参数，不是另一套 Infra。
- **RL**：rollout、奖励/环境、有效样本、权重同步。有效样本吞吐 = 各阶段服务率与保留比例的最小耦合（Ch.10/11 展开）。
- **Scaling law**：模型规模与数据量的统计约束，用来估全生命周期成本，不是用来跳过容量检查。

## 设计规则

比较方案必须**同一质量与完成标准**。长期服务需求会回改前期训练投入。实时多模态另加「数据必须按时到」的串行边。

# Citations

[1] [Ch.3](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/03-推理与训练负载.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
