---
type: Raw Source
title: "PCM: Programmable Congestion Management for Terabit RDMA NICs"
source_url: https://arxiv.org/abs/2610.13130
pdf: PCM_Programmable_Congestion_Management_RDMA_NIC_2026.pdf
retrieved: 2026-10-13
org: ETH Zürich / Broadcom / Microsoft / UCLM
venue: arXiv preprint (cs.NI)
---

# Abstract (verbatim, arXiv:2610.13130)

Datacenter congestion control (CC) and load balancing (LB) evolve rapidly as workload demands change, but deployment depends on RDMA hardware and transport interfaces. Emerging programmable RDMA engines tie policy code to vendor APIs. Operators must therefore port each policy for every platform they deploy. We address this with PCM, a programming model that separates portable congestion management from platform integration on datacenter NICs. Developers write event-driven handlers that they can debug in simulation and reuse on real hardware. PCM exposes flow telemetry as signals and uses triggers to support per-event reactions and coarser responses to accumulated feedback. Vendors provide optimized backends that map signals and output controls to native NIC mechanisms with defined feedback and control semantics. We demonstrate PCM's expressivity by implementing eleven well-known datacenter CC and LB algorithms. We deploy PCM across four distinct datapaths: an Ultra Ethernet simulator, CPU-based UCCL, and on-NIC offloads on NVIDIA ConnectX-8 and Microsoft 1P. On CX-8, PCM-Swift achieves processing capacity equivalent to one reaction per three 4 KiB packets at 800 Gbit/s, using one-fifth of the NIC's hardware threads. In UCCL, it matches native Swift's 1.56 Tbit/s goodput with 64 KiB chunk-level control. PCM's design informed ongoing Ultra Ethernet work toward a portable congestion management interface.
