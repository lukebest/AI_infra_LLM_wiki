---
type: Paper
title: "Die Scaling 如何破坏 GPU 细粒度调度"
description: "上交/NUS/NVIDIA — floorsweep 拓扑 + HBM/L2 NUMA；不对称感知调度 kernel 最高 1.22×、多路 LLM decode +14.3%。"
tags:
- architecture
- gpu
- nvidia
- inference
- llm
- scheduling
- memory
- chiplet
- throughput
- cache
created: 2026-09-23
updated: 2026-09-23
timestamp: '2026-09-23T00:00:00Z'
paper_author: [Xiaoze Fan, Jianhao Wang, Weihao Cui, Han Zhao, Zhuobin Huang, Yangjie Zhou, Yuxian Qiu, Shixuan Sun, Bingsheng He, Quan Chen, Minyi Guo]
year: 2026
arxiv: '2609.24270'
sources:
  - raw/papers/Die_Scaling_GPU_Fine_Grained_Scheduling_2026.pdf
  - raw/papers/die-scaling-gpu-fine-grained-scheduling.md
---

# Die Scaling 如何破坏 GPU 细粒度调度

## 一句话结论

现代 GPU 因 die scaling 出现 **floorsweep 拓扑不对称** 与 **cache/HBM NUMA**；逻辑 SM/内存抽象会遮住这件事。轻量刻画物理亲和后做拓扑感知调度，主流 kernel 最高 **1.22×**，多路 LLM 推理 decode 最高 **+14.3%**，并规避最高 **1.33×** 的分配波动。

## 动机

H200/B200 等已不再物理对称：制造 floorsweep 让各片 CU 拓扑不同；分区缓存与 HBM 使远端访问变贵。细粒度调度若只决定“分多少 CU”，同一逻辑配置可差到 **1.33×**。

## 方案

1. 轻量方法发现每芯片的 compute topology 与 memory affinity。
2. 调度同时选择 **数量** 与 **物理位置**（拓扑感知 SM + 自适应 NUMA）。
3. 覆盖全 GPU kernel、应用内多路复用、应用间共置；含 LLM prefill/decode 重叠。

## 量化结果

- **远端代价**：HBM 延迟 H200 ~**+34%**、B200 ~**+67%**；L2 H200 ~**+51%**、B200 近 **2×**。
- **波动**：拓扑无关分配最高 **1.33×**（文中 B200 cluster size 8）。
- **收益**：主流 kernel 最高 **1.22×**；多路 LLM decode 相对 CA Overlap 最高 **+14.3%**。

## 局限与解读

聚焦调度层暴露物理不对称，不改 ISA/编译器；与 [GPU SIMT Architecture](../concepts/gpu-simt-architecture.md)、[Hopper Utilization](dissecting-gpu-utilization-llm-inference-hopper.md) 同属“逻辑利用率 vs 物理资源”叙事——前者测 SM/GMMA fill，本篇测 die 内 NUMA/floorsweep。

# Citations

1. Fan et al. “Dissecting How Die Scaling Breaks GPU Fine-grained Scheduling.” arXiv:2609.24270, 2026. [arXiv](https://arxiv.org/abs/2609.24270)
2. [本地原文 PDF](../raw/papers/Die_Scaling_GPU_Fine_Grained_Scheduling_2026.pdf)；[原始来源记录](../raw/papers/die-scaling-gpu-fine-grained-scheduling.md)
