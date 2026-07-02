---
type: Concept
title: Multi-plane Clos Topology for AI Training
description: 多平面 CLOS 拓扑：2-tier 131K GPU，低延迟高冗余，MRC 容错，Z3 形式化分析，bitwise reproducibility
tags:
- scale-up
- fabric
- topology
- switch
- infrastructure
- networking
timestamp: '2026-05-13T00:00:00Z'
created: 2026-05-13
sources:
- raw/articles/resilient-ai-supercomputer-networking-using-mrc-and-srv6.pdf
- raw/articles/resilient-ai-supercomputer-networking-mrc-srv6.md
---

# Multi-plane Clos Topology for AI Training

## 定义

将高带宽 NIC（如 800 Gb/s）按 lane 拆分为多条低速链路（8×100 Gb/s 或 4×200 Gb/s），构建多个并行的 Clos 平面，从而在 100K+ GPU 规模下实现两层拓扑。与 [Mrc](/entities/mrc.md) 和 [Srv6 Source Routing](/concepts/srv6-source-routing.md) 协同设计。

## 拓扑对比

### 传统 3-tier 800 Gb/s 单平面
- T0: 32 NIC + 32 上行 → 1K NIC/pod
- T2: 64 pod → 64K NIC（不足 100K）
- 需要 4 层、oversubscribe 或多 rail
- 最长路径 5-7 跳

### Multi-plane 2-tier (8×100 Gb/s)
- 同样 51.2Tb/s 交换机 → 512 端口 @ 100 Gb/s
- T0: 256 NIC 下行 + 256 T1 上行
- T1: 512 T0 → **131K GPU**
- 最长路径仅 3 跳

## 优势

| 维度 | Multi-plane | 传统 3-tier |
|------|-------------|-------------|
| 规模 | 131K GPU (2-tier) | 64K GPU (3-tier) |
| 跳数 | 3 | 5-7 |
| 一跳可达节点 | 256 | 32 |
| 光模块数量 | 2/3 | 1× |
| 交换机数量 | 3/5 | 1× |
| T0-T1 link loss 影响 | 0.4% | 3% |
| NIC-T0 link 可生存 | ✅ (降 12% 带宽) | ❌ |

## 挑战与解决

1. **NIC 端口故障**：[Mrc](/entities/mrc.md) 自动重映射 EV 到其他平面
2. **平面间负载均衡**：[Mrc](/entities/mrc.md) 的 EV set 等分到各平面，ECN 反馈微调
3. **Incast 拥塞**：MRC packet trimming + 禁用 PFC

## 部署实例

| 集群 | 配置 | 规模 |
|------|------|------|
| Cluster A (OpenAI) | 4×200 Gb/s, NVIDIA CX8, SP4+BRCM TH5 | 75K GPU |
| Cluster B | 8×100 Gb/s, NVIDIA CX8, Spectrum 5 | — |
| Cluster C (AMD) | 4×100 Gb/s, AMD Pollara, TH5 | 64 GPU (testbed) |

## 关系

- 拓扑基础与 [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md)、[Switching Networks](/concepts/switching-networks.md) 中的 CLOS 理论一致
- 与 [Nvidia Vera Rubin Nvl72](/entities/nvidia-vera-rubin-nvl72.md) 的 NVLink 拓扑不同层面（scale-out vs scale-up）
- [Cerebras Wse](/entities/cerebras-wse.md) 的 2D Mesh 是另一种拓扑选择
- 对比 [Csa Hca](/concepts/csa-hca.md) 中的注意力压缩，这里优化的是通信基础设施

# Citations

[1] [raw/articles/resilient-ai-supercomputer-networking-using-mrc-and-srv6.pdf](raw/articles/resilient-ai-supercomputer-networking-using-mrc-and-srv6.pdf)
[2] [raw/articles/resilient-ai-supercomputer-networking-mrc-srv6.md](raw/articles/resilient-ai-supercomputer-networking-mrc-srv6.md)
