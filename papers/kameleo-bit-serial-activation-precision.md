---
type: Paper
title: "Kameleo: In-Situ Activation-Precision Selection for Bit-Serial LLM Accelerators"
description: "KU Leuven MICAS — 四模型七数据集上，1% PPL 预算内把 prefill MXU 周期降到 2.11–2.34×；选择硬件使 16 nm 加速器面积 +3.7%"
tags:
- accelerator
- quantization
- numeric-format
- mixed-precision
- llm
- inference
- prefill
- energy
- dataflow
- architecture
- hardware
created: 2026-11-23
updated: 2026-11-27
timestamp: '2026-11-27T00:00:00Z'
paper_author: [Robin Geens, Thomas Debelle, Marian Verhelst, Chao Fang]
year: 2026
venue: preprint
arxiv: '2611.25971'
sources:
  - raw/papers/Kameleo_Bit_Serial_Activation_Precision_2026.pdf
  - raw/papers/kameleo-bit-serial-activation-precision.md
---

# Kameleo：在 bit-serial 加速器上当场选定激活尾数长度

## 一句话结论
KU Leuven MICAS 的 Kameleo 把激活尾数长度的选择从离线、靠全模型 PPL 的校准，改成加速器在数据上当场完成。它利用 bit-serial 数据通路里「短尾数结果是满尾数计算的中间态」，用局部代理比较降精度与满精度 GEMM 输出，两趟扫描工作负载的前缀即可锁定每个 GEMM 的长度。四模型、七数据集上，PPL 恶化落在 1% 预算内，prefill 的 MXU 周期降到 2.11–2.34×，接近在评测数据上离线校准的配置；选择硬件只让加速器面积增加 3.7%。

## 动机
只量化权重时，片上成本转向更高精度的激活运算。可变长度的 bit-serial 加速器可以只算每层需要的尾数，但长度通常靠代表数据集上的全模型 PPL 搜索来定（作者复现 ANDA 时，每次搜索需要 13–25 次全模型评估，约 0.4–1.7 个 H100 GPU 小时），换一套数据后质量会在无人察觉时越界。

## 方案
在已有 bit-serial 处理元件上增加候选/参考寄存器和误差检查，把局部代理嵌进部分和路径。两趟扫描工作负载的前缀（文中仿真用前 T=8192 个 token，硬件搜索看 2T=16,384 个 token）为每个 GEMM 锁定尾数。容忍度 τ=0.28 被当作设计常数：在 WikiText2 上把 τ 从 0.15 扫到 0.6，周期收益从 1.91× 到 2.83×，PPL 在 τ=0.32 以内仍落在 1% 预算里。

评测模型为 Llama2-13B、Llama3.1-8B、Qwen2.5-7B、Yi1.5-34B，权重为 OmniQuant 初始化的 INT4（无学习 clipping）。质量是 2048-token 窗口 PPL，预算相对 W4A16、满 11-bit BFP 尾数恶化 1%。吞吐是相对 W4A16 + FP16 激活的 prefill MXU 周期解析计数（含注意力 GEMM，注意力保持满尾数），并用周期精确 RTL 仿真校验。硬件用 SystemVerilog，在 TSMC 16 nm、250 MHz、0.75 V 下与 ANDA 实现同样综合，功耗来自仿真 VCD。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| WikiText2，无需校准 | 四模型周期降低 **2.12–2.29×**，PPL 恶化低于在该集上校准的 ANDA；摘要给出的四模型七数据集范围为 **2.11–2.34×** | Table I / Abstract / §IV-C |
| 跨数据迁移 | ANDA 在 42 次「在一套数据上校准、到另一套上部署」里有 **18** 次超过 1% 预算，PPL 恶化最高 **2.9%**。Kameleo 在各数据集上自行选择，预算均满足，周期降低 **2.25–2.28×** | Fig. 4 / §IV-D |
| 下游零样本 | 六个零样本任务上，用 WikiText2 选出的长度，各模型平均准确率变化最多 **0.1** 个百分点；Llama2-13B 从 72.8% 到 72.9% | §IV-C |
| 面积与功耗 | 选择硬件使 FP 累加路径面积 +55%、MXU +25.8%，加速器级（SRAM 占主导）为 **+3.7%**；推理期 MXU 功耗 **+3.5%**。选择过程中 MXU 为 **166.7 mW**（相对 ANDA +50%） | Fig. 5 / §IV-E |
| 对照格式 | FIGNA 的 13-bit 尾数保持 FP16 精度，周期收益仅 **1.23×**；VS-Quant 的逐向量 INT4 达到 3.56–3.68×，PPL 恶化 4.4–6.8%。ANDA 在 WikiText2 本集上校准达到 **2.24–2.83×**，贴近 1% 预算 | §IV-C |

前缀长度从 2048 改到 32,768，周期收益最多变 0.02×，PPL 最多变 0.07%（τ=0.28）。

## 与已有页的增量
[FlexPosit](/papers/flexposit-tunable-fractional-precision-llm.md) 用可调 Posit + bit-serial 换格式，长度仍偏设计期。[Coffee](/papers/coffee-elastic-precision-mixed-precision-llm.md) 在脉动阵列上按 GEMM 双侧输入在线分配宽度。[Rising-Precision VLA Accelerator](/papers/rising-precision-vla-accelerator.md) 把上升位宽用在 VLA 动作头的权重上，同组、同属 bit-serial。本篇针对 LLM 激活尾数，强调在加速器上、按当前数据当场选择，并量化离线校准换数据后越界的比例。

## 与 wiki 的关系
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 可变激活尾数与 1% PPL 预算
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — bit-serial MXU 与选择逻辑的面积开销
- [FlexPosit](/papers/flexposit-tunable-fractional-precision-llm.md) — 同属 bit-serial LLM 加速器
- [Rising-Precision VLA Accelerator](/papers/rising-precision-vla-accelerator.md) — 同一组的另一条 bit-serial 数据通路，对象是 VLA 权重日程

## 开放问题
- 吞吐数字是 MXU 周期，覆盖全部 GEMM，但在整模型 token/s 或端到端服务上还要另算。
- 选择过程本身要跑两趟普通 prefill；作者把它写成相对 13–25 次全模型离线评估的代价。
- 综合节点是 TSMC 16 nm、250 MHz，与同文复现的 ANDA 对齐；和 7 nm 的 VLA 加速器页不宜直接比面积。
- 层间分析画在 Llama2-7B 上，主表是另外四套模型。


2026-11-24：[CarrierKV](/papers/carrierkv-positional-carrier-kv.md) 在边缘加速器上处理 4-bit KV 的位置载波，与本页的激活尾数选择是同一条低比特数据通路上的不同对象。


2026-11-27：[ISTS](/papers/ists-bit-slice-steiner-llm-accelerator.md) 同样面向低比特 LLM 的比特级数据通路，但复用对象是 Hamming 近邻上的 Steiner 部分和，评测是 28 nm 仿真而不是激活尾数选择。

# Citations
- [arXiv:2611.25971](https://arxiv.org/abs/2611.25971) — Geens, Debelle, Verhelst, Fang（KU Leuven MICAS）
- [raw stub](/raw/papers/kameleo-bit-serial-activation-precision.md)
- [PDF](/raw/papers/Kameleo_Bit_Serial_Activation_Precision_2026.pdf)
