---
title: "Resilient AI Supercomputer Networking using MRC and SRv6"
created: 2026-05-13
updated: 2026-05-13
type: paper
tags: [scale-up, routing, transport, switch, protocol, fabric, load-balancing, congestion-control, nvidia, amd]
sources: [raw/articles/resilient-ai-supercomputer-networking-mrc-srv6.md]
---

# Resilient AI Supercomputer Networking using MRC and SRv6

**作者**: OpenAI, Microsoft, AMD, NVIDIA, Broadcom 联合团队 (Mark Handley, Christoph Paasch, Jitendra Padhye 等)

**核心贡献**: 三管齐下解决 100K+ GPU 同步预训练的网络可靠性和性能问题：

1. **[[mrc]]** — 多路径 RDMA 传输，包 spraying + 自适应负载均衡 + 选择性重传
2. **[[multi-plane-clos-topology]]** — 2 层 multi-plane Clos 拓扑，高冗余低成本
3. **[[srv6-source-routing]]** — 静态源路由，禁用动态路由，简化控制面

**生产验证**: 已在 OpenAI/Microsoft 最大训练集群用于训练 ChatGPT 和 Codex 前沿模型。

**关键指标**:
- 延迟: T0-local 5.09µs, cross-T1 6.54µs
- 带宽: ~770 Gb/s (96% peak)
- MRC 1 QP > RoCE 16 QPs (all-reduce)
- T0-T1 link flap 对 job 几乎无影响
- T1 switch reboot: job 不中断

## 关系

- [[mrc]] 协议实体页
- [[multi-plane-clos-topology]] 概念页
- [[srv6-source-routing]] 概念页
- 与 [[switching-networks]] 的 CLOS 理论相关
- 与 [[switching-principles]] 中分组交换/电路交换对比相关
