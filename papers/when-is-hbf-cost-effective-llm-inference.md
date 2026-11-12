---
type: Paper
title: "When Is High-Bandwidth Flash Cost-Effective for LLM Inference?"
description: "UC Merced — 468 组公开器件仿真把 HBF 的 GPU 数节约、可服务性、购入成本与吞吐拆开；98 组降低最少 GPU 数，每栈半价 GPU 时 63 组仍划算；100 张 4090 规模卡上三家大 MoE 离线吞吐 16.4–26.5×"
tags:
- hbf
- flash
- hbm
- memory
- inference
- serving
- moe
- energy
- dram
- ssd
- simulator
created: 2026-11-12
updated: 2026-11-12
timestamp: '2026-11-12T00:00:00Z'
paper_author: [Zhiyu An, Yiping Li, Wan Du]
year: 2026
venue: arXiv preprint
arxiv: '2611.11036'
sources:
  - raw/papers/When_Is_HBF_Cost_Effective_LLM_Inference_2026.pdf
  - raw/papers/when-is-hbf-cost-effective-llm-inference.md
---

# When Is HBF Cost-Effective：HBF 何时比加 GPU 更划算

## 一句话结论
加州大学默塞德分校用公开器件数据与 NVIDIA AISimulate，在九个 dense/MoE 模型、五种负载、两种 GPU 平台、1–100 卡上做了 **468** 组对照，把「更少 GPU」「原先服务不了」「购入成本更低」「吞吐更高」四件事情分开记账。固定需求下，HBF 在 **98** 组降低达到服务目标所需的最少 GPU 数（正文口径是：双方都通过且常规方案需要超过 1 张 GPU 的 224 组里有 98 组）；每栈按半张 GPU 计价时，这 98 组里仍有 **63** 组划算。固定卡数下，16 卡以下匹配对照里吞吐提升占 **48%**，更大规模只剩 **13%**；100 张 RTX 4090 规模 GPU 上，级联 HBF 把三家大 MoE 的离线吞吐提到 **16.4–26.5×**。节约 GPU 与抬吞吐出现在不同场景。

## 动机
已有 HBF 工作多在刻画延迟、寿命、KV 放置与层级带宽。本篇问的是部署判据：给定需求，HBF 能否用更少 GPU 达到 SLO，并且这些节约能否付清闪存栈；已有 GPU 装机上，HBF 能否在达标的同时服务更多请求。作者强调这四类结果经常被写在一起，需要分开看。

## 方案
1. **两种组织**：shared-site 用 HBF 换掉 8 个近存位点里的 2 或 4 个，牺牲近存容量与带宽；cascaded 在保留近存的同时外加闪存。
2. **平台假设**：RTX 4090 规模 GDDR **24 GiB / 1.008 TB/s**；H200 规模 HBM **141 GiB / 4.8 TB/s**。每栈 **512 GiB**（OCP Table 3）；每 GPU 链路天花板 **2 TB/s**；每栈 **20 W**（2 W 静态，8 pJ/read bit），持续读封顶 **281.25 GB/s/栈**（四栈 **1.125 TB/s**），物理写 **8 GB/s/栈**。八卡节点；流水线有效带宽 H200 **315 GB/s**、4090 规模 **8.4 GB/s**；跨节点 **35 GB/s + 8 µs/endpoint**。GPU 时间来自钉死的 AISimulate 表，4090 路径做了 timing transfer。
3. **扫描矩阵**：九个模型（Qwen3-8B/32B、Llama 3.1-70B/405B、Qwen3-30B-A3B/235B-A22B、DeepSeek V3、Kimi K2、Muse Spark Open），五种负载（paused、short chat、long RAG、tool-agent、offline），responsive / balanced / relaxed / offline 四档服务目标（Table II），1–100 GPU。

