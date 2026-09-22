---
type: Raw Source
title: "DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale"
description: "DeepSeek DSec 原始论文来源：面向 agentic training/evaluation 的大规模有状态沙箱基础设施。"
timestamp: '2026-09-22T00:00:00Z'
source_url: https://arxiv.org/abs/2609.22978
arxiv: '2609.22978'
ingested: 2026-09-22
sha256: 649edc87e70b8e57f9515360b15ed5576c6c8afb3c46a3763e83c22a85a660e2
---

# DeepSeek Elastic Compute (DSec)

**Authors:** Jialiang Huang, Hongxuan Tang, Jingchang Chen, et al.  
**Affiliation:** DeepSeek-AI; Tsinghua University  
**PDF:** [DeepSeek_DSec_Agentic_Sandbox_Infrastructure_2026.pdf](DeepSeek_DSec_Agentic_Sandbox_Infrastructure_2026.pdf)  
**arXiv:** [2609.22978](https://arxiv.org/abs/2609.22978)（2026-09-19，cs.DC）

## 问题

Agentic RL/eval 的执行环境既突发、长寿命、带状态，又需要不同隔离强度；单个作业可一次请求 **32K** 沙箱，完整镜像预拉会把启动与节点 I/O 打爆。

## 方法要点

- 统一 SDK 暴露 FnCall、container、Firecracker microVM、QEMU full VM 四种 backend。
- 用 3FS + EROFS/OverlayBD 做按需镜像、可组合环境层；用内存共享/回收与 CPU QoS 支撑高密度超售。
- 把 agent loop 搬离可抢占 GPU trainer，保持 rollout/sandbox 状态并支持 pause/resume。

## 摘录数字（仅论文给出）

- 单 scale unit 约 **160 节点**，每日约 **300 万** sandbox；峰值并发 **>380K**、创建 **>5,000/s**。
- 生产稳定点：每节点至少 **3,200 containers** 或 **800 microVMs**。
- 8,192-container 测试：按需 EROFS 约 35 分钟完成，eager pull 超 60 分钟（**1.71×** 慢），磁盘写入 **−57%**。

**Working page:** [DSec paper](/papers/dsec-agentic-sandbox-infrastructure.md)  
**Related:** [DSec Sandbox Platform](/concepts/dsec-sandbox.md)
