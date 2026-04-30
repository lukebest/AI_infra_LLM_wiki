# Inside NVIDIA Groq 3 LPX: The Low-Latency Inference Accelerator for the NVIDIA Vera Rubin Platform

Source: https://developer.nvidia.com/blog/inside-nvidia-groq-3-lpx-the-low-latency-inference-accelerator-for-the-nvidia-vera-rubin-platform/
Fetched: 2026-04-16

---

NVIDIA Groq 3 LPX is a rack-scale inference accelerator for the NVIDIA Vera Rubin platform, designed for low-latency and large-context demands of agentic systems. Co-designed with Vera Rubin NVL72.

## Key Specs

| Specification | NVIDIA Groq 3 LPX |
|---|---|
| AI inference compute | 315 PFLOPS |
| Total SRAM capacity | 128 GB |
| On-chip SRAM bandwidth | 40 PB/s |
| Scale-up density | 256 chips |
| Scale-up bandwidth | 640 TB/s |

## Compute Tray Specs (per tray)

| Resource | Per LPX Tray |
|---|---|
| LPU chips | 8 |
| On-chip SRAM | 4 GB |
| SRAM bandwidth | 1.2 PB/s |
| DRAM via fabric expansion logic | Up to 256 GB |
| DRAM via host CPU | Up to 128 GB |
| AI inference compute (FP8) | 9.6 PFLOPS |
| Scale-up bandwidth | 20 TB/s |

## Groq 3 LPU Architecture

- 320-byte vectors as unit of work
- MXM (Matrix Execution Modules): dense MAC for tensor ops
- VXM (Vector Execution Modules): pointwise arithmetic, activations
- SXM (Switch Execution Modules): permutation, rotation, distribution, transposition
- MEM block: 500 MB on-chip SRAM, 150 TB/s bandwidth per LPU
- 96 C2C links per LPU at 112 Gbps = 2.5 TB/s bi-directional
- Plesiosynchronous C2C protocol for deterministic multi-chip coordination
- Compiler-orchestrated spatial execution (no runtime HW scheduler)

## Architecture Philosophy

- Deterministic execution, not peak throughput optimization
- SRAM-first memory (no hardware-managed caches)
- Explicit data movement under compiler control
- Heterogeneous: LPX handles FFN/MoE decode, Rubin GPU handles prefill + decode attention
- Targets 1000+ tokens/sec/user for agentic AI

## Key Claims

- 35x higher inference throughput per megawatt vs prior gen
- 10x more revenue opportunity for trillion-parameter models
- 32 liquid-cooled 1U compute trays, cableless design
- MGX ETL rack architecture integration

## Vera Rubin Platform (7 chips total)
LPX adds LPU as the 7th chip alongside Rubin GPU, NVLink, etc.
