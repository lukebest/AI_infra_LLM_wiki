---
type: Paper
title: "ProtoBridge: 把协议效应写进超节点互连的包级仿真"
description: "清华 / MetaX / 无问芯穹 / 港科大 / 上交 — 集体通信对照 H200 NVLink4 平均延迟误差 17.76%、C500 MetaXLink 10.33%；代理模型把延迟-带宽模型的 MAPE 从 55.7% 降到 11.8%，单次操作评估 20.5 µs；一小时探索 38,232 个超节点设计"
tags:
- scale-up
- interconnect
- fabric
- protocol
- flow-control
- simulator
- llm
- inference
- nvidia
- nvlink
- cpo
- hbf
- topology
- architecture
- communication
- serving
created: 2026-11-26
updated: 2026-11-26
timestamp: '2026-11-26T00:00:00Z'
paper_author: [Yu Zhu, Xinhao Yang, Zhaoshi Li, Baodong Wu, Boxun Li, Wenxue Li, Guohao Dai, Hongyang Jia, Shuwen Deng, Huazhong Yang, Yuan Xie, Zhenhua Zhu, Yu Wang]
year: 2026
venue: HPCA 2027
arxiv: '2611.30191'
sources:
  - raw/papers/ProtoBridge_LLM_to_Packet_Superpod_2026.pdf
  - raw/papers/protobridge-superpod-interconnect-sim.md
---

# ProtoBridge：用包级仿真把 scale-up 协议效应显式化

## 一句话结论
清华大学、MetaX、无问芯穹、港科大与上海交大提出 ProtoBridge：在 ns-3 上加两层抽象，把 LLM 通信操作映到包交换，用来探索超节点互连。集体通信对照里，平均延迟误差在 H200 NVLink4 上为 **17.76%**，在 C500 MetaXLink 上为 **10.33%**，在 NVL72 开源数据上为 **1.76%**。把操作到包（OTP）参数和包执行（PEX）解析模型合成代理后，相对延迟-带宽模型的 MAPE 从 **55.7%** 降到 **11.8%**，单次操作评估从 **2.38–75.70 s** 降到 **20.5 µs**。代理再加包级精修，一小时扫过 **38,232** 个超节点设计，并用来看 scale-up 内存池和共封装光学（CPO）互连。

## 动机
模型与上下文变大之后，服务要把权重、KV 和激活切到多卡，通信延迟会进到 decode 时间里——文中举例 GLM-5.2 的通信可占 decode 的 **32.4%**。延迟-带宽模型只用启动项和有效带宽，吃不到争用和协议差异：8 卡 H200 上，256 MB AllReduce 会被低估 **38.6%**。ns-3 这类包级仿真能刻画排队与路由，但每种 scale-up 协议都要单独做 LLM-to-packet 实现，仿真时间也撑不起端到端设计扫描。

## 方案
ProtoBridge 在 ns-3 事件系统上拆成两层：

- **OTP（operation-to-packet）**：描述协议特有的包交换与依赖。
- **PEX（packet-execution）**：把信用流控、FEC、链路重传等共享包级机制接到同一套事件系统上。

为加快探索，作者再从 OTP 参数和 PEX 机制的解析模型导出代理，先用代理筛设计，再用包级仿真精修前列候选。硬件对照包括：8 卡 H200（NVLink4 / NVSwitch，每 GPU 18 条平面链路、每条 200 Gb/s）；4 卡 C500（MetaXLink 全互连）；NVL72 的开源数据；以及 ns-3 上的 UB 参考。仿真跑在 Xeon Platinum 8358 上。

## 量化结果
包级精度（34 组配置、跨数据大小平均 MAPE）：

| 平台 | ProtoBridge | 最好的 ASTRA-sim 后端 |
|---|---|---|
| H200 | 17.76% | 52.01% |
| C500 | 10.33% | 28.85% |
| NVL72 | 1.76% | 15.62% |
| UB | 2.77% | 18.49% |

UB AllToAll 在二维全互连上有多跳争用：ASTRA-sim 解析后端误差 **68.59%**，HTSim / ns-3 后端因使用 DCQCN 仍为 **56.96% / 75.35%**；ProtoBridge 用信用流控，MAPE 为 **8.65%**。4 MB tree AllReduce、BER (10^{-8})、50 GB/s 争用流量下，关掉 PEX 机制后误差可到 **82%**。中等消息（16 KB–1 MB）误差主要来自未建模的 NCCL 软件开销（chunk DMA、fence、nProc 屏障）。

代理保真（860 组：8/16 GPU，多种 AllReduce / AlltoAll，4 KB–256 MB，不同信用、BER、FEC 与重传）：

