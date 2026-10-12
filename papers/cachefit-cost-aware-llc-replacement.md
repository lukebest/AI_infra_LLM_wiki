---
type: Paper
title: "CacheFit: The Rising Cost of Cache Replacement and Constraint-Driven Redesign of Last-Level Cache Replacement Policies"
description: "NC State — ChampSim + 电路级成本模型 HARCOM + LLM 提议策略，把面积/功耗/延迟预算放进 LLC 替换策略搜索目标；Fit-MPPPB 存储 −60.3%、静态功耗 −56.3%、IPC +1.1%"
tags:
- cache
- cpu
- power
- architecture
- optimization
- agentic-ai
created: 2026-10-12
updated: 2026-10-12
timestamp: '2026-10-12T00:00:00Z'
paper_author: [Bita Aslrousta, Kaushal Mhapsekar, Darsh Asher, Azam Ghanbari, Joshua Kalyanapu, Samira Mirbagher Ajorpaz]
year: 2026
arxiv: '2610.10579'
venue: arXiv preprint (cs.AR)
sources:
  - raw/papers/CacheFit_Cost_Aware_LLC_Replacement_2026.pdf
  - raw/papers/cachefit-cost-aware-llc-replacement.md
---

# CacheFit：把电路成本放进 LLC 替换策略设计回路

## 一句话结论
LLC 替换策略一向先按 IPC 选、再在 RTL 里压成本，成本进场太晚。CacheFit 把 ChampSim 仿真、电路级成本模型 HARCOM 和 LLM 提议器连成闭环，候选策略在算法成形时就按延迟/面积/功耗/加速比打分，设计者设预算，所有提议与经验以可读文本保存。

## 效果（仅论文数字，SPEC CPU2017）
| 起点 | 结果 |
|---|---|
| MPPPB（功耗、晶体管最贵基线）→ Fit-MPPPB | 存储 **−60.3%**、静态功耗 **−56.3%**、晶体管 **−58.9%**；IPC **+1.1%**，命中率 **+7.5 pp** |
| SHiP++（IPC 最高基线）→ Fit-SHiP++ | 存储 **−56%**、静态功耗 **−61%**、晶体管 **−56%**；IPC **−1.54%**，命中率 **−2.1 pp** |

## 与 wiki 的关系
- [Memory Hierarchy & Cache](/concepts/memory-hierarchy-cache.md) — 替换策略的硬件成本维度
- [Branch Prediction](/concepts/branch-prediction.md) — 同属超标量核内预测器结构，感知器类预测器（MPPPB 源自此）同样面临存储/功耗成本
- [Terracotta](/papers/terracotta-flexible-dram-interface-controller.md) — 同为"控制器/策略可编程化 + 成本可量化"的内存层工作

## 局限与开放问题
- 成本模型对部分路径只给下界（论文脚注）；多核共享 LLC 场景覆盖有限。
- LLM 搜索的可复现性与对 SPEC 过拟合风险。

# Citations
- Aslrousta et al., "CacheFit", arXiv:2610.10579, 2026. [raw](/raw/papers/cachefit-cost-aware-llc-replacement.md)
