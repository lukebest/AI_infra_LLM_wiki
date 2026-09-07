---
type: Concept
title: NVLink NVSwitch Scale-Up Fabric
description: Hopper/Blackwell/Rubin NVLink + NVSwitch — 固定 fat-tree；NVLink 6 3.6 TB/s all-to-all；与 TPU v4 OCS 对照
tags:
- nvlink
- nvswitch
- nvidia
- scale-up
- fat-tree
- hopper
- blackwell
- gpu
timestamp: '2026-08-31T00:00:00Z'
created: 2026-07-22
updated: 2026-09-07
sources:
- raw/articles/paper-deepdive-day-08.md
- raw/papers/hc2026-nvidia-rubin.md
- raw/papers/Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf
- raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf
- raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf
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
| **Rubin NVLink 6**（HC2026） | **3.6 TB/s per GPU all-to-all** | 72 GPU；Counted Write；130 TFLOPS in-network |
| NVSwitch Gen4（笔记） | 高基数 ASIC（数百 port 级） | Clos/fat-tree 中枢 |

工艺：H100 ~80B 管；B200 笔记称 ~208B（双 die 等）。实体延伸：[Nvidia Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md)、[Kyber Rack](/entities/kyber-rack.md)。

Hot Chips 2026：[Fusion 教程](/papers/hc2026-nvidia-riscv-nvlink-fusion.md) 给 NVL72 机柜几何（9×4 NVLink 6 switch，**28.8 TB/s**/tray，**900 GB/s** C2C，CHI）。[Rubin GPU](/papers/hc2026-nvidia-rubin.md) 补协议：**Counted Write** 替换 MEMBAR+atomic；相对 Ethernet **3×** 延迟、**10×** packet rate、**130 TFLOPS** in-network。同日对照 [Helios UALoE](/papers/hc2026-amd-helios-ualoe.md)（以太网 load-store，**1.8 TB/s/dir**）。[TPU 8](/papers/hc2026-google-tpu8.md) 仍走 OCS/Boardfly，不是 fat-tree。

[Photonic Prefill](/papers/scaling-inference-prefill-photonic.md)（arXiv:2609.01821）把电学 **72-GPU** 铜域当作 MoE prefill 的硬边界：跨 rack 后走慢 scale-out，光学配对给出 **4×** SU 带宽与最大 **1152** GPU 全光 pod；B300 FP4 上 128K@288 ~**2.9×**、生产平台跨边界 **2.2–4.5×**（分析模型，非实测光子）。

[Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md)（Cornell, arXiv:2608.22503）指出第二条趋势和第一条打架：集体墙钟里有一段 **与 B 无关** 的 barrier 等待 τ。8-GPU 域可占通信时间 >50%；EVT 下最优带宽随域规模 **下降**（512 vs 8 GPU 为 2.06× 更低 B*）。论文 Table 1 口径 NVLink GB/s/GPU：A100 300 / H100·H200 450 / B200 900，域 8→72——与上表双向 ~900 GB/s（Hopper）不要混用。


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
- [Hot Chips 2026 Rubin GPU](/papers/hc2026-nvidia-rubin.md)
- [Hot Chips 2026 Helios UALoE](/papers/hc2026-amd-helios-ualoe.md)
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) — τ 征税，B* 随域规模下降


## 训练侧：把集体关在 NVLink 域

[BASP](/papers/basp-batch-aware-sequence-parallelism.md) 在 Ulysses 训练中按 micro-batch 建 SP 子组；当子组大小 = 每节点 GPU 数时，attention all-to-all 可不出节点，避开 IB。[Einsummable](/papers/einsummable-multi-gpu-parallelism.md) 默认假设单机 NVSwitch 非阻塞域做 intra-op 并行。片内更细一层：[CREDIT](/papers/credit-dsmem-inter-cta-tiling.md) 的 DSMEM 是 GPC 内 inter-SM，不是 NVLink。

# Citations

[1] [raw/articles/paper-deepdive-day-08.md](raw/articles/paper-deepdive-day-08.md) — Hopper/Blackwell NVLink 精读（Day 8）
[2] [raw/papers/hc2026-nvidia-rubin.md](raw/papers/hc2026-nvidia-rubin.md) — Rubin GPU / NVLink 6, Hot Chips 2026
[3] [raw/papers/Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf](raw/papers/Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf) — Devraj et al., arXiv:2608.22503；同步税 vs 带宽缩放
[4] [raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf](raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf) — Madhavan et al., arXiv:2609.01821；光学 1152 pod vs 电学 72