- 该集合上代理 MAPE **13.4%**，延迟-带宽模型 **60.6%**，随机森林 / XGBoost / MLP 为 30.7% / 38.4% / 28.3%。
- 95% 预测误差小于 **34.9%**，正确排序 **87.8%** 的候选对。
- 按代理排序再跑包级仿真，平均仿真 **31.6%** 的候选即可找到最低延迟设计；延迟-带宽模型需要 **99.2%**。
- 相对 SimAI（解析通信后端）在 DeepSeek-V3 多种并行与 batch 上，TGS / TTFT / TPOT 端到端 MAPE 为 **4.5–7.9%**；代理约 **21 µs**/操作，SimAI 约 **16 ms**。摘要给出的总括数字是 MAPE **55.7%→11.8%**、**20.5 µs**/操作。

设计探索覆盖 531 种互连与 72 种差错处理，共 **38,232** 点。内存池案例：128 张 H200，DeepSeek-V3 / GLM-5.2 / Qwen3-235B，百万 token 上下文。GLM-5.2 的帕累托前沿上，内存池点都用 HBF。G1 点用 128/128 分预填充与 decode、八副本、张量并行 16，并挂 46 节点 HBF KV 池到 rail-optimized 胖树，交互性与 TGS 均为 **1.31×**。GLM-5.2 的 78 层里有 75 层用稀疏注意力，百万上下文下每层只读选出的 2,048 个 token 和索引摘要，约占稀疏层 KV 的 **0.54%**。该案例用 15% 交互性/TGS 阈值覆盖全部真实帕累托点，总运行 **58** 分钟（代理 51 分钟、包级精修 7 分钟）。

CPO 案例：相对光电互连，每 GPU **128×800 Gb/s**、预 FEC BER (10^{-9}) 时，GLM-5.2 的三次 prefill 通信加快 **3.55–24.8×**，decode 通信为 **0.99–1.40×**；增加通道数后 decode AlltoAll 有 **39%** 改进（64/128 通道走到二维全互连）。Table V 服务延迟：

| 模型 | TTFT (s) 光电 → CPO | TPOT (ms) 光电 → CPO |
|---|---|---|
| DeepSeek-V3 | 63.49 → 63.22 | 24.75 → 24.02 |
| GLM-5.2 | 3.834 → 3.543 | 9.252 → 8.386 |
| Qwen3-235B | 39.10 → 38.85 | 12.79 → 13.11 |

TTFT 降低 **0.42–7.58%**；DeepSeek-V3 / GLM-5.2 的 TPOT 降低 **2.93% / 9.36%**，Qwen3-235B 的 TPOT 升高 **2.50%**。作者写明 prefill 仍偏计算受限，所以通信加快之后 TTFT 只小幅下降。

## 局限与解读
- H200 / C500 的误差是集体通信对照；超节点扫描、内存池与 CPO 的服务数字来自代理加包级精修，不是完整超节点硬件测量。
- 中等消息的误差来自未进入协议层的 NCCL 软件开销。
- CPO 的 decode 收益对延迟和差错处理敏感，Qwen3-235B 的 TPOT 在该配置下升高。
- 内存池的 1.31× 出现在 GLM-5.2 的稀疏注意力设置里，稠密层会在每次注意力时等待池读取。

## 与 wiki 的关系
- [ScaleWire](/papers/scalewire-scale-up-ethernet-simulation.md) — 面向开放 scale-up Ethernet 网卡机制与片上缓存；ProtoBridge 校准的是 NVLink / MetaXLink 协议栈，并扫 CPO 与内存池
- [XM-Sparse](/papers/xm-sparse-scale-up-memory-pool.md) — 把稀疏注意力卸到 scale-up 内存池并在仿真池上测吞吐；ProtoBridge 在 128 卡探索里给出 HBF KV 池对稀疏模型 TGS 的设计结论
- [SURMA](/papers/surma-scale-up-rma-engine.md) — scale-up RMA 引擎的 FPGA/GPU 对照；ProtoBridge 补的是协议与拓扑的包级设计空间
- [NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — H200 与 NVL72 对照落在这条织物上
- [NVIDIA CPO Roadmap](/concepts/nvidia-cpo-roadmap.md) — CPO 案例把通道数、BER 和 decode 延迟写进同一条探索流程

# Citations
- [arXiv:2611.30191](https://arxiv.org/abs/2611.30191) — Zhu 等，HPCA 2027
- [raw stub](/raw/papers/protobridge-superpod-interconnect-sim.md)
- [PDF](/raw/papers/ProtoBridge_LLM_to_Packet_Superpod_2026.pdf)
