---
type: Paper
title: "HDA-MoE: Hybrid Parallelism for MoE on 3D Near-Memory Processing"
description: 北大/阿里 DAMO — 3D NMP 上离线 hybrid 放置 + 在线自适应调度；vs TP 1.1–3.4×、vs HD-MoE 1.1–1.3×（仿真）
tags:
- moe
- inference
- 3d
- hybrid-bonding
- noc
- mesh
- scheduling
- expert-parallelism
- llm
- memory
- interconnect
- accelerator
- architecture
- parallelism
timestamp: '2026-09-10T00:00:00Z'
created: 2026-09-10
updated: 2026-09-10
sources:
- raw/papers/HDA_MoE_3D_NMP_Hybrid_Parallel_2026.pdf
- raw/papers/hda-moe-3d-nmp-hybrid-parallel.md
---

# HDA-MoE: Hybrid Parallelism and Dynamic, Adaptive Scheduling for Mixture-of-Experts with 3D Near-Memory Processing

**Authors:** Haochen Huang, Shuzhang Zhong, Shengxuan Qiu, Zhe Zhang, Shuangchen Li, Cong Li, Dimin Niu, Hongzhong Zheng, Guangyu Sun, Runsheng Wang, Meng Li
**Affiliation:** Peking University；Alibaba DAMO Academy
**arXiv:** [2609.08682](https://arxiv.org/abs/2609.08682)（2026-09-09，cs.AR）
**Venue:** 预印本；文称基于 HD-MoE 的期刊扩展（系统建模 / 精度 / 可扩展性）。
**PDF:** [raw/papers/HDA_MoE_3D_NMP_Hybrid_Parallel_2026.pdf](raw/papers/HDA_MoE_3D_NMP_Hybrid_Parallel_2026.pdf)

相对 [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) 的异构存算+树 NoC，本文把 **3D NMP bank 阵列** 当部署目标，主旋钮是 **hybrid TP–EP 放置 + 运行时调度**。相对 [DynaNDE](/papers/dynande-near-data-expert-scheduling.md) 的 NPU–NDP 调度，本文显式建 NoC 链路占用与 Mesh/Torus/Fat-tree 抽象。

## 动机

MoE 省算力但抬内存容量/带宽。3D NMP（DRAM 与 compute **hybrid bonding** 垂直叠）内部带宽高、能效好，可是：

- **TP**：专家切分跨 bank → AllReduce / 同步通信重。
- **EP**：整专家落单 bank → 路由偏斜时算力空转。
- 动态 top-k 路由让静态映射不够；GPU 集群那套「专家复制」在内存紧的 NMP 上不划算。

## 方案

**离线 hybrid 映射。** Node Balance（LP）按计算负载把专家（可分数）放到节点；Link Balance（贝叶斯优化）按共激活/流量压链路拥塞。支持把专家再切到多个节点（hybrid TP–EP）。

**在线动态调度。**

1. **Pre-broadcast**：把预估热专家提前推到低负载节点。
2. **Node Balance（runtime）**：按当前 batch 负载迁移/重绑。
3. **Hardware-aware gating**：在 gating 分数上加 \(r_{comp} T_{comp}+r_{comm} T_{comm}\)，允许非 Top-1 替换以换通信/负载（文测精度影响）。

**建模与仿真。** 离散事件 NoC（Mesh XY、Torus、4-pod Fat-tree）+ 端到端 MoE 层仿真；通信延迟模型与 ASTRA-sim 对照（Table I，\(R^2\) 文称超过阈值阈值）。算力/带宽扫描：2.5 TFLOPS/75 GB/s、5/50、10/25；每节点内存带宽 **625 GB/s**。

## 效果（仅论文数字）

**端到端（四模型：Mixtral-8x7B、DeepSeek-V2-Lite、Qwen2-57B-A14B、Qwen3.5-35B-A3B）**

| 对照 | 加速比 |
|------|--------|
| TP | **1.1×–3.4×** |
| EP | **1.1×–1.5×** |
| Hybrid TP-EP（compute-balanced） | **1.1×–3.7×** |
| HD-MoE | **1.1×–1.3×** |

**组件**

- Node Balance alone：vs TP/EP **1.0×–3.0×**，vs compute-balanced hybrid **1.5×**；EP compute tail 平均 **2.0×** 降。
- Link Balance：平均通信延迟 **1.2×** 降；在 Torus / Fat-tree 上仍优于基线。
- Pre-broadcast 2 / 5 专家：平均 **1.15×** / **1.25×**。
- 离线搜索：多数模型数小时内；Qwen2 因共激活组多，LP 可到数千秒量级（Table VI）。

## 与 wiki 概念的关系

- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — NMP 用 hybrid bonding 叠 DRAM+logic，是 HB 的近存算用例。
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 分布式 bank 上的专家异构放置。
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) / [Mesh Torus](/concepts/mesh-torus-topology.md) — Link Balance 跨 Mesh/Torus/Fat-tree。
- [LLM Collectives](/concepts/llm-distributed-training-collectives.md) — 推理侧 MoE 通信；本文压的是 NMP NoC 上的 AllReduce/dispatch，不是跨机 NCCL。

## 开放问题

1. 仿真 → 硅：真实 3D NMP 的 bank 带宽/热约束会不会改写 hybrid 最优区？
2. Hardware-aware gating 在长尾任务分布 / 多租户下的质量下限？
3. 与 [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) / [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) 的存内专家驻留路线如何拼？

# Related

- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md)
- [DynaNDE](/papers/dynande-near-data-expert-scheduling.md)
- [Mozart 3.5D](/papers/mozart-35d-wafer-scale-moe-training.md)
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md)

# Citations

[1] [raw/papers/HDA_MoE_3D_NMP_Hybrid_Parallel_2026.pdf](raw/papers/HDA_MoE_3D_NMP_Hybrid_Parallel_2026.pdf) — Huang et al., arXiv:2609.08682
[2] [raw/papers/hda-moe-3d-nmp-hybrid-parallel.md](raw/papers/hda-moe-3d-nmp-hybrid-parallel.md) — ingest stub
