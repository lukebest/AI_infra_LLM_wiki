---
type: Paper
title: "Understanding the Power Consumption of Modern HBM: Real HBM2 Chip Characterization"
description: "ETH SAFARI MICRO'26 — 36 颗真实 HBM2 功耗实测：读电流是 refresh 的 3.1×，BG 总线翻转多耗 29.4%，构造访存模式比 JEDEC 最高测试环高 23.6%（最高 35.4%）；新模型 Ayna MAPE 7.6–8.1%，H200 HBM3E 误差 2.4–5.3%，HBM4 8 Gbps 读能耗与 HBM3E 持平到低 6%"
tags:
- hbm
- memory
- power
- 3d
- tsv
- memory-bandwidth
- benchmark
- llm
- nvidia
created: 2026-10-15
updated: 2026-10-15
timestamp: '2026-10-15T00:00:00Z'
paper_author: [Ataberk Olgun, Spiros Galanopoulos, Andreas Kosmas Kakolyris, İsmail Emir Yüksel, Haocong Luo, F. Nisa Bostancı, Onur Mutlu]
year: 2026
arxiv: '2610.14244'
venue: MICRO 2026（扩展版）
sources:
  - raw/papers/HBM2_Power_Characterization_Real_Chips_2026.pdf
  - raw/papers/hbm2-power-characterization-real-chips.md
---

# 真实 HBM2 芯片功耗实测与建模

## 一句话结论
HBM 芯片里数据搬运占功耗的比重更高，并且强烈依赖数据模式与内部总线（TSV、bank group 总线）翻转。只按 JEDEC 测试环或厂商 IDD 估功耗会低估真实 AI 负载，可能导致热降频甚至失效。作者用 36 颗真实 HBM2 做出首个系统性测量，并据此建了一个开源 HBM 功耗模型 Ayna，在 H200 的 HBM3E 上也对得上。

## 动机
- 作者实测三台 H200 的 HBM3E 平均功耗最高 **248 W**，约占 700 W 预算的 **35%**。
- HBM 与平面 DDR 有两点结构差异：数据 I/O 引脚从个位数到上千；数据要经过 TSV、bank group 总线等多级不同宽度/频率的内部总线。公开的真实 HBM 命令电流数据几乎没有。

## 方法
- 18 块 AMD Alveo U55C FPGA 板上的 36 颗 HBM2，基于 DRAM Bender 搭测试平台，最高 600 MHz（1200 MT/s），温度 48–86 °C。
- 测 JEDEC 标准电流测量环（IDD2N/3N/0/4R/4W/5B 等），扫温度、带宽、结构位置（通道/伪通道/bank group/bank）和 32 种数据模式。

## 关键发现（论文数字）
- 读操作电流是 refresh 的 **3.1×**（平面 DDR3L 里 refresh 最大）；实测全 0 的 IDD4R 为 **1716 mA**，现有 HBM2 模型用的是 1079 / 966 mA。
- 电流随温度线性上升，平均每 1 °C **+6.7 mA**。
- 读电流跨 bank group 差 **8.1%**、跨 bank 差 **5.3%**。
- 翻转全部 bank group 总线信号比保持不变多耗 **29.4%**；据此构造的访存模式比 JEDEC 最高功耗测试环 IDD4R 平均高 **23.6%**、最高 **35.4%**。

## 模型 Ayna（基于 DRAMPower）
- 把芯片内数据相关能耗拆成 TSV 翻转与 bank group 总线翻转两项：读能耗/bit 误差从校准后 FGDRAM 的 **11.4%** 降到 **2.3%**。
- 36 颗芯片、多种负载（含 Llama3.1-8B decode）MAPE **7.6–8.1%**，Llama 负载 **5.2–7.3%**；现有模型 **20–42%**。DRAMSim3 预测 Llama3.1-8B decode（batch 8）**2235 mW**，实测 **4201 mW**。
- H200 验证：高读带宽微基准功耗误差在 HBM3E 电压范围内 **2.4–5.3%**；空闲功耗误差较大（12.0–20.3%）。
- HBM4 推算：读能耗随速率升高（VDDC 1.05 V/VDDQ 0.9 V 下 4.8→8.0 Gbps 为 **6.24→6.73 pJ/bit**）；8 Gbps HBM4 与 6.4 Gbps HBM3E 同电压时相差 **0.1%** 以内，降压到 (1.05, 0.7) / (1.00, 0.7) V 时低 **1.5% / 6.0%**。
- 开源：CMU-SAFARI/HBM-Power，并并入 Ramulator 2.1。

## 与 wiki 的关系
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 补上 HBM 功耗这一维：数据搬运与内部总线翻转主导
- [TSV 3D Physical Layer](/concepts/tsv-3d-physical-layer.md) — TSV 翻转作为独立能耗项被单独建模
- [Handy HBM 开场](/papers/hc2026-handy-hbm-tutorial.md)、[Samsung HBM base die](/papers/hc2026-samsung-hbm-base-die.md) — Hot Chips 侧的 HBM 产业视角；本文给出实测功耗基线
- [Terracotta](/papers/terracotta-flexible-dram-interface-controller.md) — 同一 SAFARI 组的可编程 DRAM 控制器；功耗模型可用于评估这类新命令
- [FORGE](/papers/forge-procedural-weight-generation-sparse-moe.md) — 同日入库，减少 MoE 权重读取；读是 HBM 最耗电操作

## 局限与开放问题
- 实测对象是 HBM2（FPGA 平台，最高 1200 MT/s）；HBM3E/HBM4 依靠外推，H200 侧只能用 nvidia-smi 测整体显存功耗，HBM3E 真实电压未公开。
- 无主动温控；奇偶位置芯片的 IDD2N 差异部分来自 FPGA 封装与板级集成。
- 对架构设计的含义：编码/数据翻转率优化（如数据总线反转、权重布局）可能直接影响 AI 负载的 HBM 功耗，值得在 KV/权重布局研究中纳入（本页判断）。

# Citations
- Olgun et al., "Understanding the Power Consumption of Modern High Bandwidth Memory: Experimental Analysis and Modeling Using Real HBM2 DRAM Chips", MICRO 2026, arXiv:2610.14244. [raw](/raw/papers/hbm2-power-characterization-real-chips.md) · [PDF](/raw/papers/HBM2_Power_Characterization_Real_Chips_2026.pdf)
