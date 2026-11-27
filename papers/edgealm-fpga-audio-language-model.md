---
type: Paper
title: "EdgeALM: 在边缘 FPGA 上统一加速大型音频语言模型"
description: "中山大学集成电路学院 — Alveo U50 装在普通台式主机上板测；8 GB HBM 内可跑到 13B 参数 ALM；Mini-Omni 音频到文本 decode 峰值 169.5 token/s，平均板功耗 26 W、带宽利用率 94%"
tags:
- fpga
- accelerator
- edge
- inference
- decode
- quantization
- compression
- hbm
- architecture
- llm
- energy
- throughput
- isa
created: 2026-11-27
updated: 2026-11-27
timestamp: '2026-11-27T00:00:00Z'
paper_author: [Chenglin Yang, Feifan Xu, Xingyuan Li, Xinpeng Xing, Dihu Chen]
year: 2026
venue: preprint
arxiv: '2611.30216'
sources:
  - raw/papers/EdgeALM_FPGA_Audio_Language_Model_2026.pdf
  - raw/papers/edgealm-fpga-audio-language-model.md
---

# EdgeALM：一块 U50 上同时跑矩阵、卷积和音频语言模型

## 一句话结论
中山大学集成电路学院提出 EdgeALM：面向大型音频语言模型（ALM）的全栈 FPGA 加速器，把卷积与矩阵乘拆到可并发的专用引擎，配 Extra-Coarse-Grained ISA，并用智能体驱动的软硬件递归环做实现优化。压缩侧是统一的 AWQ 风格量化，再加按模态条件的词表裁剪。设计在一块 Alveo U50 上实现，板卡插在普通台式主机（Intel Core i7-8700，自制风扇把 FPGA 温度保持在 60°C 以下），计算主时钟 160 MHz，HBM 平台时钟 450 MHz，HBM2 容量 8 GB。文中报告可在该容量内推理超过 20 个模型，ALM 最大到 13B 参数；音频到文本 decode 中 Mini-Omni 峰值 **169.5 token/s**；用 xbutil 测得平均板功耗 **26 W**，带宽利用率平均为设计上限的 **94%**。词表裁剪与量化合在一起，把 Kimi-Audio 的权重大小从 25.14 GB 降到 **7.35 GB**（70.8%），把 LLaMA-Omni2-3B 从 9.68 GB 降到 **2.75 GB**（71.6%）。

## 动机
边缘侧部署 ALM 同时受模型体积、异构工作负载（卷积、矩阵、注意力）和软件栈限制。已有 HBM FPGA 加速器多针对文本 LLM，而且往往装在机架级板卡上。U50 的板功耗上限为 75 W，可以插进普通台式机，把带 HBM 的加速放到更接近边缘的环境。

## 方案
- **Conv-Matmul Disaggregation**：矩阵引擎（MCE）与卷积引擎（CCE）并发，分别吃各自负载，共享 HBM 带宽。
- **Extra-Coarse-Grained ISA**：把规律的片上搬运与执行序列收进计算指令，降低软件复杂度。
- **压缩**：统一 AWQ 风格量化，加上按模态条件的词表裁剪，使 13B 级 ALM 能放进 8 GB HBM。
- **递归优化**：硬件环在开发服务器（256 GB 内存）上连续迭代，从可综合的初始 RTL 演化到最终布局；软件环从零生成可运行栈，再按人给定的性能目标继续优化。一个被智能体找到的关键改动，是把全部模型推理收进单次 FPGA 启动，减少中间写回 HBM 和与主机的搬运。

实现工具为 Vivado / Vitis 2022.2。最终资源：LUT 587,244，FF 623,683，DSP 1,263，BRAM 567，URAM 204；MCE 主要在 SLR1，CCE 在 SLR0，两颗 SLR 的 LUT 接近均衡。

## 量化结果
压缩（Table II，每格上一行为 Kimi-Audio，下一行为 LLaMA-Omni2-3B）：

- 原始 A2T 为 69.90 / 41.61，WER/CER 为 5.18%/3.07% 与 2.91%/2.15%，权重 25.14 / 9.68 GB。
- 量化后 A2T 降 3.22 / 1.66 分；与词表裁剪合在一起后，A2T 为 66.68 / 39.95，WER/CER 最多升高 **1.19** 个百分点，权重变为 7.35 / 2.75 GB。

板上性能：

- 音频到文本 decode 中，Mini-Omni 峰值 **169.5 token/s**。文中把 **12.5 token/s** 写成实时音频到音频的门槛（对应输出语音至少 12.5 帧/s、每帧至多 80 ms）。经过软件环优化后，所评 ALM 都达到该门槛，并维持实时流式音频到音频。
- 平均板功耗 **26 W**（xbutil），带宽利用率 **94%**。
- 硬件递归环共 158 天、705 个设计版本。软件环在 GLM-4-Voice 的音频到文本任务上，36 分钟得到首个可运行栈（**1.79 token/s**），19.5 小时、127 个版本后达到 **12.52 token/s**。
- 独立 ASR、纯文本 LLM 与 TTS 也可运行，并能级联。相对先前音频加速器，文中称 ASR 准确率更高（Table V）。

Table VI 把 EdgeALM 与 FlightLLM、EdgeLLM、CLAT、AccLLM 四篇 HBM FPGA LLM 加速器并列：对照工作评的是纯文本模型，板卡为 U280 或 VCU128，带宽利用率写为 65.9% / 约 75% / 未给出 / 未给出，功耗写为 45 / 56.86 / 未给出 / 33 W；EdgeALM 为多模态、最大 13B、U50、94%、26 W。这些数字来自不同论文、不同板卡与不同模型，只能作平台与功耗量级上的对照。

## 局限与解读
- 主结果是 **U50 板测**，这是今日四篇里唯一的整板实测。
- 169.5 token/s 是 Mini-Omni 音频到文本 decode 的峰值；实时门槛 12.5 token/s 按输出语音帧率定义。
- 与 FlightLLM / EdgeLLM 等的对照是跨论文表格，模态、模型与板卡都不同。
- 硬件演化耗时 158 天，智能体递归环是实现方法，加速器本身的增量在异构引擎、ISA 与压缩。

## 与 wiki 的关系
- [Chimera](/papers/chimera-fpga-llm-decode.md) — 同样是 HBM FPGA 上的 LLM decode，对象是 U280 与纯文本模型；EdgeALM 把音频模态和卷积路径放到功耗上限 75 W 的 U50 上
- [Cruella](/papers/cruella-mxfp4-bf16-dot-product-fpga.md) — U55C 上的统一 MXFP4/BF16 点积单元；EdgeALM 用的是量化加词表裁剪，以及矩阵/卷积双引擎
- [HETEROVLM](/papers/heterovlm-versal-aie-vlm-serving.md) — Versal VC1902 上的视觉语言模型服务；EdgeALM 面向音频语言模型与桌面级 U50
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 记录把矩阵与卷积拆成可并发引擎、并用粗粒度 ISA 收拢搬运的设计

# Citations
- [arXiv:2611.30216](https://arxiv.org/abs/2611.30216) — Yang、Xu、Li、Xing、Chen（中山大学集成电路学院）
- [raw stub](/raw/papers/edgealm-fpga-audio-language-model.md)
- [PDF](/raw/papers/EdgeALM_FPGA_Audio_Language_Model_2026.pdf)
