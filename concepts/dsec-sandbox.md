---
type: Concept
title: DSec Sandbox Platform
description: DeepSeek Elastic Compute 沙箱平台，4 种执行基板，数十万并发
tags:
- sandbox
- training-system
- inference-system
- agentic-ai
timestamp: '2026-04-28T00:00:00Z'
created: 2026-04-28
updated: 2026-09-22
sources:
- DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
- raw/papers/DeepSeek_DSec_Agentic_Sandbox_Infrastructure_2026.pdf
- raw/papers/dsec-agentic-sandbox-infrastructure.md
---

# DSec (DeepSeek Elastic Compute) Sandbox

DeepSeek-V4 的生产级沙箱平台，用于后训练和评估中的 agentic 任务执行。

## Architecture
三个 Rust 组件：
- **Apiserver**: API 网关
- **Edge**: 每主机 agent
- **Watcher**: 集群监控

基于 3FS 分布式文件系统，单集群管理数十万并发沙箱实例。

## Four Execution Substrates

| 基板 | 隔离级别 | 用途 | 技术 |
|------|---------|------|------|
| Function Call | 无 | 无状态调用 | 预热容器池，零冷启动 |
| Container | 容器级 | 一般任务 | Docker + EROFS 按需加载 |
| microVM | VM 级 | 安全敏感/高密度 | Firecracker |
| fullVM | 完整 VM | 任意 OS | QEMU |

统一 Python SDK (libdsec)，切换只需改参数。

## Fast Image Loading
- Container: 3FS-backed readonly EROFS layers → overlay lowerdirs
- microVM: overlaybd 格式，只读层在 3FS，写层在本地 COW
- 支持链式 snapshot，毫秒级恢复

## Density Optimizations
- 缓解虚拟化环境中的重复 page-cache footprints + 内存回收
- 减少容器运行时的 spinlock 竞争，降低 CPU 开销

## Trajectory Logging
- 全局有序的轨迹日志
- 支持：client fast-forwarding（抢占后快速恢复）、provenance 追溯、deterministic replay

## Relations
- Used in: [Deepseek V4](#DeepSeek-V4)
- Related: [Tilelang](#TileLang)


## 2026-09 paper update (arXiv:2609.22978)

论文把既有生产平台表述成独立执行平面：统一 SDK 下的 FnCall / container / Firecracker microVM / QEMU fullVM，3FS + EROFS/OverlayBD 按需镜像，以及与 RL trainer 解耦的 pause/resume。量化边界来自原文：约 160 节点 scale unit 每日约 **300 万** sandbox；峰值并发 **>380K**、创建 **>5,000/s**；稳定点每节点至少 **3,200 containers** 或 **800 microVMs**；8,192-container 批量启动中 lazy EROFS 相对 eager pull **1.71×** 更短并减少磁盘写入 **57%**。

与 [Ask the Tool](../papers/ask-tool-progress-agent-kv-serving.md) 对照：DSec 保存工具执行环境状态，Ask the Tool 用 waiting-time 预测管理 KV。与 [PipeSwift](../papers/pipeswift-pipeline-parallel-agentic-serving.md) 对照：PipeSwift 优化 agentic serving 的模型侧流水，DSec 覆盖 RL/eval 的沙箱执行面。完整论文页见 [DeepSeek DSec](../papers/dsec-agentic-sandbox-infrastructure.md)。

# Citations

1. Huang, J., Tang, H., Chen, J., et al. “DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale.” arXiv:2609.22978, 2026. [paper](../papers/dsec-agentic-sandbox-infrastructure.md)
2. [本地原文 PDF](../raw/papers/DeepSeek_DSec_Agentic_Sandbox_Infrastructure_2026.pdf)；[原始来源记录](../raw/papers/dsec-agentic-sandbox-infrastructure.md)
3. [旧来源指针 DeepSeek_V4 PDF](DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf)
