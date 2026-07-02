---
type: Concept
title: Eyeriss Accelerator
description: MIT 65nm CNN 加速器：168 PE 空间阵列、Row Stationary (RS) 可重构 dataflow、四级存储层次、GIN 单周期组播 NoC、RLC 压缩与 PE data gating；AlexNet 83.1 GMAC/s/W
tags:
- accelerator
- dnn
- cnn
- dataflow
- noc
- energy-efficiency
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf
---

# Eyeriss Accelerator

**Eyeriss**（MIT, JSSC 2017）是首批**流片验证**、在 **AlexNet/VGG-16** 上报告 **系统级**（芯片 + DRAM）能效的经典 CNN 推理加速器。核心思想：**data movement 比计算更耗能**（Horowitz [10]）→ 用可重构 **Row Stationary (RS)** dataflow 最大化局部复用，配合 **custom multicast NoC**、**RLC 零值压缩** 与 **PE data gating**。

**Authors:** Yu-Hsin Chen, Tushar Krishna, Joel S. Emer, Vivienne Sze | **Venue:** IEEE JSSC, Jan. 2017 | **Chip:** 65 nm CMOS, ISSCC 2016 | **Dataflow 详述:** ISCA 2016 [32]

## 系统架构

```
DRAM ←async FIFO→ GLB (108 kB) ←GIN/GON/LN→ 12×14 PE array (168 PEs)
                      ↑ RLC CODEC + ReLU
```

| 组件 | 规格 |
|------|------|
| PE 阵列 | **12×14 = 168** PE；非 lock-step（非纯 systolic） |
| GLB | **108 kB**（100 kB ifmap/psum 可重构 + 8 kB filter preload） |
| PE 本地 | **spads**：filter 224×16b SRAM + ifmap 12×16b reg + psum 24×16b reg |
| 时钟 | Core **200 MHz** / Link **60 MHz**（异步域） |
| 配置 | **1794 b** scan chain，<100 µs/layer |

**四级存储层次**（能耗递增）：spads → inter-PE 通信 → GLB → **DRAM**。

## Row Stationary (RS) Dataflow

RS 将任意 CNN shape **映射到 PE 阵列**，同时最小化 ifmap / filter / psum 三类数据的移动（相对 prior dataflow 在 AlexNet 上 **1.4–2.5×** 更节能 [32]）。

### 三种复用

| 复用类型 | 含义 |
|----------|------|
| **Convolutional** | 同 filter 权重在 E×F 次复用；同 ifmap 像素在 R×S 次复用 |
| **Filter reuse** | 权重跨 batch N 个 ifmap 复用 |
| **Ifmap reuse** | 像素跨 M 个 filter（ofmap channel）复用 |

### 映射层次

1. **1-D primitive / PE**：一行 filter × 一行 ifmap → 一行 psum；**row stationary**——行对在 PE 内滑动窗口处理；spad 容量 ∝ **S**（filter 行宽），与 W 无关
2. **PE Set (R×E)**：2-D 卷积 — filter 行**水平**复用、ifmap 行**对角**复用、psum 行**垂直**累加
3. **PE 阵列映射**：strip-mining（CONV1 11×55→11×7）、分段（CONV2 5×27→5×14+5×13）；参数 **p,q**（PE 内多 channel/filter）、**r,t**（多 PE set 并行）
4. **Processing Pass**：一次 GLB 读入 ifmap，阵列内完成 q×r channel × p×t filter 子计算；GLB 缓存跨 pass 的 ifmap/psum 复用

离线优化映射参数（Table II）→ 给定 shape + GLB/spad/PE 资源 + 各级存储能耗。

## NoC：Custom Multicast（非 hop-by-hop mesh）

| 网络 | 功能 |
|------|------|
| **GIN** | GLB → PE **单周期组播**；(row,col) tag + 可配 row/col ID；filter/ifmap/psum 各独立 GIN |
| **GON** | PE → GLB 读 psum（GIN 反向） |
| **LN** | 列内相邻 PE 间 **64b 直连** psum 垂直累加 |

Y-bus（12 行）× X-bus（14 列 PE）；未匹配 bus/PE **clock gating**。对比通用 mesh NoC 避免 ramp-up 与 router 开销 [34][35]——与 [Collective-Capable NoC](/concepts/collective-capable-noc.md) 的 XY fork 组播异曲同工（固定 CNN 映射 vs 通用 AXI collective）。

## 零值统计优化

| 技术 | 机制 | 效果 |
|------|------|------|
| **RLC** | Run-length 压缩 fmap（max run 31）；DRAM 存压缩格式 | AlexNet fmap DRAM 访问 **~30%（CONV1）~75%（CONV5）** 节省 |
| **Data gating** | Zero Buffer 标记 ifmap 零 → 跳过 filter 读与 MAC 翻转 | PE 功耗 **−45%**（CONV5 零值 ~75%） |

## 芯片结果（实测）

| 指标 | AlexNet (N=4) | VGG-16 (N=3) |
|------|---------------|--------------|
| 帧率 | **34.7** frames/s（~35） | **0.7** frames/s |
| 吞吐 | 23.1 GMAC/s（peak 33.6） | — |
| 芯片功耗 | **278 mW** @ 1 V | **236 mW** |
| 能效 | **83.1 GMAC/s/W**（max **122.8** @ 0.82 V） | — |
| DRAM access/MAC | **0.0029** | **0.0035** |
| PE 利用率 | ~88% active | — |

**面积**：on-chip storage（GLB+spads）**2/3**；MAC 仅 **7.4%**；ALU 功耗 **<10%**，数据移动（spad+GLB+NoC）**~45%** — 验证「移动比算贵」。

集成 **Caffe**（PCIe offload，Jetson TK1 + VC707）；1000-class ImageNet 实时 demo [29]。

## 与 FEATHER / 现代 DNN 加速器

| 维度 | Eyeriss (2017) | [FEATHER](/concepts/feather-accelerator.md) (2024) |
|------|----------------|-----------------------------------------------------|
| Dataflow | **固定 RS**（层间 scan chain 重配） | 每层 **(dataflow, layout) co-switch** |
| 瓶颈 | DRAM + GLB 带宽；Timeloop 未建模 layout | Bank port conflict 可致 **128×** 慢 |
| 可重构 | CNN shape 映射参数 | NEST + BIRRD 蝶形 reorder |
| 基线关系 | FEATHER 对比的 **固定 Eyeriss-like** 基线（+6% 面积换 co-switch） |

谱系：DianNao/ShiDianNao/DaDianNao [17–19] → **Eyeriss（RS + 流片 + AlexNet/VGG 系统 benchmark）** → Eyeriss v2 / SIGMA / NVDLA → FEATHER layout-aware。General **parallel patterns** CGRA 见 [Plasticine](/concepts/plasticine-accelerator.md)（ISCA 2017，含 CNN 映射）。

## 相关页面

- [FEATHER Accelerator](/concepts/feather-accelerator.md) — 可重构 dataflow-layout；Eyeriss-like 固定基线
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 固定 dataflow vs 可编程/可重构
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 片上 multicast NoC 对照
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — mesh/router 设计基线
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 片上 memory bank 与利用率
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — parallel patterns CGRA 对照

# Citations

[1] [raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf](raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf) — Chen et al., JSSC 2017
[2] [raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf](raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf) — FEATHER vs Eyeriss-like baseline
