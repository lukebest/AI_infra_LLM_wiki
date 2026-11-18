---
type: Paper
title: "Exstill: The Most Efficient Single-Chip Processor for the Next Token"
description: "Exstill — 预硅 5 nm class；Qwen3-1.7B@16K 算术地板 0.89 mJ/token，同构模型上 3.0 mJ（3.4×地板）；协同设计后地板 0.29 mJ、token 0.52 mJ，12 用户各 50 µs；相对实测 B300 同 12 用户 110× 更快、能量 690× 更低（作者估计手调软件栈约收窄一半）"
tags:
- accelerator
- chip-design
- energy
- decode
- inference
- sram
- kv-cache
- speculative-decoding
- llm
- nvidia
- gpu
- memory
- power
- serving
- latency
- throughput
- agentic-ai
- numeric-format
created: 2026-11-18
updated: 2026-11-18
timestamp: '2026-11-18T00:00:00Z'
paper_author: [Valavan Manohararajah, Vithursan Thangarasa]
year: 2026
venue: arXiv preprint (technical report)
arxiv: '2611.18859'
sources:
  - raw/papers/Exstill_Single_Chip_Next_Token_2026.pdf
  - raw/papers/exstill-single-chip-next-token.md
---

# Exstill：把下一枚 token 做到接近算术能量地板的单芯片

## 一句话结论
Exstill 技术报告给出一套模型–硅片协同设计：把单一模型架构写进数据通路（权重仍可加载），并把权重与每路对话的 KV 放在算术单元旁边。门级测量把 Qwen3-1.7B 在 16K 上下文、5 nm class 的算术地板定为 **0.89 mJ/token**；保持该模型不变的预硅设计把一枚 token 做到 **3.0 mJ（地板的 3.4×）**、每 **57 µs** 一枚，片上只容 1 路用户。质量对齐后放开模型，同封装（**125 W / 575 mm²**，实用 **526 mm²**）把地板降到 **0.29 mJ**、完整 token（含漏电）**0.52 mJ（新地板的 1.8×）**，片上容 **12** 路 16K 上下文，每路 **50 µs**（约 **19,921** token/s/用户，整片约 **239,000** token/s）。相对同一负载下实测的一块 NVIDIA B300（12 用户、每 token **5.35 ms / 361 mJ**），预硅设计每路解码 **110×** 更快、能量 **690×** 更低。芯片数字来自预硅门级流程；B300 为 vLLM 出厂配置的 decode 实测，两边都不含 prefill。

## 动机
生成一枚 token 的算术量是固定的，其能耗构成任何硬件的下限。作者在 16 路 FP8 点积、累加到 16-bit 浮点的数据通路上，把 Qwen3-1.7B@16K 的地板测成 **0.89 mJ**。同一模型在一块 B300 上，按用户数不同，每 token 能量是该地板的 **391–1,120×**（1 用户 **2.15 ms / 994 mJ**，12 用户 **5.35 ms / 361 mJ**，16 用户 **6.35 ms / 347 mJ**）。多余部分来自通用软件层、可编程硬件，以及从片外搬运权重与 KV；工艺演进中数据搬运改进慢于逻辑，这段差距还会拉大。

## 方案
1. **去掉中间层、去掉搬运**：单一模型架构固定在数据通路里，权重仍可换；权重与每路对话的 KV 全部留在片上，挨着算术单元。
2. **门级搜索环**：在相同质量门槛（作者自有探测文本上的 bits per byte，对齐 Qwen3-1.7B）和封装预算里，同时搜索模型与电路。数据中心封装为 **125 W、575 mm²**，每路 16K 上下文。作者称对电路做了 304 个模块、逾一千万种设计的代价评估；协同设计改变了模型与硅片的哪些部分，报告标明为 Exstill 专有。
3. **对照**：先固定发布版 Qwen3-1.7B 只改硅片，再放开模型。另给出更大的 DC2 设计（约 **750 mm² / 106 W**，服务 4 路、Polyglot-DC2 4B）。
4. **Polyglot-DC 协同处理器**：同一架构经蒸馏专用于草稿、护栏、智能体与金融推理，作为前沿模型旁的低时延协处理器。

