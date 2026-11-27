---
type: Paper
title: "ISTS: 用 Steiner 点复用比特切片转移，加速低比特 LLM 推理"
description: "中国科学技术大学 — 28 nm RTL 综合 + 基于 ANT 的周期精确仿真（DRAMSim3 DDR4，并与 RTL 对时序交叉验证）；相对 ANT / BBS / LUTA / TA-D / MCBP-BRCR 平均加速 3.09× / 2.41× / 2.18× / 1.27× / 1.41×，能效 1.67× / 1.52× / 1.41× / 1.17× / 1.22×"
tags:
- accelerator
- numeric-format
- quantization
- bitplane
- inference
- attention
- architecture
- llm
- energy
- systolic
- microarchitecture
created: 2026-11-27
updated: 2026-11-27
timestamp: '2026-11-27T00:00:00Z'
paper_author: [Yifan Wang, Zetao Guo, You Xiao, Wendi Sun, Song Chen]
year: 2026
venue: preprint
arxiv: '2611.34630'
sources:
  - raw/papers/ISTS_Bit_Slice_Steiner_LLM_Accelerator_2026.pdf
  - raw/papers/ists-bit-slice-steiner-llm-accelerator.md
---

# ISTS：在密集的低位切片里，沿 Hamming 近邻复用部分和

## 一句话结论
中国科学技术大学提出 ISTS：一种算法–硬件协同的比特切片加速器。观察是比特切片向量（BSV）在 Hamming 空间里高度聚集，许多向量只离少数代表图案几个比特翻转。把这些代表图案当作共享的 Steiner 点，目标 BSV 的部分和可以由对应 Steiner 点的部分和用少量加/减重建。算法侧用 Steiner Absorption Table Construction（SATC）选出紧凑的 Steiner 集合，再用 FlipPrune 有选择地修剪翻转，扩大可复用群体；硬件侧同时支持静态线性层权重和运行时生成的注意力 K/V。RTL 在 28 nm、500 MHz 上综合，片上 SRAM 用 CACTI 7.0，片外用 DRAMSim3 的 DDR4；端到端是基于 ANT 的周期精确仿真，并与 RTL 对时序交叉验证。相对 ANT、BBS、LUT Tensor Core 扩展阵列（LUTA）、Transitive Array 动态计分板（TA-D）和 MCBP-BRCR，平均加速为 **3.09× / 2.41× / 2.18× / 1.27× / 1.41×**，能效为 **1.67× / 1.52× / 1.41× / 1.17× / 1.22×**。评测负载为 prompt 加上 128 token 的 decode，batch 为 8。

## 动机
比特切片加速器把量化操作数沿位维切开，便于跳过无效的高位切片。低比特 LLM 里，GELU / SiLU 会保留负响应，高位切片的稀疏性下降；符号-幅度表示能让高位更稀，但在 4-bit 里可跳过的高位只剩 1 bit，剩下的计算和功耗被密集、不规则的低位切片主导。文中给出不同量化配置下，低位切片处理占总功耗的 **50.5%–70.2%**。已有复用方法里，MCBP 要求图案精确重复，Transitive Array 沿传递关系复用已算过的部分和，对「只差几个比特」的近邻覆盖有限。

## 方案
- **SATC**：为 BSV 选出一组 Steiner 点，使大多数向量能在很小的双向翻转半径内被吸收；每个目标 BSV 的部分和由所属 Steiner 点重建。
- **FlipPrune**：有选择地修剪翻转，提高吸收覆盖。保守 / 激进配置的目标覆盖分别为 97% 与 98.2%。在 Qwen2.5-7B / LLaMA-2-7B 上，1-bit 修改分别占权重的 **1.92% / 2.05%**，2-bit 修改各约 **0.02%**，3-bit 修改可忽略。
- **硬件**：32×32 PE 阵列，另有 Steiner 引擎（SE）生成共享部分和。设计点取 BSV 宽度 Bw=10、Steiner 点数 K=16、组大小 G=128。Steiner 缓冲仅 **40 KB**，对照 Transitive Array 的 90 KB 前缀缓冲。解码器与编码器相对朴素实现分别减少面积 21.8% 与 14.3%，占 ISTS 核心总面积的 **0.54%** 与 **3.71%**。编码器只在运行时为 K/V 编码时打开。

质量侧在 OPT-1.3B、Qwen-2.5-7B、LLaMA-2-7B/13B、LLaMA-3-8B 上报告 WikiText-2 困惑度，下游任务包括 ARC-Challenge、HellaSwag、PIQA、MMLU、GSM8K。INT8/INT4 基线按模型分别来自 OmniQuant 或 GlowQ。

## 量化结果
- WikiText-2 上，ISTS(C,8) / ISTS(A,8) 的 PPL 上升分别低于 **0.04 / 0.07**，ISTS(C,4) / ISTS(A,4) 低于 **0.05 / 0.08**。ISTS(C,4) 与 ISTS(A,4) 的下游准确率变化落在 **3.5%** 以内，文中把少量上升归为评测波动。
- 在上述 prompt + 128 token decode、batch 8 的端到端设定下，相对 ANT / BBS / LUTA / TA-D / MCBP-BRCR 的平均加速为 **3.09× / 2.41× / 2.18× / 1.27× / 1.41×**，能效为 **1.67× / 1.52× / 1.41× / 1.17× / 1.22×**。
- 计算核心内，PE 阵列占总功耗的 **73.53%**，SE 为 **6.48%**（部分和在多个 BSV 间共享），解码器 **1.36%**，编码器 **9.01%**。片上缓冲在面积和功耗上都占主导。
- 消融中，双向复用的 ISTS-B 把吸收覆盖提到 93.52%，相对对照有 **1.23×** 加速；再加上 FlipPrune 后，再获得 **1.12×**。

## 局限与解读
- 性能与能效来自 **28 nm 综合 + 周期精确仿真**（DRAMSim3 DDR4，仿真器基于 ANT 并与 RTL 对时），不是 GPU 或流片板测。
- 平均加速针对给定 prompt 长度、128 token decode 与 batch 8；不同序列长度会改变线性层与注意力的占比。
- LUT Tensor Core 被作者扩展成 PE 阵列（LUTA）后再比；MCBP 侧只为 GEMM 建模了 BRCR。
- FlipPrune 会改动少量权重比特，PPL 与下游数字是软件侧在改动后的检查点上测的。

## 与 wiki 的关系
- [Kameleo](/papers/kameleo-bit-serial-activation-precision.md) — 在加速器上按当前数据选择激活尾数；ISTS 在比特切片的 Hamming 近邻上复用部分和
- [Cruella](/papers/cruella-mxfp4-bf16-dot-product-fpga.md) — FPGA 上统一 MXFP4/BF16 点积；ISTS 走的是 ASIC 风格的比特切片数据通路
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 低比特 LLM 里低位切片变密之后，复用对象从「全零高位」转到近邻 Steiner 点
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 32×32 PE 阵列与 Steiner 引擎的分工，以及相对 Transitive Array / MCBP 的复用粒度

# Citations
- [arXiv:2611.34630](https://arxiv.org/abs/2611.34630) — Wang、Guo、Xiao、Sun、Chen（中国科学技术大学）
- [raw stub](/raw/papers/ists-bit-slice-steiner-llm-accelerator.md)
- [PDF](/raw/papers/ISTS_Bit_Slice_Steiner_LLM_Accelerator_2026.pdf)
