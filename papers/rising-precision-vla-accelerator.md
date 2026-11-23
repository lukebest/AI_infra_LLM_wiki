---
type: Paper
title: "Rising-Precision VLA Accelerator: Weight Widths that Rise over Flow Steps"
description: "KU Leuven MICAS — LPDDR5X 时序下的 RTL；GR00T N1.6 的 [2,3,3,4] 为 8.02 ms / 78 mJ，在 Thor 一半带宽下相对 Thor 与 FlashRT NVFP4 为 1.7×，能量为后者的 1/9.1"
tags:
- accelerator
- edge
- quantization
- numeric-format
- mixed-precision
- energy
- inference
- latency
- lpddr
- dataflow
- transformer
- ai-agent
- hardware
- architecture
- chip-design
created: 2026-11-23
updated: 2026-11-23
timestamp: '2026-11-23T00:00:00Z'
paper_author: [Robin Geens, Simon Haepers, Jonas Crols, Chao Fang, Marian Verhelst]
year: 2026
venue: preprint
arxiv: '2611.24234'
sources:
  - raw/papers/Rising_Precision_VLA_Accelerator_2026.pdf
  - raw/papers/rising-precision-vla-accelerator.md
---

# 精度随 flow step 上升的 VLA 加速器：让后几步去吸收前面的量化误差

## 一句话结论
KU Leuven MICAS 观察到，VLA 动作头（如 GR00T 的 flow-matching DiT）后几步会衰减前几步的量化误差，因此权重位宽应当随 step 上升。用普通逐通道取整、不必校准或训练，[2,3,3,4] 这一日程在仿真闭环里的多套基准上保持成功率。作者给出的可编程加速器在 LPDDR5X 时序的 RTL 上，把 GR00T N1.6 跑到 8.02 ms / 78 mJ；在 Thor 一半的内存带宽下，相对 Thor 与 FlashRT 的 NVFP4 头都是 1.7×，能量为 FlashRT NVFP4 的 1/9.1。

## 动机
动作头每个 flow step 都要从 DRAM 重读全部权重，却只作用在大约五十个 token 上，推理是访存受限，时间和能量主要由传输的权重比特数决定。作者在 Jetson AGX Thor 上测到，现有 GPU kernel 有固定开销，吃不到逐步变窄的位宽红利。他们因此做一块延迟和能量都随传输比特数缩放的加速器，并让同一套 bit-serial 子阵列在线性层与注意力之间按 step 做运行时分配。

## 方案
存储接口为八条 x16 LPDDR5X-8533，容量 8 GB，峰值 136.5 GB/s（Thor 带宽的 50%），设计目标是 50 Hz 控制率下每拍一次动作头推理。权重从 DRAM 经 FIFO 与熵解码进入 bit-serial 树形阵列，片上只留当前 chunk 的激活、当前层 KV 和常量。Chisel 写 RTL，Verilator 仿真，Ramulator 2 按 JEDEC 时序建模 LPDDR5X；综合为 TSMC 7 nm、1 GHz。还提出 Quantization-in-DRAM：体存储一份 8-bit 副本，在 bank 侧按当前 step 重量化并做 Huffman 编码。

闭环成功率在仿真环境中评估（约 1700 H100 小时），只替换动作头的数据类型与取整。成功率保持的定义是相对发布模型的 90% 区间高于 −3 个百分点。Thor 对照为预热后的 CUDA graph，能量在模块输入处测量并扣掉 idle。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 日程与比特 | 相对逐步都用 4-bit，上升位宽少传 **25%** 的比特。成功 episode 的长度平均变化 **−1%**、最多 2%，于是每任务仍至少少读 **7.8×** 权重比特（每推理为 8.0×） | Abstract / §7.1 |
| 闭环成功率 | [2,3,3,4] 在八套基准里的 **五套** 上保持成功率；均匀 3-bit 与下降的 [4,3,3,2] 在两套筛选基准上都掉点。G1 上成功率下降，该套件上 jerk 为发布模型的 **1.9×** | Fig. 9 / §7.1 |
| RTL 延迟与能量 | GR00T N1.6 的 [2,3,3,4] 为 **8.02 ms**（125 Hz），时间高出 DRAM 地板 14–20%；每推理 **78 mJ**（50 Hz 时约 3.9 W），其中 DRAM 读取占 51%。均匀 8-bit 为 91 mJ，[2,3,3,4] 是其 **31%** | Fig. 10 / §7.4–7.5 |
| 相对 Thor | 在本加速器带宽（Thor 的 50%）下，相对 Thor 与 FlashRT NVFP4 均为 **1.7×**；Thor 在 idle 之上为 **543 mJ**。FlashRT NVFP4 的能量为本设计的 **9.1×**。若缩放到 Thor 带宽，均匀 8-bit 为 **1.3×**，[2,3,3,4] 为 **3.1×** | §7.6 / Fig. 10 / Fig. 12 |
| 面积 | 加速器 **4.6 mm²**，按 Apple M2 同宽度接口的裸片照片估计 PHY **14.4 mm²**，合计 **19 mm²**（60% 逻辑密度），PHY 约占 76% | Fig. 11 / §7.5 |
| 其他头与 VLM | 同一份 RTL 上，GR00T N1.5 的 [2,3,3,4] 为 **5.16 ms**，π0.5 两步 [2,5] 为 **2.70 ms**。单相机策略推理中，动作头相对 Thor 上发布的 BF16 头为 **3.9×**，System 2 用时为 Thor 的 **1.2×**；整次推理 405 mJ，对照 Thor idle 之上 2944 mJ | §7.7 |

## 与已有页的增量
[VLA Workload Characterization](/papers/vla-workload-characterization-embodied-ai.md) 在 Orin 上刻画闭环 VLA 的访存/计算边界，没有给出按 flow step 变宽的加速器。[FlexPosit](/papers/flexposit-tunable-fractional-precision-llm.md) 与 [Kameleo](/papers/kameleo-bit-serial-activation-precision.md) 也走 bit-serial，对象是 LLM 的格式与激活尾数。本篇把上升位宽写进 VLA 动作头的数据通路，并在 7 nm RTL 上给出相对 Thor 的时间和能量。

## 与 wiki 的关系
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 按 step 变化的权重位宽与逐通道取整
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 随带宽缩放的 bit-serial 计算织物
- [VLA Workload Characterization](/papers/vla-workload-characterization-embodied-ai.md) — 同属端侧 VLA，本篇补硬件与量化日程
- [Kameleo](/papers/kameleo-bit-serial-activation-precision.md) — 同一组的 bit-serial LLM 加速器，选择的是激活尾数

## 开放问题
- 全部闭环数字来自仿真。作者写明，量化策略在仿真中保持成功率时，在真实机器人上有过失败记录。
- Quantization-in-DRAM 需要现有商用颗粒尚未提供的模式。
- 芯片能量来自带时钟树、在布局布线之前的网表；DRAM 能量来自模型。
- 主对照里加速器只用 Thor 一半的内存带宽；缩放到同等带宽的数字单独写在 Fig. 10a。动作头时间不含 System 2 的 KV 投影。

# Citations
- [arXiv:2611.24234](https://arxiv.org/abs/2611.24234) — Geens, Haepers, Crols, Fang, Verhelst（MICAS, KU Leuven）
- [raw stub](/raw/papers/rising-precision-vla-accelerator.md)
- [PDF](/raw/papers/Rising_Precision_VLA_Accelerator_2026.pdf)
