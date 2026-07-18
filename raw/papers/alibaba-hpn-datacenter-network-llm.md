---
type: Raw Source
title: 'Alibaba HPN: A Data Center Network for Large Language Model Training'
source_path: /home/luke/wiki/raw/papers/Alibaba_HPN_Datacenter_Network_LLM_Training_2024.pdf
doi: '10.1145/3651890.3672265'
zotero: NCXPMX2X
ingested: 2026-07-17
sha256: 42faa880dfce3824ed628b4a31c6cb2d101d94dfc57a44e5e5f1b31b1075bbbc
---

# Alibaba HPN: A Data Center Network for Large Language Model Training

Authors: Kun Qian, Yongqing Xi, Jiamin Cao, Jiaqi Gao, et al. (Alibaba Cloud)
Venue: ACM SIGCOMM 2024 | DOI: 10.1145/3651890.3672265

Structured notes / key excerpts:

- **Problems vs general cloud**: (1) LLM training = few periodic **400Gbps** bursty flows, low entropy → ECMP hash polarization. (2) Synchronous training → ToR single-point failure costly (**20×** vs general cloud fault cost).
- **HPN architecture**: **2-tier dual-plane** interconnecting **15K GPUs**/Pod (vs traditional 3-tier Clos); reduces ECMP search space 1–2 orders of magnitude.
- **Non-stacked dual-ToR**: Two independent ToRs per rack (not vendor stacked dual-ToR) — eliminates switch sync, improves reliability.
- **Rail-optimized + 51.2Tbps chip**: **1K GPUs** in tier-1; **96.3%** jobs get best network perf.
- **Traffic**: DP AllReduce, PP stage handoff, TP AllReduce/AllGather; bursts in backward gradient sync.
- **Deployment**: **8+ months** production; no ToR single-node failures observed; **+14.9%** LLM training throughput vs traditional DCN.
- **Choice**: Ethernet over InfiniBand (avoid lock-in, Ethernet Alliance evolution).
