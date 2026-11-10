---
type: Paper
title: "Should You Split Decode? Disaggregation Across Future Models and Accelerators"
description: "Hadidi / SiliconForge — 独立优化 P/D 与 P/D+AFD；SLO goodput/kW 无稳健 AFD 部署级优势，多数名义结果偏 P/D；KV-heavy + 小 scale-up 域时 AFD 有名义领先；固定硬件承诺中位损失 36%→重优化映射/池后 9%"
tags:
- disaggregated-inference
- afd
- decode
- prefill
- serving
- kv-cache
- nvlink
- scale-up
- inference
- throughput
- moe
- serving-system
- parallelism
- latency
created: 2026-11-10
updated: 2026-11-10
timestamp: '2026-11-10T00:00:00Z'
paper_author: [Ramyad Hadidi]
year: 2026
venue: arXiv preprint
arxiv: '2611.08299'
sources:
  - raw/papers/SiliconForge_Should_You_Split_Decode_2026.pdf
  - raw/papers/siliconforge-should-you-split-decode.md
---

# SiliconForge：还要不要再拆 Decode？

## 一句话结论
Ramyad Hadidi 提出校准模型 **SiliconForge**，把服务分解（P/D vs P/D+AFD）与硬件指派做成两个独立轴，在相同流水重叠规则与功率预算下分别优化映射和池大小。主比较中，SLO goodput/kW **未见稳健的部署级 AFD 优势**，多数名义估计偏向 P/D；最大名义 AFD 领先来自多放下一个 prefill replica。KV-heavy 且共置专家池跨越多个小 scale-up 域时，AFD 有名义领先。提前锁定硬件的中位归一化 goodput 损失约 **36%**（§IV-D 为 **35.7%**），同硬件重优化映射与池大小后约 **9%**（**9.3%**）。

## 动机
生产中已广泛部署 prefill/decode 解耦（P/D）。Attention/FFN 解耦（AFD）再把 decode 拆成读增长 KV 的 attention 池与流权重/专家的 FFN 池，同时引入跨池通信、放置约束和又一个供给池。AFD 每个 MoE 层每 decode 步把激活跨边界交换两次；DeepSeek-V3 为 **116** 次。基础设施往往在未来模型与芯片可实测之前就要承诺。既有 AFD 数字多来自特定硬件与基线的捆绑评测，难以把「拆不拆 decode」和「用哪类加速器」分开看。

## 方案
1. **SiliconForge**：跨层校准模型，组合 LLM 架构与硬件规格，独立变化服务分解与硬件指派。目录含 **39** 款加速器、六种硬件原型；主比较用四类（锚定现有与已宣布部件）和电学 / 光子两种 fabric。
2. **四种前瞻模型方向**：Expert-heavy MoE、KV-optimized MLA、KV-heavy GQA-MoE、Sparse-attention MLA（由 DeepSeek / Kimi / Qwen 等公开模型放缩宽度或深度得到）。
3. **共同优化规则**：P/D 与 P/D+AFD 各自搜索允许的硬件指派、映射（TP/DP/EP/PP、每副本 batch、微批数 M）和池大小，目标为功率预算内的 SLO goodput。主预算 **128 kW**，规模实验 **512 kW**。标题工况示例：上下文 32K、TPOT 50 ms、TTFT 5 s。
4. **稳健性检验**：名义幅度超过 **9%** 包络，并且在每个规格角保持同一符号，才算通过双部分测试。排队模型把服务时间转为 goodput，并用事件驱动仿真核验。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 主结论（摘要 / Finding I） | SLO goodput/kW 未见稳健的部署级 AFD 优势；多数名义估计偏向 P/D |
| Fig 4（修订模型，128 kW） | 单类上加 A/FFN 边界使 goodput/kW 变动 **−10.4% 到 +8.1%**；八个 AFD+ 里七个落在 **9%** 包络内 |
| 最大名义 AFD 领先 | 光子互联 + KV-heavy GQA-MoE，**+8.1%**；来源是多放下一个 prefill replica。单独优化 decode 时，P/D+AFD 的每 decode kW 吞吐更低 |
| Finding II | KV-heavy 且共置专家池跨越多个小 scale-up 域时 AFD 有名义领先；更大域或双方都用高速互联会削弱该领先 |
| 映射固定时的灵敏度 | 内存带宽翻倍使 TPOT **−39–49%**；FLOPs 翻倍最多 **−1.8%**。评测部署里内存读占 TPOT 的 **57–95%** |
| 提前锁定硬件（摘要 / §IV-D） | 中位归一化 goodput 损失 **36%**（精确值 **35.7%**）；同硬件重优化映射与池大小后 **9%**（**9.3%**）；25% 冗余降到 **5.1%** |
| 相对 FastAFD 的对照建模 | FastAFD 报告每 GPU decode 吞吐 **1.35–1.45×**；在其 GPU 预算内独立优化两边后，模型给出 **0.94×**（8K 与 16K） |

作者因此认为：prefill 供给、decode 内存带宽、链路和池粒度比「要不要再拆 decode」本身更能决定部署；映射与池大小应保持可调，让边界和硬件选择跟随模型需求。

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 把 P/D 与 AFD 分成可独立优化的两级边界
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 内再分为读 KV 的 attention 与流权重的 FFN
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — scale-up 域粒度改变 AFD 名义领先
- [AFORE](/papers/afore-afd-expert-reconfiguration.md) — AFD 放大专家不均后的微批级重配对照
- [MegaScale-Infer](/papers/megascale-infer-2504.02263.md) — 生产向 AFD / 异池 MoE 服务对照

## 开放问题
- 结论来自校准模型而非大规模生产 A/B；对 FastAFD 等已发表对照，独立优化两边后名义 AFD 增益可以消失（0.94×）。
- 9% 包络是作者自设的稳健性门槛；包络内的名义领先仍可能在特定 SLA 下有运营意义。
- 目录与规格角会随路线图更新；文中建议持续重跑映射与池大小，而不是一次性锁定加速器类别。

# Citations
- [arXiv:2611.08299](https://arxiv.org/abs/2611.08299) — Ramyad Hadidi（独立撰写）
- [raw stub](/raw/papers/siliconforge-should-you-split-decode.md)
