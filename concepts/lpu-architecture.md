---
title: LPU Architecture
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [lpu, accelerator, architecture, deterministic, inference]
sources: [raw/articles/nvidia-groq3-lpx-blog-2026-04.md]
---

# LPU Architecture（Language Processing Unit）

LPU 是 Groq（现 NVIDIA）设计的推理专用加速器架构。核心思想：不追求峰值算力，而是追求可预测的低延迟。

## 设计哲学
- **SRAM-first**：片上 SRAM 作为主要工作存储，不用硬件缓存
- **向量为主**：320-byte 固定向量作为计算/内存/通信的统一工作单元
- **编译器控制**：显式调度一切，无运行时决策
- **确定性互联**：C2C 链路 + plesiosynchronous 协议

## Groq 3 LPU 执行模块
| 模块 | 功能 |
|------|------|
| MXM (Matrix) | 密集 MAC，固定数据类型，可预测吞吐 |
| VXM (Vector) | 逐元素运算、类型转换、激活函数 |
| SXM (Switch) | 排列、旋转、分发、转置 |
| MEM | 500 MB SRAM，150 TB/s 带宽 |

## 与 GPU 的区别
| 维度 | GPU | LPU |
|------|-----|-----|
| 内存层次 | HBM + 缓存（硬件管理） | SRAM（编译器管理） |
| 调度 | 硬件 warp scheduler | 编译器静态调度 |
| 数据搬运 | 隐式（缓存一致性） | 显式（编译器编排） |
| 优化目标 | 峰值吞吐 | 可预测延迟 |
| 通信 | NVLink（自适应路由） | C2C（确定性） |

## 相关页面
- [[nvidia-groq-3-lpx]] — Groq 3 LPU 实体
- [[deterministic-execution]] — 确定性执行概念
- [[spatial-execution]] — 空间执行模型
