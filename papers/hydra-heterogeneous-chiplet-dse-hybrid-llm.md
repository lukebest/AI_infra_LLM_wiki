---
type: Paper
title: "HYDRA: Heterogeneous Chiplet DSE for Hybrid LLM Serving"
description: UW–Madison/Ulsan — 2.5D 异构 chiplet 上 Hybrid LLM serving 的宏架构+运行时联合 DSE；平均 1.55× 吞吐、TTFT −43.7%，最高 2.3×；Markov 剪枝 2520–8520×
tags:
- chiplet
- interconnect
- noc
- fabric
- llm
- inference
- serving-system
- architecture
timestamp: '2026-08-24T00:00:00Z'
created: 2026-08-24
sources:
- raw/papers/HYDRA_Heterogeneous_Chiplet_DSE_Hybrid_LLM_2026.pdf
- raw/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md
---

# HYDRA: A Heterogeneous Chiplet DSE Framework for Serving Dynamic Hybrid LLM Workloads

**Authors:** Jiahao Lin, Alish Kanani, Sangwan Lee, Jaehyun Park, Umit Y. Ogras  
**arXiv:** [2608.19395](https://arxiv.org/abs/2608.19395)（2026-08-19）  
**Venue:** 预印本。文内**未**自称会议接收。  
**PDF:** [raw/papers/HYDRA_Heterogeneous_Chiplet_DSE_Hybrid_LLM_2026.pdf](raw/papers/HYDRA_Heterogeneous_Chiplet_DSE_Hybrid_LLM_2026.pdf)  
**Code:** 文内写 Github，**URL 未知**。

## 中文摘要

Hybrid Transformer–Mamba（Jamba / Nemotron-H / Zamba 一类）把 Attention 的 KV 增长和 Mamba 的常状态 decode 塞进同一 serving 环。单片加速器做不了相位特化；2.5D chiplet 可以拆 prefill/decode × Attention/Mamba 四种计算 die，但组成、放置、D2D 带宽、动态 batch、弹性调度一起搜，穷尽事件仿真要按天计。HYDRA 用通信感知放置 + 动态 batch + 弹性调度，再加一个只做剪枝的 Markov 估计器（与全仿真平均 cosine similarity **0.9**），把探索从天压到分钟。全负载平均 **1.55×** 吞吐、TTFT 低 **43.7%**，吞吐最高 **2.3×**。

这不是 [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) 的 scale-up C2C 口级 DSE，也不是 [Fovea](/papers/fovea-physical-implication-aware-wafer-scale-dse.md) 的晶圆物理可行域，也不是 [Mozart](/papers/mozart-35d-wafer-scale-moe-training.md) 的 3.5D 训练 All-to-All。对象是**封装内 NoI mesh** 上的 hybrid **推理** serving。

## Motivation

- 模型侧：SSM 随序列变长 element-wise 变多；Transformer 仍是 GEMM；Mamba 还有门控/非线性。
- 相位侧：prefill 两边都偏算力；decode 时 Mamba 近恒定、Attention 的 KV 扫带宽随上下文涨。
- 工具侧：Gemini / Cascade / WSC-LLM 要么不做 hybrid，要么不做运行时动态。表 I：HYDRA 对标 24 chiplet 宏架构 + 请求轨迹 + NoI 拓扑 + 面积预算。

## Approach

1. **Chiplet 库**：\(A_p,A_d,M_p,M_d\)（Attention/Mamba × prefill/decode）+ HBM3。prefill die 算力/SRAM 大致均分，decode die SRAM 大约 2× 算力。工艺折到 22 nm（DeepScale）。
2. **物理约束**：被动硅 interposer，2D mesh；D2D 按 NVIDIA GRS PHY + UCIe x64 advanced-package；带宽档 **256/384/512/640 GB/s**（带宽吃面积，挤 SRAM/算力）。Interposer **2700–3000 mm²**，单 die 上限约 **121 mm²**（对标 HBM 堆面积）。
3. **放置**：HBM 放外圈并按 Mamba/Attention 切容量（最大化 \(\min(r_M,r_A)\) 并发）；计算 die 按曼哈顿距离贴自己的 HBM 组，大组先占位。
4. **运行时**：连续 batch（token budget + 虚拟块，像 vLLM）；OOM 时抢最少已生成 token 的请求；弹性调度在放置偏好映射上，按队列+通信距离改派，而不是纯 work-stealing。
5. **估计器**：连续时间马尔可夫链，状态 = 分给 prefill 的 chiplet 数；流体队列近似占用。只剪枝，不替代仿真。相对穷尽少评 **2520–8520×** 点。

评测模型：Nemotron-H-4B、LLaMA3-7B、Mamba-2.8B。数据集：ArXiv-4K、BWB、LongWriter-6K、LMSYS-Chat-1M。事件仿真 100 s 工作时间。对比 Gemini/Cascade/WSC-LLM 类静态 DSE，以及 round-robin/random 放置、FCFS/work-stealing 调度。

## Results（仅 PDF 数字）

| 项 | 数字 |
|----|------|
| 全负载平均 | 吞吐 **1.55×**，TTFT **−43.7%** |
| 吞吐上限 | **2.3×** |
| Markov vs 全仿真 | 平均 cosine similarity **0.9** |
| 探索时间 | LLAMA3-7B：穷尽 **2 d 8 h** / HYDRA **4 min**；Mamba-2.8B：**3 d 1 h** / **4 min**；Nemotron-H-4B：**8 d 8 h** / **15 min** |
| 找回最大吞吐 | 穷尽 **100%**，roofline **74%**，HYDRA **93%** |
| 通信感知放置（相对 RR） | 平均 TP/TTFT **1.29×**、吞吐 **1.22×**（Nemotron-H 四数据集） |
| 弹性调度（相对静态映射） | TP/TTFT **1.40–2.04×**，最大吞吐 **1.17–1.73×** |
| 动态 batch | 吞吐 **+15%**，TTFT **−23%**（平均） |

消融：通信放置、弹性调度、动态 batch 叠上去才到 1.55× / −43.7%。单模型特化迁到别的 hybrid 会掉到 0.31–0.44（\(B^\star\) 正规化分）；三模型一起搜能把最差 case 拉到约 0.84–0.96。

**仿真，不是硅。** 无实测 UCIe 链路，无生产集群。

## 和 wiki 已有概念的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md)：这里拆的是 **封装内** prefill/decode × 算子类型，不是机柜 AFD。
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)：应用层流量（hybrid serving 轨迹）倒逼 NoI 带宽和放置，而不是先定 mesh 再灌合成流。
- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md)：物理假设停在 UCIe x64 + GRS；没有 [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) 那种 PAM4/FEC 运行时模型。
- [Network-on-Wafer](/concepts/network-on-wafer.md)：HYDRA 是 interposer 上的 chiplet-on-fanout 近亲，**不是**场拼接/WoW。
- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md)：C2C 是超节点口；HYDRA 是包内 NoI。
- [Mozart](/papers/mozart-35d-wafer-scale-moe-training.md)：Mozart 是 3.5D **训练** MoE All-to-All；HYDRA 是 hybrid **推理**。

## 开放问题

1. 功耗/热/可靠性明确留给未来；DSE 目标只有吞吐和 TTFT。
2. Github URL 文内未写，代码不可复核。
3. 24 chiplet / ~3000 mm² 包是否还叫「chiplet 而不是小晶圆」，和 [Fovea](/papers/fovea-physical-implication-aware-wafer-scale-dse.md) 的可行域怎么接，文内没比。

# Citations

[1] [raw/papers/HYDRA_Heterogeneous_Chiplet_DSE_Hybrid_LLM_2026.pdf](raw/papers/HYDRA_Heterogeneous_Chiplet_DSE_Hybrid_LLM_2026.pdf) — Lin et al., arXiv:2608.19395
[2] [raw/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md](raw/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md) — 结构化摘录
