---
type: Summary
title: AI Infra Book Ch.10 Training System
description: 第10章训练系统—16B/param 状态、ZeRO、流水气泡、checkpoint 周期、临界 batch、RL 配比
tags:
- book
- training
- training-system
- collective
- distributed
- memory
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.10 训练系统（优先章）

对接 [LLM Collectives](/concepts/llm-distributed-training-collectives.md)、[Mixed Precision](/concepts/mixed-precision-training.md)、[CXL Tiered Memory](/concepts/cxl-tiered-memory.md)（卸载同族）。

任务：Qwen3-8B 继续训练 100B token / 30 天；预留 5 天 → 25 天有效，每步预算 **67.9 s**（31,790 步，全局 384×8K）。

## 容量

混合精度 Adam：**16 bytes/param**（BF16 权重+梯度，FP32 主权重+m+v）→ 8B 约 **131 GB**，约 8× 推理权重。峰值是同时驻留的状态+激活+临时缓冲，不是各项永久相加。

FP16 要损失缩放；BF16 同 FP32 指数、不必缩放。FP8 操作数副本 ~1 B/param，主权重/优化器仍高精度——常驻 16 B 不会变成 1 B。

## 计算下界

100B token ≈ \(5.27\times10^{21}\) FLOPs。H100 @ 40% MFU ≈ 7500 tok/s → 计算至少 **6 卡**；两张 80 GB 装得下均分状态但要 ~77 天。40% 取 Llama 3 405B 公开 38–43%。其余 60%：未重叠通信、PP 气泡、带宽受限的更新、重算、掉队、checkpoint。

4090 @ 40%：≥31 卡。32 卡每步算 78.3 s（已超 67.9）；**48 卡 52.2 s**，留 15.7 s 给通信/输入/恢复。

## 状态：ZeRO / 重算 / 卸载

分片只缩小常驻状态；激活与收集缓冲可占满「减半」的幻想（误区：分片×2 ⇒ 峰值/2）。重计算换激活容量。卸载换 PCIe/C2C 时间；转换应在 GPU 带宽侧做还是 CPU 侧，看链路与格式（书 SuperOffload / CPUAdam 案例）。

临界 batch \(B_{\mathrm{crit}}\approx B_{\mathrm{noise}}\)。噪声尺度取 2M token 时，弱扩展加速上限约 **1.64×**（1536 卡 19.4→12.1 天）；强扩展不受此限但固定等待占比上升。

## 步内调度

micro-batch、梯度累积、1F1B / 交错 / 零气泡 / DualPipe：气泡公式见 Megatron / 零气泡论文 / V3 DualPipe（书给事件模型，非实测）。分桶 AllReduce：处理时间可以更长，但能藏进反向空隙——看**完成时刻**是否露出计算。

MoE：容量因子、溢出、反向仍要按路由重放（训推一致）。

## Checkpoint / 故障 / 掉队

\(\epsilon\approx C/I+\lambda(I/2+R)\)。Meta：1024 卡约 7.9 h/中断，折合每卡 ~337 天。异步保存返回 ≠ 可恢复到该点。掉队：步时间由最慢卡决定；MegaScale 约 0.5% 机器明显慢。损失尖峰回滚与硬件故障一起进周期模型。

书案例：**32 卡 ~34.3 天（超期），48 卡 ~24.6 天**。ZeRO-3 每步 12 s 链路大部分被计算覆盖。

## RL

生成 / 验证 / 学习三相。生成 12/s、验证 6/s、保留 75% → 学习端 4.5 轨迹/s，加生成无用。异步有策略版本与长轨迹恢复；路由记录必须与 token 对齐。

# Citations

[1] [Ch.10](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/10-训练系统.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
