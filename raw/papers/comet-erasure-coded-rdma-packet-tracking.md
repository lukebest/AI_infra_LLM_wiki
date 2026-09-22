---
type: Raw Source
title: "Scalable Packet Tracking on FPGAs for Erasure-Coded RDMA over Lossy WANs"
description: "COMET 原始论文来源：纠删码 RDMA over WAN 的 FPGA 包到达追踪数据路径。"
timestamp: '2026-09-22T00:00:00Z'
source_url: https://arxiv.org/abs/2609.21774
arxiv: '2609.21774'
ingested: 2026-09-22
sha256: 0c4aa8d2aa118593bdaa79bb36c5490ab4041be3e60b191c704cb0113c65c70e
---

# COMET: FPGA Packet Tracking for Erasure-Coded RDMA over WAN

**Authors:** Yicheng Qian, Konstantin Taranov, Yevgeny Yankilevich, Assaf Shacham, Mahmoud Elhaddad, Abdul Kabbani, Miriam Leeser, Nadeen Gebara  
**Affiliation:** Northeastern University; Microsoft  
**PDF:** [COMET_Erasure_Coded_RDMA_WAN_2026.pdf](COMET_Erasure_Coded_RDMA_WAN_2026.pdf)  
**arXiv:** [2609.21774](https://arxiv.org/abs/2609.21774)（2026-09-18，cs.AR）

## 问题

跨数据中心 scale-across 把 RDMA 带进高 RTT、丢包、乱序 WAN；传统 packet-arrival bitmap 的状态随 BDP 增长，FPGA NIC 很快被片上 SRAM 与 read-modify-write hazard 限住。

## 方法要点

- 多路径 `(n,k)` erasure-code stripe；每路径独立 `eStripe`，把状态上界从 BDP 改写为 bandwidth-jitter product。
- COMET Cache 不记录每个已到包，而记录稀疏丢包；set-associative Data Manager 与 Completion Manager 解耦并行。
- SystemVerilog 实现于 Intel Agilex 7 FPGA SmartNIC。

## 摘录数字（仅论文给出）

- 4 KiB MTU 下达到 **400 Gb/s**；8 路配置按 post-layout Fmax 推导可超过 **1.6 Tb/s**。
- 8 路/16 路实现均占 FPGA ALM 与 M20K **<1%**。
- 0.5 ms jitter、3 MiB 状态预算下，连接数为 SDR-RDMA 的 **6×**、传统 bitmap 的 **57×**。

**Working page:** [COMET](/papers/comet-erasure-coded-rdma-packet-tracking.md)  
**Related:** [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md)
