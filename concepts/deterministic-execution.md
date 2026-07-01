---
type: Concept
title: Deterministic Execution
description: 编译器控制时序、消除 jitter 的执行范式
tags:
- deterministic
- compiler
- spatial-execution
- scheduling
- inference
timestamp: '2026-05-29T00:00:00Z'
created: 2026-04-16
sources:
- raw/articles/nvidia-groq3-lpx-blog-2026-04.md
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
- Color 同时充当虚拟通道 ID 和任务选择器（Color×4 → 指令地址）
- 详见 [Cerebras Wse](/entities/cerebras-wse.md) 和 [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md)

### Groq LPU Spatial Execution
- 编译器显式调度 MXM/VXM/SXM 操作
- Plesiosynchronous C2C 协议消除多芯片时钟漂移
- 详见 [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md)

## 为什么重要
- Agentic AI 需要 ~1000 tokens/sec/user，延迟 jitter 直接影响用户体验
- 小 batch 下传统 GPU 的硬件调度引入不可预测延迟
- 确定性执行使 TTFT 和 per-token 延迟稳定可预测

## 挑战
- 编译器复杂度高（需要精确建模所有时序）
- 灵活性降低（动态 workload 需要重新编译或过度配置）
- 资源利用率可能低于自适应调度

## WSE 上的性能可预测性

确定性执行使 WSE 的 collective 通信可以用解析模型精确预测：< 4% 误差（CS-2 实测）。详见 [Wse Performance Model](/concepts/wse-performance-model.md) 和 [Wse Reduce Algorithms](/concepts/wse-reduce-algorithms.md)。

## 与通用 CPU 的对比

确定性执行是 **OoO CPU 的反面**：不依赖 [Branch Prediction](/concepts/branch-prediction.md)、[Out-of-Order Execution](/concepts/out-of-order-execution.md)、Cache 推测（[Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md)）、[Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) 或 [Memory Fence and Barrier](/concepts/memory-fence-barrier.md)（无 coherence/Store Buffer 链）。即 **Software-Managed Everything**——编译器在 [ISA Design Principles](/concepts/isa-design-principles.md) 之上直接编排时序、地址与数据流；详见 [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md)。

## 相关页面
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 高级编程与编译时 spatial 编排
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPU 确定性执行实例
- [Cerebras Wse](/entities/cerebras-wse.md) — WSE color-based 确定性路由
- [Wse Performance Model](/concepts/wse-performance-model.md) — WSE 通信性能模型
- [Wse Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — WSE Reduce/AllReduce 算法族

# Citations

[1] [raw/articles/nvidia-groq3-lpx-blog-2026-04.md](raw/articles/nvidia-groq3-lpx-blog-2026-04.md)
