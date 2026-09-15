---
type: Raw Source
title: "Dissecting GPU Utilization for LLM Inference on Nvidia Hopper"
source_url: https://arxiv.org/abs/2609.12923
arxiv: '2609.12923'
ingested: 2026-09-15
sha256: a3578bf4fa1d978350de1e0014a07a8016d37f7f5a7f6d95059bf45c1997d057
---

# Dissecting GPU Utilization for LLM Inference on Nvidia Hopper

**Authors:** Mohammad Siavashi, Gerald Q. Maguire Jr., Dejan Kostić, Marco Chiesa
**Affiliations:** KTH Royal Institute of Technology
**PDF:** [Dissecting_GPU_Utilization_LLM_Inference_Hopper_2026.pdf](Dissecting_GPU_Utilization_LLM_Inference_Hopper_2026.pdf)
**arXiv:** [2609.12923](https://arxiv.org/abs/2609.12923)（2026-09-11，cs.PF→cs.AR）

## 问题

单一 SM utilization（sm__throughput）把多种机制压成一个百分比；decode 小行 GEMM 在 Hopper BF16 GMMA 固定 **64-row** fragment 上填不满。

## 方法要点

- H100 NVL（94 GB HBM3）上 vLLM + FlashAttention-3 + cuBLASLt。
- 四模型：Llama-3-8B、Qwen3-14B、Qwen3-32B、Qwen3-30B-A3B；冷/暖 prefill + decode；八个 NCU 锚定利用率视图。

## 摘录数字（仅论文给出）

- 冷 prefill 稠密 GEMM SM util **73–97%**（均值 **92%**）；暖 prefill 塌到 **8–11%**；decode 稠密 **6.5–12.7%**（均值 **9.4%**）。
- GMMA M-fragment fill ηM decode 均值 **5.86%**（范围 **1.6–12.5%**）；可把「有用 matmul」高估 **8–64×**。
- 设备级 compute SOL：冷 prefill **92.0%** vs decode **7.9%**（**11.7×** 差距）。
- Occupancy：decode ~**9.0–9.4** warps/SM = 架构 64-warp 的 **12–15%**，但对 kernel 资源上限常 **75–95%**（分母差约 **5×**）。
- Decode 主 stall：long_scoreboard **70–84%**。
- B=32 验证：稠密 GEMM SM-busy 从 B=1 ~**12%** 升到 **71.9%**；FA3-fwd 占 decode iteration **49.5%**。
