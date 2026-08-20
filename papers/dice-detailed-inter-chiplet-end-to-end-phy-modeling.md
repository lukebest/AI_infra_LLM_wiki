---
type: Paper
title: "DICE: Detailed Inter-Chiplet End-to-End PHY Modeling"
description: Uppsala — gem5 运行时建模 chiplet PHY（QC-LDPC/PAM4/AWGN）；相对 HeteroGarnet IPC 平均偏移 6.8%、最高 27.6%；EPYC 9454P 跨 die 最大 C2C RMSE 89.5 vs 141.2 cycle
tags:
- chiplet
- interconnect
- noc
- scale-up
- physical-layer
- serdes
- fec
- retransmission
- flow-control
- protocol
- fabric
- communication
- packaging
- architecture
timestamp: '2026-08-20T00:00:00Z'
created: 2026-08-20
sources:
- raw/papers/DICE_Detailed_Inter_Chiplet_End_to_End_PHY_Modeling_2026.pdf
- raw/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md
---

# DICE: Detailed Inter-Chiplet End-to-End PHY Modeling for Accurate Chiplet Simulation

**Authors:** Rashid Aligholipour, Stefanos Kaxiras, Yuan Yao（Uppsala University）
**arXiv:** [2607.24221](https://arxiv.org/abs/2607.24221)（2026-07 投稿窗口；本轮 2026-08-20 取 PDF）
**Venue:** PDF 页眉仍写 *ISCA 2026 Submission — Confidential Draft*；GitHub artifact 自称 ISCA 2026。**未独立核实会议程序册，不当成已录用。**
**PDF:** [raw/papers/DICE_Detailed_Inter_Chiplet_End_to_End_PHY_Modeling_2026.pdf](raw/papers/DICE_Detailed_Inter_Chiplet_End_to_End_PHY_Modeling_2026.pdf)
**Code:** https://github.com/RashidAGP/DICE-Simulator

## 动机

单体多核撞上功耗/热、大 die 良率与测试成本。Chiplet（CCD + IOD，Infinity Fabric / AIB / UCIe 一类封装内 PHY）是工业解法；带宽和布线密度把短距链路推到噪声、串扰、插损边缘，IEEE HIR 已把 **FEC** 写成下一代 PHY 的一等公民。

现有仿真器（gem5+HeteroGarnet、Sniper、BookSim、Noxim、Muchisim、BZSim、CNSim、RapidChiplet）把跨 die 连成**固定延迟或带宽节流**。这抹掉三件运行时耦合的事：信道 SNR 漂移、QC-LDPC 迭代收敛、解不出则重传。作者指出：HeteroGarnet 的包延迟构成几乎长得像 monolithic；相对真实硅，固定延迟有时乐观、有时悲观，**不能靠调一个节流参数校正**。

本文不是 LLM 工作负载论文。增量在 **chiplet 物理层**——补 [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) 停在 AXI/MAC/credit、不建 PAM4/FEC 的那一层。

## 方案

在 gem5 Garnet 里把跨 chiplet 数据路径做成运行时模块，而不是离线查表。

1. **片内**：EPYC 风格。默认 4×CCD，每 CCD 8 核、私有 L1/L2 + 共享 LLC、**2×4 mesh**、2.0 GHz、128-bit、router 1 cycle / link 2 cycle。IOD 居中 2×2 PHY router、8 个内存控制器、1.0 GHz（模拟 IOD 更老工艺）。一致性 MESI-Two-Level。
2. **FEC**：flit 粒度 QC-LDPC。128-bit flit + **2 parity byte**（码率 **R≈0.88**）；控制包 1 flit，数据包 6 flit（HEAD + 4×BODY 承载 64 B cacheline + TAIL）。TSMC **40 nm** Yosys/OpenSTA：flit 级编码器 **175** 标准单元、满足 2.0 GHz；若改成 768-bit 包级则 **2320** 单元且 **达不到** 2.0 GHz。
3. **调制与信道**：PAM4 Gray 映射，摆幅 **±50 / ±150 mV**（d=50 mV）。AWGN 叠 jitter（σ_t≈1 ps → SNR_jitter≈**26.0 dB**）与串扰（SNR_XT≈**20.0 dB**）。默认 SNR_base≈**35.0 dB**（HIR 短距），有效 SNR≈**19.0 dB**，σ≈**12.7 mV**。符号率默认 **32 GT/s**（文称对齐 Infinity Fabric / UCIe 2.0 上限）。
4. **解调/解码**：PAM4 比特 LLR → layered min-sum。35 dB 下各码率均 ≤2 次迭代收敛，预算 **N=4**；综合征 1 cycle、每轮 1 cycle，总时延 **2N+1** cycle。解不出则 NACK 只重传该 flit。
5. **PHY 流控**：边界 router 上 cut-through；发送缓冲按包预留、按 flit ACK；多包可并存，避免 HOL。
6. **对照**：HeteroGarnet 固定延迟节流；Linux C2C 工具测 AMD EPYC **9454P**（8 CCD×6 核）、ThreadRipper **3960X**、EPYC **7R13**。应用侧 14 个负载（GAPBS / SPEC 2017 / Splash-4 / Rodinia / XSBench），每 CCD 一份进程。

## 效果（仅论文数字）

**保真（C2C 延迟 vs 硅）**

| 机器 | 指标 | HeteroGarnet | DICE |
|------|------|--------------|------|
| 9454P 跨 die **最大**延迟 | RMSE | **141.2** cycle（均值 304.6 的 46.4%） | **89.5** cycle（29.4%）；尾部保真相对 HG **+17.0%** |
| 3960X **平均** C2C | RMSE | 36.6（19.1%） | 17.1（8.9%） |
| 7R13 平均 C2C | RMSE | 39.9（18.9%） | 24.9（11.8%） |
| 9454P 平均 C2C | RMSE | 100.4（40.5%） | 73.9（29.8%） |

三台机器平均 C2C 的相对 RMSE 降幅 **7.1%–10.7%**。

**系统指标**

- 相对 HeteroGarnet，IPC **平均偏移 6.8%、最高 27.6%**。文内强调方向**不固定**：HG 对有的负载乐观、有的悲观。
- bfs 跨 chiplet flit：平均 32.99 vs HG 39.26（差约 6 cycle），**尾部 104 vs 61 cycle**。把 HG 平均对齐（HG+）仍补不上长尾；bc 上 HG+ 甚至 backlog 到仿真失败。
- 多线程 XSBench、全局共享 LLC：DICE 相对 monolithic **9.53×** 墙钟（单线程 3.55×）；HG 仅 1.74× / 1.29×。
- FEC 纠正平均 **97.8%** 误 flit，剩 **2.2%** 走重传。SNR_base 低于约 **25 dB** 后，2-byte parity 不够，要加 parity、加迭代或上层 CRC。
- 符号率 2→32 symbol/cycle：APL 下降，**16 symbol/cycle 之后收益递减**；bc/bfs/cc/mcf/XSBench 敏感，leela/radiosity 几乎不动。
- gem5 额外开销 **0.3–26.1%，平均 9.2%**，主要在 layered min-sum 解码。

## 与 wiki 的关系

- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) — LLM 轨迹驱动的 scale-up AXI/MAC/credit DSE；**不建 PAM4/FEC**。DICE 补封装内 PHY 保真，负载是 CPU 多核而非 LLM collective。
- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md) — 把 Physical/Link 从「片上 wire、无 SerDes」扩到 chiplet PAM4+QC-LDPC。
- [UB 物理层](/concepts/ub-physical-layer.md) — 工业 PHY 对照（RS FEC + PAM4）；DICE 是 gem5 里的 QC-LDPC 研究模型，不是 UB 规格实现。
- [Network-on-Wafer](/concepts/network-on-wafer.md) — NoW/WoW hybrid bonding **不需要 SerDes PHY**；DICE 建模的是有机/硅中介层短距 SerDes，层级不同。
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — 垂直 logic-on-logic 隔离 D2D 争用；DICE 是 2.5D CCD–IOD 水平 PHY。
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 板级/机柜 scale-up；DICE 停在封装内 Infinity Fabric 类链路。

## 开放问题

1. 14 个负载里没有 LLM 训练/推理 collective；PHY 长尾会不会打穿 AllReduce/All-to-All 的计算重叠，本文没测。
2. 默认 SNR_base=35 dB 来自 HIR 公开值，不是某条 UCIe 硅的实测 bathtub。
3. PDF 仍是 ISCA 投稿页眉；录用版本数字是否改动未知。
4. 与 [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) 的 AXI 流量发生器尚未对接：一边有 LLM 轨迹，一边有 PHY 误码，中间缺一层。

# Citations

[1] [raw/papers/DICE_Detailed_Inter_Chiplet_End_to_End_PHY_Modeling_2026.pdf](raw/papers/DICE_Detailed_Inter_Chiplet_End_to_End_PHY_Modeling_2026.pdf) — Aligholipour, Kaxiras, Yao, arXiv:2607.24221
[2] [raw/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md](raw/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — 结构化摘录
