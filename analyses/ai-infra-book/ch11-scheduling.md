---
type: Summary
title: AI Infra Book Ch.11 Scheduling
description: 第11章资源调度与运行环境—工具环境驻留、成组分配、RL 配比、API vs 自建成本
tags:
- book
- serving
- scheduling
- sandbox
- infrastructure
- agentic-ai
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.11 资源调度与运行环境

Agent/工具任务把模型服务和 **CPU 环境**放在同一条关键路径上。对接 [DSec Sandbox](/concepts/dsec-sandbox.md)、[Ch.3 负载](/analyses/ai-infra-book/ch03-workloads.md)。本 wiki 的 NoC 主线较远，只留约束级结论。

## 核心算例（书）

平台平均 30 CPU 核，环境却要 600 GiB——因为 27 s 在等模型，工具环境一直占内存。在模型调用期间准备环境：累计内存从 60 → 18 GiB·s。模型调用仍超 24 s 期限时，把 V4-Flash 每副本会话 32→16，调用 9→6 s，任务 30→21 s；副本 10→12。

## 机制

- 隔离边界、暂停/恢复/重建；始终驻留 vs 按需 vs 预热。
- 异构成组分配（GPU+CPU+内存必须一起给）。
- RL：rollout 实例先完成权重加载；验证与后续生成重叠。
- 模型路由、前缀缓存、排队/限流；自建 vs 按量 API 用同一套「合格任务成本」。

设计：分析需求看总工作量；分析完成时间看顺序与重叠。局部加快若占内存的环境不释放，期限仍破。

# Citations

[1] [Ch.11](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/11-资源调度与运行环境.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
