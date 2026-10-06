---
type: Raw Source
title: "AFORE: Attention–FFN Disaggregation with Overlapped Reconfiguration of Experts"
source_url: https://arxiv.org/abs/2610.03203
ingested: 2026-10-06
arxiv: '2610.03203'
pdf: AFORE_AFD_Expert_Reconfiguration_2026.pdf
---

HKUST / Cambridge / 武汉大学 — Wenshuang Li, Youhe Jiang, You Peng, Jiawei Jiang, Binhang Yuan。cs.DC。AFD（attention–FFN 解耦）MoE serving 下的微批级专家重配置：利用 attention 侧提前暴露的下一微批 expert-token 分布做 demand prefetch，并在 AFD 流水窗口内用 NVLink GPU-GPU 拷贝重叠迁移。2×8 A100（NVLink 300 GB/s/GPU；8×50 GB/s RDMA bond/节点），GLM-4.5-Air 110B，PD+AFD，ShareGPT/FineWeb/CodeForces/GSM8K 四种回放。本地 PDF：`AFORE_AFD_Expert_Reconfiguration_2026.pdf`。
