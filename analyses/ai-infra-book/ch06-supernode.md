---
type: Summary
title: AI Infra Book Ch.6 Supernode
description: 第6章超节点—六种并行、环/树集体、NVLink/TPU/UB、Engram 放置、实例数 vs 协作组
tags:
- book
- supernode
- scale-up
- parallelism
- collective
- fabric
- moe
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.6 超节点（优先章）

概念页：[AI Infra Supernode](/concepts/ai-infra-supernode.md)。集体对照：[LLM Collectives](/concepts/llm-distributed-training-collectives.md)。Fabric：[NVLink](/concepts/nvlink-nvswitch-scale-up-fabric.md)、[UB](/entities/unifiedbus-ub.md)。

硬件贯穿：HGX H100，NVLink **450 GB/s/dir**，NIC **50 GB/s/dir**。模型：Qwen3-235B-A22B（容量/EP）、Qwen3-32B（长 KV 逼 TP）。

## 容量与 Roofline

逐卡 \(W_i+K_i+A_i+U_i\le C_i\)。235B BF16 权重 470.2 GB；每 token KV 188 KiB；8K KV 1.58 GB。单卡约 473.9 GB；TP8 每卡约 **61.50 GB**（含每卡一份 norm/router）。一层 8 专家权重读 288 MiB ≈ 90.1 μs @ 3350 GB/s，矩阵 0.31 μs → batch-1 MFU 上限约 **0.3%**。

\[
T_{\mathrm{op}}=\max(F/P,\,V/B_{\mathrm{HBM}}).
\]

Prefill 8K 时同一层专家改为 compute-bound（读 1.44 ms vs 算 2.50 ms）。隐藏向量 1 token = 8 KiB，8K = 64 MiB——同次数交换，字节差 8192×。

## 六种并行（切哪个维）

| 方式 | 切 | 必须交换 |
|------|----|----------|
| DP | 样本 \(B\) | 推理无；训练梯度 |
| TP | 特征 \(H\) | 部分和 AllReduce / 分片收集 |
| SP | 逐 token 算子的 \(S\) | 进 GEMM 前收集 |
| CP | 注意力的 \(S\) | 远端 K/V 或统计量 |
| PP | 层 \(L\) | 相邻阶段激活（训练再回传梯度） |
| EP | 专家 \(E\) | dispatch + combine（不是 AllReduce） |

切特征才必须**相加**部分和。组合用设备坐标（如 TP2×EP4），不要先锁缩写。

## 集体：环 vs 树 vs 争用

环形 AllReduce：\(T_{\mathrm{ring}}=2(n-1)\alpha+2(n-1)M/(nB)\)。\(\alpha\) 取 MSCCL++ H100 NVLink **0.822 μs**。Qwen3-32B、10 KiB、128 次归约：

| TP | 本地访存 | 128×AR | 单步 |
|----|----------|--------|------|
| 2 | 14.68 ms | 0.21 ms | 14.89 ms |
| 4 | 7.34 ms | 0.64 ms | 7.97 ms |
| 8 | 3.67 ms | 1.48 ms | 5.15 ms |

八卡一次归约 11.55 μs 里 **11.51 μs 是启动**；带宽翻倍只省 ~2.5 μs，\(\alpha\) 减半省 ~0.74 ms。树：\(T_{\mathrm{tree}}=2\log_2 n(\alpha+M/B)\)；八卡交点约 **680 KiB**（decode 10 KiB 偏树，prefill 80 MiB 偏环）。

NCCL：`algbw=M/T`，AllReduce `busbw=2(n-1)M/(nT)`。重叠必须测同时运行，不能把独占时间相减。发起位置：CPU proxy（控制面 3×PCIe）/ SM（2×）/ NIC 处理器（0×）。

**TP16 跨两台 HGX**：本地 2.48 ms + 128×32.74 μs ≈ **6.67 ms**，慢于机内 TP8 的 5.15 ms。

## 拓扑 / 功率 / 三家系统

NVSwitch Gen3：64 端口 × 25 GB/s/dir。32/32 上联 800 GB/s；48/16 仅 400 GB/s。DGX H100 NVLink 出节点 **2:1 收敛**。64 卡：环面 vs 交换——维序归约打平；All-to-All 交换约 3×（512 卡 6×）。功率式 (6-11)：120 kW → 88 卡；风冷 ~40 kW/柜。

- NVIDIA：八卡机箱 → NVL72；更大域的价值常是**更多实例或装下超八卡模型**，不是把 32B 切到 TP16。
- TPU：\(k^3\) 环面，割集 \(2k^2\)；k=4→8 芯片×8、割集×4，每芯片跨半带宽减半。OCS 重连：8 MiB AR 省 ~196 μs/次，1 ms 切换约 6 次回本，100 ms 要 511 次。
- **UB**（6.5.5）：事务层 Jetty vs 传输通道。256 KiB 片上缓存、A=8：逐对 QP \(S_{\mathrm{pair}}=512A^2(H-1)+32A\) 只能 ~8 主机；UB \(52A+56(H-1)\) 到四千主机。CloudMatrix384 的 192 主机：QP ~6 MiB vs UB ~11 KiB。N=M=1024 建连：QP 并行 ~17 s vs UB ~16 ms。控制器上片上总线：64 B 读 0.42 μs vs PCIe NIC 2.2 μs（Ch.7 表）。NVLink 目录一致性把规模钉在几十对端（NVL72）。昇腾 950 UB 双向合计 2016 GB/s（单向 1008）。

内存池：全局有空、局部不够 → 借远端；窗口带宽 \(uq/L\)，重复读才值得搬回（Ch.7 快照交点）。

## 实例数 vs 协作组（6.7）

四会话 128K、八步、八卡：

| 部署 | 八步/会话 | 全部完成 |
|------|-----------|----------|
| 4×TP2 | 119.1 ms | 119.1 ms |
| 2×TP4 | 63.8 ms | 127.6 ms |
| 1×TP8 | 41.2 ms | 164.7 ms |

130 ms、≥75% 按时 → **四个 TP2**（0.238 GPU·s/按时会话）。单会话 50 ms → TP8。故障注入后更大实例 blast radius 更大。

切分五步：记模型/负载/硬件 → 按瓶颈列方案 → 写数据归属与时间线 → 同一目标排序 → 测量改排名。

## Engram / ROM / SRAM（6.7.4）

V4.1 Flash 200K：8→64 卡每卡吞吐 7.4×；单用户仍 362 tok/s。Engram 两表 203.1 GB、每 token 查 12.7 KB。H100 上 69 μs 窗口内 PCIe/RDMA 预取 1.05 μs 或 NVLink 0.83 μs 都藏得住 → DeepSeek 放**主机内存**。ROM 晶圆第一块只有 6.1 μs，主机往返占 1/6，表应靠近可写存储。权重进 ROM 后通信占单用户时间 65%（4070 tok/s）。KV 进 SRAM：单会话速度不变，总吞吐掉三个数量级。

# Citations

[1] [Ch.6](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/06-超节点.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
