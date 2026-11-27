---
type: Paper
title: "CarrierKV: An Edge LLM Accelerator with Positional Carrier Decomposition for Low-Bit KV Cache"
description: "Brown / Google Research — 22 nm FDSOI 综合；与 NVFP4 相同缓存体积下，Qwen3-4B 的 32K RULER 从 79.4 升到 91.1，面积 +2.9%，20K token 推理请求能量 +0.12%"
tags:
- kv-cache
- quantization
- numeric-format
- edge
- accelerator
- inference
- decode
- attention
- energy
- llm
- architecture
- hardware
created: 2026-11-24
updated: 2026-11-27
timestamp: '2026-11-27T00:00:00Z'
paper_author: [Junyi Luo, Xinting Jiang, Ruichen Qi, Gregory Kielian, Quan Cheng, Mehdi Saligane]
year: 2026
venue: preprint
arxiv: '2611.26857'
sources:
  - raw/papers/CarrierKV_Positional_Carrier_Decomposition_2026.pdf
  - raw/papers/carrierkv-positional-carrier-kv.md
---

# CarrierKV：先去掉位置载波，再把 Key 量化到 4-bit

## 一句话结论
布朗大学与 Google Research 的 CarrierKV 观察到：RoPE 之前，每个 KV 头的 Key 里有一个与内容无关的常向量，旋转之后变成随位置转的「位置载波」，并占掉大部分能量。NVFP4 的共享缩放会被这段载波定住，内容残差大约损失 5 dB 的量化信噪比。方案在 RoPE 之前去掉载波、只存内容残差，用片上相位引擎按位置再生载波对分数的贡献。与 NVFP4 相同的缓存体积下，Qwen3-4B 的 32K RULER（七项）从 79.4 升到 91.1（BF16 为 92.6）；四模型上 32K PG19 的 PPL 增量降到 NVFP4 的 1/1.8 到 1/5.9。22 nm FDSOI、600 MHz 下，相对同配置的 NVFP4 加速器面积 +2.9%，Qwen3-4B 一条 20K token 推理请求的能量 +0.12%。

## 动机
边缘侧 batch 1 解码时，每个生成 token 都要读完全部权重和整份 KV。Qwen3-4B 在 32K 时 BF16 KV 约 4.8 GB，4-bit 权重下约占每 token 读出的 70%。NVFP4 把这份缓存缩小约 3.6×，但同一模型的 32K RULER 从 92.6 降到 79.4；再加 Hadamard 旋转会降到 57.7。已有方法在 RoPE 之后减均值、按通道缩放或做旋转，没有用「每头一个固定向量 + 位置」把这段载波算出来。

## 方案
位置载波分解：在 RoPE 之前减去每头的常向量，缓存只保留内容残差；残差旋转并量化之后，注意力分数直接在 4-bit 码上算。片上相位引擎按「每周期一个 Key」再生载波分数项，一组 64 个 cos/sin 供该头的全部 query 头共用。

准确率在四张 H100 上用软件模拟加速器的数值格式与算法。线性层为 W4A4 NVFP4，Query 为 FP8，Value 为 NVFP4，各组只在 Key 处理上不同。对照为 NVFP4、SageAttention（RoPE 后减均值）和 P3-LLM（RoPE 后按通道缩放、128 一组的 INT4）。RULER 用 13 项中的 7 项 KV 敏感子任务，每项 100 条，长度 32K。

