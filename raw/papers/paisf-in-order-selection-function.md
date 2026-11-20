---
type: Raw Source
title: "PAISF: A Partially Adaptive In-Order Selection Function for Routing in On-Chip, Inter-Chiplet, and Wafer-Scale Networks"
source_url: https://arxiv.org/abs/2611.22772
pdf: PAISF_In_Order_Selection_Function_2026.pdf
retrieved: 2026-11-20
ingested: 2026-11-20
org: ETH Zurich
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.22772)

The growing number of compute elements per chip, along with advances such as chiplet systems and wafer-scale integration, drives the need for scalable and efficient routing algorithms for irregular topologies. A routing algorithm consists of a routing function (RF) that ensures deadlock freedom and a selection function (SF) that avoids congestion and, in some cases, guarantees in-order packet delivery. We propose two novel SFs for irregular topologies, ISF and PAISF, which ensure in-order delivery by hashing a packet’s entropy value to determine its path. Packets with the same entropy follow the same path and arrive in order. Compared to a deterministic RF, a deterministic SF, and Multi, three alternative in-order delivery strategies, (PA)ISF improves throughput by 15.2% and reduces energy per packet and latency under load by 12.1% and 11.3%, at the cost of a zero-load latency increase by 3.3% on average across workloads and topologies.

# Excerpts / key facts

- Authors: Patrick Iff, Luca Oertig, Andrin Weber, Luca Benini, Torsten Hoefler（ETH Zurich）。arXiv:2611.22772，cs.AR / cs.NI，提交标注 17 Nov 2026。预印本。
- 评测栈：周期精确 BookSim2，每组 3 次；Orion3（45 nm）经 DeepScaleTool 缩放到 7 nm，链路 0.1 pJ/bit/mm。延迟算术均值、吞吐调和均值、相对性能几何均值；非参数 95% bootstrap CI，平均相对半宽吞吐 15.80%、延迟 2.82%。
- 默认参数：每消息 16 包、每包 4 flit，50% 保序；1 GHz；NoC/ICI 64-bit flit，WSI 16-kbit flit（对标 Dojo 2 TB/s）；路由器 3 周期；4 VC；缓冲 8/16/32 flit；ICI 另加 4 周期 PHY。
- 域分解：NoC 吞吐 +18.9%；ICI-P +15.1%；ICI-A +18.9%；WSI +7.8%，且注入率 0.1 时延迟 +1.2%。CPU 轨迹延迟 −12.2%；GPU 轨迹相对 LASH-TOR −3.8%。
