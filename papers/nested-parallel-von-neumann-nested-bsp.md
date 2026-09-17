---
type: Paper
title: "Nested Parallel von Neumann Architecture and Nested BSP"
description: Huawei 廖恒 — Nested BSP + Nested Parallel von Neumann；Unified Bus 端到端 peer；与 τ Scaling law 配对；SuperNode 理论根基
tags:
- huawei
- interconnect
- scale-up
- fabric
- architecture
- distributed
- collective
- protocol
- supernode
- datacenter
timestamp: '2026-09-17T00:00:00Z'
created: 2026-09-17
updated: 2026-09-17
sources:
- raw/papers/Nested_Parallel_von_Neumann_Nested_BSP_2026.pdf
- raw/papers/nested-parallel-von-neumann-nested-bsp.md
---

# Nested Parallel von Neumann Architecture and Nested BSP

**Author:** Heng Liao
**Affiliation:** Huawei Technologies Co., Ltd.
**arXiv:** [2609.16787](https://arxiv.org/abs/2609.16787)（2026-09-15，cs.DC/cs.AR；Wed 9/16 列表）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.16787)

把「百万处理器仍是一台计算机」写成两套嵌套玩偶：**Nested BSP**（软件）与 **Nested Parallel von Neumann Architecture**（硬件），由端到端 **[UnifiedBus (UB)](/entities/unifiedbus-ub.md)** 串起；与 [Huawei τ / LogicFolding](/papers/huawei-tau-chip-logicfolding-thermal.md) 的 **τ Scaling law** 配对。

## 动机

- 规模 AI 不再是「更强单处理器」竞赛，而是如何让一支处理器军队仍服从一台机器的命令结构。
- 批判两点外推：(1) 把多台计算机联网就得到更大一台；(2) 几乎处处假设 master/slave（host>device、CPU>加速器）。

## 方案

1. **Nested BSP**：经典 BSP 四步（并行工作 / barrier / exchange / aggregate）递归嵌套到每一层；硬约束——**每层节点皆 peer**。
2. **硬件嵌套**：CORE → chiplet → package → board → rack → SuperNode → data hall → autonomous zone。
3. **Unified Bus**：memory-semantic、全路径同一协议；**physically sparse, logically tight**；近铜远光、协议不变。
4. 文称 **Huawei SuperNode** 以 Nested BSP 为理论根基；τ 在系统层「折叠时间」，本架构「折叠并行层次」。

## 效果

论述/架构论文，**无**独立吞吐或硅测表。定量线索指向既有 τ 芯片（密度/功耗）与 UB 规范叙述；勿把本文当成基准数据源。

## 与 wiki 的关系

- [UnifiedBus (UB)](/entities/unifiedbus-ub.md) — 文中 interconnect 本体
- [AI Infra Supernode](/concepts/ai-infra-supernode.md) — SuperNode / 自治区层次
- [Huawei τ Chip](/papers/huawei-tau-chip-logicfolding-thermal.md) — τ Scaling law 配对
- [Constraint-Driven AI Infra Design](/concepts/constraint-driven-ai-infra-design.md) — 「一台计算机」约束叙事
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 协议/拓扑设计空间对照
- [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 另一条「域内一台机」产品路径

## 开放问题

1. Nested BSP 各层 barrier/exchange 的可测延迟界与失败模型。
2. peer equality 与现有 host-driven 软件栈的迁移成本。
3. 与 NVLink/UALink 域的对照应落在哪些可复现指标上。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.16787) — Liao, arXiv:2609.16787
[2] [raw/papers/nested-parallel-von-neumann-nested-bsp.md](raw/papers/nested-parallel-von-neumann-nested-bsp.md) — ingest stub
