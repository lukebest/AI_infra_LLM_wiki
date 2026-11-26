---
type: Paper
title: "ScaleWire: An End-to-End Scale-Up Ethernet Simulation Framework for LLM Systems"
description: "中科院信工所 / 微电子所 — 相对 ETH-X 四主机实测，全互连吞吐 MAPE 3.0%；DeepSeek-R1 dispatch 上六种网卡设计的片上存储预算相差 4.5×（862–3,858 KiB/XPU）"
tags:
- scale-up
- interconnect
- fabric
- transport
- protocol
- flow-control
- retransmission
- simulator
- llm
- inference
- training
- architecture
- hardware
created: 2026-11-24
updated: 2026-11-26
timestamp: '2026-11-24T00:00:00Z'
paper_author: [Kai Ma, Quanfeng Lv, Bowei Dai, Jingguo Ge, Kefan Ruan, Ruoqi Li]
year: 2026
venue: preprint
arxiv: '2611.26086'
sources:
  - raw/papers/ScaleWire_Scale_Up_Ethernet_Simulation_2026.pdf
  - raw/papers/scalewire-scale-up-ethernet-simulation.md
---

# ScaleWire：把 scale-up Ethernet 网卡机制和片上缓存一起仿真

## 一句话结论
中国科学院信息工程研究所与微电子研究所的 ScaleWire，把跨层网卡（NI）机制的包级仿真和一套资源探索引擎接到一起，用来给 LLM 的 scale-up Ethernet 选机制、定片上缓存。对照 ETH-X 四主机、400 Gb/s 交换机原型，全互连吞吐的平均绝对百分比误差为 3.0%，双方都在每主机约 345 Gb/s 饱和。在 32 个 XPU 的模型里，DeepSeek-R1 dispatch 上六种 NI 设计的每 XPU 存储预算相差 4.5×（Hash 862 KiB，LLR+E2E 3,858 KiB）。探索引擎用穷举搜索 6–19% 的仿真次数，九次网格对照里有八次预算达到或低于网格最优。

## 动机
训练和推理都依赖加速器之间高带宽、低时延、带存储语义的 scale-up 网络。以太网正在成为这类互连的开放选项。网卡里的传输、网络和链路机制会互相耦合，既决定通信时间，也决定片上缓存要开多大。只看其中一层，很难同时选对机制和缓存配额。

## 方案
框架包含包级仿真器、解析容量模型，以及「解析估计 + 仿真」的资源探索引擎。传输机制以 SUE-T 为参照，覆盖打包与确认、多路径与保序、端到端重传、链路级重试、逐跳信用流控这五组耦合。探索引擎在完成时间相对充足缓存基线升高不超过 2% 的约束下给 TX / Replay / RX / Reorder 定容量，并做联合修正。

