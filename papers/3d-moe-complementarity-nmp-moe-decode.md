---
type: Paper
title: "3D-MoE: Complementarity-Guided Hardware-Software Co-Design for MoE Decode on 3D-Stacked NMP"
description: "中科院计算所/爱丁堡 — 利用专家负载跨 decode 步此消彼长的「互补性」做离线分组，3D 堆叠近存（NMP）逻辑 die 上加轻量 Collaborative Memory-Network 局部广播热专家权重；MoE 层比 EP 平均 4.63×，端到端比最强 NMP 基线 1.58–1.86×，面积 +2.11%"
tags:
- moe
- decode
- near-memory-processing
- pim
- 3d
- dram
- noc
- expert-parallelism
- load-balancing
- inference
- simulator
created: 2026-10-22
updated: 2026-10-22
timestamp: '2026-10-22T00:00:00Z'
paper_author: [Yudong Pan, Lian Liu, Shixin Zhao, Yintao He, Kaiyan Chang, Tianhua Han, Chenyang Ai, Haonan Zhu, Mengdi Wang, Yinhe Han, Ying Wang]
year: 2026
arxiv: '2610.26991'
sources:
  - raw/papers/3D_MoE_Complementarity_NMP_MoE_Decode_2026.pdf
  - raw/papers/3d-moe-complementarity-nmp-moe-decode.md
---

# 3D-MoE：用专家「互补性」解 3D 近存上的 MoE decode 负载均衡

## 一句话结论
MoE decode 的专家负载随步数剧烈波动，但不同领域偏好的专家之间呈反相波动。把这样的专家配成一组放在同一片 NMP 区域，组间先天平衡；组内残余热点交给逻辑 die 上一条可临时重配置的局部广播通路，热专家权重从所在 DRAM 通道只读一次就送到邻近帮手核。

## 动机
- MoE 层在 batch 64 时占端到端延迟 **83–92%**；最热专家某一步收到的 token 可超过步均值 **20×**，且随步数和层变化。
- 3D 堆叠 NMP（每个 DRAM 通道下挂一个计算核，核间走 NoC）本地访存便宜、远程搬运贵。EP 保留局部性但热点失衡；TP/工作窃取等分布式策略打散局部性，作者分析中 NoC 开销可达 **52%**。
- 热点预测类方法在先前工作中准确率低于 50%，难以提前搬权重。

## 方案
1. **专家互补性（expert complementarity）**：领域化路由让不同专家的逐步负载相互抵消。三个模型上 **82.2–88.3%** 的专家有互补伙伴，跨数据集保持 **70.6–80.5%**，256 步窗口内留存 **94.5% / 92.7% / 90.8%**。
2. **离线一次性分组 + 局部性映射**：以组内逐步负载极差为目标，把互补专家分组并映射到相邻核，建立组间粗粒度平衡。
3. **Collaborative Memory-Network（CMN）**：组内热专家由宿主通道流式读出权重 tile，经临时重配置的局部广播路径一次送到多个帮手核，跨核其他通信仍走常规 NoC。
4. **代价感知在线重映射**：三级调整（组内再分配 / 组内迁移 / 跨组交换），EMA 触发；暴露的端到端开销 **0.87%**。

## 效果（论文数字，周期级模拟）
| 项目 | 结果 |
|---|---|
| 系统 | 4 个 NMP 栈（2×2），每栈 16 GB 8-hi、16 通道、16 核 4×4 mesh（512-bit 链路）；核 650 MHz、1.33 TFLOPS、本地 166.4 GB/s；栈间 128 GB/s/方向；xPU 0.99 PFLOPS |
| 模型 / 负载 | DeepSeek-V2-Lite、Qwen3-30B-A3B、GLM-4.5-Air；ShareGPT、MATH、HumanEval |
| MoE 层 decode 加速 | 对 GPU / EP / HD-MoE 平均 **5.87× / 4.63× / 1.72×**；算力利用率平均 **83%** |
| 端到端吞吐 | 比最强 NMP 基线 **1.58–1.86×**；比 H100 GPU（vLLM 0.8.1）**5.54× / 7.88× / 6.95×** |
| 尾延迟 | DeepSeek-V2-Lite batch 64，p50/p90/p99 TBT 比 HD-MoE 降 **45.3% / 43.7% / 26.0%** |
| 面积 | 逻辑 die **+2.11%** |

## 与 wiki 的关系
- [HDA-MoE](/papers/hda-moe-3d-nmp-hybrid-parallel.md) — 同一类 3D NMP 上 MoE 并行放置；3D-MoE 把 HD-MoE 作为最强基线之一，差异在于用互补性分组替代全局 TP 摊热点
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 通道-核瓦片组织带来的本地/远程代价不对称
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — CMN 属于 NoC 内建局部广播的轻量实例
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md)、[DuoPD](/papers/duopd-hybrid-gpu-pnm-pd-disaggregation.md) — 同期 3D 近存 decode 路线
- [M2N Communication](/concepts/m2n-communication.md) — 专家 dispatch/gather 流量

## 开放问题
- 互补性依赖领域化路由；路由更均匀（强辅助损失或共享专家吸收共性）的模型上增益会缩小，论文对多专家模型已观察到共享专家削弱效应。
- 评测模型最大到 GLM-4.5-Air（106B），DeepSeek-V3 级 256 专家、跨多栈多设备时分组求解规模与收益待验证。
- CMN 需要改 NoC 链路做临时广播模式，对现有 HBM 逻辑 die 的可定制程度有要求。

# Citations
- [arXiv:2610.26991](https://arxiv.org/abs/2610.26991) — Pan et al., 2026
- [raw/papers/3d-moe-complementarity-nmp-moe-decode.md](/raw/papers/3d-moe-complementarity-nmp-moe-decode.md)
