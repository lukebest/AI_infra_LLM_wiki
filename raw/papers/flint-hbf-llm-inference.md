---
type: Raw Source
title: FLINT High Bandwidth Flash for Capacity-Scalable LLM Inference
source_url: https://arxiv.org/abs/2608.25062
arxiv: '2608.25062'
ingested: 2026-08-28
sha256: 26a732a1f0612966eb23a2f773d38104e73bf965c5bf8724b7eaed37bfb4ad2a
---

# FLINT: Efficiently Leveraging High Bandwidth Flash for Capacity-Scalable LLM Inference Acceleration

**Authors:** Geraldo F. Oliveira*, Arash Tavakkol*（共一）, Xiangyu Zhu, Ahmet Caner Yüzügüler, Vamanan Arulchelvan, Lukas Cavigelli, Renzo Andri, Mohammad Sadrosadati, Jia Xinglei, Onur Mutlu, Zhou Ke, Shai Bergman, Ji Zhang
**Affiliations:** Huawei Technologies Switzerland AG / Huawei / ETH Zürich / HUST
**PDF:** [FLINT_HBF_LLM_Inference_2026.pdf](FLINT_HBF_LLM_Inference_2026.pdf)
**arXiv:** [2608.25062](https://arxiv.org/abs/2608.25062)（2026-08-25）

## 问题

单卡/小节点推理被封装容量卡住，不是算力。HBF 能给 TB 级近加速器容量，但既有方案（H3 等）用编译器层前预取 + HBM 基座 SRAM staging，refresh 进关键路径，FTL 还按 SSD 写路径堆。

## 方法要点

- 封装：xPU–HBM D2D，HBM–HBF 再 D2D 级联（daisy-chain），不是 [DASH](../../papers/dash-dual-path-hbf-moe-inference.md) 的三条 UCIe。
- 硬件 burst-buffer：把 LLC miss 聚成 plane-parallel burst；用 NAND 自带 page/cache buffer 做双缓冲，去掉 HBM 侧 LHB。
- Phantom-plane refresh：每 die N+1 物理 plane，1 个离线编程，refresh 不占读通道。
- Read-only FTL：2 MB burst 粒度；512 GB 栈 256 K 项，约 1.8 MB/栈。

## 摘录数字（仅论文给出）

- decode 吞吐 vs HBM+SSD / HBM-only / H3：**1,205× / 2.2× / 6.2×**；能耗降 **408× / 1.1× / 6.8×**。
- 50 ms TPOT：相对 HBM-only **3.1×** 更少 GPU 封装（最高 8×）。
- 面积：HBF die **+3.1%**（phantom plane）；基座 **3.9 mm² @ 7 nm**。
- 有用 HBF 带宽相对 H3 **6.2×**（MoE 4.0–14.3×）；吃掉所取流量 **90–97%**。
- 仿真，不是硅。评测表 t_R=**2 μs**；正文现代 SLC 另写 **12 μs**，两处不要混。
