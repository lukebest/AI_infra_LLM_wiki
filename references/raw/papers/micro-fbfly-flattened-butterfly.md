---
type: Raw Source
title: micro fbfly flattened butterfly
description: Immutable source material from wiki raw/papers/micro-fbfly-flattened-butterfly.md
timestamp: '2026-06-12T00:00:00Z'
ingested: 2026-06-12
---

# Flattened Butterfly Topology for On-Chip Networks

## 核心贡献

将 flattened butterfly（扁平蝴蝶）拓扑从 off-chip 高基数网络引入片上网络（NoC），论证高基数路由器在片上场景的优势，并提出 bypass channel 机制使非最小路由在不增加物理传输距离的前提下降低延迟和功耗。

## 问题背景

- 片上网络大多使用低基数 2D mesh（RAW、TRIPS、Intel Teraflops、Tilera），缺点：直径大（hop 多）、每跳功耗高
- 片上线带宽廉价但 buffer 昂贵，与 off-chip 成本结构相反
- 2D mesh 的 Th（header latency）远大于 Ts（serialization latency），延迟不均衡

## Flattened Butterfly 拓扑

### 构造方法
- 从 k-ary n-fly butterfly 出发，将每行路由器"压扁"合并 → 保留所有跨行连接
- 64 节点示例：3-stage radix-4 butterfly (4-ary 3-fly) → 2-D flattened butterfly, 16 个 radix-10 路由器，concentration factor = 4
- 每维度路由器全互连（行内全连接 + 列内全连接）

### 关键参数（64 节点配置）
| 参数 | FBFLY | MESH | CMESH |
|------|-------|------|-------|
| 路由器数 | 16 | 64 | 16 |
| 路由器基数 | 10 | 5 | 8 |
| 直径（hop）| 2 | 14 | 6 |
| 每端口带宽 | 窄（bisection 恒定）| 宽 | 中 |

### 与 Generalized Hypercube 的区别
- FBFLY 使用 concentration，大幅减少跨 bisection 通道数
- 64 节点 2D-GHC 跨中分线通道数为 mesh 的 16×，serialization 严重影响延迟
- FBFLY 通过 concentration 将通道数增幅限制为 4×（带宽仅减半）

## 路由算法

1. **Minimal routing**: Dimension-Ordered Routing (DOR)，天然无死锁
2. **Non-minimal routing**: UGAL (Universal Globally Adaptive Load-balancing)
   - 负载均衡：根据当前负载决定最小/非最小路径
   - 非最小路径分两阶段：先最小路由到中间节点，再最小路由到目标
   - 使用 DOR 限制每个阶段内无死锁 → 仅需 2 VC

## Bypass Channel 机制

### 问题
非最小路由可能让数据包经过超过最小物理距离的路径（overshoot 或 detour）。

### 解决方案
在 bypass channel 经过路由器处添加 input/output mux：
- **Input mux**: 让本应 bypass 的数据包提前下高速
- **Output mux**: 让本应绕远的数据包提前上高速
- 不增加 switch 尺寸（10×10 → 18×18 不可接受），仅增加 mux

### Yield Arbiter
- Primary input（直接输入）优先；idle 时才让 non-primary 用
- 防止 non-primary 饥饿：沿非最小路径发 control packet（仅路由信息），control packet 到达时强制授权 non-primary
- 最坏情况：延迟等价于无 bypass 的 FBFLY，但仍有能耗节省

## 性能评估

### 合成流量
- **Tornado**: FBFLY-BYP throughput 比 CMESH 提升 50%
- **Bit complement**: FBFLY-BYP 延迟比 CMESH 降低约 28%
- Uniform random: FBFLY-BYP ≈ FBFLY-NONMIN

### SPLASH Trace
- equake/tomcatv: <5% 延迟改善（通信少）
- barnes/ocean: 最高 20% 延迟改善

### 功耗（65nm 模型）
- FBFLY vs MESH: **功耗降低 38%**（减少中间路由器、减少 hop）
- FBFLY vs CMESH: 仍有额外功耗节省
- Bypass mux 功耗可忽略（相比 buffer 和 channel）

### 面积
- 估算 FBFLY 面积为 mesh 的 **1/4**
- CMESH 的 **1/2.5**

## 扩展性

| 方法 | 节点数 | 说明 |
|------|--------|------|
| 增加 concentration | 64→128 | 基数从 10→14，需调整通道带宽 |
| 增加维度 | 2D→3D | 最多 256 节点 |
| 混合（局部 FBFLY + 顶层 mesh）| 更大 | 减少 bisection 通道数，hop 略增 |

## VC 需求分析
- 高基数 + FBFLY 拓扑本身减少了阻塞（仅同源同列冲突）
- 增加 VC 数量反而降低性能（总 buffer 恒定，每 VC buffer 减少）
- 2 VC 足够（1 路由 + 1 协议）

## 关键引用
- Kim et al., "Flattened Butterfly: A Cost-Efficient Topology for High-Radix Networks", ISCA 2007 [15]
- Balfour & Dally, "Design Tradeoffs for Tiled CMP On-Chip Networks", ICS 2006 [3]
- Dally & Towles, "Principles and Practices of Interconnection Networks", 2004 [11]
- Singh, "Load-Balanced Routing in Interconnection Networks", PhD thesis, Stanford, 2005 [23]
