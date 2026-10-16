---
type: Paper
title: "FastEEP: Fast Intra-Instance Elastic EP for MoE Serving"
description: "SJTU IPADS — MoE 实例内改 EP 度：复用 worker/通信/CUDA Graph，地址稳定卸页；相对 vLLM Elastic EP 伸缩 4.5–11.7×（几何均值 7.0×），4.2–13.4 s 完成"
tags:
- moe
- expert-parallelism
- serving
- inference
- gpu
- nvidia
- distributed
- serving-system
created: 2026-10-16
updated: 2026-10-16
timestamp: '2026-10-16T00:00:00Z'
paper_author: [Yunfei Feng, Jingkai He, Shiqi Liu, Cheng Zhang, Dong Du, Erhu Feng]
year: 2026
arxiv: '2610.18451'
sources:
  - raw/papers/FastEEP_Intra_Instance_Elastic_EP_MoE_Serving_2026.pdf
  - raw/papers/fasteep-intra-instance-elastic-ep-moe-serving.md
---

# FastEEP：MoE 实例内弹性 EP 伸缩

## 一句话结论
宽 EP 省权重复制、却让「整实例」伸缩粒度过粗。FastEEP 在已初始化的最大拓扑内做 **intra-instance** EP 缩放：父 NCCL + 活跃子组、NIXL 掩码、CUDA VMM 保虚址卸物理页、shadow worker 休眠，避免拆进程、重建通信与重捕 Graph。

## 动机（论文数字）
- 拉起 DeepSeek-V2-Lite 一个 rank（DP=EP=8）到稳态要 **126 s**；稳态 runtime 状态 **10.90 GiB**，超过该 rank 上模型权重 **9.62 GiB**。
- vLLM Elastic EP 闭环 8→4→8：缩容 **47 s**、扩容 **75 s**，服务不可用 **31 s / 44 s**；整进程重启 downtime **141 / 149 s**。
- BurstGPT 等轨迹显示需求波动远快于「整实例」重建。

## 方案
| 挑战 | 做法 |
|---|---|
| 通信组不可变 | 最大世界父 NCCL；每次 resize `split` 出活跃子组；NIXL 掩码藏 inactive rank |
| 卸内存毁上下文 | CuMem 池保虚址；权重/KV/Graph buffer 卸页后按语义回填；Graph 不重捕 |
| Worker 强耦合 | 先排空/迁请求与专家副本，再统一切换路由/放置/通信成员；shadow 跳过 forward |

## 效果（仅论文数字；vLLM 0.27 + 2×8 H20-3e）
- 六模型 × 六次 EP 转移：FastEEP **4.2–13.4 s**（FullAsync **3.2–9.8 s**）；vs Elastic EP **36.4–92.0 s** → **4.5–11.7×**（几何均值 **7.0×**）；vs restart 几何均值 **22.0×**。
- 负载下 8→4→8 零输出窗口：**4.2 s / 7.3 s**（Elastic EP 31/44；restart 141/149）。
- Qwen3-30B 相位：缩容合计 **4.21 s**（resize 2.81 s）；扩容 **7.15 s**（NIXL 恢复 2.50 s + resize 2.55 s）。
- 稳态吞吐与未改 vLLM 在 EP4/EP8 对齐；可把释放 GPU 交给同机另一服务而无实例重建。

## 与 wiki 的关系
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP all-to-all / DP 集体的成员变更路径
- [AFORE](/papers/afore-afd-expert-reconfiguration.md)、[RailWave](/papers/railwave-ep-rail-incast-scheduling.md) — 同属 MoE 服务侧弹性；FastEEP 动的是 EP 世界大小本身
- [NCCL M2N](/papers/nccl-m2n-layout-topology-aware-resharding.md) — 权重重分片集体；FastEEP 侧重服务实例生命周期

## 局限
- 只能在启动时最大拓扑内伸缩；更大拓扑变更仍要重建。
- 评测到 16 GPU；异步路径可能与推理争用带宽。

# Citations
- Feng et al., "FastEEP: Fast Intra-Instance Elastic Scaling for Expert-Parallel MoE Serving", arXiv:2610.18451. [raw](/raw/papers/fasteep-intra-instance-elastic-ep-moe-serving.md) · [PDF](/raw/papers/FastEEP_Intra_Instance_Elastic_EP_MoE_Serving_2026.pdf)
