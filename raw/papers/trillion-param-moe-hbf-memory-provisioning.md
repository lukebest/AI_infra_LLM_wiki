---
type: Raw Source
title: "Trillion-Parameter MoE in a Box: Decoupling Memory Provisioning with High-Bandwidth Flash"
source_url: https://arxiv.org/abs/2609.15636
arxiv: '2609.15636'
ingested: 2026-09-16
sha256: 0389a920d0e1d0e6b5908763cbb8ae97e279ec08715c513131c75e98fe35e7a1
---

# Trillion-Parameter MoE in a Box: Decoupling Memory Provisioning with High-Bandwidth Flash

**Authors:** Pengfei Xia, Tuo Hao, Shengwei Li, Jinjing Chen, Shiru Wei, Wenjun Zou, Rui Zhang, Hui Zang
**Affiliation:** Huawei Technologies Co., Ltd.
**PDF:** [Trillion_Param_MoE_HBF_Memory_Provisioning_2026.pdf](Trillion_Param_MoE_HBF_Memory_Provisioning_2026.pdf)
**arXiv:** [2609.15636](https://arxiv.org/abs/2609.15636)（2026-09-14，cs.AR；Tue 9/15 列表）

## 问题

低并发万亿 MoE 一体机：量化权重 TB 级，HBM-only 难驻留；权重迁到 HBF 后，状态层 DRAM 与 HBF→host 暴露带宽成为两个正交供给膝点。

## 方法要点

- 工作负载：DSV4-Pro（1.6T/49B act）与 Kimi-K3（2.8T/104B act）；实测专家路由 + 多轮 agentic serving traces。
- 设计空间：HBF×DRAM 配置、B_ext 暴露、可选 near-data FP8 引擎。
- 两问：Q1 状态层带宽/容量比；Q2 HBF 内部带宽随容量增长时 host 暴露是否需同比。

## 摘录数字（仅论文给出）

- 256-GB 状态层地板：两模型达 **1.10×** 完成时间目标只需 **1.4–4.0 s⁻¹**（DSV4-Pro 4.0 / Kimi-K3 1.4），相对 HBM3e **33.3 s⁻¹** 约一个数量级。
- LPCAMM2×8：512 GB、**1.09 TB/s** 可达 DSV4-Pro 目标。
- HBF×6：每包暴露 **384 GB/s**（4×96 GB/s quanta），聚合 **2.30 TB/s**，相对全暴露参考 **6.14 TB/s** 低 **62.5%**，仍在约 10% 性能窗内。
- 量化权重：DSV4-Pro **865 GB**；Kimi-K3 **1560 GB**。
