---
type: Paper
title: "MiracleGro / BLOOM: 自主生长更好的乱序超标量核"
description: "UC Berkeley — FireSim 跑完整 SPEC CPU2017 intspeed；SkyWater 130nm 上 IPC 几何均值 1.85×、频率 69.85→88.37 MHz，墙钟 2.34×，面积约 +33%；商业 16 nm 上关键路径大约长 14%"
tags:
- architecture
- cpu
- superscalar
- out-of-order
- microarchitecture
- chip-design
- risc-v
- agentic-ai
- performance-analysis
created: 2026-11-25
updated: 2026-11-25
timestamp: '2026-11-25T00:00:00Z'
paper_author: [Angela Cui, Ferran Hermida-Rivera, Jack Toubes, Jim Fang, Chengyi Lux Zhang, Borivoje Nikolić, Christopher W. Fletcher, Sagar Karandikar]
year: 2026
venue: preprint
arxiv: '2611.26517'
sources:
  - raw/papers/BLOOM_MiracleGro_OOO_Core_2026.pdf
  - raw/papers/bloom-miraclegro-ooo-core.md
---

# MiracleGro / BLOOM：用智能体循环改 BOOM 乱序核

## 一句话结论
加州大学伯克利分校的 MiracleGro 在 CHIA 框架里自动读周期精确的 RTL 行为与综合 QoR，识别瓶颈并把微架构改动写回开源乱序核 BOOM。最佳设计 BLOOM 出现在第 34 轮：SkyWater 130nm 上频率从基线 **69.85 MHz** 升到 **88.37 MHz**（关键路径 11.32 ns，约 **+27%**），面积从 **90.60 mm²** 到 **120.94 mm²**（约 **+33%**）。FireSim 跑完整 SPEC CPU2017 intspeed 参考输入（约 30 万亿条指令）时，几何均值 IPC 为基线的 **1.85×**（加速 85%），墙钟 **2.34×**。循环外在商业 16 nm PDK 上，BLOOM 的关键路径比基线 BOOM 大约长 **14%**，面积大约多 **21%**。

## 动机
把性能、面积与频率一起做对，需要性能模型、RTL、综合与验证协同迭代。工业大团队可以承担这条链路，小团队往往只能停在高层仿真，而高层仿真会丢掉实现约束。LLM 智能体提供了在 RTL 上持续改核的可能，前提是循环能同时看到周期精确性能与 ASIC QoR，并且实验环境能挡住奖励作弊。

## 方案
MiracleGro 搭建在 CHIA 之上，让分析、实现、时序与调试智能体共用同一套工具与隔离规则。性能用 GSIM 做 checkpoint 级周期精确软件 RTL 仿真（各 SimPoint 约 3000 万条指令），最终用 FireSim 在 FPGA 上跑完整参考输入；平台随设计变大，从 VU9P 的 Alveo U250 / F2 迁到 VU19P 的 Corigine MimicTurbo GT。综合 QoR 用开源 SkyWater 130nm 与商用门级综合，SRAM 时序与面积由缩放到 Sky130 的 CACTI 给出——先进 PDK 受许可限制，不能交给智能体。最终 Loop v2-p4 每轮分析并实现 4 个结构相关特性，并行跑 2 轮；约 300 小时后把目标从纯 IPC 改为墙钟时间。最佳设计 BLOOM 出现在第 34 轮。

## 量化结果
- 软件 RTL checkpoint：BLOOM 的几何均值 IPC 为 **2.23**，Sky130 频率 **88.37 MHz**，相对 checkpoint 基线的墙钟 **2.28×**，面积约 **+33%**。
- FireSim + 完整 intspeed（600.perlbench、602.gcc、605.mcf、620.omnetpp、623.xalancbmk、625.x264、631.deepsjeng、641.leela、648.exchange2、657.xz；xz 因 FPGA 约束使用 16GB swap）：基线 IPC 例如 perlbench **1.07** / gcc **0.78** / mcf **0.59**，BLOOM 为 **2.86 / 2.00 / 0.98**。几何均值 IPC 加速 **1.85×**，墙钟 **2.34×**（墙钟用 FireSim IPC 乘以 69.85 MHz 与 88.37 MHz）。
- 只盯 IPC 时，合并步 m16c0 相对基线 IPC **+74%**，关键路径变为 **2.5 倍**，墙钟收益被频率吃掉，这条设计没有进入最终谱系。第 16 轮相对第 11 轮把关键路径改善 **47%**，IPC 下降 **3%**；第 18 轮把关键路径压到基线以下。墙钟优化流单轮大约 **41 小时**。
- 循环外的商业 16 nm 综合：关键路径大约长 **14%**，面积大约多 **21%**。文中另给出同一基线 SoC 在现代 16 nm 上为 **4.75 mm²、1.02 GHz**，作为对照刻度。

## 局限与解读
- Sky130 上的频率与面积胜利没有自动迁到商业 16 nm；作者写明，许可保护使 MiracleGro 无法从该 PDK 取得 QoR 反馈，开源工艺到现代工艺的可迁移性仍是社区问题。
- FireSim 验证覆盖完整 intspeed，657.xz 使用 16GB swap；墙钟数字把 Sky130 频率乘到 FireSim IPC 上。
- 循环运行可达数百小时，失败轮次来自基础设施故障与人工停环修改，时间计入总运行估计。
- 这是实现约束下的通用乱序核优化，评测集是 SPEC CPU2017，没有直接给出 LLM 推理数字。

## 与 wiki 的关系
- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — 把「RTL + 综合 QoR 闭环」补进超标量研究主线
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — BLOOM 在加深/改写前端、LSQ、预取与唤醒逻辑的同时，必须看关键路径
- [PaFeDSE](/papers/pafedse-pareto-feedback-microarch-dse.md) — 用代理模型搜 OoO 参数；MiracleGro 直接改 BOOM RTL
- [Superscalar Loop Processors / Schnizo](/papers/superscalar-loop-processors-schnizo.md) — 用静态循环结构抬 PE 的 IPC；BLOOM 走通用乱序应用核

# Citations
- [arXiv:2611.26517](https://arxiv.org/abs/2611.26517) — Cui, Hermida-Rivera, Toubes, Fang, Zhang, Nikolić, Fletcher, Karandikar（UC Berkeley）
- [raw stub](/raw/papers/bloom-miraclegro-ooo-core.md)
- [PDF](/raw/papers/BLOOM_MiracleGro_OOO_Core_2026.pdf)
