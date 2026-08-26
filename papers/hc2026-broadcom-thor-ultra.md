---
type: Paper
title: "Hot Chips 2026: Broadcom Thor Ultra"
description: Broadcom — 800G eRoCE/MRC++ NIC；最多 8-plane spray；RCCC；RDMA write 781 Gbps（97.6% of 800G）
tags:
- broadcom
- rdma
- protocol
- congestion-control
- scale-out
- interconnect
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Broadcom_Thor_Ultra.pdf
- raw/papers/hc2026-broadcom-thor-ultra.md
---

# Thor Ultra Ethernet NIC for AI and HPC

**Speaker:** Hemal Shah（Broadcom, Distinguished Engineer）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_Broadcom_Thor_Ultra.pdf](raw/papers/HC2026_Broadcom_Thor_Ultra.pdf)

商用 800G NIC，把 [MRC](/entities/mrc.md) 做成 eRoCE。对照 [Spectrum-X Multiplane](/papers/hc2026-nvidia-spectrum-x-multiplane.md) 与 [Helios UALoE](/papers/hc2026-amd-helios-ualoe.md)。

## 硅

**800G** NIC；host **PCIe Gen6 x16**；SR-IOV **256 VF**；网侧 **8× 100G PAM4/NRZ**。端口：OSFP112 1×800 / 2×400 / 4×200 / 8×100；双 QSFP112。芯片 **5 nm**，**2.4B+** 管；pkg **27×27**；芯片功耗 **40–42 W**；板（无光）**50–55 W**。板型 HHHL / OCP NIC 3.0 TSFF。

## eRoCE = MRC++

**64K+ QP**；packet spray + OOO placement；SACK/NACK、选择性重传、path probe。基线 **receiver-credit congestion control (RCCC)** + P4-like 可编程 CC；遥测 ECN / trim / CSIG。Spray 最多 **8 planes**。OOO：Write & Read response 可乱序落；Send / Read Request / Atomic 保序。

Peer memory：eRoCE 远端 + Linux dma-buf 本地 P2P（GPU/XPU 无关）。集体走上游 verbs + xCCL 插件，不改应用。

## 数字

Gen5 GPU 平台（2 node × 8 GPU，16 rank，16×400G）：all_gather **381.92 GB/s @ 8 GB**（ceil 400）；all_reduce **383.93 @ 2 GB**；alltoall **84.62 @ 8 GB**（93）；reduce_scatter **380.23 @ 2 GB**。gather/reduce/RS **>96%**。

TCP（Gen6 CPU）：uni **791 Gbps @ 16 flows = 98.9%** of 800G。RDMA write：uni **781 Gbps (97.6%)**；bi **1558 Gbps (97.9% of 1.6 Tb/s)**；32 KB 已 ~88% 线速。

## 与 wiki 的关系

- [MRC](/entities/mrc.md) — 商用 NIC 落地
- [Spectrum-X Multiplane](/papers/hc2026-nvidia-spectrum-x-multiplane.md) — 8-plane 工厂侧
- [OpenAI Jalapeño](/papers/hc2026-openai-jalapeno.md) — 同场 Broadcom 交换/网卡伙伴

# Citations

[1] [raw/papers/HC2026_Broadcom_Thor_Ultra.pdf](raw/papers/HC2026_Broadcom_Thor_Ultra.pdf) — Shah, Hot Chips 2026
[2] [raw/papers/hc2026-broadcom-thor-ultra.md](raw/papers/hc2026-broadcom-thor-ultra.md) — 结构化摘录
