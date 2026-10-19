---
type: Paper
title: "Causal Top-Down Microarchitecture Analysis (CTMA)"
description: "ICT CAS / BenchCouncil — TMA 只建模「负载→CPI→性能」一条因果路径；CTMA 加入「负载→退休指令数」两条隐藏路径，在 Skylake-SP / Zen 3 / Kunpeng 920 上揭示 CPI 冻结而时间翻倍、过度投机拥塞、ROB→前端填充瓶颈转移、op-cache SMT 差异与 kill -9 幽灵态（SPEC CPU2017 +22.75%）"
tags:
- cpu
- superscalar
- microarchitecture
- out-of-order
- branch-prediction
- smt
- performance-analysis
- methodology
- benchmark
created: 2026-10-19
updated: 2026-10-19
timestamp: '2026-10-19T00:00:00Z'
paper_author: [Chenxi Wang, Lei Wang, Wanling Gao, Guoxin Kang, Fanda Fan, Jianfeng Zhan]
year: 2026
arxiv: '2610.21387'
sources:
  - raw/papers/Causal_Top_Down_Microarchitecture_Analysis_2026.pdf
  - raw/papers/causal-top-down-microarchitecture-analysis.md
---

# CTMA：给 Top-Down 微架构分析补上因果模型

## 一句话结论
Top-Down（TMA）把流水线槽位分成 Frontend/Backend/Retiring/Bad Speculation，默认输入固定、指令流静态，于是把性能变化全归到 CPI。CTMA 把「数据集/算法 → 退休指令数」显式建模成两条额外因果路径，并用「处理（treatment）」——只改数据集拓扑/分布/局部性——来分离算法效应与微架构效应。

## 三条因果路径
| 路径 | 链条 | TMA 是否看见 |
|---|---|---|
| 微架构效率 | Workload → CPI → Performance | 看见 |
| 算法效率 | Workload → Instructions(Retired) → Performance | 看不见 |
| 微架构-算法耦合 | Workload → Instructions → CPI → Performance | 看不见 |

## 发现（论文数字；Xeon Gold 5120T / EPYC 7543 / Kunpeng 920，SPEC CPU2017）
- **CPI 画像盲区**（leela_r）：改数据集空间局部性，耗时变化 >**100%**，CPI 画像不动；跨 ISA 指令膨胀 **2.06×**。
- **过度投机拥塞**（mcf_r）：数据越规则分支预测越准，性能反而减半；投机把访存请求灌进后端，Line Fill Buffer 溢出、内存控制器拥塞；插 NOP 节流前端反而略快。
- **ILP 窗口坍塌**（cactuBSSN_r）：用 SMT 兄弟线程 pause 压缩 ROB 份额，完美拓扑数据集降 ~**23%**（Intel）/ ~**12%**（AMD），扭曲拓扑仅 ~**9%** / ~**10%** —— 瓶颈从 ROB 容量转到前端填充率。
- **Op-cache SMT 重叠**（xalancbmk_r）：极小递归足迹装进 Intel DSB 时 SMT 有加速；AMD Zen 3 退化 >**50%**。
- **幽灵态**（Xeon Gold 5120T）：kill -9 掉 SMT 兄弟进程且 OS 未做微架构刷新，流水线停在激进状态，SPEC CPU2017 平均虚高 **22.75%**、SPEC CPU2026 **42.20%**，与 Spectre v2 缓解开关相关。
- 据此建议「动态投机节流」做在线拥塞控制（论文给出建议，未见 RTL/模拟实现的量化评估）。

## 与 wiki 的关系
- [Superscalar CPU Research 2023–2026](/concepts/superscalar-cpu-research-2023-2026.md) — 补「评估方法」一环：OoO 边际饱和的判断需排除算法路径
- [Out-of-Order Execution](/concepts/out-of-order-execution.md)、[Branch Prediction](/concepts/branch-prediction.md) — ROB 份额与预测准确度的反直觉效应
- [Multicore, SMT & NUCA](/concepts/multicore-smt-nuca.md) — SMT 前端共享策略（DSB vs op-cache）差异
- [Architecture Benchmark Methodology](/concepts/architecture-benchmark-methodology.md) — 固定输入基准的系统性偏差与测量伪影

## 开放问题
- 投机节流机制停留在建议层，收益与硬件代价待验证。
- 「NOP 节流略快」等结论来自少数 SPEC 负载，泛化范围未知。
- 幽灵态只在一款 Skylake-SP 上复现，其他平台/微码版本是否存在需复测；对生产基准测量规范影响大。

# Citations
- Wang et al., "Top-Down Microarchitecture Analysis Without Causal Modelling Is Dangerous!", BenchCouncil TR, arXiv:2610.21387. [raw](/raw/papers/causal-top-down-microarchitecture-analysis.md) · [PDF](/raw/papers/Causal_Top_Down_Microarchitecture_Analysis_2026.pdf)
