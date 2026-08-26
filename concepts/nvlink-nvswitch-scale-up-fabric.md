---
type: Concept
title: NVLink NVSwitch Scale-Up Fabric
description: Hopper/Blackwell NVLink + NVSwitch — 固定 fat-tree、极高每链路带宽、NVL72；与 TPU v4 OCS 可重构哲学对照
tags:
- nvlink
- nvswitch
- nvidia
- scale-up
- fat-tree
- hopper
- blackwell
- gpu
timestamp: '2026-08-26T00:00:00Z'
created: 2026-07-22
updated: 2026-08-26
sources:
- raw/articles/paper-deepdive-day-08.md
---

# NVLink / NVSwitch Scale-Up Fabric

NVIDIA Hopper / Blackwell 白皮书与 GTC 材料。paper-deepdive **Day 8**：[raw/articles/paper-deepdive-day-08.md](raw/articles/paper-deepdive-day-08.md)。摘要：[papers/nvidia-nvlink-hopper-blackwell.md](/papers/nvidia-nvlink-hopper-blackwell.md)。

哲学（相对 [TPU v4 OCS](/concepts/tpu-v4-ocs-reconfigurable-fabric.md)）：**Topology is fixed (fat-tree)；把每链路带宽做胖**，使运行时换拓扑不必要。

## 关键数字（白皮书/笔记）

| 代际 | 每 GPU NVLink 双向带宽 | 备注 |
|------|------------------------|------|
| Hopper NVLink 4 | **~900 GB/s** | H100 |
| Blackwell NVLink 5 | **~1.8 TB/s** | 2× Hopper |
| NVL72 | **72 GPU** 单域 | ~18 NVSwitch tray；聚合带宽笔记称 ~130 TB/s/rack 量级 |
| NVSwitch Gen4（笔记） | 高基数 ASIC（数百 port 级） | Clos/fat-tree 中枢 |

工艺：H100 ~80B 管；B200 笔记称 ~208B（双 die 等）。实体延伸：[Nvidia Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md)、[Kyber Rack](/entities/kyber-rack.md)。

Hot Chips 2026（[NVIDIA RISC-V / NVLink Fusion](/papers/hc2026-nvidia-riscv-nvlink-fusion.md)）：Vera Rubin NVL72 写成单 **72 GPU** 全铜 L1；**9** switch tray × **4** NVLink 6 switch = **36** switch；**28.8 TB/s per switch tray**；**3.6 TB/s per GPU**；**900 GB/s** CPU–GPU 经 NVLink-C2C；每 GPU 旁一颗 Fusion chiplet。Custom CPU 经 **CHI** 进 fabric。无新 HBM 数字。

## 两条 scale-up 哲学

| | **Google TPU v4** | **NVIDIA NVLink** |
|--|-------------------|-------------------|
| 拓扑 | OCS **可重构** | **固定** fat-tree |
| 每芯片链路 | 相对薄 | **极胖**（~6× ICI 叙事） |
| 域规模 | Pod **4096** chip | NVL72 **72** GPU |
| 交换 | 光电路（慢切换、低 pJ/bit） | 高基数 packet switch |
| 理论祖先 | Day 4/6「拓扑是旋钮」 | Day 6 high-radix Clos 工业极致 |

## 与 NoC 经典的连接

- Fat-tree / Clos：[Clos and Fat-Tree](/concepts/clos-fat-tree-topology.md)、[High-Radix Clos Adaptive Routing](/concepts/high-radix-clos-adaptive-routing.md)  
- VC + credit：[Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md)  
- 集体通信直径 O(log N) vs Mesh O(√N)：[LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)  

WSE 路径第三极：单晶圆 Mesh，无 NVSwitch/OCS——见 [Cerebras WSE](/entities/cerebras-wse.md)。

## 相关页面

- [TPU v4 OCS Reconfigurable Fabric](/concepts/tpu-v4-ocs-reconfigurable-fabric.md)
- [Nvidia Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md)
- [UnifiedBus UB](/entities/unifiedbus-ub.md) — 另一 scale-up 协议栈
- [Multi-plane Clos Topology for AI Training](/concepts/multi-plane-clos-topology.md)
- [Paper Deep-Dive Map](/summaries/paper-deepdive.md)
- [Hot Chips 2026 NVIDIA Fusion](/papers/hc2026-nvidia-riscv-nvlink-fusion.md)

# Citations

[1] [raw/articles/paper-deepdive-day-08.md](raw/articles/paper-deepdive-day-08.md) — Hopper/Blackwell NVLink 精读（Day 8）
