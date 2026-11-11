---
type: Paper
title: "FastAFD: When Does Attention-FFN Disaggregation Pay on Rack-Scale NVLink?"
description: "UCSD Hao AI Lab — GB200 NVL72 上调优 AFD 引擎；相对每负载调优的 vLLM wide EP，decode 吞吐 Qwen3 最高 1.17×、Qwen3.5 最高 1.16×，MiniMax-M2.5 持平；解析模型均值误差 2.9%；投机再加约 8%；SRAM 专家理想天花板 2.48×"
tags:
- afd
- disaggregated-inference
- moe
- expert-parallelism
- decode
- serving
- kv-cache
- nvlink
- scale-up
- inference
- throughput
- serving-system
- parallelism
- latency
- nvidia
created: 2026-11-11
updated: 2026-11-11
timestamp: '2026-11-11T00:00:00Z'
paper_author: [Yichao Fu, Yuxuan Zhang, Minshen Zhang, Ruitian Wang, Junda Chen, Hao Zhang]
year: 2026
venue: arXiv preprint
arxiv: '2611.07149'
sources:
  - raw/papers/FastAFD_When_Does_AFD_Pay_NVL72_2026.pdf
  - raw/papers/fastafd-attention-ffn-disaggregation-nvl72.md
---

# FastAFD：机架级 NVLink 上 AFD 何时划算

## 一句话结论
UCSD Hao AI Lab 在 **GB200 NVL72** 上实现并仔细调优 AFD 引擎 **FastAFD**（双微批 ping-pong，把一微批的 MoE 叠在另一微批的 attention 后面），对照每负载调优过 EP 宽度的 vLLM wide EP。标准 decode 下，全 GPU 计入的吞吐 Sall：Qwen3-235B 最高 **1.17×**（16K），Qwen3.5-397B 最高 **1.16×**（4K），MiniMax-M2.5 为 **1.00–1.02×**。只吃 colocated vLLM 画像的解析模型，在 65 个部署上均值误差 **2.9%**。加速比拆成 batch gain、overlap gain 与把 GPU 分给专家的 disaggregation cost；投机解码对轻专家模型帮助最大，摘要称再给 AFD 优势加约 **8%**。

## 动机
已有 AFD 数字多来自其他硬件、较窄的共置基线或解析模型（如 MegaScale-Infer 相对共置最高 1.90×），而生产引擎在 NVL72 一类机架级 NVLink 域上常用宽专家并行（wide EP）。wide EP 同样能把大量 HBM 留给 KV。需要在同一套 GB200 NVL72 上，把调优过的 AFD 直接对照调优过的 wide EP。

## 方案
1. **FastAFD 运行时**：attention 节点只持 KV、做 attention 与投影；FFN 节点持专家权重、经 NVLink 收发 token。每步两个微批 ping-pong，整步收入一条 CUDA graph，host 簿记放在步间。
2. **对照协议**：每个负载单独选择 vLLM 的最佳 EP 宽度；FastAFD 扫描 A:F 节点比（1:1 到 17:1）。主度量 **Sall** 计入全部已分配 GPU，**Satt** 只计 attention GPU。
3. **解析模型**：输入只来自硬件规格与一份 colocated wide-EP 画像，不对 FastAFD 跑数拟合。把 Sall 写成 `(bA/bV)×(TV/TA)×(r/(r+1))`（Eq. 2 / Fig 5）。
4. 评测模型为 FP8 MoE：MiniMax-M2.5（10B/229B，256 experts）、Qwen3-235B-A22B（22B/235B，128 experts）、Qwen3.5-397B-A17B（17B/397B，512 experts）；上下文 4K–16K。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 标准 decode Sall vs 最佳 wide EP | Qwen3 16K **1.17×**（EP32，A:F 11:1）；Qwen3.5 4K **1.16×**；Qwen3.5 16K **0.99×**；MiniMax **1.00–1.02×** | Table 1 / Fig 3 |
| 相对单节点 EP4（SEP4） | **1.30–2.36×**；rack 内调优 wide EP 把基线抬升 **22–114%**（峰在 EP16–EP32）后，优势收窄到 0.99–1.17× | Fig 3 / Table 1 |
| Satt（只计 attention GPU） | 标准 decode 全负载 **1.08–1.39×**；相对 wide EP 的 batch 优势 **1.06–1.16×** | Table 1 / Fig 3 |
| 投机 d=3（q=4，ā≈1.8） | MiniMax Sall 升到 4K/16K **1.08×**；Qwen3 **1.10–1.13×**；Satt 最高 **1.70×**；最优 A:F 收缩过半；摘要称优势再加约 **8%** | Table 2 / Fig 4 |
| 解析模型误差 | 65 个部署均值 **2.9%**（标准 3.0%、投机 2.6%），单次最高 **7.4%** | Fig 6c / §4.4 |
| 运行时消融 | k=2 微批最好；一处消融使 E2E 吞吐 **−32%**；peak-tuned CAD 只有 FastAFD 每 GPU 吞吐的 **0.68–0.78×** | Fig 7 |
| SRAM 专家理想天花板 | 去掉 GPU 预算上的 disaggregation cost 后，标准 decode **1.20–1.76×**，投机 **1.38–2.48×**（文中举例 Groq 3 LPX + Vera Rubin NVL72） | Fig 8 / §6 |

开源：[hao-ai-lab/FastAFD](https://github.com/hao-ai-lab/FastAFD)。

[SiliconForge](/papers/siliconforge-should-you-split-decode.md) 对照过 FastAFD 此前发表的 **1.35–1.45×** 声称，并在其 GPU 预算内独立优化两边后给出 **0.94×**。本文是在 NVL72 上相对调优 wide EP 的实测，标准 decode 的 Sall 上限为 **1.17×**。

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 在机架级 NVLink 上把 AFD 对照 wide EP
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 内 attention / FFN 再拆的实测边界
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — GB200 NVL72 域内 AFD 与 wide EP
- [SiliconForge](/papers/siliconforge-should-you-split-decode.md) — 校准模型对 AFD 声称的交叉检验
- [AFORE](/papers/afore-afd-expert-reconfiguration.md) — 另一条 AFD 专家重配路线，勿与 FastAFD 混淆
- [MegaScale-Infer](/papers/megascale-infer-2504.02263.md) — 较早的 AFD / 异池 MoE 服务对照

## 开放问题
- 评测停在 16K 上下文与 18 节点机架上限；更长上下文、跨机架与生产流量形状仍待补。
- 2.48× 是去掉 FFN GPU 成本后的模型天花板，不是已部署的异构系统实测。
- 与 SiliconForge 的 0.94× 对照用的是不同目标（吞吐 vs SLO goodput/kW）和不同优化规则，不宜直接抵消。

# Citations
- [arXiv:2611.07149](https://arxiv.org/abs/2611.07149) — Fu, Zhang, Zhang, Wang, Chen, Hao Zhang（UCSD）
- [raw stub](/raw/papers/fastafd-attention-ffn-disaggregation-nvl72.md)
- [PDF](/raw/papers/FastAFD_When_Does_AFD_Pay_NVL72_2026.pdf)
