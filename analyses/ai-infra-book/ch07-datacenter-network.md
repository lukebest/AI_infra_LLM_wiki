---
type: Summary
title: AI Infra Book Ch.7 Datacenter Network
description: 第7章数据中心网络—分层梯度、Clos 超售、多轨、UB 延迟分解、拥塞/incast、1024 卡超节点缩放
tags:
- book
- networking
- scale-out
- fabric
- rdma
- topology
- congestion-control
- datacenter
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.7 数据中心网络（优先章）

对接 [Clos](/concepts/clos-fat-tree-topology.md)、[Design Space](/concepts/interconnection-network-design-space.md)、[Collectives](/concepts/llm-distributed-training-collectives.md)、[UB](/entities/unifiedbus-ub.md)、[CASSINI](/entities/cassini.md)。

三个模型：**流量/资源**（割集 \(T=V/B\)）、**并发/吞吐**（带宽–时延积）、**依赖/关键路径**（从数据就绪画起）。

场景：两台 HGX H100，16 rank；NVLink 450 GB/s/dir；每卡 400 Gbit/s NIC = 50 GB/s/dir；小消息 \(\alpha\approx0.83\) μs（25 μs / 30 轮）。192 MiB 梯度、3 ms 通信预算（藏进 20 ms 步的尾巴）。

## 为何出超节点

混合精度 Adam 8B ≈ 16 B/param → 128 GB 状态；284B → ~4.5 TB。推理 V4-Pro ~800 GB、Kimi K3 ~1.4 TB 权重（0.5 B/param）——八卡 640 GB 装不下。MoE 未选中专家权重仍要存放。

## Clos / 超售 / 半分带宽

QM9700：k=64，400 Gbit/s。无阻塞两层：2048 端、96 交换机、半分 **51.2 TB/s**。三层：65536 端。3:1 超售（48/16）：两层 3072 端、80 交换机，半分 25.6 TB/s，每端跨半 **16.7 GB/s**。

1024 卡分区割集：

| 超售 | 叶 | 割集 | 每卡份额 |
|------|----|------|----------|
| 1:1 | 32 | 51.2 TB/s | 50 GB/s |
| 3:1 | 22 | 17.6 TB/s | 17.2 GB/s |

上联不堵的条件：跨叶比例 \(f\le 1/r\)。rail 对齐可让配对归约 \(f=0\)。

## 分层梯度 vs 环

连续环跨服务器 720 MiB/一张 NIC；分层：先机内 ReduceScatter，跨机只换分片，跨服务器 **384 MiB、八张 NIC**。发送总量可以相同，经过的出口不同——「字节相同则时间相同」是误区。多轨：编号相同的 NIC 接同一 leaf；错位配对把流量打上脊层。

强扩展：跨机 360 MiB @ 50 GB/s ≈ 7.5 ms 下界；计算 20/x ms。完全重叠时 x≈2.6 后加卡不再缩短步时间。

## 远程访问（UB 一手数字）

64 B 读、L=100 ns（OpenURMA 仿真对照）：

| 路径 | 推导 | 仿真 | 其中 PCIe |
|------|------|------|-----------|
| PCIe NIC 异步 | 2222 ns | 2236 | 5 次 / 1650 ns |
| UB 异步（片上控制器） | 746 ns | 757 | 0 |
| UB Load | 419 ns | 500 | 0 |

总时间 = 固定截距 + 2L。相对收益在超节点内最大。NIC 内处理器发起约 1572 ns（省控制面、省不了数据跨地址空间）。

并发：\(N\ge\lceil BT/m\rceil\)。50 GB/s、256 B、槽位 2 μs → **391** 在途；128 槽位只有 16.4 GB/s。RoCE RC 启动间隔 18.6 ns vs UB 6.2 ns。KV-Direct：读受 in-flight tag 限，写受报文率限。

快照 144 MiB：每次远程 ~3.02 ms vs 搬回 3.07 ms + 本地 0.046 ms；整份复用交点 r≈1.03；只碰 10% 则 r≈10.3。

## 拥塞 / 多路径 / 死锁

平均利用率 40% 仍可排队：两作业各 20 ms@50 GB/s 对齐高峰 → 积压 1 GB。512 KiB 缓冲只容忍 ~10.5 μs 重叠。[CASSINI](/entities/cassini.md) 错峰；一次性相位偏移会漂。

反馈：\(T_f\le Q_{\mathrm{free}}/(\lambda-B)\)。incast：N=8 超额 300 GB/s，允许反馈 3.50 μs；PFC 一跳 ~0.33 μs，DCQCN RTT 20 μs 灌 6–62 MB，1 MiB 放不下。只靠端到端不丢包：1 MiB 仅 N≤3。

ECMP：8 流/32 上联，整组速度仅无冲突的 **60.1%**；32/32 最差 **28.3%**。8 MiB 逐包喷洒八路：~29 μs vs 单路 169 μs，乱序缓存峰值 1.39 MB。UEC：熵喷洒 + 选择性重传。

死锁：请求/响应用独立通道与预留；UB 为完成通知、地址转换、恢复预留槽位。

## 关键路径与 1024 卡

就绪偏差：三人 0 ms、一人 2 ms + 0.4 ms 交换 = 2.4 ms；减半交换只到 2.2 ms，对齐就绪到 0.4 ms。MegaScale：带宽稳但 rank 越来越晚到。

例 7.6（192 MiB）：环串行 29.6 ms；分层 23.3 ms；17 ms 就绪重叠后分层 **22.0 ms**（通信被计算盖住）。改进顺序：减跨机字节 → 凑满在途 → 提早通信 → 再优化计算。

小消息：8 卡环 \(T=14\times5\mu s+1.75M/B\)，交点 M≈1.91 MiB。36 层×2 次 8 KiB：带宽×3 几乎不动，\(\alpha\) 5→2 μs 省 ~3.0 ms。

1024 卡、Qwen3-32B、TP8×DP128、41% MFU：

| 超节点 | 出口随卡增长 步时间/吞吐 | 出口封顶 400 GB/s |
|--------|--------------------------|-------------------|
| 8 | 0.939 s / 1.12M tok/s | 同左 |
| 64 | 0.690 s / 1.52M | 仍 0.939（选连续环） |
| 128 | 0.672 / 1.56M | 0.935 |
| 256 | 0.663 / 1.58M | 0.896 |

8→64 约 **+36%**；再往上 <2%。同域枚举 TP 仍是 **TP8 最好**。故障：Meta 1024 卡约 7.9 h/次；更大节点恢复更慢（128/256 卡 +3.4%/3.8%）。

# Citations

[1] [Ch.7](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/07-数据中心网络.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