硬件对照是已发表的 ETH-X 原型：四台 FPGA 主机、400 Gb/s 交换机、5 m 链路。设计空间评测则建模 32 个 XPU、四个交换平面、每平面每 XPU 两个 400 Gb/s 端口。默认设计组合链路级重试（LLR）、operational ACK、最少排队平面选择和每端口投递上下文（Lane）；五个变体分别改恢复范围、ACK 模式或端口选择（E2E、LLR+E2E、Delivery ACK、Hash、Sticky）。负载来自既有 LLM 通信模式：DeepSeek-R1 的 dispatch / combine、Llama-3.1-405B prefill 环，以及 Qwen3-30B 训练环。推理一节再用 vLLM prefill 轨迹，把在 GH200 上测得的 kernel 时间沿依赖图回放：Llama-3.1-70B 用 8 个 XPU，DeepSeek-V3.1 用 16 个 XPU，集体通信按四平面网络上的包级环来仿真。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 硬件对照（ETH-X） | 四主机全互连、13 种消息大小（每对端 1 KiB–1.75 MiB）MAPE **3.0%**，吞吐在每主机约 **345 Gb/s** 饱和；一对全 MAPE **7.3%** | Fig. 4 / §III-A |
| DeepSeek-R1 dispatch 存储预算 | 六种设计相差 **4.5×**：Hash **862 KiB/XPU**，LLR+E2E **3,858 KiB**，Default **1,073 KiB**（其中 Reorder 占 28%） | Fig. 7 / §IV-C |
| 约束放宽 | 完成时间约束从 2% 放到 5% / 10%，四个负载的中位预算相对 2% 约束分别低 **11.5% / 21.0%**；预算跨度仍为 4.5–4.9× | §IV-C |
| 探索引擎代价 | 九次网格对照使用穷举搜索 **6–19%** 的仿真次数；八次预算达到或低于网格最优，剩下一次多 14% 存储 | §III-C |
| ACK 与恢复 | DeepSeek-R1 dispatch 上，Delivery ACK 的包数是 operational ACK 的 **3.1×**，充足缓存下完成时间 +8%，TX 从 28 升到 36 KiB/TC。E2E 的 TX 在 dispatch 上到 320 KiB/TC，在 Qwen3 环上到 64 KiB/TC，对应 LLR-only 为 28 与 6 KiB/TC | Fig. 6 / §IV-B |
| 误码恢复 | BER = 3×10⁻⁷ 时，LLR 下完成时间为无误码的 1.14×（dispatch）与 1.15×（Qwen3 环）；E2E 下为 **1.81×** 与 **3.08×** | §IV-B |
| 信用与背压 | 5 m / 50 m 链路要维持链路利用率，大约需要 **26 / 48 KiB/VC**。dispatch 流量翻四倍且目的端只按链路速率 1/4 排空时，其余 31 个 XPU 的完成时间为 1.98×；把交换机 RX 加倍到 128 KiB/VC 后为 1.05×，同等存储加在端点 RX 上则为 1.92× | Fig. 6 / §IV-B |
| 推理 prefill 配额（Default vs LLR+E2E） | Llama-3.1-70B：421 vs 893 KiB/XPU；DeepSeek-V3.1：267 vs 502 KiB。打开 E2E 大约把每 XPU 存储加倍。独立定容会把完成时间抬到约束以上 2.2% / 2.1%，联合修正后回到 2% 以内 | Fig. 8 / §IV-D |

在均匀 dispatch 上，Hash 相对 Default 的 Lane 少 20% 存储（Reorder 102 vs 305 KiB）；在 Zipf 偏斜的 dispatch 上，Hash 反而多 13% 存储。充足缓存时，Sticky 完成 dispatch 比 Lane 快 7%，但在 Llama / Qwen 环上 Hash 与 Sticky 的完成时间大约是 Lane 的 1.18× / 1.23×。

## 与已有页的增量
[SURMA](/papers/surma-scale-up-rma-engine.md) 用 FPGA 原型加 Hopper 轨迹讨论 scale-up RMA 引擎。[Zero-SM NCCL](/papers/zero-sm-nccl.md) 在 NVLink 域内测集体通信。[NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) 记录的是专有 scale-up 织物。ScaleWire 把对象换到开放的 scale-up Ethernet 网卡，强调机制选择会让片上存储差出数倍，并用 ETH-X 测量校准仿真器。

## 与 wiki 的关系
- [NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 专有 scale-up 织物的对照面
- [SURMA](/papers/surma-scale-up-rma-engine.md) — scale-up 一侧通信引擎
- [Zero-SM NCCL](/papers/zero-sm-nccl.md) — 域内集体通信的硅测
- [ProtoBridge](/papers/protobridge-superpod-interconnect-sim.md) — 在 NVLink / MetaXLink 上做协议显式的包级仿真，并扫 CPO 与 scale-up 内存池
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 网卡片上缓存也是端到端路径的一部分

## 开放问题
- 硬件对照是四主机 FPGA 原型；32 XPU 与推理配额数字来自仿真。
- 推理一节回放 GH200 上测得的 kernel 时间，集体通信按包级环来建模，和真实交换机队列仍有距离。
- 默认约束是完成时间相对充足缓存升高不超过 2%；文中已表明放宽约束会明显缩小预算。
- 传输机制以 SUE-T 为参照，换一套不同的 scale-up 以太网规范需要重新标定。

# Citations
- [arXiv:2611.26086](https://arxiv.org/abs/2611.26086) — Ma, Lv, Dai, Ge, Ruan, Li（中国科学院信息工程研究所 / 微电子研究所 / 国科大）
- [raw stub](/raw/papers/scalewire-scale-up-ethernet-simulation.md)
- [PDF](/raw/papers/ScaleWire_Scale_Up_Ethernet_Simulation_2026.pdf)
- [arXiv:2611.30191](https://arxiv.org/abs/2611.30191) — ProtoBridge
