---
type: Summary
title: AI Infra Book Ch.8 Inference Optimization
description: 第8章推理优化—连续批处理、分页 KV、前缀缓存、量化/卸载、推测解码
tags:
- book
- inference
- serving
- kv-cache
- batching
- quantization
- speculative-decoding
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.8 推理优化

单实例内把 Ch.1–5 的预算变成服务配置。对接 [PagedAttention](/concepts/pagedattention-vllm.md)、[Inference Capacity Trap](/concepts/inference-capacity-trap.md)、[DSpark](/concepts/dspark-speculative-decoding.md)。部署分工交给 [Ch.9](/analyses/ai-infra-book/ch09-distributed-inference.md)。

## 资源

权重跨请求共享；KV 随上下文线性涨。容量：权重 + 各请求 KV + 运行时缓冲。从单请求时间到 SLO：排队 + 批执行。

## 机制

- **合批**：摊薄每 token 权重读；每条仍读自己的 KV。权重若改由更快独立存储供给（Ch.6 ROM），合批收益要重算。
- **连续批处理**：短请求释放槽位立刻补人。
- **分块 prefill**：减少长输入对在途 decode 的抢占（同构集群上常优于硬 PD 分离，见 Ch.9）。
- **分页 KV**：按块分配，减碎片；分支 CoW；前缀缓存省重算。准入/换出/重算是容量不够时的旋钮。
- **压缩与卸载**：权重量化改 \(M_W\)；KV 压缩改读成本；权重卸载每步要搬得回来。
- **推测解码**：草稿+验证；每轮耗时 vs 每轮输出数。输出变短时优势可消失。

## 设计规则

先检查内存能否同时放下目标并发，再看能否按期，最后比每个**合格**结果的 GPU 时间。记录三件事：能驻留多少请求状态、P/D 各多快、延迟随 batch 与到达率怎么变。

# Citations

[1] [Ch.8](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/08-推理优化.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
