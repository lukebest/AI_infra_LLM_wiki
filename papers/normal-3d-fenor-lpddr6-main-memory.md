---
type: Paper
title: "NORmal: Architecting 3D Ferroelectric NOR Flash as Main Memory"
description: "北大/IME CAS/港科大广州 — BEOL 3D FeNOR 作未改 LPDDR6 主存 rank；手机多代理 200B 级；vs UFS 8.9×–28.0×，相对无限 DRAM ≤0.4% 差距，>256K vs HBF 2.8×–6.3× 更快且能耗/token 8.1×–17.8× 更低"
tags:
- memory
- 3d
- hbf
- flash
- nor
- fenor
- lpddr
- edge
- llm
- agentic-ai
- inference
- serving
- dram
created: 2026-11-04
updated: 2026-11-04
timestamp: '2026-11-04T00:00:00Z'
paper_author: [Zhuoran Li, Chen Gu, Zhuohang Bian, Haochen Yu, Yibo Zhao, Xuxiao Yang, Youwei Zhuo]
year: 2026
venue: arXiv
arxiv: '2610.40000'
sources:
  - raw/papers/NORmal_3D_FeNOR_LPDDR6_Main_Memory_2026.pdf
  - raw/papers/normal-3d-fenor-lpddr6-main-memory.md
---

# NORmal：把 3D FeNOR 做成手机主存 rank

## 一句话结论
手机多智能体要跑 **200B 级**模型与长会话，UFS 当存储会饿死按 token 的权重流，移动 HBF 又要改 SoC 且难吞持续 KV 写。NORmal 用已流片的 **BEOL 3D 铁电 NOR**（感知 **sub-7.5 ns**）经 under-array DRAM 仿真桥接到**未改 LPDDR6** 总线当普通 rank；按可变性与寿命摆放权重/规划器 KV/工人 KV。服务级仿真相对 UFS 卸载 **8.9×–28.0×** 更快（agent 团队 **21.4×**），吞吐达无限 DRAM 理想的 **>99.6%**（差距 **≤0.4%**）；会话 **>256K** 相对 HBF **2.8×–6.3×** 更快，内存能耗/token **8.1×–17.8×** 更低。

## 动机
- 手机上 planner+并行 worker 的 agent 团队需要远超手机 DRAM 的模型与上下文。
- 闪存若只当存储：UFS 带宽撑不起按 token 读权重；移动 HBF 需改 SoC，且写寿命/带宽难扛持续 KV。
- 非易失介质要进未改 LPDDR6 时序窗口，NAND 延迟达不到；需要可拟合 DRAM timing 的 NOR 类阵列。

## 方案
1. **共制 BEOL 3D FeNOR**：密 3-bit MLC 与可原地写、高耐久 SLC 同片；阵列感知 **sub-7.5 ns**。
2. **DRAM 仿真桥**：under-array 逻辑把阵列变成字节寻址、确定性时序的 load/store rank，挂在**未改 LPDDR6**（共享 **153.6 GB/s**）；交错 bank 读 + 零周期权重 swizzle + posted SLC 写。
3. **生命周期放置**：MLC 放权重（容量 **49–197 GB**）；SLC 放规划器 KV（**4–24 GB**）；DRAM 放工人 KV；按 agent 阶段动态切分 subchannel。
4. **评测**：生产 agent 轨迹上的 serving 级仿真，对照 UFS 卸载、无限 DRAM、移动 HBF。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| vs UFS 卸载端到端 | **8.9×–28.0×**（agent 团队 **21.4×**） |
| 相对无限 DRAM 吞吐 | **>99.6%**（差距 **≤0.4%**） |
| 会话 >256K tokens vs HBF | **2.8×–6.3×** 更快 |
| 内存能耗/token vs HBF | **8.1×–17.8×** 更低 |
| 阵列感知延迟 | **sub-7.5 ns** |
| 共享 LPDDR6 上容量 | MLC **49–197 GB**；SLC **4–24 GB** |

## 与 wiki 的关系
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — BEOL 垂直 FeNOR 阵列与封装/堆叠路线对照
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 主存总线级非易失 rank，相对 HBF/UFS/无限 DRAM
- [Characterizing HBF for LLM Serving](/papers/characterizing-hbf-llm-serving.md) — 同属移动/近存闪存服务，HBF 需改 SoC；NORmal 走未改 LPDDR6
- [Hot–Cold HBM/HBF](/papers/hotcold-hbm-hbf-agentic-llm.md) — agentic 热冷分层；NORmal 用可变性/寿命而非纯热度

## 开放问题
- 数字来自 serving 级仿真 + 阵列实测；完整手机 SoC 硅验证与量产工艺窗口未在文中展开。
- 与其它移动 HBF 控制器/封装路线的系统级共设计边界仍需对照实测。

# Citations
- [arXiv:2610.40000](https://arxiv.org/abs/2610.40000) — Li et al., PKU / IME CAS / HKUST-GZ, 2026
- [raw stub](/raw/papers/normal-3d-fenor-lpddr6-main-memory.md)
