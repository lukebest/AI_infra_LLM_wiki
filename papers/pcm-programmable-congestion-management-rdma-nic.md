---
type: Paper
title: "PCM: Programmable Congestion Management for Terabit RDMA NICs"
description: "ETH Zürich/Broadcom/Microsoft — 把拥塞控制/负载均衡写成可移植事件处理器（signal/trigger/control），厂商后端生成 shell；11 种算法，跑通 UET-htsim、UCCL、ConnectX-8 DPA、Microsoft 1P；CX-8 用 1/5 硬件线程在 800 Gbit/s 下每 3 个 4 KiB 包可做一次反应"
tags:
- rdma
- congestion-control
- transport
- programming-model
- networking
- nvidia
- microsoft
- broadcom
created: 2026-10-13
updated: 2026-10-13
timestamp: '2026-10-13T00:00:00Z'
paper_author: [Mikhail Khalilov, Timo Schneider, Tommaso Bonato, Siyuan Shen, Marcin Chrapek, Yehor Kozyr, Alberto Merino, Rip Sohan, Surendra Anubolu, Mohan Kalkunte, Ahmad Ghalayini, Abdul Kabbani, Torsten Hoefler]
year: 2026
arxiv: '2610.13130'
venue: arXiv preprint (cs.NI)
sources:
  - raw/papers/PCM_Programmable_Congestion_Management_RDMA_NIC_2026.pdf
  - raw/papers/pcm-programmable-congestion-management-rdma-nic.md
---

# PCM：一份拥塞控制源码，跑在仿真器、CPU 传输和多家 NIC 上

## 一句话结论
AI 集群的拥塞控制（CC）与负载均衡（LB）迭代速度远快于 RDMA ASIC 流片周期；可编程 RDMA 引擎（DOCA PCC、Falcon、P4 类流水线）又各自绑定厂商 API。PCM 定义一套可移植的事件驱动编程模型，策略写一次、在仿真里调好，再由各平台后端生成 shell 原样部署到 NIC，设计已反哺 Ultra Ethernet 的可移植 CC 接口工作。

## 动机（论文数字）
- 1.6 Tbit/s 下 4 KiB 包每 **20 ns** 到一个；1.5 GHz、IPC 0.5 的核每包只有约 **15 条指令**预算，一次函数调用就可能用完。
- CCP 这类主机侧可移植方案：Linux 内核 IPC 约 3 µs、DSL 解释 350 ns，比包间隔高出几个数量级。

## 方案
| 抽象 | 含义 |
|---|---|
| Signal | 流遥测/实时状态（ACK/NACK/RTO/ECN 计数、RTT、队列、路径 ID），各自选 SUM/MIN/MAX/LAST 累加器；AArch64/RISC-V 上每次累加 1–2 条指令 |
| Trigger | 对累加值做单指令阈值判断（RAW/DELTA/MAGNITUDE），既能逐包反应，也能抬高阈值改为粗粒度反应 |
| Control / 私有状态 | 窗口、速率、熵（路径）输出；handler 写入在 commit 前对数据通路不可见（snapshot 语义） |
| 平台 shell | 生成器把访问器编译成原生 load/store；独立流映射到 NIC 多核并行；同步/异步两种执行模式 |

- 实现 **11** 种 CC/LB 算法（Swift、MP-RDMA 类、EQDS 接收端 pull 等），多数不足 100 行 C。
- 四个平台集成代码量：UET-htsim 约 600 行、UCCL 约 1000 行、Microsoft 1P 约 2500 行、CX-8 DOCA PCC 约 2000 行。

## 效果（仅论文数字）
- ConnectX-8：PCM-Swift 在 800 Gbit/s 下处理能力相当于**每 3 个 4 KiB 包一次反应**，占用 DPA **256** 个硬件线程中的 **48** 个（约 1/5）。
- UCCL（CPU 软件 RDMA，16×100G 平面）：64 KiB chunk 级控制下与原生 Swift 同为 **1.56 Tbit/s** 有效吞吐。
- Microsoft 1P：shell 运行在 **192** 个硬件线程中的 **8** 个上。
- 定点数选择决定行为：CX-8 DPA 无浮点，原生 Q16.16 让 Swift 窗口失真（流完成 **8.76 ms** vs 参考 **2.17 ms**，**1030** 次重传）；64 bit Q32.32/Q42.22 最大 FCT 与参考相差 **0.3%** 以内。
- 反应延迟容忍度：调度延迟拉到 291/582 µs 时，CWND 公平性中位数降到 **0.818/0.782**。

## 与 wiki 的关系
- [Network Interface & System Design](/concepts/network-interface-and-system-design.md) — 流控 vs 拥塞控制、NI 上的策略执行
- [MRC](/entities/mrc.md) — 多路径 RDMA 传输与包喷洒 LB，PCM 的 LB handler 面向同类需求
- [Ofan](/papers/ofan-destination-aware-load-balancing-ai-training.md) — 交换机侧 LB；PCM 是端侧 NIC 的 CC/LB 可编程化
- [ByteExpress](/papers/byteexpress-rdma-deployment-inference-training.md) — 生产中在 RNIC 之上用软件发送窗口补 DCQCN，同题不同层
- [Broadcom Thor Ultra](/papers/hc2026-broadcom-thor-ultra.md) — 论文点名的 P4 类可编程 NIC 流水线

## 局限与开放问题
- CX-8 与 1P 未公开 LB、接收端 CC 钩子，这两类只在合成 trace 上测；测试床为两节点四 NIC。
- 源码可移植之外，算术精度、反馈粒度、调度延迟仍需逐平台做行为验证。

# Citations
- Khalilov et al., "PCM: Programmable Congestion Management for Terabit RDMA NICs", arXiv:2610.13130, 2026. [raw](/raw/papers/pcm-programmable-congestion-management-rdma-nic.md) · [PDF](/raw/papers/PCM_Programmable_Congestion_Management_RDMA_NIC_2026.pdf)
