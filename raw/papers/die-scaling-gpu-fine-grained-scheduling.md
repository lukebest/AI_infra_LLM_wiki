---
type: Raw Source
title: "Dissecting How Die Scaling Breaks GPU Fine-grained Scheduling"
description: "上交/NUS/NVIDIA — die scaling 导致 floorsweep 拓扑与 NUMA；不对称感知调度最高 1.22×、多路 LLM decode +14.3%。"
timestamp: '2026-09-23T00:00:00Z'
source_url: https://arxiv.org/abs/2609.24270
arxiv: '2609.24270'
ingested: 2026-09-23
sha256: 1b468bc67c025f2226aed83c71e36bbbb63f374c9f3ceee1b3787ea3028a4249
---

# Die Scaling Breaks GPU Fine-grained Scheduling

**Authors:** Xiaoze Fan, Jianhao Wang, Weihao Cui, Han Zhao, Zhuobin Huang, Yangjie Zhou, Yuxian Qiu, Shixuan Sun, Bingsheng He, Quan Chen, Minyi Guo  
**Affiliation:** Shanghai Jiao Tong University; National University of Singapore; NVIDIA  
**PDF:** [Die_Scaling_GPU_Fine_Grained_Scheduling_2026.pdf](Die_Scaling_GPU_Fine_Grained_Scheduling_2026.pdf)  
**arXiv:** [2609.24270](https://arxiv.org/abs/2609.24270)（2026-09-21，cs.AR/cs.DC）

## 问题

现代 GPU 物理上不再对称：floorsweep 造成片间不同的 CU 拓扑；cache/HBM 分区带来 NUMA。逻辑资源抽象隐藏这些不对称，细粒度调度若只看“数量”会踩雷。

## 方法要点

- 轻量刻画每芯片的 compute topology 与 memory affinity。
- 调度同时决定 **分配多少** 与 **分配哪些物理资源**（拓扑感知 SM + 自适应 NUMA）。
- 评测覆盖 H200 / B200（GB100×2）等。

## 摘录数字（仅论文给出）

- 拓扑无关 CU 分配可致最高 **1.33×** 性能波动（B200 cluster size 8 上 1.33×）。
- 远端 HBM 延迟：H200 约 **+34%**（~490→~655 cycle）；B200 约 **+67%**（~552→~920）。
- 远端 L2：H200 约 **+51%**；B200 近 **2×**（~364→~725）。
- 不对称感知：主流 kernel 最高 **1.22×**；多路 LLM 推理 decode 最高 **+14.3%**。

**Working page:** [Die Scaling GPU Scheduling](/papers/die-scaling-gpu-fine-grained-scheduling.md)
