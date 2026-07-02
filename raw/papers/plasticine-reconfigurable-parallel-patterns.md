---
source_url: https://doi.org/10.1145/3079856.3080256
ingested: 2026-06-24
sha256: f5eef0521d18d9ca3661c3ba498f731ad7b3919d1660b9575fb2e49fe6698bbf
---

# Plasticine: A Reconfigurable Architecture For Parallel Patterns (ISCA 2017)

**Authors:** Raghu Prabhakar, Yaqi Zhang, David Koeplinger, Matt Feldman, Tian Zhao, Stefan Hadjis, Ardavan Pedram, Christos Kozyrakis, Kunle Olukotun — Stanford

**Venue:** ISCA 2017, Toronto | **DOI:** 10.1145/3079856.3080256

## Motivation

- FPGAs: >60% area/power in programmable interconnect; bit-level reconfigurability inefficient
- CGRAs: word-level FUs, higher clock, but low-level programming + long compile times
- Parallel patterns (Map, FlatMap, Fold, HashReduce) capture data locality, memory access, parallelism for dense + sparse apps
- Need: coarse-grain fabric with **direct architectural support** for parallel patterns — area/power efficient + high-level compile

## Programming Model

| Pattern | Behavior |
|---------|----------|
| **Map** | One output per index via f; independent; captures gather, zip, windowed filter |
| **FlatMap** | Arbitrary outputs per index via g; concatenated; filter = 0/1 output special case |
| **Fold** | Map then associative reduce r |
| **HashReduce** | Key k + value v per index; on-the-fly reduce by key; dense or sparse keys |

Nested patterns (e.g. Map outer + Fold inner for GEMM). DHDL (Delite Hardware Definition Language) — hierarchy of parallelizable dataflow pipelines.

## Architecture

2-D array of **Pattern Compute Units (PCUs)** and **Pattern Memory Units (PMUs)** + static hybrid interconnect (scalar / vector / control) + 4× DDR channels.

### PCU

- Multi-stage reconfigurable **SIMD pipeline** (innermost parallel pattern)
- 32b FUs (int + float); PR chain per lane; cross-lane **reduction tree** + **shift network** (stencil reuse)
- Scalar/vector/control IO with input FIFOs
- Reconfigurable counter chain + control block (LUTs, state machines)

### PMU

- Banked scratchpad + scalar address datapath (address calc offloaded from PCU)
- Banking modes: strided, FIFO, line buffer, duplication (parallel gather reads)
- N-buffering (generalized double buffering) for coarse-grain pipelined nested patterns

### Interconnect

- Static scalar (word), vector (multi-word), control (bit) networks; same topology; pipelined switches
- Control logic in switches for outer pipeline (reduces PCU control hotspot routing)

### Off-chip Memory

- **Address Generators (AG)** per channel side; dense (burst) + sparse (gather/scatter) requests
- **Coalescing unit** with coalescing cache; multiple outstanding requests

### Control Flow

Three protocols for nested patterns: (a) sequential + tokens, (b) coarse-grained pipelining + credits + M-buffering, (c) streaming + FIFO backpressure

## Compiler (DHDL → Plasticine)

1. Unroll outer pipelines
2. Allocate virtual PMUs/PCUs; schedule inner DFG to virtual stages
3. Greedy partition virtual → physical units
4. Generate control hierarchy; bind + route; emit static config bitstream
5. **Minutes** compile vs hours for FPGA

## Final Parameters (28 nm, 1 GHz)

| Component | Value |
|-----------|-------|
| Array | **16×8** units, **64 PCUs + 64 PMUs** (1:1) |
| PCU | 16 lanes, 6 stages, 6 reg/stage, 6 scalar in, 5 scalar out, 3 vector in/out |
| PMU | 16×16KB banks = **256 KB** scratchpad; 4 addr stages |
| Chip area | **112.77 mm²** |
| Peak FP32 | **12.3 TFLOPS** |
| On-chip SRAM | **16 MB** total scratchpad |
| Max power | **49 W** |
| DRAM | 4× DDR3-1600, **51.2 GB/s** peak |

## Evaluation vs Stratix V FPGA (28 nm)

Cycle-accurate VCS + DRAMSim2; FPGA: 150 MHz fabric, 6× DDR3-800 @ 37.5 GB/s.

| Benchmark | Speedup | Perf/W vs FPGA |
|-----------|---------|----------------|
| Inner Product | 1.4× | 1.6× |
| Outer Product | 6.7× | 6.1× |
| Black-Scholes | 5.1× | 5.8× |
| TPC-H Q6 | 1.4× | 1.5× |
| GEMM | 33.0× | 24.4× |
| GDA | 40.0× | 25.9× |
| LogReg | 11.4× | 9.2× |
| SGD | 6.7× | 15.9× |
| Kmeans | 6.1× | 11.3× |
| CNN | 95.1× | **76.9×** |
| SMDV | 8.3× | 9.3× |
| PageRank | 14.2× | 18.2× |
| BFS | 7.3× | 11.4× |

Area overhead vs app-specific ASIC (same perf): geo-mean **~11×** after full homogenization; reconfigurable hetero base ~2.8×.

## Related

- Prior FPGA from parallel patterns [15,36]; DianNao family; later CGRA/SDA work (SpaDA, FEATHER different niche)
