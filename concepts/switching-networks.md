---
type: Concept
title: Switching Networks
description: 交换网络：CLOS 三级网络（严格/可重排无阻塞），TST 网络，Banyan 网络
tags:
- fabric
- topology
- routing
- scale-up
- deterministic
timestamp: '2026-05-08T00:00:00Z'
created: 2026-05-08
sources:
- raw/articles/浅谈交换原理（3）——交换网络.md
---

# Switching Networks（交换网络）

交换网络 = 若干交换单元按拓扑结构 + 控制方式组成。三要素：**交换单元、拓扑连接、控制方式**。

## 基本分类

### 单级 vs 多级
- **单级**：入线到出线只经过一个交换单元（或同级的多个交换单元间可互连）
- **多级（K 级）**：交换单元分 K 级串联，入线 → 第 1 级 → … → 第 K 级 → 出线

### 有阻塞 vs 无阻塞

**阻塞**：不同输入争抢同一公共资源（内部竞争或出线竞争）。

**无阻塞网络**三种类型：

| 类型 | 定义 |
|------|------|
| **严格无阻塞 (Strict)** | 任何时刻，只要起终点空闲就能建立连接，不影响已有连接 |
| **可重排无阻塞 (Rearrangeable)** | 任何时刻可建立连接（可能需要对已有连接重选路由） |
| **广义无阻塞 (Wide-sense)** | 存在固有阻塞可能，但存在精巧选路方法可避免所有阻塞 |

### 单通路 vs 多通路
- **单通路**：任一入线到任一出线仅一条路径
- **多通路**：存在多条可选路径（更高的容错和负载均衡）

## CLOS 网络

### 动机

N×N 全 crossbar 需 N² 个开关。用多级小 crossbar 组合可大幅减少开关数：
- 单级 NxN：N² 开关（100×100 = 10,000）
- 两级单通路：2×N×√N×√N = 2N√N（100×100 用 10×10 单元 = 2,000）
- 三级多通路（CLOS）：3×N×√N×√N = 3N√N（100×100 = 3,000）

用少量额外开关（+50%）换得多通路、低阻塞。

### 三级 CLOS 结构

用三元组 **(m, n, r)** 描述：

```
Input Stage          Middle Stage          Output Stage
r 个 n×m crossbar    m 个 r×r crossbar     r 个 m×n crossbar
┌───┐                ┌───┐                ┌───┐
│IS₁│ ────────────── │MS₁│ ────────────── │OS₁│
│   │ ────────────── │   │ ────────────── │   │
├───┤                ├───┤                ├────┤
│IS₂│ ────────────── │MS₂│ ────────────── │OS₂│
│   │ ────────────── │   │ ────────────── │   │
├───┤                ├───┤                ├────┤
│...│                │...│                │...│
└───┘                └───┘                └───┘
```

- **r** = input/output switch 数量
- **n** = 每个 input/output switch 的端口数
- **m** = middle switch 数量
- 每个 middle switch 连接所有 input 和 output switch（全连接）

### 无阻塞条件

| 条件 | 类型 |
|------|------|
| m ≥ 2n - 1 | **严格无阻塞** |
| m ≥ n | **可重排无阻塞** |

### 路由算法

CLOS 路由选择仅在 input switch（选哪个 middle switch）：

1. 如果有 middle switch 两端（a 和 b）均空闲 → 选择它
2. 如果无两端空闲的 middle switch → 选 a 端空闲的 middle switch，建立连接
3. 被"抢占"的 input switch c → 重新为 c→b 寻路
4. 迭代直到所有连接建立

## TST 网络

电话交换常用三级网络：**T-S-T**（Time-Space-Time）

```
T 接线器 (×32) → S 接线器 (32×32) → T 接线器 (×32)
```

- **第 1 级 T**：输出控制方式（32 个 T 接线器，每条 PCM 线一个）
- **第 2 级 S**：32×32 空分接线器（任何控制方式）
- **第 3 级 T**：输入控制方式
- 每 PCM 线 32 时隙，入出线编号相同组成双向复用线
- S 级出入线数 = 两侧 T 接线器数

**本质**：时分交换解决时隙变换，空分交换解决线路切换 → 组合实现任意时隙×线路的交换。

## Banyan 网络

自路由交换网络，广泛用于高性能计算和分布式系统。

### 特性
- **L 级 Banyan**：任何输入到输出通路都经过 L 级
- **规则 Banyan**：所有交换单元相同
- **矩形 Banyan**：每个交换单元入线数 = 出线数
- 拓扑类似二叉树，每节点 2 入 2 出

### 优势
- **低延迟**：节点间直连
- **高带宽**：多端口并行传输
- **可扩展**：增加节点和连接即可扩展
- **容错**：冗余路径提高可靠性

### 典型应用
超级计算机、数据中心、[Switching Networks](/concepts/switching-networks.md) 中的蝶形/胖树拓扑变体。

## 与 AI 基础设施的关联

- **CLOS 与 scale-up fabric**：NVIDIA NVL72/144 的 NVLink switch 网络本质是多级 CLOS——多级 crossbar switch 互联 GPU，用 radix 适当的 switch 组合替代超大单级 crossbar
- **[Kyber Rack](/entities/kyber-rack.md) 的两级 all-to-all**：NVL576 中 8 个 Oberon rack 通过 CPO 互联 → 中间级 = CPO switch，input/output 级 = rack 内 NVLink switch → 类似 CLOS 三级结构
- **严格无阻塞 vs 可重排无阻塞**：训练 workload 对 all-to-all 带宽有严格需求 → 倾向严格无阻塞；推理 workload 可能容忍可重排无阻塞（利用时间维度的 traffic reshaping）
- **TST 与 [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md)**：C2C 网络在时间维度的确定性调度 + 空间的 mesh 拓扑 → 类似 TST 的时分+空分组合思想
- **Banyan 与 NoC**：Cerebras WSE 的 2D mesh 路由、[Cerebras Wse](/entities/cerebras-wse.md) 的 24-color 路由与 Banyan 的自路由思想有关联

## 相关页面
- [Switching Principles](/concepts/switching-principles.md) — 交换原理概述
- [Switching Elements](/concepts/switching-elements.md) — 交换单元（S/T 接线器）
- [Kyber Rack](/entities/kyber-rack.md) — 多级 NVLink 交换网络
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — C2C 网络拓扑
- [Cerebras Wse](/entities/cerebras-wse.md) — WSE NoC 路由
- [Multi Plane Clos Topology](/concepts/multi-plane-clos-topology.md) — 100K+ GPU 的多平面 CLOS 实践
- [Mrc](/entities/mrc.md) — 配合 multi-plane CLOS 的多路径传输协议
- [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) — Flattened Butterfly 片上拓扑（高基数路由器降低直径）
- [Noc Router Microarchitecture](/concepts/noc-router-microarchitecture.md) — NoC Router 微架构（Router 是多级交换网络中的节点）

# Citations

[1] [raw/articles/浅谈交换原理（3）——交换网络.md](raw/articles/浅谈交换原理（3）——交换网络.md)