硬件：CarrierKV 与 NVFP4 基线加速器在同一 22 nm FDSOI、0.8 V、600 MHz 流程下实现，门级功耗用 Qwen3-4B 数据，SRAM 来自存储器编译器。每 token 时延与能量来自 SCALE-Sim v3（GEMM）加 Ramulator 2.1（LPDDR5-6400 x64），DRAM 能量跟数据手册电流。基线共享同一套 GEMM、SRAM 与注意力引擎，只去掉 CarrierKV 新增部分。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 32K RULER（七项平均） | Qwen3-4B：BF16 92.6，NVFP4 79.4，Sage 86.9，P3-LLM 75.1，CarrierKV **91.1**（并高于 FP8 Key 的 89.3）。四模型上 CarrierKV 都高于三个 4-bit 对照 | Table IV / Abstract / §V-B |
| 32K PG19 PPL 增量（相对 BF16 KV） | 四模型上把 NVFP4 的增量降到 **1/1.8 到 1/5.9**。Qwen3-4B：NVFP4 0.917，CarrierKV **0.199** | Table IV / §V-B |
| 随缓存变长的损失 | Qwen3-4B 上 NVFP4 的增量从首个 4K 的 0.80 升到末段 1.07，CarrierKV 保持在 0.17–0.24，末段低于 FP8 Key（0.19 vs 0.27） | Fig. 6 / §V-B |
| 思考模式（Qwen3-8B） | 六个基准平均：BF16 54.6，NVFP4 与 Sage 均为 51.1，CarrierKV **52.6**，并在各项上领先或打平这两个 4-bit 对照 | Table V / §V-B |
| 面积与请求能量 | 相对 NVFP4 加速器面积 **+2.9%**（4.945→5.087 mm²）；Qwen3-4B、1K prompt + 20K 生成的能量 **+0.12%**（86.595→86.700 mJ/token），其中 DRAM 约占 96% | Table VI / §V-C |
| 相对 FP8 Key | 32K 缓存时每 decode step **1.16×** 更快、能量少 **13.7%**；128K 时 **1.28×**、少 **22.2%** | §V-C |
| 3-bit TurboQuant Key | Qwen3-4B 的 32K PPL 增量从 **69.7 降到 0.76** | Abstract |

相对「RoPE 之前就缓存、每次读取再旋转」的路径，作者估计同等吞吐下 BF16 点积加 FP8 Query 与 RoPE 至少比 NVFP4 分数单元多 166 pJ/key，是 CarrierKV 所加 32 pJ 的 5.2 倍。

## 与已有页的增量
[Kameleo](/papers/kameleo-bit-serial-activation-precision.md) 在加速器上当场选择激活尾数。[Numeric Formats](/concepts/numeric-formats-ai-hardware.md) 已记下 NVFP4 / MX 缩放格式的硅代价。CarrierKV 针对长上下文 Key 里可计算的位置载波，把 4-bit 块缩放的信噪比找回来，并给出与 NVFP4 基线加速器对齐的 22 nm 面积和请求能量。

## 与 wiki 的关系
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — NVFP4 块缩放与位置载波对共享 scale 的影响
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 边缘侧 decode 被 KV 读出主导
- [Kameleo](/papers/kameleo-bit-serial-activation-precision.md) — 同属低比特加速器上的格式选择
- [OptiDecode](/papers/optidecode-fso-kv-regeneration.md) — 另一条减少 decode 期 KV 流量的路径

## 开放问题
- 任务准确率是在 H100 上用软件模拟加速器格式得到的；面积来自 22 nm 综合，时延与能量来自 SCALE-Sim + Ramulator，不是板级芯片。
- RULER 用了 13 项中的 7 项 KV 敏感子任务；思考模式表是 Qwen3-8B。
- LPDDR5 占请求能量约 96%，所以面积开销几乎不反映到能量上；换一套更靠近计算的存储器会改变这笔账。


2026-11-27：[Gossamer](/papers/gossamer-constant-budget-kv-compression.md) 把量化放到恒定 KV 预算下的效用选择里，与本页在去掉位置载波后再量化 Key 是同一条低比特 KV 数据通路上的不同切入点。

# Citations
- [arXiv:2611.26857](https://arxiv.org/abs/2611.26857) — Luo, Jiang, Qi, Kielian, Cheng, Saligane（Brown University / Google Research）
- [raw stub](/raw/papers/carrierkv-positional-carrier-kv.md)
- [PDF](/raw/papers/CarrierKV_Positional_Carrier_Decomposition_2026.pdf)
