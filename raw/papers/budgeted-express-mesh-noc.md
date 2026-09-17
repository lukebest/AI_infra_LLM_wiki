---
type: Raw Source
title: "Budgeted Express-Mesh: Traffic-Aware Link Placement and Deadlock-Free Adaptive Routing"
source_url: https://arxiv.org/abs/2609.17057
arxiv: '2609.17057'
ingested: 2026-09-17
sha256: 47d813f1c1c8db4df9ce1a41c03b808e6353021d442f1f7327909c16d4311fd2
---

# Budgeted Express-Mesh

**Authors:** Li Cao, Jingyuan Ma（清华课设；Instructor: Kaisheng Ma）
**PDF:** [Budgeted_Express_Mesh_NoC_2026.pdf](Budgeted_Express_Mesh_NoC_2026.pdf)
**arXiv:** [2609.17057](https://arxiv.org/abs/2609.17057)（cs.AR/cs.NI；Wed 2026-09-16 列表，v2）

## 问题

2D mesh 上少量长距离链路决定饱和吞吐；固定线预算下如何放置 express links 并配套死锁自由自适应路由。

## 方法要点

- 拓扑：固定 wire budget B 下加 traffic-aware express links。
- 放置：ASPL-based Greedy，再 simulation-guided simulated annealing（SA）。
- 路由：committed top-K，基于延迟的 express 拥塞与 reservation；escape 路径。
- 仿真：gem5 Garnet；主评 8×8、B=32；扩展 16×16 异构 SoC 流量。

## 摘录数字（仅论文给出）

- 静态：Mesh ASPL **5.333**/Diam **14** → Greedy ASPL **3.837**/Diam **8**（8 links、wire cost 31）。
- 高负载注入率 0.80：Tornado 上 Greedy 相对 Random 吞吐 **+50.7%**；SA 再相对 Greedy **+1.3–7.1%**（多流量）。
- 注入率 0.70：Tornado Greedy vs Random **+45.7%**；CutStress **+33.2%**。
