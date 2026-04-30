---
title: NVIDIA Vera Rubin NVL72
created: 2026-04-16
updated: 2026-04-16
type: entity
tags: [nvidia, gpu, accelerator, training, inference, scale-up]
sources: [raw/articles/nvidia-groq3-lpx-blog-2026-04.md]
---

# NVIDIA Vera Rubin NVL72

NVIDIA Vera Rubin 平台的核心 GPU 系统，72 个 Rubin GPU 通过 NVLink 互联。通用 AI 工作负载（训练 + 推理），与 [[nvidia-groq-3-lpx]] 组成异构推理架构。

## 角色
- AI factory 的通用工作马（training + inference）
- 处理 prefill 和 decode attention
- 高吞吐、高并发服务

## 与 LPX 的分工
- GPU：prefill + decode attention（memory-bandwidth 密集）
- LPU：FFN / MoE expert（compute 密集、延迟敏感）
- 两者共同扩展 Pareto 前沿

## 相关页面
- [[nvidia-groq-3-lpx]] — 异构推理搭档
- [[heterogeneous-inference]] — 异构推理概念
