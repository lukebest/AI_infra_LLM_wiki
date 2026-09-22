---
type: Paper
title: "COMET: 丢包 WAN 上纠删码 RDMA 的 FPGA 包追踪"
description: "以每路径 eStripe 和稀疏 loss tracking 取代 BDP 级到包 bitmap，在 Agilex 7 上实现 400 Gb/s，资源占用低于 1%。"
tags:
- architecture
- networking
- interconnect
- accelerator
- memory
- rdma
- transport
- hardware
created: 2026-09-22
updated: 2026-09-22
timestamp: '2026-09-22T00:00:00Z'
paper_author: [Yicheng Qian, Konstantin Taranov, Yevgeny Yankilevich, Assaf Shacham, Mahmoud Elhaddad, Abdul Kabbani, Miriam Leeser, Nadeen Gebara]
year: 2026
arxiv: '2609.21774'
sources:
  - raw/papers/COMET_Erasure_Coded_RDMA_WAN_2026.pdf
  - raw/papers/comet-erasure-coded-rdma-packet-tracking.md
---

# COMET：丢包 WAN 上纠删码 RDMA 的 FPGA 包追踪

## 一句话结论

COMET 发现跨数据中心 RDMA 的包追踪状态不必按 bandwidth-delay product（BDP）增长：纠删码流量可按路径维护短 `eStripe`，并只缓存稀疏丢包。Agilex 7 FPGA 实现达到 **400 Gb/s**，8/16 路版本 ALM 与 M20K 均 **<1%**；0.5 ms jitter、3 MiB 状态预算下，支持连接数是 SDR-RDMA 的 **6×**、传统 bitmap 的 **57×**。

## 动机：scale-across 的 BDP 吃掉 NIC SRAM

跨地域训练/推理希望用 RDMA 直接搬 GPU memory，但 WAN 同时具有高 RTT、乱序与丢包。Selective Repeat 常为每连接维护覆盖整个 in-flight window 的 packet bitmap；100 Gb/s、200 ms RTT、2 KiB MTU 的单连接就需要约 **1.22 MiB** 状态。状态随 BDP 与连接数相乘，FPGA NIC 片上 memory 和每包 read-modify-write 都难以扩展。

## 方案

### 1. 用 erasure stripe 缩短追踪窗口

发送端把每个 `(n,k)` stripe 的编码包分散到多条独立路径。每路径只需维护一个 `eStripe`，覆盖从最早未完成 stripe 到当前 stripe 的短窗口。状态上界从端到端 BDP 转为 bandwidth-jitter product，因为 path delay 差异只造成短时乱序。

### 2. 记录丢失而不是记录到达

COMET Cache 不为每个已到包置 bitmap bit，而只在检测到序号 gap 时写入 loss record；正常到达路径无需读状态。Data Manager 采用 set-associative SRAM，Completion Manager 用小型 heap 保持 stripe completion 顺序。两者解耦、并行处理，规避单存储体 read-modify-write hazard。

### 3. FPGA 数据路径

设计以 SystemVerilog 实现并映射到 Intel Agilex 7。每路处理一个 packet/cycle，多路可线性复制；论文评估 8 路与 16 路配置，并把 tracking 单元放在 RDMA receive/data path 中。

## 量化结果

- **吞吐**：4 KiB MTU 时实现在目标板达到 **400 Gb/s**；按 post-layout Fmax 推导，8 路配置可超过 **1.6 Tb/s**，16 路约 **1.2 Tb/s**。
- **资源**：8 路与 16 路均消耗 FPGA ALM、register、M20K 的 **<1%**。
- **状态扩展性**：3 MiB memory、0.5 ms jitter 下，COMET 连接数为 SDR-RDMA 的 **6×**、传统 bitmap 的 **57×**；论文也报告相对 selective-repeat bitmap 的 tracking state 最高降低 **250.25×**。
- **时延**：COMET 额外增加的 tracking pipeline latency 约 **80 ns**。

## 局限与解读

- 400 Gb/s 是目标板实现；1.6 Tb/s 是依据 post-layout Fmax 和并行路数的推导值，不是完整 NIC 的实流量测量。
- 论文核心是 packet tracking，不含完整 erasure-code encoder/decoder、congestion control 或 end-to-end GPU training benchmark。
- 稀疏 loss tracking 的收益依赖丢包稀少；高 burst loss 会增加 COMET Cache 压力。

COMET 对 [Interconnection Network Protocol Stack](../concepts/interconnection-network-protocol-stack.md) 的价值，是把 transport reliability 状态重新编码成适合 FPGA 并行数据面的形式；它与 [Meta's RoCE Networks for Distributed AI Training at Scale](rdma-over-ethernet-meta-training.md) 讨论的单数据中心 RoCE 不同，面向 lossy WAN 和 scale-across。其片上状态权衡也可与 [SRAM](../concepts/memory-hierarchy-cache.md) 一起理解。

# Citations

1. Qian, Y., Taranov, K., Yankilevich, Y., et al. “Scalable Packet Tracking on FPGAs for Erasure-Coded RDMA over Lossy WANs.” arXiv:2609.21774, 2026. [arXiv](https://arxiv.org/abs/2609.21774)
2. [本地原文 PDF](../raw/papers/COMET_Erasure_Coded_RDMA_WAN_2026.pdf)；[原始来源记录](../raw/papers/comet-erasure-coded-rdma-packet-tracking.md)
