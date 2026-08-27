---
type: Raw Source
title: Maia 200 Software Defined Dataflow
source_url: https://arxiv.org/abs/2608.24664
arxiv: '2608.24664'
ingested: 2026-08-27
sha256: 2eacdd195c9501177a3c9a89e863380573d4f16dc742f62aaf455f2d030a7dbf
---

# Maia 200: A Software Defined Dataflow System for Large-scale AI Acceleration

**Authors:** Sherry Xu, Marco Heddes, Jackson Peng, Tom Savell, Monica Tang, Prashant Ranjan, Jesse Benson, Ofer Dekel, Saurabh Dighe, Anupama Kurpad, Artour Levin, Matthew Mattina, George Petre, Cheng Tang, Yuan Yu, Li Zhang, Torsten Hoefler  
**Affiliation:** Microsoft  
**PDF:** [Maia_200_Software_Defined_Dataflow_2026.pdf](Maia_200_Software_Defined_Dataflow_2026.pdf)  
**arXiv:** [2608.24664](https://arxiv.org/abs/2608.24664)  
**Submitted:** 2026-08-25 15:05 UTC

Hot Chips 2026 幻灯见 [hc2026-microsoft-maia-200.md](hc2026-microsoft-maia-200.md)。本页只摘**全文相对幻灯的增量数字**。

## 摘录数字（仅 PDF/HTML）

- 集群 **6144** SoC：最高 **62** exaflop/s FP4、**43 PiB/s** 内存带宽、**8.6 PiB/s** Ethernet。
- 相对 Microsoft 机队其他加速器：内部数据 **TCO −30%**、能量 **−15%**。
- 晶体管 **>140B**；die **26×33 mm**；19 层金属。
- SoC：4 cluster × 9 或 10 tile；tile **3 MiB** SRAM；TTU **65,536** FP4 MAC/cycle @ **2 GHz** → 每 TTU **262.14** Tflop/s FP4。
- 9 tile/cluster 打开：BF16 峰值 **1180** Tflop/s、FP8 **4785** Tflop/s；BF16 GEMM 计算界最高 **99.69%** 峰值、存储界最高 **51.4%** 峰值带宽；FP8 计算界 **96%** / 存储界 **56%**。
- **28×400G** ANC = **1.4 TB/s** 全双工；其中 **20** 固定链路 + **8** 接到 **4** plane 交换（每 plane 2×400G）。
- Hamming Mesh 特例：盘上全连接；T0 **51.2T**（128×400G）接 **48** SoC / **12** tray，余 **32** 口上 T1，过订阅 **1:3** → **48×128 = 6144**。
- ATLv2：receiver-driven RDMA；AES-GCM-256；selective retransmit；小消息交换路径约 **4 µs**。
- 8 芯两 tray Allgather：延迟界 **78%** SoL、带宽界 **94%** SoL。
- Qwen 2.5 7B decode（S=1，上下文 **16,384**，KV **939.52 MiB**）：**2434** token/s，>**70%** 估计上限。SRAM 占 die **<20%**；网络占系统成本 **<20%**。
