---
type: Summary
title: AI Infra Book Ch.5 Operators and Runtime
description: 第5章算子与运行时—分块复用、FlashAttention、CUDA Graph、persistent kernel、提交重叠
tags:
- book
- compiler
- scheduling
- kernel
- gpu
- optimization
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.5 算子与运行时

对接 [FlashAttention](/concepts/flashattention.md)、[GPU SIMT](/concepts/gpu-simt-architecture.md)、作者 AKG 经历（[实体](/entities/bojieli-ai-infra-book.md)）。

## 三个判断

1. **复用需要空间**：更大 tile / 保留量化中间结果，减重读，但占 SRAM，并决定能驻留多少 CTA（隐藏延迟的在途访存）。
2. **依赖决定顺序**：逐元素可融合；归约要部分和或在线统计。FlashAttention = 分块 + 在线 softmax（作者写 AKG 时摸到的同族思路）。
3. **总时间看执行顺序**：带宽给传输下界；流水线由较慢阶段定间隔；关键路径决定局部优化是否可见。

## 机制速写

- Host→device 拷贝、stream/event、kernel launch：提交时间 ≠ 结果可用时间。
- 沿输出维切 vs 沿归约维切：后者跨卡就变成 AllReduce（Ch.6）。
- CUDA Graph：减提交，但输入复制/动态形状有代价。
- Persistent kernel：按数据块调度，适合 decode 小 kernel 风暴。
- 综合：一次 Qwen3 请求按热点占比选融合/图/持久化，而不是全开。

跨卡后，「一片结果何时就绪、谁读、保存多久」变成通信启动与双缓冲——直接进入 [超节点](/analyses/ai-infra-book/ch06-supernode.md)。

# Citations

[1] [Ch.5](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/05-算子与运行时.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
