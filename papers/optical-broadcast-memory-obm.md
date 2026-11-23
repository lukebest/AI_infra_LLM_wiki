---
type: Paper
title: "Optical Broadcast Memory: Eliminating Weight HBM in Datacenter LLM Serving"
description: "Uppsala — 80,000 加速器建模；split-port 相对 HBM3e，Llama-3.1-405B / Llama-4-Maverick / DeepSeek-V4-Pro 吞吐 0.96× / 0.97× / 1.57×，能量 0.90× / 0.90× / 0.58×，去掉 4.05 / 4.00 / 8.44 PB 权重 HBM"
tags:
- optical
- photonic
- cpo
- hbm
- datacenter
- inference
- serving
- moe
- memory
- interconnect
- systolic
- llm
- energy
- throughput
- expert-parallelism
- decode
created: 2026-11-17
updated: 2026-11-23
timestamp: '2026-11-17T00:00:00Z'
paper_author: [Hannah Atmer, Yuan Yao, Thiemo Voigt, Stefanos Kaxiras]
year: 2026
venue: arXiv preprint
arxiv: '2611.17097'
sources:
  - raw/papers/Broadcast_Dont_Replicate_OBM_2026.pdf
  - raw/papers/optical-broadcast-memory-obm.md
---

# Optical Broadcast Memory：用光纤广播权重，省掉复制的 HBM

## 一句话结论
Uppsala 提出 **Optical Broadcast Memory（OBM）**：中心权重服务器在开放的层次化 Tap-and-Amplify 光纤上持续广播只读权重，接收端用仅接收共封装光学（CPO）把参数直接送进激活静止计算单元。在对 **80,000** 个 H100 算力级加速器的建模评估中，split-port 布局相对 HBM3e 基线，在 Llama-3.1-405B / Llama-4-Maverick / DeepSeek-V4-Pro 上分别达到 **0.96× / 0.97× / 1.57×** 解码吞吐、**0.90× / 0.90× / 0.58×** 每 token 能量，并去掉 **4.05 / 4.00 / 8.44 PB**（**40% / 39% / 82%**）集群权重 HBM。评估来自分析模型。

## 动机
数据中心级 LLM 推理同时受内存容量与带宽约束。权重只读且在同模型实例间完全相同，常规架构仍把参数复制到成千上万加速器的本地 HBM，放大存储成本、静态功耗和重复取数能耗。先驱工作 Fiber Memory Ring（Atmer et al.，将发表于 HotNets’26，[arXiv:2607.08407](https://arxiv.org/abs/2607.08407)）用光纤环作延迟线存储器，但闭合环必须装下整个模型：环长随模型增大，slack 在建环时固定，现代 MoE 所需的高效布局也放不进去。

## 方案
1. **层次化 Tap-and-Amplify**：主干经全光 MC-PDFA 分段，抽头进 pod、再抽头进机箱；信号经过的抽头数随层次下降。评估取 400 pods、每 pod 25 机箱、共 80,000 加速器（单段配置示例可到 120,000，文中取保守值）。
2. **激活静止脉动阵列**：权重从光纤直接流入计算织物，激活、部分和与 KV 留在本地 SRAM/HBM。每机箱 8 加速器，摄入 8 缆 × 16 芯 MCF、每芯 16 波长、每 λ 100 Gbps，机箱合计 **25.6 TB/s**，每加速器 **3.2 TB/s** 仅接收 CPO（对照 H100 SXM 的 3.35 TB/s HBM3）。
3. **动态 slack 与 split-port**：推送流不可暂停，GEMM 效率折到 η=0.85，硬上限 \(b^*=263\) token / 加速器 / 权重趟。OBM 按最忙单元为每次广播动态定 slack。MoE 上用 DP-attention + EP（split-port），只需在端口上重复「每个 token 都用到的」共享权重。
4. **对照**：Baseline 为每 GPU 存自己的权重分片、HBM3e 128 GB；Ring 为同一作者组的光纤延迟线环（PP 与 TP/TP+EP）。工作负载拟合 LMSYS-Chat-1M。

## 效果（论文数字）
全部为集群 / roofline / 功耗模型 + 2,000 步放置仿真，在各自吞吐曲线膝点、等 KV 容量下相对 HBM3e 基线（Table V；集群权重 HBM 基线 10.24 PB）。

| 模型 | 配置 | 吞吐 | 每 token 能量 | 去掉的权重 HBM |
|---|---|---:|---:|---|
| Llama-3.1-405B | OBM (TP) | **0.96×** | **0.90×** | **4.05 PB（40%）** |
| Llama-4-Maverick | OBM (DP-attn. + EP) | **0.97×** | **0.90×** | **4.00 PB（39%）** |
| DeepSeek-V4-Pro | OBM (DP-attn. + EP) | **1.57×** | **0.58×** | **8.44 PB（82%）** |
| 三模型整模型流（OBM DP / Ring PP） | 单端口流完整权重 | **0.47× / 0.28× / 0.25×** | 高于基线 | 同上 |

V4-Pro 上的增益来自：基线每 GPU 105.5 GB 权重挤占 KV，且单 KV head 迫使 TP+EP 在 8 GPU 上复制 KV；OBM 不在本地存权重、不复制 KV，用 22.5 GB 预算中的 4.2 GB 就达到计算膝点。等吞吐、等 KV 时，split-port OBM 使集群功率在 405B / Maverick 降 **10%**，在 V4-Pro 降 **42%**（加速器从 80.0k 降到 50.9k）。tokens/s per TB HBM 为基线的 **1.59× / 1.59× / 8.9×**。

Ring (TP) 在 405B 同样达到 0.96× / 0.90×（假定跨缆 skew 被主动校正）；两个 MoE 上 TP+EP 被 \(b^*\) 压到 0.31× / 0.25× 吞吐。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把只读权重从每卡复制的 HBM 收到光纤广播路径
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 激活静止脉动，权重从光纤直接流入
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 解码侧反复读权重是这条路径要解决的主账
- [晶圆级光互连热调谐](/papers/wafer-scale-optical-interconnect-moe-thermal.md) — 同为光路服务 MoE，对象是晶圆 interposer 上的 MRR 热 stall
- [When Is HBF Cost-Effective](/papers/when-is-hbf-cost-effective-llm-inference.md) — 从容量成本侧对照：OBM 直接取消权重 HBM

## 开放问题
- 评估来自 80,000 加速器的分析模型。
- 热专家在 split-port EP 上超过计算膝点时，由权重服务器在端口上动态复制，文中列为后续工作。
- 跨缆 deskew 的硬件成本同样留待后续；敏感性中，未校正的 10 K 热漂移使 Ring (TP) 在 405B 的相对吞吐从 0.96× 降到 0.94×。
- 输出长度分布为作者假设（中位 200）；Ring 上「在全部 8 缆重复每个 token 都用的权重」的布局未评估。

2026-11-23：[OptiDecode](/papers/optidecode-fso-kv-regeneration.md) 把自由空间光学用在 decode 注意力的 KV 再生上，对照是等带宽的理想 GPU KV 读取；与本页的硅光广播权重路径层次不同。

# Citations
- [arXiv:2611.17097](https://arxiv.org/abs/2611.17097) — Atmer, Yao, Voigt, Kaxiras；Uppsala University
- [arXiv:2607.08407](https://arxiv.org/abs/2607.08407) — Fiber Memory Ring（HotNets’26，同一作者组先驱）
- [raw stub](/raw/papers/optical-broadcast-memory-obm.md)
- [arXiv:2611.19279](https://arxiv.org/abs/2611.19279) — OptiDecode
