---
type: Paper
title: "Embodied Emissions of 2.5D and 3D Scaling in Chipletized GPUs for Low-Carbon AI"
description: "imec 短文 — 以 MI300X 式 chiplet GPU 为基线，算力与 HBM 容量翻倍：2.5D 摊大封装隐含碳 +141%，3D（XCD 叠 XCD + 16-Hi HBM）+89%；2.5D 训练仿真只快 6.8–13.5%"
tags:
- chiplet
- 3d
- hybrid-bonding
- tsv
- packaging
- hbm
- gpu
- carbon
created: 2026-10-27
updated: 2026-10-27
timestamp: '2026-10-27T00:00:00Z'
paper_author: [Hannah Watson, Arjun Singh, Jennifer Stephenson, Job Soethoudt, J. Svedas, Debjyoti Bhattacharjee, James Myers]
year: 2026
venue: arXiv cs.AR (short paper)
arxiv: '2610.32830'
sources:
  - raw/papers/Embodied_Emissions_2p5D_3D_Chiplet_GPU_2026.pdf
  - raw/papers/embodied-emissions-2p5d-3d-chiplet-gpu.md
---

# 2.5D 与 3D 扩展 chiplet GPU 的隐含碳排放

## 一句话结论
GPU 下一代要把计算 die 和 HBM 容量翻倍时，往上叠（3D）比往外铺（2.5D）制造碳排放少得多：3D 增加 89%，2.5D 增加 141%。差距主要来自 2.5D 需要两倍 IO die、更大的硅中介层和更多子封装，良率在每一级都被放大。

## 动机
- 数据中心容量预计到 2030 年接近三倍、其中 70% 来自 AI；GPU 的制造（隐含）排放随设计复杂度上升，封装方案是设计期就能决定的变量。

## 方案（建模设定）
- 工具：imec.netzero 自底向上虚拟晶圆厂模型；Murphy 良率模型、0.1 defects/cm²，逻辑 die 关键面积 100%、无源中介层 15%；每 die/子封装贴装良率 99%。
- 基线（仿 AMD MI300X）：无源硅中介层；4 个 IOD（5 nm，带 TSV，micro-bump）；8 个 XCD 以 hybrid bonding 叠在 IOD 上；8 叠 12-Hi HBM3。基线隐含碳中 DRAM die 占 53.2%，逻辑 die 占 28%。
- 2.5D 扩展：封装面积 +100%（约 7 倍光罩），16 XCD / 8 IOD / 16 叠 12-Hi HBM3。
- 3D 扩展：在原 XCD 上再 hybrid-bond 8 个 XCD，12 叠 16-Hi HBM（对齐 HBM4），封装 +25%（约 4 倍光罩）。

## 效果（论文数字）
| 指标 | 基线 | 2.5D 扩展 | 3D 扩展 |
|---|---|---|---|
| 中介层 die 良率 | 64.9% | 43.5% | 58.5% |
| IOD-XCD 子封装良率 | 97.0% | 97.0% | 95.1% |
| HBM 子封装良率 | 87.8% | 87.8% | 84.3% |
| GPU 封装组装良率 | 88.6% | 78.6% | 85.1% |
| 隐含碳（相对基线） | 1× | **+141%** | **+88.5%（≈89%）** |

- 2.5D 比 3D 隐含碳高 28%；最终组装损失对 3D 加 18%、对 2.5D 加 27%；2.5D 中介层大 60%，计良率后中介层隐含碳高 168%。
- 性能（Hespas 训练仿真，等 FLOPs、等 HBM 容量）：2.5D HBM 带宽更高，但 8 个 IOD 分成两组交换互连，3D 的 4 个 IOD 全互连；2.5D 只快 **6.8–13.5%**。

## 与 wiki 的关系
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — hybrid bonding 计算叠计算 + TSV/micro-bump HBM 的组合，在碳维度给出量化论据
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 3D 扩展路线的另一项评价指标（隐含碳）
- [TSV 3D Physical Layer](/concepts/tsv-3d-physical-layer.md) — 组装良率损失来自 TSV 制造与对准失败
- [Token-Energy Law](/papers/token-energy-law-llm-decode.md) — 运行期能耗模型；本篇补制造期一侧

## 开放问题
- 未计入光罩拼接、翘曲、16-Hi 额外减薄带来的良率损失，这些恰好更伤 3D 与超大中介层，结论的幅度会变。
- 没有算运行期排放与散热：3D 叠计算的热密度可能限制频率或增加冷却能耗，作者也把热管理列为 3D 的潜在瓶颈。
- 性能侧只用两组 IOD 分组拓扑的简化模型，2.5D 若用更好的片间网络，性能差距可能扩大。

# Citations
- [arXiv:2610.32830](https://arxiv.org/abs/2610.32830) — Watson et al. (imec), 2026
- [raw stub](/raw/papers/embodied-emissions-2p5d-3d-chiplet-gpu.md)
