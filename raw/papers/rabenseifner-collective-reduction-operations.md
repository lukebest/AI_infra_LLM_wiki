---
source_url: https://doi.org/10.1007/978-3-540-24785-4_1
ingested: 2026-06-24
sha256: c12a678e3b4da3a052c7c177453cf8aa181606bb1a36cb5b42a258f6e141def6
---

# Optimization of Collective Reduction Operations (2004)

**Author:** Rolf Rabenseifner — HLRS, University of Stuttgart

**Venue:** ICCS 2004, LNCS 3036, pp. 1–9 | **Extended version:** author publication page

## Motivation (Cray T3E 5-year production profiling)

- **40.7%** of MPI time in **MPI_Allreduce + MPI_Reduce** (8.54% total app time in MPI)
- **25%** of runtime with **non-power-of-two** process counts
- Vendor implementations optimized for **short vectors** only; long-vector speedups **3× (IBM sum)** to **100× (Cray maxloc)** possible

## Cost model (Thakur & Gropp flat model)

- Communication: **α + nβ** (bidirectional), **α_uni + nβ_uni** (unidirectional); f_α = α_uni/α, f_β = β_uni/β
- Computation: optimal load balance **(p−1)/p · nγ** total reduction work on p processes

## Five algorithms

### 1. Binary tree
- Full-vector exchange each step; **⌊lg p⌋** steps
- **Best:** short vectors (min latency term)
- Allreduce: T ≈ ⌊lg p⌋(2α_uni + 2nβ_uni + nγ)

### 2. Recursive doubling
- Distance doubling; both peers reduce **full vector** redundantly
- **Best:** short vectors (often optimal ≤32 B on T3E)
- Allreduce: T ≈ ⌊lg p⌋(α + nβ + nγ)

### 3. Recursive halving & doubling (RHD)
- **Reduce-scatter** (vector halving + distance doubling) + **allgather** (vector doubling + distance halving)
- Non-POT: peel r = p − 2^⌊lg p⌋ processes first
- **Best:** long vectors, power-of-two p
- T ≈ 2⌊lg p⌋α + 2nβ + nγ (POT); basis for **MPICH-2** default
- Key vs Thakur rank-ordered scatter: **any scatter order OK** → nearest-neighbor exchanges (hierarchical networks)

### 4. Binary blocks
- Decompose p into sum of power-of-two blocks; reduce within blocks then combine
- **Best:** non-POT, long vectors, many processes (e.g. δ_expo,max criterion on T3E)
- POT case identical to RHD

### 5. Ring
- Pairwise exchange reduce-scatter (stride +i/−i) + **ring allgather** (stride 1)
- **Best:** medium non-POT, long vectors, **small p** (latency ∝ p)
- Allreduce: T = 2(p−1)α + 2nβ + nγ − (1/p)(2nβ + nγ)

## Algorithm selection

Runtime chooses among 5 protocols by **(p, vector length n)** — break-even heatmaps (Figs 3–4):
- ≤32 B: recursive doubling
- ≤1 KB: vendor / binary tree / recursive doubling
- Long + small p: ring
- Long + large p + non-POT: binary blocks
- Long + POT: halving & doubling

## Impact

Halving & doubling in **MPICH-2**; IBM SP **1.5–5×** bandwidth gains for 8 KB–8 MB buffers.

## Lineage

Precursor to Thakur & Gropp MPICH tuning (LNCS 2840, 2003); same reduce-scatter + allgather decomposition as [WSE Ring AllReduce](/concepts/wse-reduce-algorithms.md) and NCCL ring algorithms.
