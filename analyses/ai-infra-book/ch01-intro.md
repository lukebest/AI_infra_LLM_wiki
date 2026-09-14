---
type: Summary
title: AI Infra Book Ch.1 Intro
description: 第1章初识 AI Infra—容量/算力/带宽/延迟四类数字、MFU/MBU、70B 与 Qwen3-8B 数量级
tags:
- book
- infrastructure
- architecture
- inference
- memory
- gpu
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.1 初识 AI Infra

方法见 [Constraint-Driven Design](/concepts/constraint-driven-ai-infra-design.md)。对照 [Quantitative Architecture](/concepts/quantitative-architecture-fundamentals.md)。

## 分析顺序

先容量 \(M_W+M_{\mathrm{state}}+M_{\mathrm{work}}\le M_{\mathrm{cap}}\)，再 \(T=\max(F/\Pi,R/\beta)\)，最后看重叠与串行等待。Amdahl：只加速占比 \(f\) 的环节，总加速 \(1/((1-f)+f/s)\)。

## 硬件速查（书表）

| | RTX 4090 | A100 80GB | H100 SXM |
|--|----------|-----------|----------|
| 显存 | 24 GB | 80 GB | 80 GB |
| HBM | 1.008 TB/s | 2.039 TB/s | 3.35 TB/s |
| BF16 矩阵 | 165.2 TFLOP/s | 312 | 989.4 |
| 读 1 GB | 0.99 ms | 0.49 ms | 0.30 ms |

400 Gbit/s NIC = **50 GB/s** 线速；传 1 GB 理想 20 ms。

## 70B / 8B 预算（书中数字）

DeepSeek-R1-Distill-Llama-70B：BF16 权重 **141.11 GB**（超单卡 H100）；分组 8-bit ≈ **73.73 GB** 可进一张，加 8K KV≈2.68 GB + 工作区≈2.15 GB ≈ 78.56 GB。

Qwen3-8B BF16、并发 1、2K prefill / 2K 后一步 decode（RTX PRO 6000：503.8 TFLOP/s，1.792 TB/s）：

| 项 | 值 |
|----|----|
| 权重 | 16.38 GB |
| KV / token | 144 KiB（2K → 288 MiB） |
| Prefill 矩阵 | 29.69 TFLOPs ≈ 58.9 ms 下界 |
| Decode 矩阵 | 16.34 GFLOPs ≈ 0.032 ms |
| Decode 权重+KV 读 | 15.14+0.302 GB ≈ 8.62 ms |
| 实测 inter-token | ~26.5 ms（约 3× 读下界） |

70B 手算：权重读比矩阵算慢约 **148×** → 加带宽/减读取/批内复用，不是堆 FLOP/s。

## 需求如何推架构（1.4）

TPU：语音搜索延迟预算 → 脉动阵列。SmartNIC：40 Gbit/s 包率逼出核数预算。UB：统一本地/远程访问，去掉主机边界上的消息抽象。详见 [UB](/entities/unifiedbus-ub.md)。

## 陷阱

峰值算力翻倍 ≠ 时间减半（先看是否 compute-bound）。装得下权重 ≠ 装得下并发 KV。吞吐升 ≠ 单用户等得更短。

# Citations

[1] [Ch.1](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/01-初识%20AI%20Infra.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
