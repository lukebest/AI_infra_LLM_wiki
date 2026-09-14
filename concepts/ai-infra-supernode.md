---
type: Concept
title: AI Infra Supernode
description: 超节点：高带宽低延迟互联的一组加速器；介于单卡与数据中心之间的协作域，规模由容量/延迟/功率/故障域共同决定
tags:
- supernode
- scale-up
- fabric
- rack
- interconnect
- infrastructure
- topology
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# AI Infra Supernode（超节点）

来自 [李博杰《AI Infra》Ch.6–7](/entities/bojieli-ai-infra-book.md)。**超节点**是经高带宽、低延迟互联紧密协作的一组加速器；**推理实例**是模型如何部署。同一八卡超节点可以放八个单卡实例或两个四卡实例。

本 wiki 已有的 [NVLink / NVSwitch](/concepts/nvlink-nvswitch-scale-up-fabric.md)、[UB](/entities/unifiedbus-ub.md)、[Kyber](/entities/kyber-rack.md) 是实现；本页是**设计单位**：协作域该多大、域内外各放哪种并行。

## 三种把卡凑在一起的理由

| 目标 | 做法 | 典型通信 |
|------|------|----------|
| 容量 | 权重 / KV 装不下单卡 | TP / PP / EP 分片 |
| 延迟 | 单请求要更多算力/带宽 | 更大 TP 组 |
| 吞吐 | 独立请求多 | 更多小实例（DP / 副本） |

实例内并行与请求间并发**争同一批卡**。Ch.6 的 128K Qwen3-32B、四会话、130 ms、至少 75% 按时：四个 **TP2** 实例约 119 ms 全部完成，优于一个 TP8（单会话 41 ms 但排队到 165 ms）。

## 物理组织（三条工业路线）

| 路线 | 代表 | 端口接到哪 | 适合的流量 |
|------|------|------------|------------|
| 直连环面 | TPU v4 \(4^3\) cube + OCS | 邻居 | 沿维 AllReduce；All-to-All 随跳数变贵 |
| 交换 Clos | NVL72、CloudMatrix384 | 交换芯片 | 任意两卡近乎等距；MoE All-to-All |
| 统一总线 | [UB](/entities/unifiedbus-ub.md) / CloudMatrix384 | 主机侧计算+内存 | 内存语义 + 池化；状态按端点+通道而非 QP 对 |

书中 64 卡对照（每卡 6×50 GB/s/dir）：维序归约两种拓扑一样快；均匀 All-to-All 环面平均 3 跳，交换网约 3× 更快；512 卡环面平均 6 跳。交换网代价是芯片与线缆（CloudMatrix384：448 颗交换芯片）。

**功率**：DGX H100 系统 10.2 kW（约 1.275 kW/卡，含配套）。120 kW 柜约 11 台 / 88 卡。风冷约 40 kW/柜阈值 → 3 台/柜；64–72 卡集中布置要液冷。

## 放大超节点换什么、不换什么

V4.1 Flash、200K decode、256×H100（书 6.7.4）：

| 超节点 | 每卡权重 | 每卡会话 | 每卡吞吐 |
|--------|----------|----------|----------|
| 8 卡 | 71.0 GB | 37 | 2,632 tok/s |
| 64 卡 | 17.2 GB | 335 | 19,420 tok/s |
| 128+ | ~11–13 GB | ~360 | ~19.4k（平台） |

8→64 约 **7.4×** 每卡吞吐，主要来自专家/Engram 分片腾出的 HBM。再大无收益。**单用户** batch-1 仍是 362 tok/s（读本卡 8.2 GB 常驻权重），与超节点大小无关。同样 64 卡若拆成八台 HGX 做 EP，NIC 上 dispatch/combine 从 3.7 ms 升到 29.2 ms，每卡吞吐掉到 7,828 tok/s。

训练侧（Ch.7，1024 卡、TP8×DP128）：出口随卡数增长时，8→64 卡超节点吞吐约 **+36%**；128→256 只约 +1.3%。更大高速域不必填满更大 TP——同条件下 TP8 仍优于 TP16/32。

## 设计规则

1. 先逐卡容量，再比完整负载下的完成时刻 / GPU·s，不要先锁一个并行缩写。
2. 把高频小消息（decode TP AllReduce）关在域内；跨域放 DP 梯度或 PP 交接。
3. 出口不会随节点变大自动变宽；3:1 超售把跨域传输拉到 3×。
4. 故障域 = 实例共用的电源/交换机；更大实例 = 更大 blast radius。

# Citations

[1] [Ch.6 超节点](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/06-超节点.md)
[2] [Ch.7 数据中心网络](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/07-数据中心网络.md)
[3] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[4] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