## 效果（论文数字）
芯片侧为预硅、5 nm class；B300 为实测。质量门槛是探测文本上的 bits per byte，角色章节另有任务级评测。

| 设计 | 用户 | 每 token 时间 | 每 token 能量 | 相对地板 |
|---|---:|---:|---:|---|
| 算术地板（发布版 Qwen3-1.7B） | — | — | **0.89 mJ** | 1× |
| Exstill，模型不变 | 1 | **57 µs** | **3.0 mJ** | 地板的 **3.4×** |
| 协同设计地板 | — | — | **0.29 mJ** | — |
| Exstill 数据中心设计 | 12 | **50 µs** | **0.52 mJ** | 新地板的 **1.8×** |
| B300，同 12 用户 | 12 | **5.35 ms** | **361 mJ** | 发布版地板的 **407×** |
| B300，最快（1 用户） | 1 | **2.15 ms** | **994 mJ** | **1,120×** |

同 12 用户对比：每路解码 **110×** 更快（50 µs vs 5.35 ms），能量 **690×** 更低（0.52 vs 361 mJ），能量–延迟约 **74,000×** 更低（26 µJ·ms vs 1.93 J·ms）。B300 最快设置仍慢 **43×**；最省能的 16 用户设置每 token 能量仍高 **660×**。协同设计相对「只改硅片」：每 token 能量 **5.8×** 更低，整片吞吐 **13.7×**（17,512 → 239,056 token/s），能量–延迟 **79×** 更低（174 → 2.2 µJ·ms）。DC2（4B）预硅为每路 **71 µs / 1.88 mJ**、4 用户。

投机解码：草稿跑在 Exstill 预硅设计上，目标模型跑在 GPU；单用户、按最优链长，相对无投机的目标解码，增益 **2.3–6.6×**（编码任务均高于 **3.4×**）。目标包括 gpt-oss-120b、Qwen3-Next、DeepSeek-V4-Pro-0813、Kimi K3、Muse Spark Open。护栏：DC1 预硅约 **0.70 ms**（对照 GPU 侧 26.8 ms 量级），多语裁决「在 1 ms 或以内」，与最强开源护栏相差不到 1 个点（报告原句）。

## 与 wiki 的关系
- [Token-Energy Law](/papers/token-energy-law-llm-decode.md) — 同类把 decode 能耗拆成算术与搬运；这里把搬运从路径里拿掉，并给出相对 B300 的预硅差距
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 权重与每路 KV 全部留在片上，挨着算术
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 对比只覆盖 decode，prefill 在两边都排除
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 把单一模型架构写进数据通路的专用加速器
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 地板测在 16 路 FP8 点积、16-bit 浮点累加上

## 开放问题
- 芯片数字是预硅门级测量，整芯片数字是估计；门级流程抓不到的效应要等硅上才能出现。
- B300 对照是一块 GPU、vLLM 出厂配置、只比 decode。作者估计，手调 serving 栈会把相对 B300 的各比值大约收窄一半，关不掉这段差距，因为 12 路权重与缓存搬运在已公布带宽下仍约占 12 用户步进的 3 ms。
- 该设计固定 12 路对话与一种架构；B300 可换任意装得下的模型，也可加用户、换每路时延。
- 质量门槛是探测文本上的 bits per byte，不是任务级评测。投机加速是「B300 实测 + 预硅数字」的组合结果。报告未在同一负载上实测 Groq LPU 等其它专用设计，与它们的比较建立在已公布数字与地板论证上。

# Citations
- [arXiv:2611.18859](https://arxiv.org/abs/2611.18859) — Manohararajah, Thangarasa；Exstill
- [raw stub](/raw/papers/exstill-single-chip-next-token.md)
