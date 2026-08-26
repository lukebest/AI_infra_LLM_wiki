---
type: Paper
title: "Hot Chips 2026: AMD Instinct MI455X"
description: AMD — MI455X chiplets；N2 XCD 3D hybrid bond + N3P FCD/IOD；12× HBM4 432 GB / 23.3 TB/s；UALoE 3.6 TB/s bi-dir；MXFP4 40.26 PF
tags:
- amd
- gpu
- accelerator
- chiplet
- hbm
- scale-up
- ualink
- ualoe
- hybrid-bonding
- architecture
- training
- inference
- quantization
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_AMD_Instinct_MI455X.pdf
- raw/papers/hc2026-amd-instinct-mi455x.md
---

# AMD Instinct MI400 Series GPU Architecture（MI455X）

**Speakers:** Alan Smith, Maiyuran Subramaniam（AMD）  
**Venue:** Hot Chips 2026 Conference  
**PDF:** [raw/papers/HC2026_AMD_Instinct_MI455X.pdf](raw/papers/HC2026_AMD_Instinct_MI455X.pdf)

芯片拆解。系统见同日 [Helios / UALoE](/papers/hc2026-amd-helios-ualoe.md)。对照 [Rubin NVLink 6](/papers/hc2026-nvidia-rubin.md)。封装落到 [Hybrid Bonding](/papers/hybrid-bonding-3d-integration-recent.md) 与 [DRAM](/concepts/dram-memory-system.md)。

## Helios 一页摘要

**72 GPUs**/rack；**2.9 Exaflops** AI compute；**31 TB** HBM4；**1.7 PB/s** HBM4 bandwidth；**260 TB/s** scale-up；**43 TB/s** scale-out。Compute tray：**4** Instinct **MI455X** EAM；单路 EPYC **9006 SP7**（Venice）；**36 UALoE links (x2) per EAM**；UALoE **1.8 TB/s/dir per GPU**；Infinity Fabric to CPU **128 GB/s/dir per GPU**；每 EAM 最多 **3×** Pensando Vulcano **800** AI NIC，经 **UALink128 (x8)**、**128 GB/s/dir per NIC**。

## MI455X chiplets

- **2× FCD, N3P** — **192-channel** HBM4；**192 MB** Global L2
- **2× IOD, N3P** — **2× PCIe Gen6** *或* **3×** AI-NICs via UALink；Infinity Fabric **256 GB/s** bi-dir；**72 UALoE lanes, 3.6 TB/s** bi-dir
- **8× XCD, N2** — **256** total active Work Group Processors
- **12× HBM4** — **432 GB** at **23.3 TB/s**

封装：3D hybrid-bonded XCDs；CoWoS-L；SOIC + HBM4。概念 SoC 框图页几乎无字（**未知**）。**slide 上 192 MB Global L2 与 vs-MI355X 的 96 MB L2 都在片上**；暂按 2×96 MB FCD 读。

Cache vs MI355X：VGPR **128 KB** 不变，标 **2.0× VGPR per SIMD**；scalar **8 KB** vs **3.2 KB**；LDS **384 KB** vs **160 KB**（**2.0× LDS per WGP/CU**）；L2 **96 MB** vs **4 MB** L2 + **256 MB** Infinity Cache（**1.5× per L2 vs Cache**）；HBM **432 GB HBM4** vs **288 GB HBM3E**（**2.9× total HBM**）。Broadcast arbitrator：「up to **4×** BW amplification」。

## 算力与效率

Peak vs MI355X（AMD Performance Labs, June 2026，endnote MI400-006）：OCP MXFP4 **40.26 PF**（up to **4X**）；OCP MXFP6 **20.13 PF**（up to **2X**）；OCP MXFP8/FP8 **20.13 PF**（up to **4X**）；Matrix FP16/BF16 **5.03 PF**（up to **2X**）；Vector FP16 **315 TF**（up to **2X**）；Matrix/Vector FP32 **315 TF**（up to **2X**）。MXFP8/6/4，block-scale **16/32**；native **Wave32**。

效率：Tensor Data Mover（async Global↔LDS）；work-group cluster + L2 multicast + L2 prefetch；split/named barriers。每 GPU 专用 DMA：topology-aware，流量自动亲和 UALoE，「software … oblivious to data placement」；「scales across **72 GPUs**」。

实测 vs MI355X（ROCm.ai，July 2026）：MLA decode FP8 **20 TB/s**（**3.8×**，单卡）；FP4 compute **20 PF**（**3.3×**，单卡 AITER GEMM）；scale-up BW **3.2 TB/s**（**3.5×**，**4× MI455X vs 8× MI355X**，16 GB transfer）；scale-out BW **190 GB/s**（**2×**，Vulcano 800 vs Pollara 400）。能耗：estimated **2.4×** AI energy efficiency vs MI355X；2030 目标 rack-scale efficiency **20×**。单卡 TDP / 时钟：**未知**。

# Citations

[1] [raw/papers/HC2026_AMD_Instinct_MI455X.pdf](raw/papers/HC2026_AMD_Instinct_MI455X.pdf) — Smith / Subramaniam, Hot Chips 2026
[2] [raw/papers/hc2026-amd-instinct-mi455x.md](raw/papers/hc2026-amd-instinct-mi455x.md) — 结构化摘录
