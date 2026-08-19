---
type: Raw Source
title: Fovea Physical-Implication-Aware Wafer-Scale DSE
source_url: https://arxiv.org/abs/2608.03285
arxiv: '2608.03285'
ingested: 2026-08-19
sha256: 30a7de2bcdf60e3bbf151abc7d5e1087539d66b1af07fd178fdcefb0d3d9b065
---

# Fovea: Physical-Implication-Aware Wafer-Scale DSE with Decision-Domain-Guided Cross-Fidelity Refinement

**Authors:** Jinxi Li, Huizheng Wang, Jinyi Deng, Yang Hu, Shouyi Yin (Tsinghua)
**PDF:** [Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf](Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf)
**arXiv:** [2608.03285v1](https://arxiv.org/abs/2608.03285) (2026-08-04)

## 问题

晶圆级 DSE 不能把 die 尺寸 / tiling / D2D / 边界 I/O 当无约束笛卡尔积。低成本分析评估与 ASTRA-sim+ns-3 参考评估有 ~4000× 代价差，且 20.96% 成对排序会反转；固定 top-k 会漏掉参考最优。

## 方法要点

- 范围：同质 repeated-die 2D 阵列（不规则/异构 die 混合物不在范围内）。
- Stage I：物理含义感知可行空间——光罩合规 die 轮廓、兼容晶圆 tiling、die 尺寸相关 D2D 带宽、边界放置；等价类与同 footprint 局部严格支配削减。
- Stage II：Decision Domain — 用配对标定估分析–参考相对误差 ε，把分析分数映成参考一致区间，只对无法排除的候选做参考评估。
- 评估器对：ASTRA-sim analytical vs ASTRA-sim+ns-3；Chakra 训练 trace；gem5 Garnet 交叉验证。

## 摘录数字（仅论文给出）

- 分析 2.49 s/设计 vs 参考 2.78 h/设计（Llama-405B），约 **4000×**。
- 70 对：Spearman 0.7752；成对反转率 **20.96%**；参考最优落在分析排名平均 **10.77th percentile**。
- 10% 配对标定：70/70 对、1400/1400 run 找回参考最优；端到端相对穷尽参考平均 **4.13×**、最高 **7.80×**。
- 物理检查剔除 Area-Feasible 的 **86.4%**；分析 top-10% 里平均 **29.4%** 被物理约束打掉。
- 对照：Theseus 精确找回 25.50%、Polaris 84.86%、穷尽分析 7.14%（5/70）。
