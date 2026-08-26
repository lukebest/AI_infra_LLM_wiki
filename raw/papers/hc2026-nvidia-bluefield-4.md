---
type: Raw Source
title: Hot Chips 2026 NVIDIA BlueField-4
ingested: 2026-08-26
sha256: bd753118fcb9e630a553029de03c30738f2d5d8cf780667d245858d9f84eeb4b
venue: Hot Chips 2026
---

# NVIDIA BlueField-4 Processor Powers the AI Factory

**Speaker:** Idan Burstein（NVIDIA）  
**PDF:** [HC2026_NVIDIA_BlueField_4.pdf](HC2026_NVIDIA_BlueField_4.pdf)  
**Venue:** Hot Chips 2026 Day 2

小包图表逐点 **未知**。

## 摘录数字（仅幻灯片正文）

- Cloud DPU **200 Gb/s** vs AI DPU **7200 Gb/s**。
- Grace：SPECINT **220 (6× BF3)**；LPDDR5 **275 GB/s**；**64** Neoverse V2 @ **1.7 GHz**。
- ConnectX-9：**800G** Ethernet；200G PAM4；PCIe Gen6 x16；**200 MPPS**；**25 MIOPs**。
- Compute tray：4× 1.6 Tb/s GPU SO + 800 Gb/s scale-in = **7200 Gb/s**。Astra 把多 CX-9 接到一颗 Grace。
- 实测平均 BW 随 NIC 线性到 **7.0 Tb/s @ 8 NIC**。NVMe-oF：**8 cores / 1.6 Tb/s**；**16 cores / 20 M IOPS**。
- Storage-Scale：**3.2 Tb/s**；×10 IOPS；×5 efficiency。
