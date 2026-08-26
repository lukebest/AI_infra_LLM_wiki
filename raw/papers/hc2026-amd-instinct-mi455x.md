---
type: Raw Source
title: Hot Chips 2026 AMD Instinct MI455X
ingested: 2026-08-26
sha256: 0f8491d834f6637441c1c70417d9f5f79789fa803d32b75156235eaad43cf0f4
venue: Hot Chips 2026 Conference
---

# AMD Instinct MI400 Series GPU Architecture（MI455X）

**Speakers:** Alan Smith, Maiyuran Subramaniam（AMD）  
**PDF:** [HC2026_AMD_Instinct_MI455X.pdf](HC2026_AMD_Instinct_MI455X.pdf)  
**Venue:** Hot Chips 2026 Conference

## 摘录数字（仅幻灯片正文）

- Helios 摘要：**72** GPU；**2.9 Exaflops**；**31 TB** HBM4；**1.7 PB/s**；**260 TB/s** SU；**43 TB/s** SO。
- Chiplets：2× FCD N3P（**192-channel** HBM4，**192 MB** Global L2）；2× IOD N3P（**72 UALoE lanes, 3.6 TB/s** bi-dir）；8× XCD N2（**256** WGP）；**12× HBM4 432 GB @ 23.3 TB/s**。
- 192 MB Global L2 与 vs-MI355X 的 **96 MB L2** 都在片上。
- Peak：MXFP4 **40.26 PF**；MXFP6/MXFP8 **20.13 PF**；Matrix FP16/BF16 **5.03 PF**；Vector/Matrix FP32 **315 TF**。
- 实测 vs MI355X：MLA FP8 **20 TB/s**（**3.8×**）；FP4 **20 PF**（**3.3×**）；SU **3.2 TB/s**（**3.5×**）；SO **190 GB/s**（**2×**）。TDP/时钟未知。
