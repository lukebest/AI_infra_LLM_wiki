---
type: Raw Source
title: ThAME 3D Memory-Enabled Heterogeneous Accelerator for LLM MoE
source_url: https://arxiv.org/abs/2607.17074
arxiv: '2607.17074'
ingested: 2026-08-19
sha256: a11a93535149c27b661e91314b743090c08beec07b4ca44307194141d9f63147
---

# ThAME: 3D Memory-Enabled Heterogeneous Accelerator for LLM Mixture of Experts

**Authors:** Pratyush Dhingra, Pramit Kumar Pal, Janardhan Rao Doppa, Partha Pratim Pande (Washington State University)
**PDF:** [ThAME_3D_Memory_Enabled_Heterogeneous_MoE_2026.pdf](ThAME_3D_Memory_Enabled_Heterogeneous_MoE_2026.pdf)
**arXiv:** [2607.17074v2](https://arxiv.org/abs/2607.17074) (v1 2026-07-19, v2 2026-08-02)
**Venue:** IEEE/ACM ESWEEK-26（文内/abs 自称 accepted）

## 问题

MoE 推理三瓶颈：非连续 expert 权重带宽、输入相关 scatter-gather、同步 gather 的尾延迟。单一 DRAM/NVM 对 attention（RMW、耐久）与 expert（静态高密度）不匹配；标准 mesh/ring 不适合非确定 token 路由。

## 方法要点

- 2.5D UCIe 封装：host TPU v6e 做 prefill/gating；3D DRAM-PNM 做 attention（KV 留在 chiplet 内）；3D FeFET-NAND-PNM 做 expert。
- 垂直：CBA + Cu-Cu hybrid bonding；FeFET 读 ~10 ns / ~3 V vs Flash ~ms / ~20 V。
- FeFET 基座 32 核 systolic；分层树 NoC（局部 crossbar + 树）对所有输入相关流量先验做 MOO（均值利用率、σ、面积），相对 mesh 链路数不增。
- min-max 核分配调度（二分搜索 Eq.11），同步 gather 回 host。封装上只走 O(B·d_model) 激活，不搬 expert 权重。

## 摘录数字（仅论文给出）

- 相对 H3D-T / Stratum：TBT 最高 **15.7× / 10.2×**，能效 **9.8× / 5.6×**（B=32, MMLU）。
- Qwen1.5：TBT **2.17–2.22 ms** vs TPU v6e 18.12 / A100 22.93；约 **8.2× / 10.5×**。
- 每 token 能量 ≈**6.7 mJ** vs TPU 141 / A100 214。
- 147.5 Tokens/s/W：相对 Stratum / TPU / A100 为 **5.6× / 20.9× / 31.7×**。
- B=64 DeepSeek：吞吐相对 Stratum / H3D-T **5.92× / 12.77×**。
- 分层 NoC BFT(2,4,2) 相对 Ring 平均延迟 **4.1×**；相对 Mesh 延迟最多 **1.44×**、能效 **2.1×**（消融）。
- FeFET 容量 64 GB（每 chiplet 32 GB）；峰值带宽 ~14.7 TB/s vs 核需求 ~3.28 TB/s。
