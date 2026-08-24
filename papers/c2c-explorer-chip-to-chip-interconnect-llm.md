---
type: Paper
title: "C2C-Explorer: Chip-to-Chip Interconnect DSE for LLM Systems"
description: DAC 2026 — LLM 工作负载驱动的 scale-up C2C 仿真与贝叶斯 DSE；FPGA 原型时序误差 2.46–8.23%；DeepSeek-R1 combine goodput +44.1%、buffer −98.4%
tags:
- chiplet
- interconnect
- scale-up
- noc
- fabric
- switch
- protocol
- flow-control
- communication
- llm
- training
- inference
- architecture
timestamp: '2026-08-19T00:00:00Z'
created: 2026-08-19
sources:
- raw/papers/C2C_Explorer_Chip_to_Chip_Interconnect_LLM_2026.pdf
- raw/papers/c2c-explorer-chip-to-chip-interconnect-llm.md
---

# C2C-Explorer: An Exploration Framework for Chip-to-Chip Interconnect Architectures in LLM Cloud Computing Systems

**Authors:** Jiayi Li, Di Wu, Qingxu Li, Hongxiao Zhao, Jiaqi Yang, Anjunyi Fan, Wenbin Zhang, Boqiang Wu, Shuting Liu, Shifeng Fang, Jianbo Dong, Dimin Niu, Bonan Yan
**arXiv:** [2608.08611](https://arxiv.org/abs/2608.08611)
**Venue:** 文内写 accepted [DAC 2026](https://arxiv.org/abs/2608.08611)（2026-07-26 Long Beach）。**未独立核实会议程序册。**
**PDF:** [raw/papers/C2C_Explorer_Chip_to_Chip_Interconnect_LLM_2026.pdf](raw/papers/C2C_Explorer_Chip_to_Chip_Interconnect_LLM_2026.pdf)
**Code:** https://github.com/Selinaee/C2C-Explorer

## 中文摘要

多 XPU 超节点上，LLM 训练单 iteration 通信可超过 90%、推理超过 50%。现有工具要么停在 GPU-to-GPU 集体原语（SimAI），要么停在片上 NoC / 数据中心包网络，到不了 **chip-to-chip（C2C）** 的 AXI/以太 PHY、VC、credit 和 MAC 组帧。C2C-Explorer 把 SimAI 轨迹映射成 AXI 精确的 C2C 流，用端口周期精确 + 交换机事件驱动的混合仿真器覆盖 switch / full-mesh（文称最多数百 XPU），再用带硬件约束的贝叶斯搜索（AB-DSE）扫 packetization / scheduling / resource-allocation。对照 400 Gbps FPGA 原型，端到端时序误差 2.46–8.23%。在 32-XPU DeepSeek-R1-671B inference 的 combine 流上，相对最差可行点 goodput +44.1%、P99 −30.4%、每口 buffer −98.4%。

## Motivation

Scale-up 域 C2C（NVLink / UALink / ETH-X 一类）决定 collective 是否打满。三个缺口：(1) Megatron/DeepSpeed 的 AllReduce、All-to-All 要按物理端口和拓扑拆成 C2C 流；(2) BookSim/Garnet 是 NoC，ns-3/OMNeT++ 是 scale-out，都没有 AXI 级 C2C；(3) chunk、MAC 帧、AXI/VC 调度、VC 对数、credit 组合爆炸。作者用 ODCC ETH-X 白皮书的 400 Gbps / 467 ns 交换 / 245 ns 端口延迟作工业对照。

## Approach

1. **Traffic generator**：SimAI P2P（消息大小 + 依赖）按 mesh 或交换拓扑拆到各 C2C 口；按 BDP 滑动窗口切 chunk，下游 MAC 水位用 credit 反压；发送端展开 AXI write burst（aw + n×w + wlast），接收端回 b，chunk 完成才减窗口。
2. **C2C simulator（SimPy + 可选 PyPy JIT）**：七段流水 S1–S7——AXI 调度 → AXI/MAC 组帧（请求/响应物理分离，避免 AllReduce 双向 HOL）→ 每 VC TX buffer + CBFC → 以太/输入排队 crossbar（cut-through 近似）→ RX buffer 还 credit → unpack → 完成信号。核心旋钮：chunk 2/4/8 KB，MAC 帧 2/4 KB，AXI 调度 DRR/LQ/RR/SP，VC 1–32 对，VC 调度 DQD/FCFS/RR/WRR，credit 4–32 KB。
3. **评估指标**：goodput、P50/P99 FCT、公平性（σ/μ）、每口 buffer = N_V·C_B。用户案例权重：吞吐 0.40、P99 0.25、buffer 0.15、P50 0.15、公平 0.05。
4. **AB-DSE**：`chunk ≥ 2× MAC_frame` 等约束把 2394 点剪到 1152；LHS 播种后 GP + Expected Improvement。
5. **验证**：1 台 400 Gbps 交换机 + 4 个 FPGA C2C host，扫 One→All / All→One / All↔All。

## Results（仅论文数字）

**仿真器**

| 场景 | 相对 ETH-X/FPGA 的平均时序误差 |
|------|--------------------------------|
| One→All | **4.39%** |
| All→One | **2.46%** |
| All↔All | **8.23%** |

混合调度相对纯 cycle：128 KB All↔All、4→512 XPU 为 **1.1–7.8×**；1 MB 为 0.98–6.9×。PyPy JIT 在 ≤16 MB P2P 上最多 **1.78×**。

**微架构观察（8-XPU 等）**

- MAC 帧 1→8 KB 后 goodput 饱和，符合 (L−H)/L。
- chunk 约到 **2× MAC 帧** 后 AXI 事务开销被摊掉。
- 相对 RR：WRR goodput 1.12×，SP 1.82×，DRR-2KB **1.99×**；DRR-8KB 再降 4.06%（HOL）。
- 流量越不均衡（R=max/min 到 64），越需要 VC 数接近并发流数。

**32-XPU 用户案例（相对最差可行配置）**

| 任务 | Goodput | P50/P99 | Buffer |
|------|---------|---------|--------|
| DeepSeek-R1 dispatch | +14.7% | −12.6% | −75% |
| DeepSeek-R1 combine | **+44.1%** | **−30.4%** | **−98.4%** |
| LLaMA3.1-405B inference AR | +51.7% | −68.7% | −75% |
| Qwen3-30B training AR | +50.5% | −64.3% | −96.9% |

四任务均约 **20** 次评估收敛。最优高度 workload 相关；AXI 侧调度影响大于 MAC 侧。

## Relation to wiki

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 把 AllReduce / All-to-All 从算法层落到 C2C 端口、VC、credit
- [Network-on-Wafer](/concepts/network-on-wafer.md) — NoW 是晶圆内；本文是封装/板级 scale-up C2C
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 工业对照；本文是 ETH-X/AXI 探索框架而非新 PHY
- [Alibaba HPN](/papers/alibaba-hpn-datacenter-network-llm.md) / [Meta RDMA](/papers/rdma-over-ethernet-meta-training.md) — scale-out DCN；C2C-Explorer 填 scale-up
- [Fovea](/papers/fovea-physical-implication-aware-wafer-scale-dse.md) — 同是多保真 DSE，对象是晶圆 die 阵列而非 C2C 微架构
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — 封装内 D2D 争用；本文是多 XPU C2C 链路层
- [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — 同一 C2C 域更下一层：PAM4/FEC/重传的 gem5 PHY，负载是 CPU 而非 LLM
- [HCCL](/papers/hccl-meta-mtia-300-collective-communication.md) — 生产芯片上的编译集体 + 包内 NIC，不是 AXI/以太 DSE
- [DASH](/papers/dash-dual-path-hbf-moe-inference.md) — UCIe 预算用在 HBM↔HBF↔GPU，不是多 XPU 集体
- [HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md) — 封装内 2.5D NoI mesh 上 hybrid 推理 serving 的宏架构+运行时 DSE，不是 scale-up C2C 口级

## 开放问题

1. 仿真接到 512 XPU，用户案例只做到 32；更大 EP All-to-All 是否仍 20 步收敛未知。
2. buffer 指标是 N_V·C_B 相对配置，**不是**系统内存容量。
3. 未与真实 NVLink SHARP / NVLS / UALink 硅对照，FPGA 是 ETH-X 类 400G。
4. 与 [FlooNoC collectives](/concepts/collective-capable-noc.md) 的 in-network 算术归约正交，本文不做 in-switch reduce。

# Citations

[1] [raw/papers/C2C_Explorer_Chip_to_Chip_Interconnect_LLM_2026.pdf](raw/papers/C2C_Explorer_Chip_to_Chip_Interconnect_LLM_2026.pdf) — Li et al., arXiv:2608.08611
[2] [raw/papers/c2c-explorer-chip-to-chip-interconnect-llm.md](raw/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) — 结构化摘录
