---
type: Raw Source
title: 'Aurelia: CXL Fabric with Tentacle'
source_path: /home/luke/wiki/raw/papers/Aurelia_CXL_Fabric_Tentacle_2023.pdf
doi: '10.1145/3605181.3626287'
zotero: PZWFS6D8
ingested: 2026-07-17
sha256: 68dff43bec1006aabcb83b4af49886ac41a3dbbfffa12ff5f45bac2948d19f4f
---

# Aurelia: CXL Fabric with Tentacle

Authors: Shu-Ting Wang, Weitao Wang (UCSD, Rice)
Venue: WORDS 2023 (Workshop on Resource Disaggregation and Serverless) | DOI: 10.1145/3605181.3626287

Structured notes / key excerpts:

- **Motivation**: CXL externalizes server memory fabric for disaggregation (CXL.mem/cache/io); up to **4096** endpoints but current PBR routing + PCIe point-to-point flow control limit scale/latency.
- **Use cases**: ML training (fabric-attached memory for multi-GPU models), HPC (>90% memory BW utilization), KV stores (latency-sensitive).
- **CXL vs RDMA**: Direct load/store avoids NIC + kernel stack; DirectCXL **8.3×** lower latency than RDMA for 64B read (single-switch lower bound); PCIe 5.0 **63 GB/s**, PCIe 6.0 **121 GB/s** horizon.
- **Challenges**: (1) 12-bit Port ID routing — no multipath/adaptive routing; fabric manager = centralized SDN. (2) PCIe credit flow control doesn't prevent switch-port congestion — RDMA latency spikes **~3×** under PCIe congestion (experiment).
- **Aurelia proposal**: Map **addressing, routing, transport** as networking layers onto CXL; **Tentacle** mechanism for scalable fabric (details in full paper).
- **Workload sensitivity**: Synchronous load/store stalls requester on latency — stricter than packetized DC traffic.
