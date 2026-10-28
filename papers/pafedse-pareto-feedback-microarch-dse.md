---
type: Paper
title: "PaFeDSE: Pareto-Feedback-Guided Microarchitecture Design Space Exploration for Efficient Pareto Search"
description: "KAIST ASP-DAC'27 — OoO CPU 微架构 DSE：Pareto-hit/miss 反馈 + TCFilter；相对 MoDSE 达目标 HV 最高少 49.0% 仿真，探索开销 7.1×，PPA MAPE 0.731%"
tags:
- superscalar
- microarchitecture
- out-of-order
- design-space-exploration
- chip-design
- simulator
- performance-analysis
created: 2026-10-28
updated: 2026-10-28
timestamp: '2026-10-28T00:00:00Z'
paper_author: [Joonyong Park, Hyojeong Lee, Sejeong Yang, Joo-Young Kim]
year: 2027
venue: ASP-DAC 2027
arxiv: '2610.34838'
sources:
  - raw/papers/PaFeDSE_Pareto_Feedback_Microarch_DSE_ASPDAC2027.pdf
  - raw/papers/pafedse-pareto-feedback-microarch-dse.md
---

# PaFeDSE：用 Pareto 反馈收紧 OoO 微架构 DSE

## 一句话结论
ML 代理的微架构 DSE 仍大量仿真「Pareto-miss」、并在迭代间反复给低优先级候选打分。PaFeDSE 用 HitFormer 预测「会不会抬 HV」、MissGraph 惩罚 miss 邻域、TCFilter 按跨轮一致性裁候选；在 gem5+McPAT **22 nm**、SPEC CPU 2017、设计空间 **3,359,232** 点上，相对最强基线 MoDSE 达目标超体积最高少 **49.0%** 次仿真，探索开销 **7.1×**，PPA MAPE **0.731%**（相对 MoDSE **−30.2%**）。

## 动机
- OoO CPU 参数组合爆炸，穷举不可行；代理模型 + HVI/EHVI 迭代成为主流。
- MoDSE 一类方法最大 Pareto-miss 率可达 **85.47%**（ε=0.0001）：选中点评完后 ΔHV 几乎不涨，却烧掉昂贵仿真。
- 迭代间大量候选长期低分，仍每轮做全量代理推理与 acquisition 打分。

## 方案
1. **HitFormer**：Transformer 代理同时预测 CPI/功耗/面积与 Pareto-hit 分数；acquisition = HVI(ŷ) · p_hit · miss 惩罚项。
2. **MissGraph**：把历史 Pareto-miss 记成图，按 PPA 敏感的设计距离惩罚邻近未评估点，压制重复 miss 局部区。
3. **TCFilter**：利用跨轮 acquisition 分数一致性，裁掉持续低优先级候选，缩小活跃池（最低可保设计空间 **1%**）。
4. 评测：gem5 周期精确 + McPAT 22 nm；对比 ActBoost、BOOM-explorer、MoDSE；目标 HV 定义为各方法最终最高 HV 的 90/95/99%。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 达目标 HV 仿真次数 vs MoDSE | 最高少 **49.0%** |
| 平均达 90 / 95 / 99% HV 仿真数 | **32.9 / 43.3 / 118.8** |
| TCFilter 探索开销 | 每轮 **374.19→52.94 s**，**7.1×**；最终 HV 不掉 |
| PPA 预测 MAPE | **0.731%**（相对 MoDSE **−30.2%**） |
| 设计空间 | **3,359,232** 点 |
| 工具链 | gem5 + McPAT，**22 nm**，SPEC CPU 2017 |

## 与 wiki 的关系
- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — OoO 宽度/ROB/前端参数怎么搜；PaFeDSE 给可复用的 Pareto 搜索效率
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — 搜索空间本身就是 ROB/发射队列/缓存等 OoO 旋钮
- [DSA Processor Design Trade-offs](/concepts/dsa-processor-design-tradeoffs.md) — 通用核 PPA 前沿如何高效摸清，才能和 DSA/加速器分区对照
- [CTMA](/papers/causal-top-down-microarchitecture-analysis.md) — 评估归因；PaFeDSE 管的是「搜哪些点」，CTMA 管「怎么解释点的表现」

## 开放问题
- 设计空间与参数表沿用既有 OoO DSE 设定；换 BOOM 全参数或工业 SoC 约束时 HitFormer/MissGraph 是否迁移未验证。
- 仿真仍是主成本；与并行 SimPoint / 更轻代理组合的端到端墙钟还可再压。
- 多目标目前是 −Perf / Power / Area；加入时序、可测性或热约束后的反馈定义需扩展。

# Citations
- [arXiv:2610.34838](https://arxiv.org/abs/2610.34838) — Park et al., ASP-DAC 2027
- [raw stub](/raw/papers/pafedse-pareto-feedback-microarch-dse.md)
