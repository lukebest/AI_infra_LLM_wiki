---
type: Raw Source
title: 'MAERI: Enabling Flexible Dataflow Mapping over DNN Accelerators via Reconfigurable Interconnects'
source_path: /home/luke/wiki/raw/papers/MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf
arxiv: ''
ingested: 2026-07-22
---

# MAERI (Source)

**Authors:** Hyoukjun Kwon, Ananda Samajdar, Tushar Krishna (Georgia Tech) | **Venue:** ASPLOS 2018 | **PDF:** [raw/papers/MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf](MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf)

## Abstract (verbatim)

> "We present MAERI, which is a DNN accelerator built with a set of modular and configurable building blocks that can easily support myriad DNN partitions and mappings by appropriately configuring tiny switches. MAERI provides 8-459% better utilization across multiple dataflow mappings over baselines with rigid NoC fabrics."

## Key idea

**MAERI = Multi-dimensional Array of Reduced Expandable ISA-Like Reconfigurable Interconnects**

Three building blocks:
1. **ART (Augmented Reduction Tree)** — forward direction
2. **Distribution Tree** — reverse direction
3. **Tiny switches** between PE array and trees — **configurable** per layer

## Architecture

```
       DRAM ──┬── Aggr/Disp ── Distribution Tree ──┐
              │                                      │
              └── Controller                          ▼
                                              ┌────────────────┐
                                              │  PE Array      │
                                              │  (configurable │
                                              │   switches)    │
                                              └────────────────┘
                                                      │
                                                      ▼
                                              Augmented Reduction
                                              Tree (ART)
                                                      │
                                                      ▼
                                                  DRAM / next layer
```

## Layout / dataflow capability

- **Tiny switches can be reconfigured** to implement **any multicast / scatter / gather pattern**
- **Every PE can receive any data element** in any order → **any layout can be mapped to any dataflow**
- Tree-based fan-out: log(N) latency for distribution
- Tree-based reduction: O(log N) for partial sums

## Results

- **8-459% better utilization** than rigid NoC fabrics (Eyeriss-like / systolic-like)
- **+6.5% power overhead** vs rigid baseline (Eyeriss)
- **+47% area** vs systolic, **+49% throughput**
- Case studies: AlexNet, VGG, ResNet, GoogLeNet, RNNs, sparse LSTMs
- Layout capability verified for: conv, FC, RNN, pooling, irregular shapes

## Significance

**First paper to argue "flexible dataflow needs flexible NoC"** — established that **layout support is the dominant feature** for next-gen DNN accelerators, not just compute throughput.