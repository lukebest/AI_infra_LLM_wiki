---
title: Deterministic Execution
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [deterministic, compiler, spatial-execution, scheduling, inference]
sources: [raw/articles/nvidia-groq3-lpx-blog-2026-04.md]
---

# Deterministic Execution（确定性执行）

在 AI 推理语境下，确定性执行指编译器完全控制计算时序、数据搬运和同步，而非依赖运行时硬件调度器。目标是可预测的延迟，减少 jitter。

## 核心原则
1. **编译器编排**：所有操作时序在编译时确定
2. **显式数据搬运**：无硬件缓存，编译器管理数据放置
3. **确定性通信**：芯片间协议消除时钟漂移（如 plesiosynchronous）
4. **空间执行**：操作映射到物理资源，而非时间分时复用

## 实例

### WSE Color-based Routing
- 24 个 color 编译时静态路由，运行时零决策
- 详见 [[cerebras-wse]]

### Groq LPU Spatial Execution
- 编译器显式调度 MXM/VXM/SXM 操作
- Plesiosynchronous C2C 协议消除多芯片时钟漂移
- 详见 [[nvidia-groq-3-lpx]]

## 为什么重要
- Agentic AI 需要 ~1000 tokens/sec/user，延迟 jitter 直接影响用户体验
- 小 batch 下传统 GPU 的硬件调度引入不可预测延迟
- 确定性执行使 TTFT 和 per-token 延迟稳定可预测

## 挑战
- 编译器复杂度高（需要精确建模所有时序）
- 灵活性降低（动态 workload 需要重新编译或过度配置）
- 资源利用率可能低于自适应调度

## 相关页面
- [[nvidia-groq-3-lpx]] — LPU 确定性执行实例
- [[cerebras-wse]] — WSE color-based 确定性路由
- [[deterministic-execution]] — 空间执行模型
- [[deterministic-execution]] — 准同步协议
