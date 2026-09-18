---
type: Paper
title: "Ask the Tool: Progress-Aware KV for Agentic Serving"
description: 清华/阿里云 — 工具 progress 指导 KV；p90 TTFT after tool vs LRU −20.7%/−20.8%；接近 oracle
tags:
- agentic-ai
- ai-agent
- serving
- serving-system
- kv-cache
- llm
- inference
- scheduling
- latency
- hbm
- memory
- architecture
timestamp: '2026-09-18T00:00:00Z'
created: 2026-09-18
updated: 2026-09-18
sources:
- raw/papers/Ask_Tool_Progress_Agent_KV_Serving_2026.pdf
- raw/papers/ask-tool-progress-agent-kv-serving.md
---

# Ask the Tool, Don't Guess: Agent Tool Calls Hold Their Progress, and the Serving System Should Read It

**Authors:** Yipeng Liu, Yingqiang Zhang, Feifei Li, Huanchen Zhang
**Affiliation:** Tsinghua University; Zhejiang University; Alibaba Cloud Computing
**arXiv:** [2609.18849](https://arxiv.org/abs/2609.18849)（2026-09-16，cs.DC；Thu 9/17 列表）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.18849)

相对 [PipeSwift](/papers/pipeswift-pipeline-parallel-agentic-serving.md) 的 JCT/PP 与 [UNISON](/papers/unison-near-memory-scheduler-llm-agents.md) 的近存会话调度，本文切入 **工具等待期** 的 KV keep/evict/prefetch：停止调用前猜时长，改为读工具运行中 progress。

## 动机

- Agent 请求大量墙钟耗在工具上，期间 KV 空占 GPU。
- 名称/历史/声明时长/引擎占用等预测在环境变化下失效，甚至无法排序长调用。
- 工具进程本身已有进度，但 harness/quiet 管道把它静音。

## 方案

1. **Progress 契约**：强信号=剩余工作分数；弱信号=临近结束。
2. **Corpus 普查**：四公共 agent 语料，度量可读进度覆盖的工具时间份额。
3. **Harness 旁路**：恢复 progress bar / 解析侧信道，不改 agent 可见观察；对 agent 基准分「无可测代价」。
4. **引擎接入**：少量 hint 把剩余时间估计接到 KV 动作（驻留/换出/回迁）。

## 效果（仅论文数字）

- 强信号覆盖工具时间：leaderboard **38%**、OpenHands **51%**、自建 **48%**；弱信号 **66% / 59% / 72%**。
- KV 决策点准确度：相对最优公开预测器高「**数倍到一个数量级**」，且环境变化后仍稳。
- 生产引擎端到端：p90 **TTFT after tool call** vs LRU **−20.7%**（HBM only）、**−20.8%**（HBM+DRAM），接近 oracle。

**口径：** serving/系统论文；TTFT 是工具返回后首 token，勿与稳态 tok/s 横比。

## 与 wiki 的关系

- [PipeSwift](/papers/pipeswift-pipeline-parallel-agentic-serving.md) — agentic JCT/并行；本文是 **工具期 KV 控制面**
- [UNISON](/papers/unison-near-memory-scheduler-llm-agents.md) — 硬件近存会话 KV vs 本文软件 progress 信号
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 多租户 serving 中工具等待与内存争用
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBM/DRAM 层间 KV 回迁时机
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — 更冷层对照；本文主战场仍是 HBM±DRAM

## 开放问题

1. 强/弱信号覆盖不到的长调用（无进度条脚本）如何兜底。
2. 与 PipeSwift 式 PP/MTP 调度的联合控制面。
3. 跨租户公平性与 progress 操纵抗性。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.18849) — Liu et al., arXiv:2609.18849
[2] [raw/papers/ask-tool-progress-agent-kv-serving.md](raw/papers/ask-tool-progress-agent-kv-serving.md) — 结构化摘录
