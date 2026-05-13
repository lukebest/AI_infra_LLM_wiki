---
title: "Resilient AI Supercomputer Networking using MRC and SRv6"
source_url: "raw/papers/resilient-ai-supercomputer-networking-using-mrc-and-srv6.pdf"
ingested: 2026-05-13
authors: [Joao Araujo, Alex Chow, Mark Handley, Ryder Lewis, Christoph Paasch, Jitendra Padhye, Michael Papamichael, Greg Steinbrecher, Amin Tootoonchian, Lihua Yuan]
affiliations: [OpenAI, Microsoft, AMD, NVIDIA, Broadcom]
tags: [scale-up, routing, transport, switch, protocol, fabric, nvidia, amd, congestion-control, load-balancing]
---

# Resilient AI Supercomputer Networking using MRC and SRv6

## Summary

Paper proposes a three-pronged approach for resilient AI training networking at 100K+ GPU scale:

1. **MRC (Multipath RC)** — a new RDMA-based transport extending RoCEv2 RC with packet spraying, adaptive load balancing, selective retransmission, packet trimming
2. **Multi-plane Clos topology** — 2-tier topology using 8×100Gb/s or 4×200Gb/s planes instead of 3-tier 800Gb/s
3. **Static SRv6 source routing** — disables dynamic routing, uses IPv6 segment routing with micro-segment IDs (uSID)

Deployed in production at OpenAI and Microsoft to train frontier models (ChatGPT, Codex).

## Key Technical Details

### MRC Protocol
- Extends RoCEv2 Reliable Connection for multi-path operation, borrowing from UET
- Only supports RDMA write and write-with-immediate
- Every data packet contains RDMA virtual address + remote key (out-of-order placement)
- 32-bit Entropy Value (EV) striped across UDP source port and IPv6 flow label
- QP startup generates EV set (128-256 entries), sprayed across all planes
- Disables PFC — operates in best-effort (lossy) Ethernet mode
- Fast selective retransmission with SACK/NACK
- Packet trimming: congested packets get payload stripped, priority-forwarded as NACK trigger
- ECN-based load balancing: non-last-hop ECN signals used to avoid congested paths
- Path failure: packet loss → EV immediately retired → backup EV swapped in
- Background probes resurrect EVs when failed paths recover

### Multi-plane Topology
- 800Gb/s NIC broken into 8×100Gb/s or 4×200Gb/s
- Same 51.2Tb/s switches → 512 ports at 100Gb/s
- 2-tier topology supports 131K GPUs (vs 64K in 3-tier 800Gb/s)
- Benefits: lower latency (3 hops vs 5-7), more one-hop nodes, less cost/power, smaller failure blast radius
- Single NIC-T0 link loss: 12% bandwidth (8-plane) vs 3% per T0-T1 link

### SRv6 Source Routing
- Uses micro-segment ID (uSID) format, uN style
- Destination IPv6 address: 32-bit locator prefix + sequence of 16-bit uSIDs
- Each switch left-shifts uSID by 16 bits → next hop
- Static forwarding tables configured at install, never changed
- EV → SRv6 address: algorithmic mapping using node-specific template
- Disabling dynamic routing avoids interaction with MRC's adaptive load balancing

### Clustermapper
- Agent on every node probes all links every millisecond
- Source-routed probes to T0 (and back) and T1 (and back)
- Gives ground-truth health data, enables denylist for failed paths
- Distinguishes NIC-T0 vs T0-T1 failures

### Production Results
- Deployed on NVIDIA CX-8, AMD Pollara, Broadcom Thor Ultra NICs
- NVIDIA Spectrum-4/5, Broadcom TH5 switches
- T0-T1 link flaps largely ignored — MRC routes around them
- T1 switch reboot: ~580K packets dropped, job throughput barely affected
- NIC-T0 port failure: brief glitch, recovers in seconds
- T0-local latency: 5.09µs, Cross-T1: 6.54µs
- Bandwidth: ~770 Gb/s (96% peak) both T0-local and cross-T1
- NCCL at 42K GPUs: up to 92 GB/s
- MRC 1 QP outperforms RoCE 16 QPs in all-reduce due to no ECMP collisions
- MRC with 0.1% loss ≈ same performance as no-loss; RoCE degrades significantly

### Related Work
- UET (Ultra Ethernet Transport): MRC borrows from UET concepts
- IRN, MPRDMA: selective retransmission predecessors
- Falcon (Google): multipath RoCEv2 replacement
- HPN (Alibaba): dual-ToR rail-optimized, 15K GPUs
- REPS, Hermes, Strack: ECN/delay-based load balancing
