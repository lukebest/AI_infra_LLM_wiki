---
type: Paper
title: "CAMP: Context-Aware Mapping and Placement for LLMs on 3D-IMC Arrays"
description: "IBM Research — 冲突矩阵 + profiling + 剪枝束搜索为 3D-IMC 映射权重；利用率 42.4%→60.3%；相对 SOTA mapping 最高 2.0× 3D-IMC 吞吐、1.74× E2E 吞吐"
tags:
- 3d
- cim
- imc
- aimc
- llm
- inference
- scheduling
- accelerator
- memory
- moe
- throughput
- optimization
- pim
- near-memory-processing
- serving
created: 2026-11-10
updated: 2026-11-10
timestamp: '2026-11-10T00:00:00Z'
paper_author: [Orhun Görkem, Athanasios Vasilopoulos, Georgios Pagonis, Victoria Clerico, Hadjer Benmeziane, Irem Boybat, Hsinyu Tsai, Abu Sebastian, William Andrew Simon]
year: 2026
venue: arXiv preprint
arxiv: '2611.07707'
sources:
  - raw/papers/CAMP_3D_IMC_Mapping_Placement_2026.pdf
  - raw/papers/camp-3d-imc-mapping-placement.md
---

# CAMP：面向 3D-IMC 阵列的上下文感知映射与放置

## 一句话结论
IBM Research 提出 **CAMP**：把系统架构、目标网络和运行时上下文编码成**冲突矩阵**，再用 profiling 反馈与剪枝束搜索平衡张量并行（TP）、批并行（BP）与专家并行（EP）。这是纯离线软件方案。3D-IMC 计算利用率从 **42.4%** 提到 **60.3%**；相对 Greedy-Util 等 SOTA mapping，3D-IMC 吞吐最高 **2.0×**（Qwen-72B），端到端吞吐摘要所称最高 **1.74×**。

## 动机
Decode 阶段加载权重大矩阵与 KV 会主导访存。模拟存内计算（AIMC）把静态权重留在阵列内做 MVM，省去权重搬运。3D-IMC 用垂直层堆高容量，同一阵列的多层**不能同时访问**，于是权重放置同时决定：单次 MVM 分到多少平面资源（TP）、不同 MVM/token 能否并发（BP）、MoE 专家如何分资源（EP）。既有算法（Greedy-Util、3D-aCortex）在上下文无关的前提下最大化 TP，牺牲 BP/EP 与跨上下文稳健性，3D-IMC 计算资源利用率偏低。

## 方案
1. **冲突矩阵**：profiling 阶段按架构（tile / tier / 拓扑 / attention 单元 / 片上或片外集成 / MVM 延迟）、网络（稠密 vs 稀疏 MoE）和运行时（期望 batch、序列长度）估计成对静态 MVM 的资源冲突概率。
2. **初始映射**：把冲突概率高的 MVM 放到不相交资源组，提升 BP/EP；初始给每个 MVM 1-way TP，占用更多垂直层，作为细化起点。
3. **Profiling 驱动的剪枝束搜索**：用冲突矩阵上的代理惩罚剪掉大片搜索空间，按投影延迟保留束宽 W 个状态；在可接受运行时间内接近穷举。束搜索在 400 次无改进后终止。
4. **仿真配置**（§5.1）：**512×512**、**320** 层 AIMC tile；容纳 Llama-3.1-70B / Mixtral-8×7B 需 **1,024** tile；单 tile MVM 延迟 **100 ns**；**64** 个 leaf group、每组 **4** leaf、**4** 条 H-tree 通道。评测模型含 Llama-3-8B / Llama-3-70B / Qwen-72B / Mixtral-8×7B。主基线为 Greedy-Util，并对照 3D-aCortex 与 Full-compute 理想上界。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 3D-IMC 计算利用率（摘要；Fig 1 均值约 42% / 60%） | **42.4% → 60.3%** |
| 3D-IMC 吞吐 vs Greedy-Util | Llama-3-8B **1.95×**、Llama-3-70B **1.91×**、Qwen-72B **2.0×**；Mixtral 平均 **1.71×**、最高 **1.84×** |
| 相对 SOTA mapping 的 E2E 吞吐（摘要） | 最高 **1.74×** |
| Fig 11：A100 attention + seq=128 | CAMP 相对 GPU 基线 **5.5×**（Greedy-Util **4.4×**） |
| Fig 11：综合策略 + seq=4096 | 相对 GPU 基线 **16.3×**（Greedy-Util **12.7×**） |

长上下文时 attention / KV 加载会主导端到端时间，单纯优化权重映射的收益下降；缩短序列、降低 KV 精度、更强 GPU，或把 3D-IMC 在多 GPU 间交错共享，能把 3D-IMC 侧加速更多地传到端到端。

## 与 wiki 的关系
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 垂直层不能并发访问，放置即并行度
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 权重驻留阵列、KV/attention 仍走另一条路径
- [LEAP: IMC-NoC LLM Inference](/papers/leap-imc-noc-llm-inference.md) — 另一条 IMC + NoC 推理数据流
- [3D-MoE](/papers/3d-moe-complementarity-nmp-moe-decode.md) — 3D 近存上的 MoE decode 分组对照
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 权重/KV 加载 vs prefill 算力

## 开放问题
- 结果来自系统级仿真（3D-IMC + GPU attention 单元），硅上端到端仍待验证。
- 摘要 1.74× E2E 为相对 SOTA mapping 的最高值；正文 Fig 11 给出若干具体配置（如 5.5× vs 4.4×、16.3× vs 12.7×），完整 sweep 见原文 Figure 11。
- 映射针对预期推理上下文离线生成；serving 中 batch/序列分布漂移时的重映射成本未展开。

# Citations
- [arXiv:2611.07707](https://arxiv.org/abs/2611.07707) — Görkem, Vasilopoulos, Pagonis, Clerico, Benmeziane, Boybat, Tsai, Sebastian, Simon；IBM Research
- [raw stub](/raw/papers/camp-3d-imc-mapping-placement.md)
