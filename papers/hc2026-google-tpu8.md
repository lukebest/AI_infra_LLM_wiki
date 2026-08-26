---
type: Paper
title: "Hot Chips 2026: Google TPU 8"
description: Google — TPU 8t/8i；Boardfly 1152 chips / max 7 hops；8t superpod 9600 chips / 121 EF；Virgo 134,400 TPU
tags:
- google
- tpu
- ocs
- scale-up
- interconnect
- fabric
- inference
- training
- hbm
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Google_TPU8.pdf
- raw/papers/hc2026-google-tpu8.md
---

# The Eighth Generation TPU Family

**Speakers:** Norman P. Jouppi, Sridhar Lakshmanamurthy（Google）  
**Venue:** Hot Chips 2026 Day 2  
**PDF:** [raw/papers/HC2026_Google_TPU8.pdf](raw/papers/HC2026_Google_TPU8.pdf)

同期两颗：**TPU 8t**（训练）与 **TPU 8i**（推理）。8i 芯片 HBM TB/s **未知**（旁边 SRAM-vs-HBM 表是通例）。对照 [TPU v4 OCS](/concepts/tpu-v4-ocs-reconfigurable-fabric.md)。

## 8i（推理）

On-chip SRAM **384 MB**（**2.4×** prior）。HBM **288 GB**，文字标 **12-Hi HBM3E stacks**；框图又画 **8** stack 并标 **8-hi**——两处都在幻灯上，勿抹平。ICI **19.2 Tb/s**（**2×** prior）。Host：PCIe Gen5 x16 + Gen2 x1。ICI：**6×** link stacks，**6×200G** SerDes octals。

**Boardfly**（也写 BoardFly）：每 tray **4** TPU 全连接；**8** tray 一组全连接；最多 **36** 组 → **1152 chips/pod**；**max 7 hops**，对照 3D torus 例 **16** hops。动机：MoE all-to-all 被网络延迟卡住。

**CAE**（Collective Acceleration Engine）在 ICI I/O die 做 in-network collectives；避开 HBM，on-chip latency **5×** ↓。

## 8t / Virgo

8t superpod：**9,600** chips，**2 PB** shared HBM，**121 Exaflops**（**3×** Ironwood；标题页也写 **120 FP4 EFLOPS**），**2×** perf/W vs Ironwood，原生 FP4。每芯片 I/O **2.4 TB/s**「glueless scale-up」。OCS 可切任意形状，只受 pool 限制（例 **8×8×4**、**8×8×8**）。

8t ICI：**6** links，每条 **8** lanes bidirectional，**1.6 Tb/s per direction**；**6×224G** SerDes octals。封装 **6** 个 **12-hi HBM3E**。Tray：一级 VR + **water cooled optics（an ML first）**。机柜说明：**6 out of 300** in the superpod。

**Virgo**：单集群 **134,400** TPUs，**1.6 YottaFlops**，**47 Petabits/s**。十年口号：shared-memory 系统性能 **1,000,000×**，从 2015 TPUv1（**1** PCIe card，**90** int8 TOPS）到 2026 8t（**9600** chips/pod）。

AI-in-the-loop RTL：8t MXU **6%** 功耗 / **5.8%** 面积 → **6%** 更多 TFLOPs。总结：**>2×** perf/TCO 与 **2×** perf/W 代际。

## 与 wiki 的关系

- [TPU v4 OCS Reconfigurable Fabric](/concepts/tpu-v4-ocs-reconfigurable-fabric.md) — 4096-chip OCS；8t 仍用 OCS，8i 改 Boardfly
- [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 固定 fat-tree vs Boardfly / OCS
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — CAE 在网集体
- [NVIDIA Rubin](/papers/hc2026-nvidia-rubin.md) — 同期 GPU scale-up 对照

# Citations

[1] [raw/papers/HC2026_Google_TPU8.pdf](raw/papers/HC2026_Google_TPU8.pdf) — Jouppi / Lakshmanamurthy, Hot Chips 2026
[2] [raw/papers/hc2026-google-tpu8.md](raw/papers/hc2026-google-tpu8.md) — 结构化摘录
