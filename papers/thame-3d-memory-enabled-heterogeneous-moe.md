---
type: Paper
title: "ThAME: 3D Memory-Enabled Heterogeneous Accelerator for LLM MoE"
description: WSU ESWEEK-26 — FeFET-NAND PNM 存 expert、DRAM-PNM 做 attention、分层树 NoC 扛非确定 scatter-gather；相对 H3D-T 最高 15.7× TBT、9.8× 能效
tags:
- 3d
- hybrid-bonding
- chiplet
- noc
- moe
- llm
- inference
- accelerator
- memory
- interconnect
- packaging
- architecture
timestamp: '2026-08-19T00:00:00Z'
created: 2026-08-19
sources:
- raw/papers/ThAME_3D_Memory_Enabled_Heterogeneous_MoE_2026.pdf
- raw/papers/thame-3d-memory-enabled-heterogeneous-moe.md
---

# ThAME: 3D Memory-Enabled Heterogeneous Accelerator for LLM Mixture of Experts

**Authors:** Pratyush Dhingra, Pramit Kumar Pal, Janardhan Rao Doppa, Partha Pratim Pande（Washington State University）
**arXiv:** [2607.17074](https://arxiv.org/abs/2607.17074)（v1 2026-07-19，v2 2026-08-02）
**Venue:** abs 写 accepted IEEE/ACM Embedded Systems Week (ESWEEK-26)。**未独立核实程序册。**
**PDF:** [raw/papers/ThAME_3D_Memory_Enabled_Heterogeneous_MoE_2026.pdf](raw/papers/ThAME_3D_Memory_Enabled_Heterogeneous_MoE_2026.pdf)

## 中文摘要

MoE 推理被三件事卡住：decode 每 token 要搬非连续 expert 权重；gating 造成输入相关、突发的 scatter-gather；同步 gather 让最慢 expert 决定整批尾延迟。ThAME 用 2.5D UCIe 把三类 chiplet 拼在一起——host TPU 做 prefill/gating，3D DRAM-PNM 做 attention（KV 不离开 chiplet），3D FeFET-NAND-PNM 用 CBA+Cu-Cu hybrid bonding 把静态 expert 堆在计算基座上。基座内不用 mesh/ring，而是对「所有可能的 token→核分配」做多目标优化得到的分层树 NoC。仿真（SCALE-Sim + NeuroSim，非硅）上，相对 H3D-T / Stratum 的 TBT 最高 15.7× / 10.2×，能效 9.8× / 5.6×。

## Motivation

Attention 要 RMW、高耐久，expert 要高密度静态存储，单一 DRAM 或 NVM 对不上。Stratum 用单体 3D DRAM-PNM + Ring，一次只跑一个 expert，还要刷新；H3D-T 片上 NVM 只有数 MB，专家权重反复出片。GPU/TPU 把 EP 推到 NVLink，decode 仍然内存墙。作者认为通信骨架必须按 **输入未知的 MoE 流量组合空间** 做稳健设计，而不是为一种静态 dataflow 调 mesh。

## Approach

1. **异构 3D PNM**：FeFET-NAND 8 ch / 4 bank / 4 plane，SLC，读 10 ns，~3 V，32 nm，121 mm²；CBA 把 CMOS 基座与阵列 Cu-Cu 键合，数据 I/O **不占**逻辑有源区。DRAM 侧 8-Hi HBM-PNM，7 nm 基座，1024-bit @ 5.2 Gbps。Host 为 TPU v6e 风格 8×256×256 @ 5 nm。UCIe NoP 2 GHz、0.5 pJ/bit。
2. **映射**：prefill 与 gating 在 host；query 经 interposer 进 DRAM chiplet 做 attention，KV 留在本地；top-k 后 host 上硬件 min-max 调度（对延迟域二分，Qwen1.5 约 17 次）把 32 核分给活跃 expert；只有 **O(B·d_model)** 激活走 2.5D，权重不出 FeFET。
3. **分层 NoC**：设计变量 d=(c, l, m, n, h_mem)——每 crossbar 核数、树深、每层孩子/父亲数、存储器注入层。约束：host 到所有核连通，链路数不超过 2D mesh。目标：所有流量场景上的平均链路利用率 μ、标准差 σ、面积 A。AMOSA 求 Pareto，再周期精确挑点。路由：树用 LCA，mesh/torus/ring 用维序。
4. **评测**：DeepSeek-MoE-16B / OLMoE-7B / Qwen1.5-MoE-2.7B / Qwen3-30B / Llama3-8B（dense 对照），INT16，B=32，MMLU PyTorch 轨迹。SCALE-Sim 相对 TPU 中位误差 <3%；NeuroSim 相对 PIM 宏后仿 <1%（作者引用）。对照 Stratum、H3D-T、vLLM+A100、TPU v6e。

## Results（仅论文数字）

**NoC / 消融**

- 选出的分层树 BFT(2,4,2) 相对 Ring 平均通信延迟 **4.1×** 更好；Torus 相对 Mesh 延迟略好但面积 **+48%**。
- Qwen1.5 全组合空间：ThAME 60% 配置 |Comm−Comp|/Comp **<2%**，最坏 **27%**；Mesh/Torus 60th 百分位 13%、90th 35%；Ring 至少 **300%** 失配。
- 消融：换 Mesh 最多 **1.44×** 延迟、**2.1×** 能量；再换 DRAM-PNM 再加最多 **1.8×** 能量。相对 Stratum 累计延迟 **4.7× / 7.0×**（Qwen1.5 / DeepSeek），能效 **5.4× / 8.7×**。

**端到端（B=32, MMLU）**

| 对照 | TBT | 能效 |
|------|-----|------|
| vs H3D-T | 最高 **15.7×** | **9.8×** |
| vs Stratum | 最高 **10.2×** | **5.6×** |

Qwen1.5、prompt 128、输出 n=512–4096：ThAME TBT **2.17–2.22 ms**（TPU 18.12、A100 22.93 → **8.2× / 10.5×**）；每 token ≈**6.7 mJ** vs 141 / 214 mJ。E2E（TTFT+n·TBT）从 n=512 的 **9.8×** 增到 n=4096 的 **10.2×**（相对哪条基线：表 VI 上相对 A100 约 9.9–10.2×，相对 TPU 约 7.8–8.1×；文内「10.2×」与 TBT vs Stratum 共用表述，跨表对照时需小心）。

147.5 Tokens/s/W：相对 Stratum / TPU / A100 为 **5.6× / 20.9× / 31.7×**。DeepSeek B=64 吞吐相对 Stratum / H3D-T **5.92× / 12.77×**。FeFET 读延迟扫到 50 ns 几乎不掉，100 ns 才 **2.2×** TBT；阵列峰值 ~**14.7 TB/s** vs 核需求 ~**3.28 TB/s**。片上 FeFET **64 GB**（每 chiplet 32 GB）。

## Relation to wiki

- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — CBA + Cu-Cu HB 把 3D NAND 接到逻辑基座；数据口不占有源区
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Voxel 是 DRAM-on-logic + mesh；ThAME 把 attention/expert 拆到 DRAM vs FeFET 两种 3D 栈
- [Mozart 3.5D](/papers/mozart-35d-wafer-scale-moe-training.md) — Mozart 训练侧 NoP-Tree + SRAM HB；ThAME 是推理侧 PNM + 树 NoC
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — 3DLS 隔离 KVT vs AllReduce；ThAME 隔离 KV-RMW vs 静态 expert
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 这里是片内 scatter-gather，不是跨卡 All-to-All
- [Network-on-Wafer](/concepts/network-on-wafer.md) — 封装是 2.5D UCIe，不是晶圆级 NoW
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — host prefill / DRAM decode-attn / FeFET expert，功能解耦但同包
- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — 另一条驻留 FFN：ReRAM NMC + Core 组播，不是 FeFET 树 NoC

## 开放问题

1. 全是仿真（SCALE-Sim + NeuroSim + 热模型），无 FeFET-NAND PNM 硅。
2. Host 被建模成 TPU v6e，prefill TTFT 与 TPU 相同是构造出来的，不是端到端异构调度实测。
3. NoC 按均匀先验扫组合空间，真实 gating 可能更偏；MMLU 只是一例。
4. 与 [Mozart](/papers/mozart-35d-wafer-scale-moe-training.md) 的 NoP-Tree 同是「树扛 MoE」，一个在 package NoP、一个在 chiplet NoC，缺直接对照。

# Citations

[1] [raw/papers/ThAME_3D_Memory_Enabled_Heterogeneous_MoE_2026.pdf](raw/papers/ThAME_3D_Memory_Enabled_Heterogeneous_MoE_2026.pdf) — Dhingra et al., arXiv:2607.17074v2
[2] [raw/papers/thame-3d-memory-enabled-heterogeneous-moe.md](raw/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — 结构化摘录
