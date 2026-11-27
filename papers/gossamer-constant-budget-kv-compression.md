---
type: Paper
title: "Gossamer: 推理 LLM 上恒定预算的效用驱动 KV 压缩架构"
description: "Duke / Intel — MICRO 2026；SCALEsim-v2 周期精确仿真 + 28 nm 综合；8192 token 端到端吞吐相对未压缩最高 16.7×，相对 Oaken / Ecco / R-KV 为 5.5× / 4.9× / 1.8×；定制模块 1.46 mm²、811 mW，约占基线系统面积 0.68%、功耗 0.65%"
tags:
- kv-cache
- compression
- quantization
- inference
- decode
- reasoning
- accelerator
- architecture
- llm
- memory
- energy
- numeric-format
- systolic
created: 2026-11-27
updated: 2026-11-27
timestamp: '2026-11-27T00:00:00Z'
paper_author: [Feng Cheng, Cong Guo, Junyao Zhang, Haoxuan Shan, Chiyue Wei, Hong Wang, Hai Li, Yiran Chen]
year: 2026
venue: MICRO 2026
arxiv: '2611.29497'
sources:
  - raw/papers/Gossamer_Constant_Budget_KV_Compression_2026.pdf
  - raw/papers/gossamer-constant-budget-kv-compression.md
---

# Gossamer：在注意力空闲周期里做恒定预算的 KV 压缩

## 一句话结论
Duke 大学与 Intel 提出 Gossamer：在恒定 KV 缓存预算下，按效用在驱逐、合并与量化之间动态选择，并把余弦相似度估计融合进注意力计算（文中称为 Free-Lunch Utilization），使压缩几乎不再额外占用延迟与带宽。质量评估在 DeepSeek-R1-Distill-Llama-8B / Qwen-14B 上进行，MATH-500 / AIME 2024 用 pass@1（每题 16 个样本）。架构性能用基于 SCALEsim-v2 的周期精确仿真，128×128 脉动阵列、输出驻留、FP16 乘与 FP32 累加，片上缓冲合计 64 MB，片外按 HBM2、512 GB/s 建模；定制模块用 SystemVerilog 在商用 28 nm、500 MHz 上综合。8192 token 端到端生成的吞吐，相对未压缩 FullKV 最高 **16.7×**，相对量化方法 Oaken / Ecco 为 **5.5× / 4.9×**，相对驱逐方法 R-KV 为 **1.8×**。定制模块面积 **1.46 mm²**、功耗 **811 mW**，相对基线系统 **213.74 mm² / 123.97 W** 约为 **0.68% / 0.65%**。

## 动机
推理模型的上下文可以拉到数十万 token，KV 会变成容量和带宽的主要来源。文中转述：512 token 时 KV 约占内存不到 2%，到 128K 时可超过 84%。已有量化、剪枝与驱逐多是算法层的固定压缩，常常再增加一遍扫描，系统开销会吃掉收益；缓存仍然随上下文线性增长，batch 机会被压缩。

## 方案
Gossamer 把三种动作放进同一套效用框架，并维持恒定的 KV 预算：

- **驱逐 / 合并 / 量化**：并行估计三种效用，比较器只执行效用最高的一项。合并按预先算好的 top-k 相似度做保范数的 value 更新；量化把候选写入专用量化缓存，缓存已满时计入置换代价。
- **Free-Lunch Utilization**：把余弦相似度估计融合进注意力，利用空闲计算周期，避免单独的全局相似扫描。
- 默认画图时，Gossamer 的预算按 **75% 全精度条目 + 25% 量化条目** 折算成与全精度基线相同的实际内存；同时报告 50% 全精度变体。基线包括 FullKV、改编到 prefill 与 decode 的 SnapKV，以及推荐配置下的 R-KV；吞吐对照还加入 Ecco 与 Oaken。基线按每 128 步再压缩一次。

质量实验：MATH-500 最长生成 8,192 token，AIME 2024 为 16,384；温度 0.6、top-p 0.95；量化码本在 GSM8K 上剖析后用于主评测，并在 LongBench 上做跨域复用。

## 量化结果
- 在各模型与预算上，Gossamer 的准确率曲线最接近 FullKV；低预算时避免了 SnapKV 的大幅下降。消融里，冗余–重要性权重 β=0.1 在各预算上达到峰值。
- 预算 256 时，50% 全精度变体支持的最大 batch 比 FullKV 高出一个数量级以上，并比 R-KV 大约高 **20–40%**。75% 全精度变体在并发上略低、准确率更好。
- 短生成阶段 Ecco 与 Oaken 因立即把 KV 接到 4-bit 而领先；KV 长度超出预算后，Gossamer 在三个模型、两档预算上成为最高吞吐。QwQ-32B 的 50% 全精度变体在 8192 token 时超过 **10×** FP16 吞吐，文中把主要来源归到更大的 batch。
- 8192 token 端到端吞吐：相对 FullKV 最高 **16.7×**，相对 Oaken **5.5×**、Ecco **4.9×**、R-KV **1.8×**。文中强调 1024–2048 这一与准确率相关的预算区间里，75% 与 50% 全精度变体都保持领先。
- Llama-8B 的执行时间分解：预算 2048 时，R-KV 的全局相似扫描占到总运行时间的 **23%**；融合压缩后，相对 R-KV 在预算 512 / 2048 上为 **1.25× / 1.79×**。
- 预算 1024、MATH-500、DS-Llama-8B 上，动作分布为驱逐 **87.6%**、量化 **10.1%**、合并 **2.3%**。
- LongBench v2（DS-Llama-8B，预算 2048）总体准确率 **30.4%**，与 FullKV 相差 **0.4** 个百分点，并超过对照的压缩方法；码本只在 GSM8K 上剖析。

## 局限与解读
- 吞吐与面积来自 **SCALEsim-v2 周期精确仿真** 和 28 nm 综合，不是 GPU 或 ASIC 板测；质量数字来自软件侧的 pass@1。
- 16.7× 是 8192 token 端到端、相对未压缩基线的最高值，随预算增大吞吐会下降。
- 主质量模型是 8B / 14B 蒸馏推理模型；QwQ-32B 主要用于吞吐，并在 GPQA Diamond 与 MATH-500 上作准确率扩展。
- 片外带宽按 HBM2 512 GB/s 建模，与当代 HBM3e 平台的带宽量级不同。

## 与 wiki 的关系
- [CarrierKV](/papers/carrierkv-positional-carrier-kv.md) — 在位置载波剥离后再把 Key 压到 4 bit；Gossamer 在恒定预算下把量化与合并、驱逐放在同一套硬件动作里
- [TripleKV](/papers/triplekv-predict-prefetch-protect-agent-kv.md) — 智能体 KV 的预测、预取与保护，关心的是层级放置；Gossamer 关心的是缓存内部的恒定预算
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 记录混合精度 KV 与量化缓存分区
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 恒定预算如何把 KV 足迹换成更大的 batch 与更少的注意力访存
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 长输出推理中，KV 增长会同时抬高 decode 访存并压低可服务 batch

# Citations
- [arXiv:2611.29497](https://arxiv.org/abs/2611.29497) — Cheng、Guo、Zhang、Shan、Wei、Wang、Li、Chen（Duke / Intel），MICRO 2026
- [raw stub](/raw/papers/gossamer-constant-budget-kv-compression.md)
- [PDF](/raw/papers/Gossamer_Constant_Budget_KV_Compression_2026.pdf)
