---
type: Raw Source
title: "Hardware Acceleration of Vision-Language-Action Models with Weight Precision Rising over the Flow Steps"
source_url: https://arxiv.org/abs/2611.24234
pdf: Rising_Precision_VLA_Accelerator_2026.pdf
retrieved: 2026-11-23
ingested: 2026-11-23
org: MICAS, KU Leuven
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.24234)

Vision-language-action (VLA) models such as GR00T control robots through an action head: a diffusion transformer that turns noise into a chunk of actions in a few flow-matching steps. Every step re-reads all of the head's weights from DRAM but applies each weight to only about fifty tokens. Inference is therefore memory-bound, and its latency and energy are largely determined by the total number of transferred weight bits. We show that later flow steps attenuate the quantization errors of earlier steps, so the weight precision of an action head should rise over the steps. With plain per-channel rounding and without calibration or training, widths rising over the steps from 2 to 4 bits preserve the closed-loop success of robot policies. These widths transfer 25% fewer bits than 4-bit weights at every step. However, we show that on Jetson AGX Thor, current GPU kernels cannot exploit this per-step precision due to fixed overheads. We therefore present a programmable accelerator whose latency and energy both scale with the transferred weight bits. It decodes entropy-coded weights for bit-serial sub-arrays at the DRAM rate. Because the width changes per step, a run-time allocator divides these sub-arrays between the linear layers and the attention to balance their workloads. The same sub-arrays are thus capable of running action heads of different families and sizes, as well as a vision-language model. On the DRAM side, a requantizer and an entropy encoder at each bank let one stored 8-bit copy replace the copies of all widths. Simulated with LPDDR5X timing, our RTL implementation runs the GR00T N1.6 action head in 8.02 ms per inference with 2, 3, 3 and 4 bits in its four flow steps. With a copy per width and 50% of Thor's memory bandwidth, the accelerator runs this schedule 1.7x faster than Thor in NVFP4, at 9.1x less energy and equal closed-loop success.

# Excerpts / key facts

- Authors: Robin Geens, Simon Haepers, Jonas Crols, Chao Fang, Marian Verhelst（MICAS, KU Leuven）。arXiv:2611.24234，cs.AR，提交标注 18 Nov 2026。
- 接口：八条 x16 LPDDR5X-8533，峰值 136.5 GB/s（Thor 带宽的 50%）。Chisel RTL + Ramulator 2；TSMC 7 nm、1 GHz 综合。加速器面积 4.6 mm²，PHY 估计 14.4 mm²，共 19 mm²（60% 逻辑密度）。
- [2,3,3,4] 在 GR00T N1.6 上为 8.02 ms（125 Hz）、78 mJ；Thor 在 idle 之上为 543 mJ。相对 Thor 与 FlashRT NVFP4 均为 1.7×，能量为 FlashRT NVFP4 的 1/9.1。缩放到 Thor 带宽时，均匀 8-bit 为 1.3×，[2,3,3,4] 为 3.1×。
- 闭环成功率来自仿真（约 1700 H100 小时）。[2,3,3,4] 在八套基准里的五套上保持成功率（90% 区间高于 −3 个百分点）；G1 上成功率下降。作者写明量化策略在仿真中成立时，在真实机器人上有过失败记录；Quantization-in-DRAM 需要现有商用颗粒尚未提供的模式。
