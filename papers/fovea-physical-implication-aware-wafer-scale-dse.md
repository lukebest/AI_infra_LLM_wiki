---
type: Paper
title: "Fovea: Physical-Implication-Aware Wafer-Scale DSE"
description: 清华 — 晶圆级 DSE 先构造物理可行空间再按分析–参考误差画 Decision Domain；70 对 LLM 训练全部找回参考最优，相对穷尽参考平均 4.13×、最高 7.80×
tags:
- wse
- now
- network-on-wafer
- noc
- interconnect
- chiplet
- packaging
- architecture
- training
- llm
- optimization
timestamp: '2026-08-19T00:00:00Z'
created: 2026-08-19
sources:
- raw/papers/Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf
- raw/papers/fovea-physical-implication-aware-wafer-scale-dse.md
---

# Fovea: Physical-Implication-Aware Wafer-Scale DSE with Decision-Domain-Guided Cross-Fidelity Refinement

**Authors:** Jinxi Li, Huizheng Wang, Jinyi Deng, Yang Hu, Shouyi Yin（清华大学）
**arXiv:** [2608.03285](https://arxiv.org/abs/2608.03285)（2026-08-04）
**Venue:** arXiv cs.AR 预印本，文内未另报会议。
**PDF:** [raw/papers/Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf](raw/papers/Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf)

## 中文摘要

晶圆级是一块集成画布，不是一张固定模板：die 轮廓、兼容 tiling、算力/存储/D2D 配比互相卡住。常规「低成本筛一遍再精评 shortlist」在这里失效——候选空间不是笛卡尔积，分析评估与 ASTRA-sim+ns-3 参考评估大约差 4000× 成本，且约两成成对排序会反转。Fovea 把探索拆成两段：先按光罩、tiling、die 尺寸相关 D2D、边界放置构造**互异的物理可行空间**；再用配对标定得到的分析–参考相对误差，把每个分析分数扩成参考一致区间，只对无法排除的 **Decision Domain** 做参考评估。10 个可穷尽空间 × 7 个 LLM 训练负载（70 对）上，10% 配对标定在 1400 次独立 run 中全部找回参考最优，端到端相对穷尽参考平均 4.13×、最高 7.80×。

## Motivation

OpenAI 已把晶圆级系统接到 serving 栈（文内引 2026 Cerebras 合作，**未独立核实**）。即便同质 repeated-die，die 边长同时决定光罩合规、能铺几行几列、中心到边布线能支撑多少 D2D lane、以及边界 I/O 能否放下。面积够仍可能因边沿冲突不可行。另一方面，Llama-405B 上分析后端平均 2.49 秒/设计、参考后端 2.78 小时/设计；192 点空间穷尽参考要约 22.28 串行天。70 对上 Spearman 相关 0.7752，但成对反转率 20.96%，参考最优平均只排在分析榜的 10.77th percentile。固定分析 top-k 会漏最优，穷尽参考又付不起。Theseus 等在**已参数化的空间里**搜，不负责先把物理可行域构造出来。

## Approach

范围限定为**同质 2D 重复 die**（异构混合物、不规则 die 不在本文）。输入：负载与目标、组件库、实现约束、一对评估器。

1. **物理含义感知空间（Stage I）**：枚举光罩内 die 轮廓（5 nm、reticle 33×26 mm、可用区 220×220 mm）与几何包含的 row×col tiling；面积拆成不可放 / 固定开销 / 可配；D2D 带宽上限随中心到边布线预算下降；边界块做显式边沿放置可行性。然后做等价类归一化，以及**同 footprint 局部严格支配**削减（评估器在比较维度上单调）。
2. **Decision Domain（Stage II）**：全空间跑低成本评估；均匀抽 ρ=10% 做配对参考，取样本最大相对误差 ε̂；保留分析分数仍能在乐观界碰到低成本最优悲观界的候选。有效全域 ε 下，该域**包含**参考最优。标定结果缓存，只补评域内未抽到的点。
3. **评估**：Chakra 训练 trace → ASTRA-sim analytical / ASTRA-sim+ns-3。7 个负载（Llama-3B 到 Llama-405B，DP+TP）× 10 个 |𝒟|=179–5655 的可穷尽空间。gem5 Garnet 3.0 交叉验证四个设定，平均 Spearman 0.9946 且选出同一最优设计。Theseus / Polaris / SA 给 25% 穷尽参考墙钟预算作对照。

## Results（仅论文数字）

| 指标 | 数字 |
|------|------|
| 分析 vs 参考成本 | 2.49 s vs 2.78 h/设计，约 **4000×** |
| 成对反转率 / Spearman | **20.96%** / 0.7752 |
| 参考最优在分析排名 | 平均 **10.77th percentile** |
| 分析 top-5/10/20% 召回参考 top-k | 57.14% / 64.94% / 76.62% |
| 物理检查去掉 Area-Feasible | 平均 **86.4%**（69.4–90.7%） |
| 分析 top-10% 被物理打掉 | 平均 **29.4%**（14.1–38.2%） |
| Decision Domain 占比 | 平均 13.58%，中位 11.94%，最大 50.37% |
| 含标定的参考评估占比 | 平均 20.42% |
| 端到端加速 | 平均 **4.13×**，最大 **7.80×**（相对穷尽参考） |
| 精确找回参考最优 | Fovea **100%**（1400/1400）；Polaris 84.86%；Theseus 25.50%；SA 24.14%；穷尽分析 7.14%（5/70） |
| 构造扫到的最大互异可行空间 | **46,782** 候选 |

工作负载决定最优：三个代表最优点分别是 9×14 / 10×12 / 10×10 阵列，算力–存储–D2D 配比明显不同，**没有跨负载的万能晶圆模板**。

## Relation to wiki

- [Network-on-Wafer](/concepts/network-on-wafer.md) — Fovea 的空间是 **chiplet-on-wafer / 同质 repeated-die + 边界 D2D**，不是 WoW 重叠成网，也不是 Cerebras field stitch
- [Cerebras WSE](/entities/cerebras-wse.md) — 工业 field-stitch 模板；Fovea 论证「晶圆级仍要按负载选实例」
- [WoW Network Design](/papers/network-design-wafer-scale-wow-hybrid-bonding.md) — 放置即拓扑 vs Fovea 的 tiling/D2D/边界可行域
- [Mozart 3.5D](/papers/mozart-35d-wafer-scale-moe-training.md) — 异构 NoP-Tree，超出 Fovea 当前同质范围
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 负载是 DP+TP 训练；评估器是 ASTRA-sim 集体通信后端
- [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md) — 多保真 DSE 的「决策可靠性」案例

## 开放问题

1. 异构 die 混合物、WoW 重叠几何能否接到同一套 Decision Domain 流程？
2. ε̂ 是样本最大误差，可能低估全域 ε；文内最大低估 1.47 个百分点，更大空间是否仍 10% 够用？
3. 参考后端是 ASTRA-sim+ns-3，不是硅；Garnet 只验了四个设定。
4. Theseus 作为 wiki 里被点名的对照框架，本身尚未 ingest。

# Citations

[1] [raw/papers/Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf](raw/papers/Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf) — Li et al., arXiv:2608.03285
[2] [raw/papers/fovea-physical-implication-aware-wafer-scale-dse.md](raw/papers/fovea-physical-implication-aware-wafer-scale-dse.md) — 结构化摘录
