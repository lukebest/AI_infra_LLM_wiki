---
type: Summary
title: A Cloud-Scale Characterization of Remote Procedure Calls
description: SOSP 2023 Google — 700 天 fleet 级 RPC 剖析：>10K 方法、毫秒级延迟、RPC/CPU 比年增 30%；尾延迟由 RPC tax 主导
tags:
- rpc
- infrastructure
- latency
- throughput
- communication
- google
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Cloud_Scale_RPC_Characterization_2023.pdf
---

# A Cloud-Scale Characterization of Remote Procedure Calls

**SOSP 2023** | DOI [10.1145/3600006.3613156](https://doi.org/10.1145/3600006.3613156)  
Seemakhupt, Stephens, Khan, Liu, Wassel, et al.（Google + 学界）

Google 内部 **fleet 级 RPC 特征化**（Search/Gmail/Maps/YouTube + Spanner/BigQuery 等）：规模、延迟组成、调用树深度与资源利用，纠正小规模/微服务假设。

## 核心贡献

1. **RPC 用量快于算力**：RPS/CPU cycle **~30%/年**，700 天 **+64%**
2. **>10,000**  distinct RPC methods；毫秒级、KB 级、深层嵌套调用树
3. **延迟分解**：均值主要在应用处理；**尾延迟**由 RPC tax（队列 + 序列化 + 网络）主导
4. **CPU cycle 方差大** → 负载均衡优化空间

## 关键数字

| 指标 | 值 |
|------|-----|
| 观测窗口 | **700** 天 |
| RPC 方法数 | **>10,000** |
| 单日采样 | **722B** RPC |
| RPS/CPU 增长 | **~30%/年** |

## 与 wiki 交叉

- [Clos / Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — 超大规模 DC 网络背景
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 控制面通信设计空间

# Citations

[1] [raw/papers/Cloud_Scale_RPC_Characterization_2023.pdf](raw/papers/Cloud_Scale_RPC_Characterization_2023.pdf)
[2] [raw/papers/cloud-scale-rpc-characterization.md](raw/papers/cloud-scale-rpc-characterization.md) — 结构化摘录
