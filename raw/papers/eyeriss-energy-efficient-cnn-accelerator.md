---
source_url: https://doi.org/10.1109/JSSC.2016.2616357
ingested: 2026-06-24
sha256: 9b1e09a2d2d993d1ec989392fdd61ea3c839a80520bb82004da533cddf109abb
---

# Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep CNNs (JSSC 2017)

**Authors:** Yu-Hsin Chen, Tushar Krishna, Joel S. Emer, Vivienne Sze — MIT (Krishna → Georgia Tech)

**Venue:** IEEE JSSC Vol. 52 No. 1, Jan. 2017 (expanded from ISSCC 2016)

## Motivation

- CNN inference: tens–hundreds MB params, billions of ops → data movement (on-chip + DRAM) often **more costly than compute**
- Prior CNN accelerators: few fabricated chips benchmarked on **public SOTA CNNs** with **DRAM bandwidth** reported
- Need: reconfigurable dataflow for varying conv shapes + whole-system energy optimization

## Architecture

- 168 PEs, 12×14 array; not lock-step systolic
- 108 kB GLB (25×4kB banks, reconfigurable ifmap/psum split)
- PE spads: filter 224×16b SRAM, ifmap 12×16b, psum 24×16b
- Core 200 MHz / Link 60 MHz async domains
- 1794b scan chain reconfig per layer (<100 µs)
- RLC CODEC + ReLU module

## Row Stationary Dataflow

- Minimize ifmap, filter, psum movement simultaneously
- Reuse: convolutional (E×F, R×S), filter (batch N), ifmap (M filters)
- 1-D primitive per PE: one filter row × one ifmap row → psum row; spad ∝ S
- PE Set R×E: horizontal filter reuse, diagonal ifmap reuse, vertical psum accumulate
- Mapping: strip-mining, segmentation; params p,q (in-PE), r,t (multi-set), n,m (pass scheduling)
- Processing pass: read ifmap once from GLB; accumulate psums in array/GLB before DRAM
- vs prior dataflows: 1.4–2.5× better energy on AlexNet [ISCA'16]

## NoC

- GIN: single-cycle multicast GLB→PE; (row,col) tag + configurable IDs; separate GINs for filter/ifmap/psum
- GON: psum readback to GLB
- LN: dedicated 64b vertical psum bus between adjacent PE rows
- Custom vs mesh: lower latency/energy for fixed CNN delivery patterns

## Zero exploitation

- RLC: run-length encode zeros (max 31); ~5–10% overhead vs entropy limit
- Data gating: skip MAC on zero ifmap via Zero Buffer → 45% PE power saving

## Measured Results

**AlexNet (N=4, 1V):**
- 34.7 frames/s, 23.1 GMAC/s throughput, 278 mW, 83.1 GMAC/s/W
- 0.0029 DRAM access/MAC, 15.4 MB/batch of 4
- 88% PE active; ALU <10% power; data movement ~45%

**VGG-16 (N=3):**
- 0.7 frames/s, 236 mW, 0.0035 DRAM access/MAC

**Chip:** 65 nm CMOS; peak 33.6 GMAC/s; max efficiency 122.8 GMAC/s/W @ 0.82V

## Integration

- Caffe offload via PCIe (Jetson TK1 + Xilinx VC707)
- 1000-class ImageNet live demo

## Related

- ISCA 2016 [32]: RS dataflow optimization details
- DianNao family [17-19], Origami [24], FEATHER (2024) builds on fixed-dataflow baseline
