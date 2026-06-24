---
type: Entity
title: CASSINI
description: CASSINI 网络感知 ML 集群调度器：几何抽象交错通信相位，Affinity 图，1.6× 吞吐改善
tags:
- nvidia
- inference
- serving
- scheduling
- fabric
- deterministic
- routing
timestamp: '2026-05-08T00:00:00Z'
created: 2026-05-08
sources:
- raw/papers/cassini-network-aware-scheduling-2308.00852.pdf
---

# CASSINI — Network-Aware Job Scheduling in ML Clusters

MIT + UT Austin, arXiv:2308.00852, 2023

## 核心思想

利用 DNN 训练的**周期性通信模式**，通过**时间偏移（time-shift）交错不同 job 的通信/计算相位**，减少网络拥塞。关键洞察：

1. DNN 训练的通信模式在每次迭代中重复（只要超参数不变）
2. 不同 job 的通信 "Up-Down" 相位可以通过时间偏移交错
3. 交错后各 job 可在通信峰值时独占链路带宽 → 减少竞争 → 降低迭代时间

**不需要**交换机/NIC 特殊支持、不改拥塞控制协议，仅作为现有调度器的插件模块。

## 几何抽象（Geometric Abstraction）

### 基本方法
将每个 job 的时间序列网络需求"卷"到一个圆上，圆的周长 = 迭代时间。同一 job 的 Up/Down 相位在不同迭代中映射到圆的同一角度区域。

### 统一圆（Unified Circle）
当不同 job 的迭代时间不同时，用所有 job 迭代时间的 **LCM** 作为统一圆周长。每个 job 在统一圆上重复 r 次。

### 兼容性评分（Compatibility Score）
- 将不同 job 的圆叠加，旋转找到最优角度组合
- Score = 1 − average(Excess(demand)) / link_capacity
- Score = 1 → 完全兼容（无超额需求）
- Score < 0 → 高度不兼容
- 旋转角度 → time-shift 值

### 优化目标
```
Maximize: score = 1 − Σ Excess(demand_α) / (|A| × C_l)
Subject to:
  ∀α: Σ bw_circle_j(α − Δ_j) ≤ demand_α
  0 ≤ Δ_j ≤ 2π/r_j
```

## Affinity 图（集群级扩展）

### 问题
一个 job 可能跨越多条链路，与不同 job 在不同链路上竞争 → 需要为每个 job 找到**唯一 time-shift**。

### 二部图结构
- **U 顶点**：与其他 job 共享链路的 job 集合
- **V 顶点**：承载多个 job 的链路集合
- **边 e=(j,l)**：job j 经过链路 l，权重 = time-shift

### 图遍历算法
基于 BFS 扩展：
- 仅遍历 job 顶点（U）
- 从 job→link 方向取负权重，link→job 取正
- 从随机选定的参考 job（t=0）出发，递推计算所有 job 的唯一 time-shift
- **定理**：无环 Affinity 图保证正确且唯一的 time-shift

## 集成到调度器

以 Themis 为例（≈1000 行代码修改）：

1. **发现放置候选**：调度器返回 N 个等公平性但不同放置的候选（≈300 行改 Themis）
2. **计算唯一 time-shift**：对每个候选构建 Affinity 图 → 解优化 → 选兼容性最高的 → 遍历图算 time-shift
3. **应用 time-shift**：agent 延迟下一次迭代启动时间；监控漂移并调整（实际调整很少发生）

## 性能数据

### 测试平台
24 × A100 GPU 服务器，50 Gbps ConnectX-5 RDMA NIC，RoCEv2，Tofino 交换机构建 48 链路拓扑

### 13 个 DNN 模型
VGG11/16/19, ResNet50, WideResNet101, BERT, RoBERTa, XLM, CamemBERT, GPT-1/2/3, DLRM

### 主要结果

| 对比 | 平均迭代时间改善 | P99 尾部改善 | ECN 标记降低 |
|------|------------------|--------------|-------------|
| vs Themis | 1.4× | 1.5× | — |
| vs Themis (dynamic) | 1.5× | 2.2× | — |
| vs Pollux (dynamic) | 1.6× | 2.5× | — |
| ECN 标记 (DLRM) | — | — | 33× |
| ECN 标记 (GPT-2, model parallel) | — | — | 29× |

### 部分兼容性
- Score ≥ 0.8 时收益显著
- Score = 0.6 时收益开始衰减
- CASSINI 会避免将低兼容性 job 放在同一条链路

## 不同并行策略的流量模式

| 并行方式 | 通信特征 |
|----------|----------|
| Data parallel | Fwd 近零 → Backprop+AllReduce 高峰（1 Up/Down） |
| Pipeline parallel | Fwd 多小峰（minibatch activation）→ AllReduce 大峰 |
| Tensor parallel | Fwd + Backprop 各约 25 Gbps → 数据加载近零 |
| Hybrid | 多个 Up/Down 相位（GPT-3 hybrid = 6 个） |

## 与 AI 基础设施的关联

- **[Switching Networks](/concepts/switching-networks.md) 的实际应用**：CASSINI 在多级交换网络上做流量感知调度，是 CLOS 网络流量工程的具体案例
- **[Deterministic Execution](/concepts/deterministic-execution.md)**：CASSINI 利用 DNN 训练的确定性/周期性通信模式 → 类似 [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) 利用确定性执行做精确调度
- **[Disaggregated Inference](/concepts/disaggregated-inference.md)**：AFD 中 token routing 的 dispatch/combine 也有周期性通信模式 → CASSINI 的交错思想可应用于 disaggregated inference 的流量调度
- **Scale-up fabric 流量工程**：NVLink/C2C 网络中多 job 并存时的链路竞争问题 → CASSINI 的几何抽象提供了一种流量交错框架
- **部分兼容性阈值**：Score 0.6 以下收益衰减 → 对设计 scale-up 网络的 oversubscription 比例有参考价值

## 相关页面
- [Switching Networks](/concepts/switching-networks.md) — 交换网络拓扑基础
- [Deterministic Execution](/concepts/deterministic-execution.md) — 确定性执行（周期性通信模式）
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPX 确定性调度
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 解耦推理通信模式

# Citations

[1] [raw/papers/cassini-network-aware-scheduling-2308.00852.pdf](raw/papers/cassini-network-aware-scheduling-2308.00852.pdf)
