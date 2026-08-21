---
type: Paper
title: "ReXpert: ReRAM Near-Memory FFN Pool for Disaggregated MoE"
description: HKUST/阿里云 — 驻留 expert + core 内组播；occupancy 0.328→0.519；iso-compute vs H20 FFN 池 9.5×、权重搬运能 20×；H20-attn 混合 TPOT 1.25–10.4×
tags:
- chiplet
- noc
- interconnect
- moe
- llm
- inference
- disaggregated-inference
- accelerator
- memory
- packaging
- mesh
- scale-up
- architecture
- serving
- throughput
- latency
timestamp: '2026-08-21T00:00:00Z'
created: 2026-08-21
sources:
- raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf
- raw/papers/rexpert-reram-nmc-disaggregated-moe.md
---

# ReXpert: MoE Expert Execution in Disaggregated LLM Serving with a High-Bandwidth ReRAM Near-Memory Architecture

**Authors:** Kunming Shao, Ming Zeng, Xin Yuan, Binbin Liao, Yangming Zhang, Wei Wang, Tim Kwang-Ting Cheng, Chi-Ying Tsui（HKUST + Alibaba Cloud）
**arXiv:** [2608.13962](https://arxiv.org/abs/2608.13962)（2026-08-14）
**Venue:** 未标会议；方法/结果为 measured traces + modeled pool，**不是硅**。
**PDF:** [raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf](raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf)

## 动机

[Disaggregated Inference](/concepts/disaggregated-inference.md) 把 attention（KV 读带宽）和 FFN（权重复用）拆到不同池。MoE 的机会是：专家权重可永久驻留在高带宽近存 FFN 池，激活在池间流。

Decode SLO 卡住 run-batch。稀疏路由让激活并集 U(B) 涨得快：Qwen3.5-35B-A3B 轨迹上 U 从 B=1 的 **8** 涨到 B=64 的 **168.6/256**（B=128 时 205），64× batch 只把每 token 权重流量压约 **3.0×**。热 expert 设步延迟，冷 expert 闲着。H20 机器平衡 F=74 FLOP/byte，密 FFN 要 37 token/读才上屋顶；Qwen3.5-397B 的 MoE 膝点 B★=**1894**（H100/H800 更到 **15,123**）。B≤16 时两条 MoE 曲线都 <1.4% 峰值——这是一阶利用率膝点，不是实测 kernel MFU。

驻留去掉片外搬权重之后，FFN 池仍要：(i) 稀疏并集下的**带宽密度**（读带宽/驻留容量）；(ii) 不靠全局复制/全局共享织物，把 occupancy 从 straggler 里捞回来。

相对 [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md)：ThAME 是 FeFET-NAND PNM + 分层树 NoC；本文是 **ReRAM 近存数字 PE**（权重可编程、PE 可再分配）+ **Core 内有界组播** + 2.5D UCIe 四 die。

## 方案

层次：Unit → Core → Die → 4-die 2.5D UCIe Package → Node（8 package）。**权重不出 Core mesh**；更高层只走激活和部分和。

1. **Unit**：16×2 Mib 宏 @200 MHz → **51.2 GB/s** 本地读；4 MiB。PE 是 4-token × 128-lane FP8 @400 MHz，**400 GFLOPS**，平衡 7.81 FLOP/byte。物理 tile 宽 w=4 是能摸到算力屋顶的最窄整数。
2. **Core / Die**：side-4 = 16 Unit、64 MiB、6.4 TFLOPS。20×20 mm 12 nm die：320 Unit、20 个 side-4 core（16×20 阵列 → 4×5 Die-NoC）、**1.25 GiB / 16.4 TB/s / 128 TFLOPS**。四 die package 5 GiB / 65.5 TB/s / 512 TFLOPS。参考 FFN 池 25 die 装 Qwen3.5-35B 的 30.1 GiB FFN 权重（31.25 GiB / 410 TB/s / 3.2 PFLOPS）。每级保持 **0.128 B/FLOP**。
3. **有界 pooling**：热 expert 的读出在 Core 内组播到空闲 PE 组；borrower 拿同一权重行、不同 token；BF16 部分和回到 owner。side-4 是 occupancy 与 mesh 直径/硅的膝点。
4. **MFU 分解**：实际 MFU = 理想 MFU（tile 填充）× occupancy（有没有组在等 straggler）。组播、共激活放置、load-aware fetch 主要动 occupancy。
5. **互连按需供给**（Table IV）：Unit 外 I/O 需求 1.57 GB/s；Core mesh 流 51.2 GB/s、p99 204.8、选 64 GB/s/link 与 256 GB/s/core；Die-NoC 最忙链 24.68–24.81 GB/s（GLM BookSim2），选 512 b @1 GHz = 64 GB/s；包 D2D 每 die 47.0→96 GB/s；节点 residual 16.7→34 GB/s。
6. **归约顺序**：die j 存每个 expert 的 shard j。必须 **expert-parallel-first**（同 index 先在 die 上合）；反过来 GLM-5.2 包内 D2D 从 37.6 涨到 **213.1 GB/s（5.7×）**，Qwen3.5-397B / 35B 惩罚 2.7× / 5.7×。

评测：Qwen3.5-35B-A3B / 397B-A17B / GLM-5.2 的 router-hook 轨迹（Alpaca+code，多 batch）；GPU grouped-GEMM 校准 HBM 流到 datasheet 的 88–94%，roofline 对 kernel 时延误差 <7%。对 GPU 基线给满流带宽、不计 launch 开销。

## 效果（仅论文数字）

**Pooling 膝点（Qwen3.5-35B，B=128）**

| Core | occupancy (bcast) | 实际 MFU | round stretch | mm²/occ. |
|------|-------------------|----------|---------------|----------|
| 2×2 | 0.328 | 0.240 | 1.00× | 11.96 |
| **4×4** | **0.519** | **0.381** | **1.23×** | **7.56** |
| 6×6 | 0.532 | 0.391 | 1.69× | 10.88 |
| 8×8 | 0.678 | 0.499 | 2.50× | 11.27 |

理想 MFU 钉在 0.736（均值 4 token/expert，冷尾仍填不满 tile）。397B 同一膝点：occupancy 0.377→0.599。

**机制消融（side-4）**

- 直接→组播：occupancy 0.152→0.510，实际 MFU 0.111→0.374，轮次 8.89→2.21。
- LPT→共激活放置：occupancy 0.519→0.532，轮次 2.16→2.07。
- G=2 时 load-aware fetch：occupancy 0.422→0.552（理想 MFU 从 1.000 降到 0.778，因为更窄 job）。
- 把 w=4 缩到 1：理想 MFU 0.346→1.000，但屋顶 cap 掉到 0.256——负结果，保持 w=4。

**iso-peak-compute FFN 池（三模型、读绑定，比例与规模无关）**

- vs H20：**9.5×**；vs H100/H800：**75.6×**。Qwen3.5-35B B=8：1.93 vs 18.26 / 145.8 μs/token。
- 等带宽要对齐 ~100–122 GPU die，延迟优势消失——增益来自**带宽密度**不是总量。
- B=64 每 token 激活权重都是 331 MB；4.00 vs 0.20 pJ/byte → 搬运能正好 **20×**。无组播则 420 MB/token（1.3×）。

**AF 系统（H20 attention + ReXpert FFN vs 同质 H20）**

| 模型 | 增益范围（4K–32K ctx） |
|------|------------------------|
| Qwen3.5-35B | **1.25–4.0×** TPOT |
| Qwen3.5-397B | **2.4–10.3×** |
| GLM-5.2 | **2.5–10.4×** |

35B B=8 4K：t_attn 6.06、t_FFN 1.93 → AF TPOT 6.06 vs H20-only 24.3（**4.0×**）。32K 时注意力绑死，增益缩小。

**面积/功耗（建模）**：die ≈47 W（ReRAM 268 mm² / 3.3 W；PE 82 mm² / 19.5 W；Core mesh 35.6 mm² / 19 W）。25-die 池 ≈1.2 kW vs iso-compute 10.8-die H20 **4.3 kW TDP**（**3.7×** 功耗，约 **35×** 每 token FFN 能量）。

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 把 AFD 的 FFN 池做成驻留 ReRAM + 有界共享，而不是跨节点 EP
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — 同类「expert 驻留近存」；器件 FeFET-NAND vs ReRAM，NoC 树 vs Core 组播+Die mesh
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — 3DLS 隔离 KVT/AR；本文隔离权重流（Core 内）与激活/部分和（Die/D2D）
- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) — 包间 C2C DSE；本文把 UCIe D2D 预算从 MoE 归约顺序推出来
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Die-NoC 是 4×5 mesh；Core mesh 是组播/归约，不是通用 XY
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 驻留之后 EP/TP 权重移动变成次级；关键是放置匹配的归约顺序

## 开放问题

1. 全是轨迹+BookSim2/DSENT/RTL 投影，没有 ReXpert 硅。
2. 一次编程、读多写少的 ReRAM；器件波动/保持/耐久/良率被作者自己列为工艺前提。
3. Core mesh / Die-NoC / D2D 在 skew 下的争用调度（组播仲裁、fetch vs compute 重叠）仍开放。
4. 对 GPU 基线给满 HBM 流、不计软件开销，跨系统差距是架构带宽密度上界。

# Citations

[1] [raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf](raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf) — Shao et al., arXiv:2608.13962
[2] [raw/papers/rexpert-reram-nmc-disaggregated-moe.md](raw/papers/rexpert-reram-nmc-disaggregated-moe.md) — 结构化摘录
