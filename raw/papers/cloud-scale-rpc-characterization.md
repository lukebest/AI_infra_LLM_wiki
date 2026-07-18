---
type: Raw Source
title: A Cloud-Scale Characterization of Remote Procedure Calls
source_path: /home/luke/wiki/raw/papers/Cloud_Scale_RPC_Characterization_2023.pdf
doi: '10.1145/3600006.3613156'
zotero: VDE3HSY5
ingested: 2026-07-17
sha256: dbef2889719f22ffabe89a2a1de11421ea239e8d12cd6aebe8d75ab81f479fac
---

# A Cloud-Scale Characterization of Remote Procedure Calls

Authors: Korakit Seemakhupt, Brent E. Stephens, Samira Khan, Sihang Liu, Hassan Wassel, Soheil Hassas Yeganeh, Alex C. Snoeren, Arvind Krishnamurthy, David E. Culler, Henry M. Levy (Google + academia)
Venue: SOSP 2023 | DOI: 10.1145/3600006.3613156

Structured notes / key excerpts:

- **Scale**: 700 days (Dec 2020–Nov 2022); **>10,000** RPC methods; **722B** RPC samples (one day); Monarch + Dapper + GWP tooling.
- **Services**: Google Search, Gmail, Maps, YouTube + Spanner, BigQuery, Bigtable, F1, GFS, Chubby (Stubby/gRPC stack).
- **Growth**: RPC RPS per CPU cycle growing **~30%/year**, **+64%** over interval — RPC usage outpaces compute.
- **Latency**: Average RPCs at **millisecond** scale, **kilobyte** sizes, **deep nested** call trees; avg dominated by app processing but **tail by RPC tax** (queues + marshalling + network).
- **Architecture**: Partition/aggregate service-oriented (not microservices); data in geo-replicated GFS blocks.
- **Load balancing**: Significant CPU cycle variance per RPC → opportunity for better balancing.
- **Note**: RDMA used for data movement alongside RPC; study focuses on RPC control path.
