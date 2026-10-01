---
type: Paper
title: "Mixture-of-Kittens: MoE Megakernel for NVL72s"
description: "Stanford/Cursor — NVL72 MoE 训练 megakernel；vs 最强公开基线最高 2.37×；512 GPU 生产 e2e 1.41×"
tags:
- architecture
- llm
- moe
- training
- training-system
- expert-parallelism
- collective
- gpu
- nvidia
- scale-up
- interconnect
- kernel
- throughput
- distributed
created: 2026-10-01
updated: 2026-10-01
timestamp: '2026-10-01T00:00:00Z'
paper_author: [Stuart H. Sul, Nash Brown, Henry Wildermuth, William Lin, Federico Cassano, Christopher Ré]
year: 2026
arxiv: '2609.36070'
sources:
  - raw/papers/MixtureOfKittens_MoE_Megakernel_NVL72_2026.pdf
  - raw/papers/mixture-of-kittens-moe-megakernel-nvl72.md
---

# Mixture-of-Kittens: NVL72 上的 MoE 训练 Megakernel

## 一句话结论

面向 **Nvidia NVL72** 单跳高带宽 scale-up 域，把 token dispatch / shared+routed expert FFN / combine 融成确定性 **megakernel**；相对最强公开基线吞吐最高 **2.37×**（MXFP8 forward），生产栈 **512 GPU / 多 GB300 NVL72** 端到端训练吞吐 **1.41×**。

## 动机

- 加速器向 **scale-up**（NVL72→144/576/1152）收敛：域内像大内存，不再像 scale-out 网络；为 RoCE/IB 优化的 MoE 系统迁到 NVL72 时常 **慢于** 朴素 PyTorch+NCCL。
- MoE 在大训中占一半以上时间，但既有重叠/调度假设在单跳胖互联上失效（文中约半数配置下朴素基线反超）。

对照 [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)、[NVLink/NVSwitch](/concepts/nvlink-nvswitch-scale-up-fabric.md)、[Weave](/papers/weave-dynamic-sm-moe-overlap.md)、[FlashMoE](/concepts/flashmoe-kernel.md)。

## 方案

1. **按算子选 push/pull**：scale-up 上 pull 与 push 同级；pull dispatch + push combine 等组合把信令开销压到 **<1%**，调度开销最高 **2.2×** 更小，并共享一张调度表。
2. **可调重叠粒度**：吞吐最优 minibatch 约 **512–32,768** tokens；相对固定劣粒度最高 **3.53×**。
3. **消除 CPU–GPU 同步**：NVL72 集成 CPU 上常见 PyTorch 主机路径最高 **2.97×** 更慢；设备侧定长 **ring buffer** + 反向 replay，相对过度分配平均仅 **+1.7%** 延迟。
4. **生产特性**：确定性、FSDP RDMA 重叠、MXFP8 融合量化、router 梯度融合、可调 SM 分区。评测形状：Kimi K2.7 / GLM 5.2 / Qwen3.5-397B-A17B / DeepSeek V4 Pro。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| vs 最强公开基线（MXFP8 fwd / bwd） | 最高 **2.37×** / **1.78×** |
| vs 最强公开基线（BF16 fwd / bwd） | 最高 **1.92×** / **1.58×** |
| 生产 e2e（512 GPU，多 NVL72，tok/s/GPU） | **1.41×**（相对 DeepEP 前代） |
| 调度开销 vs Comet 类 | **1.4–2.2×** 更小；占 MoE runtime **2.1–7.7%** |

## 与 wiki 的关系

- [NVLink/NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — NVL72 域内 EP 通信代价重写
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — MoE All-to-All / megakernel 重叠轴
- [Weave](/papers/weave-dynamic-sm-moe-overlap.md) / [FlashMoE](/concepts/flashmoe-kernel.md) — 同类 SM 分区与单核融合；本文专攻 **NVL72 训练**

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.36070) — Sul et al., arXiv:2609.36070
[2] [raw stub](raw/papers/mixture-of-kittens-moe-megakernel-nvl72.md)
