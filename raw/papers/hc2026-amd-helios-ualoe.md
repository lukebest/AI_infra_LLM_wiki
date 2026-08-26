---
type: Raw Source
title: Hot Chips 2026 AMD Helios UALoE
ingested: 2026-08-26
sha256: 84b171df4250cc4e8d7322e42d717497b5fb631cbdf45e8b660ec45befe706b5
venue: Hot Chips 2026 Conference
---

# System Architecture of the AMD MI400 Series GPU（Helios / UALoE）

**Speakers:** Steve Scott, David Riddoch, Krishna Doddapaneni（AMD）  
**PDF:** [HC2026_AMD_Helios_UALoE.pdf](HC2026_AMD_Helios_UALoE.pdf)  
**Venue:** Hot Chips 2026 Conference

## 摘录数字（仅幻灯片正文）

- Venice **96** cores；CPU BW **1.6 TB/s**；MI455 **40 PF** FP4、**432 GB** / **23.3 TB/s**；Vulcano **800 Gbps**、**200M** pps。
- UALoE **1.8 TB/s/dir per GPU**；**72× IFoE @ 200G**。SO 「up to **2.4 Tb/s/dir per GPU**」。
- Rack：**72** GPU；**31 TB**；**260 TB/s** SU；**2.9 Exaflops**；**1.7 PB/s**；**43 TB/s** SO。**18** compute + **6** switch trays。
- Switch ASIC：**512-port 200G**；**10.8 TB/s/dir**；**Switch 1…12**。每 GPU **18× 800 Gbps** UALoE adapters。
- Vulcano：P4 **192 MPU**；RoCEv2 / MRC / UEC。MRC ≥64KB：**800G Tx / 800G Rx** across 1×800 / 2×400 / 4×200 / 8×100。All-reduce 逐 size 未知。
