---
type: Raw Source
title: "Ask the Tool, Don't Guess: Agent Tool Calls Hold Their Progress, and the Serving System Should Read It"
source_url: https://arxiv.org/abs/2609.18849
arxiv: '2609.18849'
ingested: 2026-09-18
sha256: c0ac6e883dda2ffc504f5714c468b987ac74e629d1e38441b3e99c7226f27fc2
---

# Ask the Tool, Don't Guess: Agent Tool Calls Hold Their Progress, and the Serving System Should Read It

**Authors:** Yipeng Liu, Yingqiang Zhang, Feifei Li, Huanchen Zhang
**Affiliation:** Tsinghua University; Zhejiang University; Alibaba Cloud Computing
**PDF:** [Ask_Tool_Progress_Agent_KV_Serving_2026.pdf](Ask_Tool_Progress_Agent_KV_Serving_2026.pdf)
**arXiv:** [2609.18849](https://arxiv.org/abs/2609.18849)（2026-09-16，cs.DC；Thu 9/17 列表）

## 问题

Agent 工具等待期间 KV 占 GPU；现有 keep/evict/prefetch 靠调用前猜测时长，无法跟踪运行中真实剩余时间。

## 方法要点

- 工具侧显式 progress 上报（强：剩余工作分数；弱：临近结束信号）。
- 四公共 agent corpus 普查 + harness 旁路恢复（不改 agent 可见输出）。
- 接入生产引擎 hint，指导 KV 驻留/换出/回迁。

## 摘录数字（仅论文给出）

- 工具时间可读信号：强信号覆盖 leaderboard **38%** / OpenHands **51%** / 自建 **48%**；弱信号升至 **66% / 59% / 72%**。
- KV 决策点：progress 相对最优公开预测器准确度高「数倍到一个数量级」。
- p90 TTFT after tool vs LRU：**−20.7%**（HBM only）、**−20.8%**（HBM+DRAM），接近 oracle。
