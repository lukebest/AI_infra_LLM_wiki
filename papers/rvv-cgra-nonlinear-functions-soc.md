---
type: Paper
title: "To SIMD or Not to SIMD: Comparing RVV vs. CGRA SoCs for Non-Linear Functions in AI"
description: "Fujitsu H2RC@SC26 — 同配 Gemmini 的 RVV 与弹性 CGRA SoC；SiLU 激活阶段 CGRA 最高 7.12×，softmax 上 RVV 最高 9.8×；整块 FFN 对应 3.16× / 4.24×"
tags:
- nonlinear
- activation
- accelerator
- cgra
- risc-v
- soc
- attention
- hardware
- fpga
- architecture
- kernel
created: 2026-11-11
updated: 2026-11-11
timestamp: '2026-11-11T00:00:00Z'
paper_author: [Sameer Deshmukh, Naoya Mizuki, Takumi Honda]
year: 2026
venue: H2RC workshop at SC26
arxiv: '2611.12435'
sources:
  - raw/papers/RVV_vs_CGRA_Nonlinear_Functions_AI_2026.pdf
  - raw/papers/rvv-cgra-nonlinear-functions-soc.md
---

# RVV 与 CGRA：给 AI 非线性函数配什么样的 SoC

## 一句话结论
富士通研究院做了两套共用 **Gemmini** 矩阵单元、由单核 Rocket CPU 驱动的 SoC：ME-VE 配 Saturn **RVV 1.0** 向量单元，ME-RE 配弹性 **RIKEN 4×4 CGRA**。在相同时钟的 cycle 计数下，点式非线性（SiLU）的激活阶段，CGRA 相对 RVV 最高 **7.12×**（N=16）；带归约的复杂非线性（softmax），RVV 相对 CGRA 最高 **9.8×**（N=128）。摊到整块前馈（含 GEMM），对应最高 **3.16×** 与 **4.24×**。

## 动机
GEMM 单元用低精度越做越快，非线性仍常走 FP32 的向量或标量单元，节奏已经跟不上（文中举 FlashAttention 4 因 Tensor Core 与 SM 差距，在软件里模拟指数）。已有工作用 FPGA/CGRA 做非线性，缺少与「同一套矩阵单元 + 传统向量单元」的对照。

## 方案
1. **ME-VE**：Saturn RVV 1.0，VLEN=128 bit，4 级流水，32 个向量寄存器；Gemmini 作矩阵引擎。
2. **ME-RE**：弹性 RIKEN CGRA（CGRA-ME），把 SiLU / softmax 映射到 4×4 阵列；矩阵单元同为 Gemmini。
3. 工作负载：SwiGLU（3 个 GEMM + SiLU）与 Attention（GEMM + softmax），N=16/32/64/128。比较报告 cycle（DRAMSim2 0.66 GHz，CPU 0.5 GHz）。RTL 仿真弃冷启动，热启动最大差 **0.93%**。
4. RVV 无指数指令，用 19 个向量操作的软件 kernel（degree-5 Taylor）；CGRA 用 FloPoCo 流水硬件 exp，SiLU 铺成 27-cycle 空间数据通路，满管后每周期一个元素。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| SiLU 激活阶段（CGRA vs RVV） | N=16：8,715 vs 1,224 cycle，**7.12×**；N=128 约 6.3× | Table III / Fig 4 |
| 整块 SwiGLU | N=16 总 cycle 10,955 vs 3,467，**3.16×** | Table III |
| 去掉软件 exp 之后 | exp 只占 ME-VE 激活 **12.7–13.2%**；去掉后仍比 CGRA 慢 **5.4–6.2×** | Fig 6 / §V-A1 |
| softmax 激活阶段（RVV vs CGRA） | N=128：149,015 vs 1,462,554 cycle，**9.8×**；N=16 约 7.5×，N=32 约 9.1× | Table III / Fig 7 |
| 整块 Attention | N=32 总 cycle 27,610 vs 117,022，**4.24×** | Table III |
| 相对 PyTorch FP32 的 L2 误差 | SwiGLU：ME-RE 2.5–3.7×10−8，ME-VE 8.2×10−8–5.5×10−7；Attention N=128 地板 2.6×10−7，ME-RE 1.10× 地板、ME-VE 1.54× | Fig 5 |

softmax 变慢的主要原因是归约后再遍历：CGRA scratchpad 有限，元素要加载两次，通信与计算串行。作者估计只克服「core copy」大约能拿回约 30% cycle。

## 与 wiki 的关系
- [In-Core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — 点式 SiLU 与带归约 softmax 对向量 / CGRA 的相反偏好
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 矩阵阵列旁的非线性伴生单元
- [FlashAttention 长向量重排](/papers/flashattention-long-vector-riscv.md) — 同属「RVV 无硬件 exp」的对照
- [FuseLSE / IntLSE](/papers/fuselse-intlse-logsumexp-neurips2026.md) — 独立 LSE / 近似指数路径

## 开放问题
- 评测是 RTL 仿真 cycle，不是硅上 wall-clock；频率、面积与功耗交叉点未报。
- 矩阵与非线性吞吐比的扫描留作未来工作；更大 scratchpad 与通信计算重叠能回收多少 softmax 差距，文中只给了约 30% 的 partial 估计。
- RVV 软件 exp 若改 minimax 系数，精度可接近 1 ULP，cycle 不变；这是基线的易改进项。

# Citations
- [arXiv:2611.12435](https://arxiv.org/abs/2611.12435) — Deshmukh, Mizuki, Honda（Fujitsu）；H2RC @ SC26
- [raw stub](/raw/papers/rvv-cgra-nonlinear-functions-soc.md)
- [PDF](/raw/papers/RVV_vs_CGRA_Nonlinear_Functions_AI_2026.pdf)
