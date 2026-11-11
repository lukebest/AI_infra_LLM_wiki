---
type: Raw Source
title: "To SIMD or Not to SIMD: Comparing RVV vs. CGRA SoCs for Non-Linear Functions in AI"
source_url: https://arxiv.org/abs/2611.12435
pdf: RVV_vs_CGRA_Nonlinear_Functions_AI_2026.pdf
retrieved: 2026-11-11
ingested: 2026-11-11
org: Fujitsu Research of Japan
venue: H2RC workshop at SC26
---

# Abstract (verbatim gist, arXiv:2611.12435)

Non-linear functions are an important class of operations in modern large language models. However, chip vendors building for AI have so far relied on traditional vector or scalar processing units for non-linear functions. The performance of these units has not kept pace with matrix multiplication units (MMUs), which can be found in both high-performance and edge-computing devices from almost every vendor. Reconfigurable units such as FPGAs and CGRAs have been proposed in the literature, but have not been systematically compared with traditional units backed by MMUs. In this paper, we build two SoCs: one using an RVV vector processor and the other using a latency-insensitive (elastic) CGRA, both coupled with an MMU and driven by a single-core CPU. We then propose mappings for common feed-forward networks on our SoCs and find that the CGRA reaches a maximum speedup in clock cycles of 7.12x over RVV on the activation stage of simple point-wise non-linear functions like SiLU, whereas the RVV reaches a maximum speedup of 9.8x over the CGRA on complex non-linear functions such as softmax. Over the enclosing feed-forward block the corresponding maxima are 3.16x and 4.24x.

# Excerpts / key facts

- Authors: Sameer Deshmukh, Naoya Mizuki, Takumi Honda (Fujitsu Research of Japan / Fujitsu Limited, Kawasaki). Venue: SC26 Workshops (H2RC), November 15–20, 2026, Chicago. arXiv:2611.12435, 2026-11-09/10, cs.AR.
- 两个 SoC 共用 Gemmini 矩阵单元与单核 in-order Rocket RV64GC：ME-VE = Saturn RVV 1.0 向量（128-bit VLEN，4-stage pipeline）+ Gemmini；ME-RE = 弹性 RIKEN 4×4 CGRA（CGRA-ME）+ 同一 Gemmini。比较在相同时钟下报告 cycle（DRAMSim2 0.66 GHz，CPU 0.5 GHz）。工作负载：SwiGLU（3 个 GEMM + SiLU）与 Attention（GEMM + softmax）。问题规模 N=16,32,64,128。RTL 仿真，弃冷启动，热启动同测量最大差 0.93%。
- Table III / Fig 4（SiLU 激活阶段，cycle）：N=16 ME-VE 8,715 vs ME-RE 1,224 → **7.12×**（CGRA 快）；N=32 34,619 vs 5,568；N=64 138,576 vs 21,752；N=128 552,435 vs 87,522（约 6.3×）。整块 SwiGLU 总 cycle N=16：10,955 vs 3,467 → **3.16×**。
- Fig 6：去掉 ME-VE 的软件 exp 后，激活阶段仍比 CGRA 慢 **5.4–6.2×**；exp 只占 ME-VE 激活 **12.7–13.2%**。CGRA 把 SiLU 铺成 27-cycle 空间数据通路，满管后每周期一个元素。RVV 无指数指令，用 19 个向量操作的软件 kernel（degree-5 Taylor，最坏相对误差 3.2×10−6 / 约 27 ULP；minimax 同次数可达 7.5×10−8）。CGRA 用 FloPoCo 流水硬件 exp。
- Table III / Fig 7（softmax 激活）：N=128 ME-RE 1,462,554 vs ME-VE 149,015 → RVV **9.8×**；N=16 约 7.5×，N=32 约 9.1×。整块 Attention 总 cycle N=32：117,022 vs 27,610 → **4.24×**（RVV 快）。
- 精度（Fig 5，相对 PyTorch FP32 的 L2）：SwiGLU 上 ME-RE 2.5–3.7×10−8，ME-VE 8.2×10−8–5.5×10−7。Attention N=128 参考地板 2.6×10−7：ME-RE 2.9×10−7（1.10× 地板），ME-VE 4.0×10−7（1.54×）。
- 分析：softmax 需要归约 + 再遍历；CGRA scratchpad 有限，元素要加载两次，且通信与计算串行。作者估计仅克服「core copy」大约能拿回约 30% cycle，其余仍受映射与控制开销限制。
