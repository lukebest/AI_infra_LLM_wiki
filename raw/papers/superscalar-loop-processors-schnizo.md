---
type: Raw Source
title: "Superscalar Loop Processors"
source_url: https://arxiv.org/abs/2611.01904
pdf: Superscalar_Loop_Processors_Schnizo_MICRO2026.pdf
retrieved: 2026-11-04
ingested: 2026-11-04
org: ETH Zurich
venue: MICRO 2026
---

# Abstract (verbatim gist, arXiv:2611.01904)

To sustain the computational demands of modern ML and HPC workloads, programmable accelerators integrate large arrays of processing elements (PEs), typically built around single-issue in-order cores to maximize integration density and energy efficiency. As a result, each PE's instruction throughput is upper-bounded at one instruction per cycle (IPC), often suffering from significant underutilization of its functional units (FUs). Conventional superscalar processors can improve FU utilization by increasing IPC, but they typically incur substantial area and energy overheads. This work proposes the Superscalar Loop Processor (SLP) architecture, a lightweight approach to superscalar execution that targets regular, compute-intensive loop kernels. We present the SLP execution model, which exploits the static structure of these workloads to enable efficient multiple-issue execution without the complexity of dynamic out-of-order scheduling. We demonstrate the SLP architecture through an open-source prototype implementation, Schnizo, developed as an enhancement of a tiny RV32I core with floating-point support. Across several ML and HPC microkernels, Schnizo achieves substantially higher IPC and FPU utilization than the scalar baseline while retaining the efficiency of lightweight in-order designs. These results demonstrate that SLPs can provide an efficient architectural solution for programmable accelerators targeting regular, compute-intensive workloads.

# Excerpts / key facts (from HTML/PDF)

- Authors: Luca Colagrande, Pascal Etterli, Luca Benini (ETH Zurich); MICRO 2026.
- Schnizo: open-source RV32I+FP enhancement of Snitch; DCP then DEP loop-local schedule reuse.
- Simple LA kernels: geomean **4.4×** speedup vs scalar; **72%** higher area efficiency than scalar.
- Geomean **92%** of ideal IPC / FPU util on diverse microkernels (max problem size).
- Targets regular compute-intensive loops for PE arrays in accelerators.
