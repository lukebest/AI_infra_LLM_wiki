---
type: Summary
title: AI Infra Book Ch.12 Edge-Cloud
description: 第12章端边云—交互时间分解、模型切分通信、WAN 窗口/丢包、Queqiao 语音
tags:
- book
- inference
- latency
- networking
- infrastructure
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.12 端边云协同

同一套五问从机房拉到 WAN / 无线。对接 [Constraint-Driven Design](/concepts/constraint-driven-ai-infra-design.md)、[Prefill/Decode](/concepts/prefill-decode-divergence.md)。边缘 NPU 细节不在本 wiki 主线，不展开产品清单。

## 三层时间

1. 数据量 / 计算量 / 传播距离 → 各步下界  
2. 依赖：哪些相加、哪些重叠  
3. 连接建立、窗口、竞争、恢复 → 实测等待  

书例：图片精修完成时间约 12.8 s；语音逐块递推；Computer Use 逐轮累积。端侧：内存带宽给 tok/s 上限，容量定模型+上下文，电池定可持续时长。

## 设计规则

- 端侧编码可能把「小图」换成「大特征」——先减相同耗时，再比省下的计算 vs 多出的传输。
- 模型内切分把一次传输换成逐层同步（与机内 AF 同构，RTT 换成几十毫秒）。
- 复用（迁移、连接预热、图编译）用准备成本 / 每次节省求回本次数。
- **丢包 ≠ 拥塞**：随机丢包路径上用丢包反推带宽可低估约三个数量级；应测带宽再加冗余。Queqiao：先消额外等待，再碰传播时间。

最终仍是：先质量与期限，再成本；平均速率够仍可能因慢轮或丢进度超期。

# Citations

[1] [Ch.12](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/12-端边云协同.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
