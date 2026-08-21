---
type: Raw Source
title: HCCL Collective Communication for Meta MTIA 300
source_url: https://arxiv.org/abs/2608.00358
arxiv: '2608.00358'
ingested: 2026-08-21
sha256: f9a1bef4da9df7346246bfc63f060e38ce37765ef6922912e8d1d135f3a9ba3c
---

# HCCL: Collective Communication for Meta Training and Inference Accelerators

**Authors:** Wesley Bland, Lars Paul Huse, Chidambaram Muthu 等（Meta Platforms）
**PDF:** [HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf](HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf)
**arXiv:** [2608.00358](https://arxiv.org/abs/2608.00358)
**Venue:** abs 写 to be published in SC '26。**未独立核实程序册。**

## 问题

NCCL/RCCL 把集体做成 GPU kernel，占 SM。MTIA 300 是 Meta 第一颗把 backend 网络做进封装的芯片（compute chiplet + 2 个 network chiplet），需要把集体完全卸到 message engine。

## 方法要点

- 每颗 2 组×8 ME；CPU-M 展开 compiled subgraph → WQE；NMC 做 line-rate 归约/拷贝（单输入 128 B/cycle，全开 96 B/cycle，合计 2.8 TB/s）。
- 每 network chiplet 6×800 Gb/s 定制 RDMA NIC；默认 8 NIC scale-up + 2 NIC scale-out = 1 TB/s，另留 2 NIC 可到 1.2 TB/s。
- Express doorbell：WQE 写即门铃。Host 编译 subgraph，ME 自治执行。
- 推理：one-sided PUT、AllToAllvDynamic、device-triggered 集体。

## 摘录数字（仅论文给出）

- 机柜内集体最高 **940 GB/s**；重叠 GEMM 吞吐降幅 **<0.5%**（约 1 TFlop）。
- 128-rank AllGather **838 GB/s**（scale-out 仅 200 GB/s）。
- 流水满后：H2D 17.1±0.3 μs，event 3.6±0.1 μs，CPU-C 2.9±0.1 μs，CPU-M 1.1±0.1 μs。
- PE 直发 RDMA Write 相对 ME 约 **450 ns** 静态开销；PUT 集体 AllToAllv/AllReduce **<6 μs**。
- 工作包缓存再入队 **<10 μs**。