工件：[ryeii/When-Is-HBF-Cost-Effective](https://github.com/ryeii/When-Is-HBF-Cost-Effective)。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 固定需求、降低最少 GPU 数 | 摘要写 **98 / 468**；正文：双方都通过且常规方案需要超过 1 张 GPU 的 **224** 组里有 **98** 组；其中 **82** 组最多 4 张带 HBF 的 GPU 就够 | 摘要 / 正文 Takeaway 段 |
| 两种 HBF 同时通过 | **178** 组：123 平、54 级联胜、1 次 shared-site 胜；另有 **29** 组只有 HBF 通过（16 个 DeepSeek V3 / Kimi K2 / Muse 在 4090 规模上的组合） | 正文 |
| 按负载的 GPU 数胜场 | paused **40/108**，short chat **39/108**，long RAG **17/108**，tool-agent **0/108**，offline **2/36**（皆为 4090 规模 Llama 3.1-405B，2→1 卡）。79 组 paused/chat 胜里，39 组至少少 9 张 GPU | Fig. 4a |
| 成本仍划算的子集 | 零溢价 98 组胜里，每栈 0.5 张 GPU 时 **63** 组（64%），1 张时 **42** 组，4 张时 **2** 组 | Fig. 4b |
| 典型装机下降 | 四用户 balanced short-chat：Qwen3-235B 在 4090 规模从常规 **32** 卡降到 shared-site **8** 或 cascaded **4**。H200 规模上 DeepSeek V3 / Kimi K2 / Muse 从常规 **16** 卡降到 shared-site **4** 或 cascaded **2** | Fig. 3 |
| 单卡可服务性 | 单用户 short-chat、relaxed SLO：HBF 让 DeepSeek V3 与 Kimi K2 在一张 RTX 4090 上达标，常规方案做不到；4090 规模 relaxed 覆盖从 2 个模型扩到 6 个 | 摘要 / Fig. 5 |
| 固定卡数的吞吐 | 16 卡以下匹配对照 **48%** 提升；16 卡及以上 **41/304（13%）** | 摘要 / 正文 Takeaway 5 |
| 100 张 4090 规模卡、离线吞吐（级联 vs 常规） | DeepSeek V3 **16.4×**，Kimi K2 **26.5×**，Muse Spark Open **16.5×**（摘要概括为 **16.4–26.5×**） | Fig. 6b / 摘要 |
| 成本例子 | H200 规模 balanced short-chat 上 Muse：常规 16 GPU，对两张级联 GPU + 八栈；每栈半价 GPU 时相当于 6 个 GPU 当量，盈亏平衡在每栈 **1.75** GPU 当量 | 正文 |

作者的判断：HBF 最有价值的情况，是权重（容量）而不是计算在迫使装更多 GPU，并且闪存能在 SLO 内把权重送到、价格低于被省下的 GPU。Paused 与 short chat 上 GPU 数节约最清楚；大 MoE 还可以让单卡变得可服务，或在最少 GPU 数不变时大幅抬离线吞吐。

## 与已有 HBF 页的增量
既有页面主要刻画层级带宽、KV 冷热/寿命放置、稀疏注意力与个人 AI 计算机形态，例如 [Characterizing HBF](/papers/characterizing-hbf-llm-serving.md)、[HBFSim](/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md)、[HyPAIC](/papers/hypaic-hbf-personal-ai-computer.md)、[FLINT](/papers/flint-hbf-llm-inference.md)、[HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md)、[Hot–Cold](/papers/hotcold-hbm-hbf-agentic-llm.md)、[Lachesis](/papers/lachesis-lifetime-aware-kv-hbm-hbf.md)、[DASH](/papers/dash-dual-path-hbf-moe-inference.md)、[Trillion-param MoE HBF](/papers/trillion-param-moe-hbf-memory-provisioning.md)。本篇补的是 **购入成本回收与最少 GPU 数** 的扫描判据，以及「节约 GPU」与「抬吞吐」不要写在同一句话里。仿真栈（AISimulate + 公开器件表）与上述工作的 HBFSim / 自研模拟器不同，数字不宜直接横比。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把 HBF 放进「加栈还是加 GPU」的成本账
- [HyPAIC](/papers/hypaic-hbf-personal-ai-computer.md) — 个人机形态下的 HBF 服务；本篇给出多卡数据中心扫描
- [Characterizing HBF](/papers/characterizing-hbf-llm-serving.md) — 完成时间与寿命；本篇问的是装机成本是否收回

## 开放问题
- 结果依赖所建模的硬件与流量。灵敏度审计里，14 组参考 GPU 数胜场在九个不利设定下只剩 2 组全部存活（Fig. 7）；256 GB/s 链路等组合设定会改变存活数。
- Muse 的 timing transfer 在邻近专家与留出滑动 decode 检查上，中位绝对百分比误差分别为 **15.4%** 与 **32.3%**。
- 作者写明 BF16 场景、静态放置、筛过的布局与 4090 规模多卡假设会限制外推；量化、投机解码与其他 host / EP 策略可能改变结论。
- 工具会话（tool-agent）上 GPU 数胜场为 0/108，与「HBF 普遍有助于智能体」的直觉并不自动对齐。

# Citations
- [arXiv:2611.11036](https://arxiv.org/abs/2611.11036) — An, Li, Du（UC Merced）
- [raw stub](/raw/papers/when-is-hbf-cost-effective-llm-inference.md)
- [PDF](/raw/papers/When_Is_HBF_Cost_Effective_LLM_Inference_2026.pdf)
- [工件](https://github.com/ryeii/When-Is-HBF-Cost-Effective)
