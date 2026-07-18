---
type: Raw Source
title: 'pHost: Distributed Near-Optimal Datacenter Transport Over Commodity Network Fabric'
source_path: /home/luke/wiki/raw/papers/pHost_Coflow_Aware_Packet_Scheduling_2015.pdf
doi: '10.1145/2716281.2836086'
zotero: 6Q8ERKZ5
ingested: 2026-07-17
sha256: 3cbbad0c1d4cb9798a22f75ab0bd3d4431aa4ef51c770b4c3b549bbf7e05321d
---

# pHost: Distributed Near-Optimal Datacenter Transport Over Commodity Network Fabric

Authors: Peter X. Gao, Akshay Narayan, Gautam Kumar, Rachit Agarwal, Sylvia Ratnasamy, Scott Shenker (UC Berkeley)
Venue: ACM CoNEXT 2015 | DOI: 10.1145/2716281.2836086

Structured notes / key excerpts:

- **Problem**: Minimize flow completion time (FCT) / slowdown in datacenters. pFabric achieves near-optimal FCT but needs specialized switch scheduling hardware; Fastpass uses commodity switches + centralized scheduler but loses performance (especially short flows).
- **Goal**: Near-pFabric performance on commodity fabric with flexible scheduling policies.
- **Mechanism**: Host-based scheduling with RTS (request-to-send), per-packet tokens from destination, source token selection, ACKs — all control at highest priority. Sources get configurable "free tokens" per flow; tokens expire in 1.5× MTU transmission time.
- **Why it works**: Packet spraying + full bisection bandwidth → little core congestion; priority levels protect signaling; decentralized bipartite matching at each destination (PIM/iSlip lineage) with backoff/downgrade to avoid starvation.
- **Flexibility**: Destination scheduling, source token pick, data priority, free-token budget configurable without fabric changes — supports slowdown minimization, deadlines, multi-tenant fairness.
- **Evaluation**: Within **4%** of pFabric under typical conditions; **3.8×** better than Fastpass on commodity hardware.
- **Assumptions**: Small RTTs, fat-tree/VL2 full bisection, 8–10 priority levels, ECMP/packet spraying, cut-through switches.
