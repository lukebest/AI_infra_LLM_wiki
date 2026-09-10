---
type: Raw Source
title: "HDA-MoE: Hybrid Parallelism and Dynamic, Adaptive Scheduling for Mixture-of-Experts with 3D Near-Memory Processing"
source_url: https://arxiv.org/abs/2609.08682
arxiv: '2609.08682'
ingested: 2026-09-10
sha256: 9c05bc5a93ed52afa52769d118cac57d146d9f09a7720273a6470188b2a6feef
---

# HDA-MoE: Hybrid Parallelism and Dynamic, Adaptive Scheduling for Mixture-of-Experts with 3D Near-Memory Processing

**Authors:** Haochen Huang, Shuzhang Zhong, Shengxuan Qiu, Zhe Zhang, Shuangchen Li, Cong Li, Dimin Niu, Hongzhong Zheng, Guangyu Sun, Runsheng Wang, Meng Li
**Affiliation:** Peking University；Alibaba DAMO Academy
**PDF:** [HDA_MoE_3D_NMP_Hybrid_Parallel_2026.pdf](HDA_MoE_3D_NMP_Hybrid_Parallel_2026.pdf)
**arXiv:** [2609.08682](https://arxiv.org/abs/2609.08682)（2026-09-09，cs.AR；HD-MoE 期刊扩展）

## 问题

3D NMP（hybrid bonding 垂直叠 DRAM+compute）带宽高，但分布式 bank 上纯 TP 通信重、纯 EP 负载不均；MoE 动态路由让静态映射不够。

## 方法要点

- 离线：Node Balance LP + Link Balance BO 的 hybrid TP–EP 放置。
- 在线：pre-broadcast 热专家、Node Balance、hardware-aware gating（rcomp/rcomm）。
- NoC 抽象：Mesh XY / Torus / Fat-tree；离散事件 NoC + 端到端仿真。

## 摘录数字（仅论文给出）

- vs TP **1.1×–3.4×**；vs EP **1.1×–1.5×**；vs compute-balanced Hybrid TP-EP **1.1×–3.7×**；vs HD-MoE **1.1×–1.3×**。
- 模型：Mixtral-8x7B、DeepSeek-V2-Lite、Qwen2-57B-A14B、Qwen3.5-35B-A3B。
- 算力/带宽点：2.5 TFLOPS/75 GB/s、5/50、10/25；节点内存带宽 625 GB/s。
- Node Balance  alone：相对 TP/EP **1.0×–3.0×**，相对 compute-balanced hybrid **1.5×**；EP compute tail **2.0×** 降；Link Balance 平均通信延迟 **1.2×** 降。
- Pre-broadcast 2/5 专家平均 **1.15×** / **1.25×**。
