---
type: Paper
title: "DeepSeek DSec: 大规模 Agentic 训练沙箱基础设施"
description: "用统一 sandbox API、3FS/EROFS 按需镜像和 CPU/内存超售支撑日均 300 万沙箱、38 万并发与每秒 5,000 次创建。"
tags:
- architecture
- agentic-ai
- training-system
- distributed
- storage
- sandbox
- infrastructure
- virtualization
created: 2026-09-22
updated: 2026-09-22
timestamp: '2026-09-22T00:00:00Z'
paper_author: [Jialiang Huang, Hongxuan Tang, Jingchang Chen, "et al."]
year: 2026
arxiv: '2609.22978'
sources:
  - raw/papers/DeepSeek_DSec_Agentic_Sandbox_Infrastructure_2026.pdf
  - raw/papers/dsec-agentic-sandbox-infrastructure.md
---

# DeepSeek DSec：大规模 Agentic 训练沙箱基础设施

## 一句话结论

DSec 把 agentic RL/eval 的执行环境做成独立、可暂停恢复的弹性层：四级隔离 backend 共用 API，3FS + EROFS/OverlayBD 按需取镜像，再用 CPU/内存 QoS 做高密度超售。约 160 节点的 scale unit 每日服务约 **300 万**沙箱，峰值 **>380K 并发 / >5,000 次创建每秒**，把“工具执行环境”从 trainer 的附属进程提升成一类系统基础设施。

## 动机：Agent rollout 不是无状态 RPC

Agentic workload 的 sandbox 可能运行秒级函数，也可能是数小时 full VM；需要文件系统状态、pause/resume 和不同安全隔离。RL rollout 还呈现脉冲式 fan-out，单作业可一次请求 **32K** 实例。若 agent loop 绑在 GPU trainer 上，trainer 被抢占或扩缩时，外部环境状态也会丢失；若每次完整拉镜像，网络与磁盘放大会拖垮冷启动。

## 方案

### 1. 同一 API 下的四级隔离

DSec 暴露统一 Python SDK，将 workload 映射为 FnCall、container、Firecracker microVM 或 QEMU full VM。调度器按安全、兼容性与性能选择 backend；调用端无需为隔离技术重写 agent loop。

### 2. 按需镜像与可组合环境

容器镜像层存于 3FS，转换为 EROFS/OverlayBD 后按块远程读取，而非先完整 pull。实验依赖、workspace 与 base image 可组成层并缓存复用。pause/resume 保留环境和文件系统状态，使 GPU trainer 可独立抢占、重调度。

### 3. 面向高密度的超售与 QoS

DSec 利用 identical-page merging、匿名页回收、swap 与 memcg 做内存超售；CPU 侧按 quota/share 限制 noisy neighbor。调度器以节点画像与资源压力做 placement，在高密度下仍维持稳定点。

## 量化结果

- **生产规模**：单 scale unit 约 **160 节点、30K CPU cores、250 TiB RAM**；每日约 **300 万** sandbox，峰值并发 **>380K**、峰值创建 **>5,000/s**。
- **节点密度**：压力测试的生产稳定点为每节点至少 **3,200 containers** 或 **800 microVMs**。
- **按需镜像**：8,192 containers 批量启动/执行中，lazy EROFS 约 35 分钟，eager pull 超 60 分钟（后者 **1.71×** 慢），磁盘写入减少 **57%**。
- **可组合环境**：相同规模下 composable EROFS 约 45 分钟，eager EROFS+OverlayFS 约 79 分钟（**1.76×** 慢）。
- **内存**：3,200-container 测试中，页共享/回收把峰值约 45.2 GiB 压到 17.3 GiB，降幅约 **61.7%**（由论文图表数字计算）。

## 局限与解读

- 论文来自自有生产系统，比较多为内部 backend/配置；没有开源调度器或与外部同规模系统的公平对照。
- GPU trainer 与 agent loop 解耦是架构贡献，但论文没有给出训练收敛或 GPU 利用率提升的端到端量化。
- 隔离 backend 的安全边界主要为工程描述，不应仅凭性能数据推导安全性。

DSec 直接扩充 [DSec Sandbox Platform](../concepts/dsec-sandbox.md)，并与 [Ask the Tool](ask-tool-progress-agent-kv-serving.md) 从不同层面处理 agent 的“等待期”：前者保存工具执行环境与状态，后者预测等待时间以调度 KV。它还补足 [PipeSwift](pipeswift-pipeline-parallel-agentic-serving.md) 关注的 agentic serving 之外，RL/eval execution plane 的资源与存储问题。

# Citations

1. Huang, J., Tang, H., Chen, J., et al. “DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale.” arXiv:2609.22978, 2026. [arXiv](https://arxiv.org/abs/2609.22978)
2. [本地原文 PDF](../raw/papers/DeepSeek_DSec_Agentic_Sandbox_Infrastructure_2026.pdf)；[原始来源记录](../raw/papers/dsec-agentic-sandbox-infrastructure.md)
