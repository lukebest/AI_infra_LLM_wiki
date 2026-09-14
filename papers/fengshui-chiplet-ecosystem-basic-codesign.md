---
type: Paper
title: "Fengshui: Chiplet Ecosystem and Bespoke Accelerator Codesign"
description: 密歇根 — 联合优化 chiplet 池与 BASIC；8 die 相对同构能量/EDP×$ 降 48.5–97.8%；LLM serving prefill energy×$ 最高 −28.7%
tags:
- chiplet
- packaging
- accelerator
- llm
- moe
- inference
- architecture
- parallelism
- memory
- optimization
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/papers/Fengshui_Chiplet_Ecosystem_BASIC_Codesign_2026.pdf
- raw/papers/fengshui-chiplet-ecosystem-basic-codesign.md
---

# Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign

**Authors:** Haoran Jin, Jirong Yang, Zhiheng Zhang, Justin Shin, Barry Lyu, Kangqi Zhang, Yunpeng Liu, Nathan Bleier  
**Affiliation:** University of Michigan  
**arXiv:** [2609.10970](https://arxiv.org/abs/2609.10970)（2026-09-10，cs.AR）  
**Venue:** 预印本。  
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.10970)

相对 [HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md) 在给定 chiplet 库上做 serving DSE，Fengshui 同时回答 **池子里该造哪些 die** 与 **怎么拼成算子级 BASIC**——把 NRE 摊薄和算子异构绑在同一个搜索环里。

## 动机

同构商品硬件难同时吃下延迟/能量 SLO。算子级拆分（微架构、批策略、内存层次）有效，但单体定制 ASIC 的 NRE 爆炸。Chiplet 复用可摊 NRE，可「哪些 die 进池」取决于将来能拼出什么加速器，而加速器质量又受池约束——循环依赖。

## 方案

**Fengshui** 联合优化：

1. **Chiplet pool generator**：在有限 N（文内主结果 **N=8**）下选可复用 die（含多种 dataflow、内存类型、MoE switch / PIM 等）。
2. **BASIC 拼装**：算子级 disaggregation；共探 chiplet/内存异构、tensor fusion、PP/TP/EP，并用 place-and-route 校验物理可实现性。
3. **洞察（文内）**：attention 类 BAO 不宜靠大批；switch chiplet 对 MoE 并行专家影响大；无单一微架构通吃。

## 效果（仅论文数字）

- 相对同构加速器：能量 / energy×$ / EDP / EDP×$ 分别降低 **48.5% / 88.1% / 93.0% / 97.8%**；相对无约束异构设计评分差距 **≤4.1%**。
- 数据中心 MoE 与稠密 LLM serving：prefill 能量与 energy×$ 最高 **16.8% / 28.7%**（文示 Qwen3-30B-A3B 与 LLaMA-3.1-8B 等场景）。
- 边缘自动驾驶感知：能量 / energy×$ **12.0% / 23.6%**（实时延迟约束）。
- 文内 Qwen3-30B 池演化例子：引入 switch（N=2）可把 prefill/decode EDP 压到相对 N=1 基线约 **0.13× / 0.094×**；再加 PIM（N=3）decode EDP 约到 **0.042×**（相对同图基线）。

## 与 wiki 概念的关系

- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — chiplet 池 + 封装内组成进入互连/封装协同设计空间。
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 算子级拆分与 DistServe 类相位拆分对照；本文强调 die 复用经济学。
- [HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md) / [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — HYDRA 固定库搜 serving；DICE 细 PHY；Fengshui 先造可复用库。

## 开放问题

1. 池前缀冻结后，新主导瓶颈族（MoE/长上下文）泛化掉多少？
2. 真实代工厂 NRE/$ 模型替换文内 CATCH/IBS 参数后，最优 N 是否仍≈8？
3. 与 UCIe/NoI 带宽档位（HYDRA）联立时，switch/PIM die 的 D2D 预算怎么砍？

# Related

- [HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md)
- [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md)
- [CHIPSMORE](/papers/chipsmore-cim-chiplets-llm-inference.md)
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)
- [Disaggregated Inference](/concepts/disaggregated-inference.md)

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.10970) — Jin et al., arXiv:2609.10970  
[2] [raw/papers/fengshui-chiplet-ecosystem-basic-codesign.md](raw/papers/fengshui-chiplet-ecosystem-basic-codesign.md) — ingest stub
