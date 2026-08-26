---
type: Paper
title: "Hot Chips 2026: AMD Helios UALoE"
description: AMD — Helios 72-GPU rack；UALoE load-store / Ethernet ESUN；1.8 TB/s/dir per GPU；Vulcano 跑 MRC/UEC；12-plane 故障隔离
tags:
- amd
- gpu
- scale-up
- ualink
- ualoe
- fabric
- protocol
- rack
- interconnect
- rdma
- switch
- architecture
- training
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_AMD_Helios_UALoE.pdf
- raw/papers/hc2026-amd-helios-ualoe.md
---

# System Architecture of the AMD MI400 Series GPU（Helios / UALoE）

**Speakers:** Steve Scott, David Riddoch, Krishna Doddapaneni（AMD）  
**Venue:** Hot Chips 2026 Conference  
**PDF:** [raw/papers/HC2026_AMD_Helios_UALoE.pdf](raw/papers/HC2026_AMD_Helios_UALoE.pdf)

72-GPU 以太网 scale-up。芯片数字见 [MI455X](/papers/hc2026-amd-instinct-mi455x.md)。对照 [Rubin NVLink 6](/papers/hc2026-nvidia-rubin.md) 的 **3.6 TB/s all-to-all / 130 TFLOPS in-network**。Vulcano 接到已有 [MRC](/entities/mrc.md)。

## 三件套与 rack

EPYC “Venice” **96** high-frequency cores、PCIe **Gen6**、CPU memory BW **1.6 TB/s**；Instinct MI455 **40 PF** FP4、**432 GB** HBM4、**23.3 TB/s**；Pensando “Vulcano” **800 Gbps**、**200M** packets/s。

Scale-up pod：switched topology；「scale driven by electrical signaling; nearing optical transition」。Scale-up IFoE/UALoE **1.8 TB/s/dir per GPU**；**72× IFoE @ 200G**。Infinity Fabric **8 @ 128G**。Scale-out Ethernet 「up to **2.4 Tb/s/dir per GPU**」。「Shared Load/Store Access Across Pod」。

Helios rack：**72 GPUs**；**31 TB** HBM4；**260 TB/s** scale-up；**2.9 Exaflops**；**1.7 PB/s** HBM4 BW；**43 TB/s** scale-out。机械：**44OU, ORW-HPR**；**18× 1OU** compute trays；**6× 1OU** switch trays；**4×** cable cartridges；**50vDC** LC busbar。

Compute tray：**4×** MI455X EAM；**12× 3×2** UALoE links per EAM；**1×** Venice SP7；每 EAM 最多 **3×** Vulcano，UALink x8（**128 GB/s/dir per NIC**）；IF to CPU **128 GB/s/dir per GPU**。

Switch tray：**2× 512-port 200G UALoE Switch ASICs**；**72× 3×2** UALoE active links per ASIC；**10.8 TB/s/dir per Switch**；UALoE multi-plane。Pod 图标 **Switch 1 … Switch 12**（6 trays × 2 ASICs）。液冷「**~7kW** infrastructure」。

## UALoE 栈

Application → runtime → programming model → **shared memory fabric** → **UALoE Transport** → **Ethernet, ESUN**。分布式共享内存：memory-registration keys + mmap；load/store fabric「spanning the whole Helios rack」。「Built on open Ethernet and ESUN standards and **Broadcom switches**」。

每 MI455X：**18× 800 Gbps** 集成 UALoE adapters。Transport：lightweight reliable scale-up；dynamic packing；**Ethernet PFC**；丢包恢复 = **link-layer replay** *或* **end-to-end retransmission**；链路/交换故障 → 在 **alternative network plane** 重传。

安全：rack-scale confidential computing；SEV-SNP；DICE；universal link encryption；UALoE 端到端包加密且 **switch outside TCB**。脚注：MI455X「hardware limitation may result in loss of Integrity guarantees with a malicious hypervisor」。

## VPod / AFM / Vulcano

VPods：节点子集隔离。故障弹性（**12 UALoE links ×2**）：单链路 → 只打本地 VPod；丢 1/12 switch → DMA 走 11/12；整盘 switch tray 丢 → DMA 走 5/6 trays。AFM：**3-node cluster on scale-up switches**；活过 1 故障；双故障只读。

Vulcano 800：P4，**192 MPU**；**UAL128 x8** + **PCIe Gen6 x16**；P4DMA 跑 RoCEv2 / **MRC** / **UEC**。Transport 演进：RoCEv2 → MRC window/lossy → MRC/UEC multipath + SACK → MRC multiplane → 「Mega Scale Source Routing」。

MRC 性能表（msg **≥64KB**，**1–4K QPs**）：**1×800G / 2×400G / 4×200G / 8×100G** 全是 **800G Tx / 800G Rx**。All-reduce 图称 MRC QP1 打过 RoCEv2 QP1–16，含 **1% drop**（逐 size 数字 **未知**）。收束：「**72 GPUs operate as a unified compute engine**」；shared-memory ld/st「over **30TB** of HBM4 at **1.8 TB/s/dir** per GPU」。

# Citations

[1] [raw/papers/HC2026_AMD_Helios_UALoE.pdf](raw/papers/HC2026_AMD_Helios_UALoE.pdf) — Scott / Riddoch / Doddapaneni, Hot Chips 2026
[2] [raw/papers/hc2026-amd-helios-ualoe.md](raw/papers/hc2026-amd-helios-ualoe.md) — 结构化摘录
