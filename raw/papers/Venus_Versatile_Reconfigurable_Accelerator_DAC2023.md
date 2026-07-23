---
type: Raw Source
title: 'Venus: A Versatile Deep Neural Network Accelerator Architecture Design for Multiple Applications'
source_path: /home/luke/wiki/raw/papers/Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf
arxiv: ''
ingested: 2026-07-22
---

# Venus (Source)

**Authors:** Jiaqi Yang et al. (George Washington University, HPCAT lab) | **Venue:** DAC 2023 | **PDF:** [raw/papers/Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf](Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf)

## Core contribution

**Venus**: tile-based architecture with **distributed buffer** + **adaptable communication fabric** that can **dynamically morph and fission** to support distinct communication and computation needs for **simultaneously running DNN models**.

## Architecture

- **Distributed buffer** per tile (vs centralized)
- **Reconfigurable systolic array** for compute fission
- **Flexible NoC** that supports **fission** (split) and **fusion** (merge) of subnets

## Key innovation: NoC Fission / Fusion

**Fission**: split a single NoC into multiple sub-NoCs for **concurrent** DNN models
- Multi-DNN serving → each gets its own private subnet
- Reduces interference, supports QoS

**Fusion**: merge subnets for **bandwidth-heavy** layers
- One large DNN layer → combine all subnets
- Maximizes bisection bandwidth for that layer

## Layout / dataflow capability

- **Distributed buffer** allows **per-tile layout** choice
- **NoC fission/fusion** adapts the **physical data path** to each layer's traffic pattern
- Equivalent to "runtime layout-aware NoC" — choose the right physical subnet for each layer's preferred data layout

## Significance

First paper to make **NoC fission/fusion** explicit — extends FEATHER's per-layer adaptation from **single layer** to **concurrent multi-DNN**. Layout-aware NoC in the **runtime multi-tenancy** sense.