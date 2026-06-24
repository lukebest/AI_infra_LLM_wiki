---
type: Concept
title: DSec Sandbox Platform
description: DeepSeek Elastic Compute 沙箱平台，4 种执行基板，数十万并发
tags:
- sandbox
- training-system
- inference-system
timestamp: '2026-04-28T00:00:00Z'
created: 2026-04-28
sources:
- DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
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

# Citations

[1] [DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf](DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf)
