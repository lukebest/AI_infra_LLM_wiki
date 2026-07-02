---
type: Summary
title: 'Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks'
description: MIT 65nm 168-PE CNN 加速器：Row Stationary dataflow、四级存储、GIN 组播 NoC、RLC+data gating；AlexNet 35 frames/s @278mW、0.0029 DRAM access/MAC
tags:
- accelerator
- cnn
- dataflow
- dnn
- energy-efficiency
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf
---

# Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks

**Authors:** Yu-Hsin Chen, Tushar Krishna, Joel S. Emer, Vivienne Sze (MIT) | **Venue:** IEEE JSSC, Jan. 2017 | **DOI:** [10.1109/JSSC.2016.2616357](https://doi.org/10.1109/JSSC.2016.2616357) | **PDF:** [raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf](raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf)

## 一句话总结

168 PE（12×14）空间阵列 + **Row Stationary** 可重构 dataflow，在四级存储层次上最大化 ifmap/filter/psum 局部复用；**custom GIN 单周期组播 NoC** + **RLC 压缩** + **PE data gating** 进一步降 DRAM 与计算能耗——**AlexNet 35 frames/s @ 278 mW、0.0029 DRAM access/MAC**，首批在公开 SOTA CNN 上报告系统级能效的流片加速器之一。

## 核心贡献

1. **RS dataflow**：1-D row primitive → PE Set (R×E) → 阵列映射 + processing pass；离线优化 p,q,r,t,n,m
2. **四级 memory hierarchy**：spads → inter-PE → GLB (108 kB) → DRAM；RS 最小化高层访问
3. **Custom NoC**：GIN/GON/LN；Y-bus×X-bus + (row,col) tag 组播；非 hop-by-hop mesh
4. **RLC + data gating**：ReLU 零值压缩 DRAM 带宽；零 ifmap 跳过 MAC（PE power −45%）
5. **流片 + 系统 benchmark**：65 nm；AlexNet & VGG-16 实测；Caffe 集成

## 关键数字

| 指标 | 值 |
|------|-----|
| PE / 峰值吞吐 | 168 / **33.6 GMAC/s** @ 200 MHz |
| AlexNet 能效 | **83.1 GMAC/s/W**（peak **122.8** @ 0.82 V） |
| AlexNet DRAM/MAC | **0.0029** |
| VGG-16 DRAM/MAC | **0.0035** |
| RS vs prior dataflow (AlexNet) | **1.4–2.5×** 更节能 |
| ALU 占芯片功耗 | **<10%** |
| On-chip storage 占面积 | **~2/3** |

## 与 wiki 交叉引用

- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — RS dataflow 与 NoC 机制
- [FEATHER Accelerator](/concepts/feather-accelerator.md) — 相对固定 Eyeriss-like 的可重构 dataflow-layout
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 片上 multicast 对照
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — DNN 加速器设计谱系

# Citations

[1] [raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf](raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf) — Chen et al. (2017)
