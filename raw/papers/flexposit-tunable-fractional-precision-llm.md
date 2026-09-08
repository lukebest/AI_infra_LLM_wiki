---
type: Raw Source
title: FlexPosit — Tunable Fractional Precision for LLM Inference Accelerators
source_url: https://arxiv.org/abs/2609.04724
arxiv: '2609.04724'
ingested: 2026-09-08
sha256: 4a0eddf543036451949a191b8f6a79dae71ba365403d1420d9ac24adb2eb5d0a
---

# FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators

**Authors:** Yimin Gao, Liangtao Dai, Jun Yin, Xinfei Guo, Mircea Stan
**Affiliations:** University of Virginia; Shanghai Jiao Tong University
**PDF:** [FlexPosit_Tunable_Fractional_Precision_LLM_2026.pdf](FlexPosit_Tunable_Fractional_Precision_LLM_2026.pdf)
**arXiv:** [2609.04724](https://arxiv.org/abs/2609.04724)（2026-09-04，cs.AR；ASP-DAC 2027）

## 问题

LLM 量化在粒度与位宽间权衡：group-wise 准但缩放/控制开销大；channel-wise 规整但低比特精度差。现有加速器多为离散精度模式，未覆盖「分数位宽」设计空间。

## 方法要点

- 算法：Posit 锥形精度 + 分布感知量化 + 敏感度引导的 channel-window 混合精度（硬件对齐的 MPQ）。
- 架构：统一 bit-serial 脉动阵列；per-column SerialPosit decoder；GPCU 全局精度控制；4-way MAC cluster 抵消 bit-serial 吞吐损失。
- 目标：channel-wise 规整度 + 接近 group-wise 精度，且可在 4–8 bit 连续调分数精度。

## 摘录数字（仅论文给出）

- 工艺：商业 **16 nm**；RTL + 综合；iso-area 对照 32×16 FlexPosit（PE 面积约 FP16 的 **0.12×**，118.2 µm²）。
- 相对 BitMoD（group-wise）：最高约 **1.8×** 吞吐、**1.2×** 更低能耗；相对 OliVe（channel-wise）：约 **1.5×** 吞吐、**2.0×** 更低能耗（摘要/结论；iso-PPL / PEB 设定）。
- 大负载点 (B=8, L=8192)：相对 FP16 / BitMoD / OliVe 加速 **3.4× / 1.6× / 1.2×**，能耗降 **3.5× / 1.2× / 1.8×**。
- sub-5-bit 权重下接近 FP16 PPL；4.1 b 起即可大幅恢复精度。
- **仿真/综合**，非硅实测。
