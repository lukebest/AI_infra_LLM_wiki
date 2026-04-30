---
title: NVIDIA Groq 3 LPX
created: 2026-04-16
updated: 2026-04-16
type: entity
tags: [nvidia, groq, lpu, accelerator, inference, deterministic, scale-up]
sources: [raw/articles/nvidia-groq3-lpx-blog-2026-04.md]
---

# NVIDIA Groq 3 LPX

Rack-scale 低延迟推理加速器，NVIDIA Vera Rubin 平台的第七颗芯片。256 个 Groq 3 LPU 互联，专注确定性、低延迟的 agentic 推理。

## 核心规格

| 指标 | 数值 |
|------|------|
| 推理算力 | 315 PFLOPS |
| SRAM 总量 | 128 GB（256 × 500 MB） |
| SRAM 带宽 | 40 PB/s |
| 芯片数 | 256 LPU |
| Scale-up 带宽 | 640 TB/s |
| 机柜 | 32 × 1U compute tray（每 tray 8 LPU） |

## 架构特点

### Groq 3 LPU 核心设计
- **320-byte 向量**为基本工作单元，计算/内存/通信统一
- **MXM**（矩阵执行模块）：密集 MAC 运算
- **VXM**（向量执行模块）：逐元素运算、激活函数
- **SXM**（交换执行模块）：排列、旋转、分发、转置
- **MEM 块**：500 MB 片上 SRAM，150 TB/s 带宽/LPU
- **无硬件缓存**：编译器显式管理数据放置

### C2C 互联
- 96 条 chip-to-chip link/LPU，每条 112 Gbps
- 聚合双向带宽 2.5 TB/s/LPU
- **Plesiosynchronous 协议**：消除时钟漂移，实现确定性多芯片协调

### 确定性执行模型
- 编译器显式调度计算、数据搬运、同步
- 无运行时硬件调度器
- 空间执行模型（spatial execution）
- 目标：TTFT 和 per-token 延迟在小 batch 下仍稳定

## 异构推理架构

LPX 不是独立运行——与 [[nvidia-vera-rubin-nvl72]] 配合：
- **LPX 负责**：FFN / MoE expert 执行（decode 阶段的计算密集部分）
- **Rubin GPU 负责**：prefill + decode attention（memory-bandwidth 密集部分）
- 两者组成异构推理流水线

## 关键数据
- vs 前代：35× 更高推理吞吐/MW
- 万亿参数模型：10× 更多收入机会
- 目标：1000+ tokens/sec/user（agentic AI 场景）
- MGX ETL 机柜架构集成，cableless 设计

## 相关页面
- [[nvidia-vera-rubin-nvl72]] — 同平台 GPU 系统
- [[deterministic-execution]] — 确定性执行模型概念
- [[lpu-architecture]] — LPU 架构概念
- [[scale-up-fabric]] — Scale-up 网络互联
- [[groq-original]] — Groq 公司及原始 LPU 架构
