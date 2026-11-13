---
type: Paper
title: "SFU-Sim: Bit-Exact Reverse Engineering of NVIDIA MUFU and Validation of PTX Paths"
description: "中山大学 — 黑盒反演 NVIDIA MUFU 并补上 PTX 外围运算；A100 / RTX 4060 / RTX PRO 5000 上 12 条常见路径全输入域逐比特 0 mismatch；8 个 FP32 函数系数不到 10 KB，相对存全表约 128 GiB"
tags:
- nonlinear
- activation
- gpu
- nvidia
- isa
- microarchitecture
- simulator
- formal-analysis
- hardware
- architecture
created: 2026-11-13
updated: 2026-11-13
timestamp: '2026-11-13T00:00:00Z'
paper_author: [Haozhi Xie, Tao Su]
year: 2026
venue: arXiv preprint
arxiv: '2611.13879'
sources:
  - raw/papers/SFU_Sim_NVIDIA_MUFU_Bit_Exact_2026.pdf
  - raw/papers/sfu-sim-nvidia-mufu-bit-exact.md
---

# SFU-Sim：按比特复现 NVIDIA 特殊函数单元

## 一句话结论
中山大学的 **SFU-Sim** 在真实 GPU 上对 NVIDIA 多功能单元（MUFU）做黑盒反演，再补上 PTX 路径里 MUFU 前后的外围运算，得到可直接计算的逐比特模型。覆盖 12 条常见形式，并在测试的 Blackwell 上另加两条 BF16 形式。在 Ampere A100、Ada RTX 4060 Laptop 与 Blackwell RTX PRO 5000 上，对指定输入域做穷尽比对：FP32 走完全部 2³² 编码，FP16 走完全部 2¹⁶ 编码，模型输出与硬件逐比特一致，mismatch 为 **0**。8 个 FP32 函数的系数合计不到 **10 KB**；若改存这 8 个函数在全部 2³² 输入上的输出，大约需要 **128 GiB**。

## 动机
厂商文档通常只给特殊函数的语义与误差上界（最大 ULP 或区间误差），同一上界仍允许不同的分段系数、中间位宽与截断点，因而不能决定每个输入的输出比特。PTX 是虚指令，一条近似特殊函数既可能直接对应一条 MUFU，也可能在前后附加缩放、修正或格式转换；只建模裸 MUFU，或只按文档误差实现，都不足以复现程序看到的结果。早期 envytools 可读 G80/Tesla 的表项，无法直接用于本测试的现代器件；Cankaya 则用 GB 级查找表保存硬件输出。

## 方案
1. **先划裸 MUFU 边界，再补外围**：反汇编 PTX→SASS 路径，把 MUFU 本身与前后运算分开建模。
2. **以 SIN/COS 走完整流程**（§III-B / Fig 4）：周期归约与象限映射、64 段（高 6 位索引 + 17 位段内坐标）、Q37 定点二次式，以及截断平方 S₁₅(v)（保留部分积列 m+n≥14，第 14 列作进位守卫，Fig 3）。外围包括 FMUL.RZ 预乘 1/(2π)。
3. **七个数值核心家族**（Table IV）：SIN/COS、EX2、TANH、RCP、RSQ、LG2、SQRT；同家族共用分段系数与求值规则。窄格式复用 FP32 核心（FP16 先拓宽再向零截断；BF16 放在 FP32 高 16 位并保留高 16 位结果）。
4. **验证设备**：A100（sm_80）、RTX 4060 Laptop（sm_89）、RTX PRO 5000 Blackwell（sm_120）。开源：https://github.com/hzX40000000/SFU-Sim 。作者写明这是功能等价模型，并不宣称等同芯片内部实现。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 常见最小 PTX 路径 | 12 条在三款 GPU 上均为 **0 mismatch**；Blackwell 上两条 BF16（EX2、TANH）同样为 0 | Table V |
| FP32 输入域 | EX2 / LG2 / RCP / RSQ / SQRT / SIN / COS / TANH 共 8 条，各覆盖全部 **2³²** 编码 | Table V |
| FP16 / FP64 高字 | EX2、TANH 全部 **2¹⁶**；RCP、RSQ 全部 **2³²** 高字（低字固定 0），比较完整 64 位输出 | Table V |
| A100 扩展路径 | 7 条非 .ftz FP32 近似、2 条 FP16x2、8 条带 RN/RZ/RM/RP 的 FP32 RCP/SQRT；各覆盖全部 2³²（FP16x2 为两个半字的全部组合），均为 **0 mismatch** | Table VI |
| 模型体积 | 8 个 FP32 函数系数合计不到 **10 KB**；存齐 8 个函数全部 2³² 输出约 **128 GiB** | §III-C |

Table VI 中带四种舍入模式的 RCP/SQRT 路径，是按 PTX 最终舍入语义预测输出；作者写明这只验证最终 PTX 结果，并不单独验证 MUFU 中间值。

## 与 wiki 的关系
- [In-Core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — 把 GPU 特殊函数从误差上界推进到逐比特可计算模型
- [RVV vs CGRA 非线性 SoC](/papers/rvv-cgra-nonlinear-functions-soc.md) — 同属核内非线性，对象是 RISC-V 向量与 CGRA 的 SiLU / softmax 实现
- [Tri-Stack-PIM](/papers/tri-stack-pim-heterogeneous-3d-llm.md) — 把 softmax 留在 3D 栈中层；本篇给出 GPU 侧特殊函数的比特级参照
- [NVIDIA NVLink Hopper/Blackwell](/papers/nvidia-nvlink-hopper-blackwell.md) — 同系列 GPU 微架构上下文（Ampere / Ada / Blackwell）

## 开放问题
- BF16 形式只在测试的 Blackwell（sm_120）上验证；其他架构的 BF16 路径未给出。
- 带舍入模式的 RCP/SQRT 未独立核对 MUFU 中间结果。
- 模型用于指令模拟器或硬件功能验证时，需要跟着新的 SASS / PTX 组合再做路径确认。

# Citations
- [arXiv:2611.13879](https://arxiv.org/abs/2611.13879) — Xie & Su（中山大学）
- [raw stub](/raw/papers/sfu-sim-nvidia-mufu-bit-exact.md)
- [PDF](/raw/papers/SFU_Sim_NVIDIA_MUFU_Bit_Exact_2026.pdf)
- [SFU-Sim 源码](https://github.com/hzX40000000/SFU-Sim)
