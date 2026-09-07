---
type: Raw Source
title: CREDIT — Cost-guided Reduction-reuse with Efficient DSMEM Inter-CTA Tiling
source_url: https://arxiv.org/abs/2609.01864
arxiv: '2609.01864'
ingested: 2026-09-07
sha256: 7a0853d24d571fff05ee64f5fec967acd878dd6f2c7b9163a2f678611dcb4a78
---

# CREDIT: Cost-guided Reduction-reuse with Efficient DSMEM Inter-CTA Tiling

**Authors:** Zhengxiong Li, Tsung-Wei Huang, Umit Ogras
**Affiliations:** University of Wisconsin–Madison
**PDF:** [CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf](CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf)
**arXiv:** [2609.01864](https://arxiv.org/abs/2609.01864)（2026-09-02，cs.DC）

## 问题

Hopper+ 的 thread block cluster + DSMEM 允许 CTA 之间直接读写对方 SMEM，但远程访问、cluster barrier、占位代价使「何时用 DSMEM」不直观。

## 方法要点

- 刻画 DSMEM：远程 load 相对本地约 **6.4×** 延迟、吞吐约 **4.4–5.4×** 更低（RTX 5090 / H100）。
- 目标模式：**reduction-reuse**（宽向量归约出标量统计量后再逐元素复用），用 owner-local 切片 + 紧凑 partial 的 replicated push/all-gather 换掉第二次 HBM 重读。
- 成本模型：用非 DSMEM baseline 实测带宽估 T_save，再减 T_ctrl / T_replay / T_DSM；跨度预测准确率 **91.7%**（55/60）。
- 工作负载：LayerNorm、weighted-variance backward、Pearson backward、softmax-logits backward、LARS、row-wise int8 quant。

## 摘录数字（仅论文给出）

- 几何均值相对最快 baseline（N=64K）：RTX 5090 **1.466×**，H100 **1.318×**。
- N=4K 时常输给单 CTA；交叉点设备相关（5090 更早、H100 barrier 851 vs 404 cycle）。
- Nsight：DRAM 流量降 **33–60%**。
- 源码：https://github.com/zhengxiongli08/CREDIT
