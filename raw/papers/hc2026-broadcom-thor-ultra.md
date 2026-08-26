---
type: Raw Source
title: Hot Chips 2026 Broadcom Thor Ultra
ingested: 2026-08-26
sha256: 52eb05017bfbd6d54948aee2cf6afb51a0c009de4655db4695330f09bf6b0301
venue: Hot Chips 2026
---

# Thor Ultra Ethernet NIC for AI and HPC

**Speaker:** Hemal Shah（Broadcom）  
**PDF:** [HC2026_Broadcom_Thor_Ultra.pdf](HC2026_Broadcom_Thor_Ultra.pdf)  
**Venue:** Hot Chips 2026 Day 2

## 摘录数字（仅幻灯片正文）

- **800G** NIC；host PCIe Gen6 x16；SR-IOV **256 VF**；8× 100G PAM4/NRZ。芯片 **5 nm**，**2.4B+** 管；pkg **27×27**；芯片功耗 **40–42 W**；板（无光）**50–55 W**。
- eRoCE = MRC++：**64K+ QP**；最多 **8 plane** spray；RCCC 基线。
- 集体（Gen5 GPU，2 node × 8 GPU，16×400G）：all_gather **381.92 GB/s @ 8 GB**（ceil 400）；all_reduce **383.93 @ 2 GB**；alltoall **84.62 @ 8 GB**（93）；reduce_scatter **380.23 @ 2 GB**。gather/reduce/RS **>96%**。
- RDMA write：uni **781 Gbps (97.6% of 800G)**；bi **1558 Gbps (97.9% of 1.6 Tb/s)**。
