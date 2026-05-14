---
title: Cerebras WSE
created: 2026-04-16
updated: 2026-04-16
type: entity
tags: [cerebras, wse, accelerator, deterministic, inference, mesh]
sources: []
---

# Cerebras WSE (Wafer-Scale Engine)

晶圆级 AI 加速器。WSE-3 为最新代：900K 核心，44 GB SRAM，214 Pbit/s fabric 带宽。

## 确定性路由
- 24 个 color（虚拟通道），编译时静态路由
- 每跳 ~0.4ns，color 之间互不阻塞
- 与 [[nvidia-groq-3-lpx]] 的 plesiosynchronous C2C 是不同路径实现确定性

## 与 Groq LPU 的对比
| 维度 | Cerebras WSE | Groq 3 LPU |
|------|-------------|------------|
| 核心 | 900K 简单 PE | 256 复杂 LPU |
| 内存 | 44 GB 片上 SRAM | 128 GB 片上 SRAM |
| 路由 | 24 color 静态 | 96 C2C plesiosynchronous |
| 编程 | CSL（数据流） | Compiler spatial |
| 模型 | 分布式内存 | 分布式内存 |

## 相关页面
- [[deterministic-execution]] — 共同使用的确定性范式
- [[nvidia-groq-3-lpx]] — 对比参照
- [[lpu-architecture]] — LPU 架构
- [[wse-nom-contradiction-analysis]] — 矛盾论六步框架分析 NoW
- [[cerebras-wse-vs-groq-network-comparison]] — WSE vs Groq 全面对比
- [[noc-router-microarchitecture]] — WSE NoC Router 的理论基础
