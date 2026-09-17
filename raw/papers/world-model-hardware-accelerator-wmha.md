---
type: Raw Source
title: "The World Model Hardware Accelerator"
source_url: https://arxiv.org/abs/2609.16244
arxiv: '2609.16244'
ingested: 2026-09-17
sha256: b5c95edbd78e3e158d27fa467d33f66e4578a1aedbce6e98c8ae997b2074eefc
---

# The World Model Hardware Accelerator (WMHA)

**Author:** Shashank Chaurasia（独立研究）
**PDF:** [World_Model_Hardware_Accelerator_WMHA_2026.pdf](World_Model_Hardware_Accelerator_WMHA_2026.pdf)
**arXiv:** [2609.16244](https://arxiv.org/abs/2609.16244)（cs.AR；列表日 Wed 9/16 交叉/近邻）

## 问题

Diffusion transformer 每步是完整序列前向、形状编译期已知，串行维仅是去噪步数——与自回归 decode 不同。需要 latency-first 的 DiT/世界模型推理加速器。

## 方法要点

- VLIW sequencer：单指令字发 4 引擎（array / VPU / DMA LD / DMA ST）；256-bit 字。
- Weight-stationary **16×16** dual-dot；FP8 E4M3 / BF16，FP32 累加。
- Single-pass online-softmax attention；skewed software pipeline 保 KV 驻留。
- SystemVerilog + UVM；sky130 物理流；语义验收门（轨迹 MSE）。

## 摘录数字（仅论文给出）

- 相对干净 latent，MSE 至少压到 1/10 的门限；实测因子 **23×**；**2.37×10⁸** 元素零失败。
- 指令调度重构：≥2 引擎并发 **1.83%→44.66%** cycles；加速 **1.484×**（算术不变）。
- 全芯片综合：**5,771,328** cells、**68.355 mm²**（sky130，无 dense memory macro）；PE cell **0.05 mm²**。
- 路由引擎例：PE **153.4 MHz / 8.03 mW**；epilogue **76.7 MHz / 172 mW**（post-route measured-activity）。
