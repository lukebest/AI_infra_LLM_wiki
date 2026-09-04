---
type: Raw Source
title: Scaling Inference Prefill with High-Radix Photonic Interconnects
source_url: https://arxiv.org/abs/2609.01821
arxiv: '2609.01821'
ingested: 2026-09-04
sha256: c5d747603efdc5ade7f51dbd5d3be00062423fd3420517fe86417fc42e4499b6
---

# Scaling Inference Prefill with High-Radix Photonic Interconnects

**Authors:** Arulselvan Madhavan, Peter Carson, Taylor Groves, Thomas Graham
**Affiliations:** （文内未另标机构；引用 Lightmatter Passage 作 3D 光子参考点）
**PDF:** [Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf](Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf)
**arXiv:** [2609.01821](https://arxiv.org/abs/2609.01821)（2026-09-01，cs.DC / cs.AR）

## 问题

推理已占 80–90% 算力周期；agentic prefill 中位 ~96K tokens。Prefill 大批次抬高 TP/EP/SP 集体流量，铜互连 reach 在 224G ~1 m、448G 数十 cm，电学 scale-up pod 通常困在单机柜（~72–144 GPU）。通信可占 prefill 延迟 >50%（带宽受限 GPU 上 TP >65%）。

## 方法要点

- XLA/MLIR 成本模型捕获生产级 TP/EP/CP 划分与集体；重叠延迟。
- 三档 MoE（Mini 21B / R1 42B / Next 201B active；MLA）；FP4/FP8。
- 电学基线 B200/B300/Rubin/R4†；光学配对：同算力/HBM、**4×** SU 带宽、最大 **1152** GPU 全光 scale-up。
- Passage 作带宽/radix/能耗参考（>64 Tb/s bi-dir、~4.3 pJ/bit），不直接仿真厂商产品。
- Device sweep + batch sweep；另做 disaggregated serving DES（72 GPU：6×8 prefill + 1×24 decode）。

## 摘录数字（仅论文给出）

- 摘要：高 batch **2.1–3.2×**；通信受限 **2.8–5.8×**；跨电学 pod 边界生产平台 **2.2–4.5×**。
- B300 FP4 R1：1K ~**2.6×**、8K ~**2.2×**、128K ~**2.9×**、1M ~**2.3×**（72–1152 GPU 扫）。
- 8K@72、batch 2048：电学通信 ~40.6 s / 算力 16.8 s；光学通信 ~10.2 s。
- 128K@288：电学通信 35.5 s；光学 2.3 s（B300 ~2.8–3.0×；B200/Rubin ~4.3–5.8×）。
- 1M@1152：电学通信 39.2 s → 光学 1.6 s；重叠延迟 27.5 s（B300 ~2.3×）。
- Table IV 峰值：Rubin 128K@288 最高 ~**5.5–5.8×**；R4 1M@1152 ~**8.0–8.5×**。
- DES：p99 TTFT −12–20%；故意单 decode worker 时 p99 TPOT +77–110%；E2E 近中性。
- **分析/投影**，非已部署光子硬件实测。
