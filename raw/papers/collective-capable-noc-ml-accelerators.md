---
source_url: https://arxiv.org/abs/2603.26438
ingested: 2026-06-24
sha256: bfbf79d1b428ddaa6a53a47b479b6b837d26cd1a25d97cea8ba9420d8841a386
---

# A Lightweight High-Throughput Collective-Capable NoC for Large-Scale ML Accelerators (arXiv:2603.26438)

**Authors:** Luca Colagrande*, Lorenzo Leone*, Chen Wu, Tim Fischer, Raphael Roth, Luca Benini (* equal contribution, ETH Zurich)

**Venue:** MLSys 2026 (Bellevue, WA)
**Code:** https://github.com/pulp-platform/FlooNoC/releases/tag/v0.8.0 , https://github.com/pulp-platform/picobello

## Motivation

- ML model scale ↑ → thousands of PEs on single die; on-chip ≈ distributed system
- FLOPS grew ~60000× vs DRAM BW ~100× over 20 years → communication-bound GEMM on large meshes (<50% util on 256×256 without collective support)
- MPI usage: reduction, barrier, broadcast most frequent collectives
- Prior multicast NoC work targets cache-coherence (flexible, heavy); few target ML burst transfers or high-throughput arithmetic reduction

## Baseline System (FlooNoC + Snitch)

- 2D mesh: compute tiles (Snitch cluster 8+1 cores, 128 KiB L1 SPM) + memory tiles (1 MB L2 SPM)
- FlooNoC: wide 512b + narrow 64b AXI networks; req/rsp/wide physical links
- DMA transfer: read source → write dest; T = α + nβ
- Multi-address encoding (Colagrande & Benini 2025): AWUSER carries (addr, mask); mask bit=1 → don't care; 2^n destinations from n mask bits

## Architecture Extensions

### Network Interface
- Translate AWUSER address mask → X/Y coordinate masks on AW flit header
- Store mask for W beats; resolve incoming collective to local address; buffer for collective response (multicast↔reduction duality in AXI)

### Multicast Router
- Extend xy_route_fork: X/Y mask → multiple output ports via stream_fork
- Accept input only when all fork outputs ready

### Parallel Reduction (narrow)
- output_arbiter: unicast → wormhole_arbiter; reduction → reduction_arbiter
- sync module per input: wait for masked directions; LZC arbitrate concurrent reductions
- Opcodes: CollectB (multicast B response merge), LsbAnd (barrier), SelectAW (reduction AW merge)

### Wide Reduction
- Centralized 2-input reduction (not 5-input tree — area)
- hdr buffer depth > FPU pipeline → 1 reduction/cycle throughput for bursts
- offload port → DCA on Snitch cluster

### Direct Compute Access (DCA)

**Paradigm**: interconnect borrows tile FPU like DMA borrows memory — no core instructions for wide FP reduction.

- Router wide reduction controller: 2-input merge only (not 5-input tree in router); multi-hop tree on mesh
- Router offload → cluster: 2×512b operands + 512b result + opcode
- 512b → 8×64b to FPUs; tag arbitrates DCA vs core requests; cores can low-power
- hdr buffer depth > FPU pipeline → 1 reduction/cycle for bursts; valid-ready backpressure
- Up to 8× DP or 64× 8b FP reductions/cycle; full tile area <1% vs router +16.9%
- SW baseline: DMA partial sums + core FPU + barrier (seq/tree); T_seq/T_tree models in paper §4.2.3
- 2D reduction limit: first-column router 3 inputs → 1 beat/2 cycles for 32 KiB
- FPU contention if DCA overlaps core compute (FCL: reduction after compute, no overlap)

### System Integration
- DMA + LSU inject collective opcode in AWUSER
- Collective submesh (X,Y,W,H): W,H powers of 2; aligned; equal per-tile address spaces, Y-major

## Implementation (TSMC 7nm)

| Config | Router area overhead |
|--------|---------------------|
| Multicast only | +5.8% |
| + parallel reduction | +8.7% cumulative |
| + wide reduction (full) | +16.9% |
| NI full collective | +3.5% |
| Full cluster tile | <1% vs 5.6 MGE baseline |

## Evaluation (QuestaSim RTL, 4×4 mesh unless noted)

### Barrier (LsbAnd vs amoadd on cluster 0)
- HW slope 1.3 vs SW 3.3 cycles/cluster (expected 1 vs 3)

### Multicast (1D row, 1–32 KiB)
- Thw = α + (n+c−1)β vs seq/tree software
- 1D: 2.3–3.2× over best SW; 4×4 2D broadcast: **5.3×** geomean
- 2D HW runtime nearly constant vs rows; SW scales poorly

### Reduction (DCA, 1–32 KiB)
- **2.8×** geomean over best seq/tree SW on 4×4
- 2D: first-column router 3 inputs → 1 beat/2 cycles for 32 KiB (1.9× slowdown vs 1D)

### GEMM Kernels
- **SUMMA** double-buffered: T = max(Tcomp, Tcomm); hw multicast keeps compute-bound to 256×256 vs SW memory-bound at 16×16 → **1.1–3.8×** speedup
- **FusedConcatLinear** (MHA fused concat+linear): reduction on critical path → **up to 2.4×**
- Energy: SUMMA **1.17×** @ 256×256; FCL **1.13×** (fewer DMA hops + DCA idle cores)

## Generalizability

Requires: (1) structured 2D mesh, (2) borrowable arithmetic per tile, (3) programmable DMA/LSU/TE — matches WSE-3, Blackhole, XDNA, SN40L, MTIA, Venus, FlatAttention, etc.

## Related Work Positioning

- Path/tree multicast for coherence (Jerger, Krishna, …): flexible, deadlock-prone, not ML burst-focused
- Industrial multicast (MTIA, SN40L, Blackhole): proprietary, undisclosed
- First open-source end-to-end collective NoC for programmable ML accelerators + first high-throughput on-chip arithmetic reduction via DCA
- Detailed HW vs optimized SW comparison (exception: prior XBAR work different topology)

## Key Equations

- Unicast DMA: T = α + nβ
- HW multicast 1D: Thw = α + (n+c−1)β
- GEMM steady-state: T = max(Tcomp, Tcomm); Tcomm = TmcastA + TmcastB
