---
type: Raw Source
title: FEATHER Reconfigurable Accelerator Dataflow Switching
source_path: /home/luke/snap/zotero-snap/common/Zotero/storage/PSQXZXHU/Tong 等 - 2024 - FEATHER A Reconfigurable Accelerator with Data Reordering Support for Low-Cost On-Chip Dataflow Swi.pdf
arxiv: '2405.13170'
ingested: 2026-06-24
sha256: 37258b2749301e77b3a446c8f4cea2fd1238df664867768432c9304018db5705
---

# FEATHER: A Reconfigurable Accelerator with Data Reordering Support for Low-Cost On-Chip Dataflow Switching

**Authors:** Jianming Tong, Anirudh Itagi, Prasanth Chatarasi, Tushar Krishna  
**Affiliations:** Georgia Institute of Technology; IBM Research  
**PDF:** [FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf](FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf)  
**arXiv:** 2405.13170v1 (May 2024) | **Code:** https://github.com/maeri-project/FEATHER

## 问题

ML 加速器 per-layer 最优 dataflow 可差两个数量级，但切换 dataflow 需 **on-chip layout reorder** + datapath 重配。忽略 layout → bank port 冲突 → 实践比理论慢 **128×**。现有方案：固定 dataflow（DPU/Gemmini）或片外 reorder（Eyeriss v2/SIGMA）。

## 架构

- **NEST**：2D PE 阵列，local temporal + 行间时分 spatial reduction
- **BIRRD**：蝶形 arbitrary reduction + **Arbitrary Reorder**
- **RIR**：Reorder in Reduction——归约时写出下一层 concordant layout

## Layoutloop

Timeloop 增强：物理 buffer (num_line × line_size)、bank port 冲突建模、dataflow-layout co-search。

## 结果

- Layoutloop：**1.27–2.89×** 延迟，**1.3–6.43×** 能效 vs NVDLA/Eyeriss/SIGMA
- ZCU104 FPGA：**3.91× / 2.65×** vs Gemmini/Xilinx DPU
- 面积：**+6%** vs 固定 Eyeriss-like
