---
type: Raw Source
title: Huawei’s τ Chip Was Supposed to Melt?（LogicFolding / hybrid bonding 热叙事）
source_url: https://arxiv.org/abs/2609.04287
arxiv: '2609.04287'
ingested: 2026-09-08
sha256: a60b77a68cedb3503e7c6dbe69fa5ad61ce55d33e95b729b3a2de210a9dcafb7
---

# Huawei’s τ Chip Was Supposed to Melt?

**Author:** Tingbo He（Huawei Technologies）
**PDF:** [Huawei_Tau_Chip_LogicFolding_Thermal_2026.pdf](Huawei_Tau_Chip_LogicFolding_Thermal_2026.pdf)
**arXiv:** [2609.04287](https://arxiv.org/abs/2609.04287)（2026-09-02，cs.AR）

## 问题

对 3D / LogicFolding 的常见反对是「叠层必热熔」。作者用 Kirin 硅测反驳：动态功耗主项是互连通勤（线电容），不是门开关；折叠缩短线长则功率密度可降。

## 方法要点 / 工艺叙事

- LogicFolding：在相近面积内用 **W2W hybrid bonding** 做跨层短跳，缩短关键路径与时钟网。
- Kirin 2026：40 nm 工具链上 **1.5 µm** HB pitch，约 **5000 万** 垂直互连（信号约 10–15%）；晶体管密度约 **155→238 MTr/mm²（+55%）**。
- Kirin 2027 硅：约 **1 µm**、**>1 亿** 垂直互连；路线图指向匹配 top-metal **720 nm**（>2 亿）。
- 折叠路径线长典型降 **20%**，部分关键路径最高 **70%**；一例时钟布线 −28%，buffer **43600→19000**。

## 摘录数字（仅论文给出；厂商自测）

- iso-performance vs 平面前代（Kirin9030 Pro）：NPU 功耗 **−66%**，GPU **−58%**，CPU 性能核 **−41%**。
- 折叠 NPU 也可「跑满」：相对前代吞吐 **+141%**（此时功率密度可升——作者强调是策略选择）。
- 折叠 CPU 保守路径：当年性能核频率回到 **3.1 GHz**；展望 3–5 年挑战 **5 GHz+**。
- 文中类比：大型 AI 集群「>80% 能量花在搬数而非算」——与片上互连主导功耗同一逻辑。
