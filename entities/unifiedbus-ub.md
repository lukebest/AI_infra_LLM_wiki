---
type: Entity
title: UnifiedBus (UB)
description: Huawei UnifiedBus 高性能互连协议，SuperPoD-scale AI/HPC，统一协议栈，全资源池化
tags:
- interconnect
- scale-up
- fabric
- huawei
- protocol
- switch
timestamp: '2026-05-11T00:00:00Z'
created: 2026-05-09
updated: 2026-09-17
sources:
- raw/articles/bojieli-ai-infra-book.md
- raw/papers/Nested_Parallel_von_Neumann_Nested_BSP_2026.pdf
- raw/articles/UB-overview.md
- raw/articles/UB-FUN.md
- raw/articles/UB-MEM.md
- raw/articles/UB-RSC.md
- raw/articles/UB-TA.md
- raw/articles/UB-TP-ch6.md
- raw/articles/UB-NETWORK-ch5.md
- raw/articles/UB-DL-ch4.md
- raw/articles/UB-PHY-ch3.md
---

# UnifiedBus (UB)

华为 (Huawei) 开发的高性能、低延迟互连协议，专为 SuperPoD 级 AI 和 HPC 部署设计。单一协议统一处理内存访问、消息传递、远程过程调用和资源管理。Revision 2.0 发布于 2025-12-31。

## 核心定位

UB 是一种 **SuperPoD-scale 互连技术**，目标是从单服务器无缝扩展到数万处理单元，同时保持 P2P 语义和动态资源池化。与 [Nvidia Vera Rubin Nvl72](/entities/nvidia-vera-rubin-nvl72.md) 的 NVLink 生态不同，UB 强调统一协议（无需协议转换）和全资源池化。

## 系统组成

| 组件 | 说明 |
|------|------|
| **UBPU** | UB 处理单元，支持 UB 协议栈并实现特定功能 |
| **UB Controller** | UBPU 内实现协议栈的组件，提供软硬件接口 |
| **UMMU** | UB 内存管理单元，负责地址映射和权限验证 |
| **UB Switch** | UBPU 内可选组件，在 UB 端口间转发数据包 |
| **UB link** | 全双工点对点连接，TX/RX lane 数可不对称 (1/2/4/8) |
| **UB domain** | 通过 UB link 互连的 UBPU 集合 |
| **UB Fabric** | 一个 UB domain 内所有 UB Switch 和 UB link |
| **UBoE** | UB over Ethernet，在标准 Ethernet/IP 网络上传输 UB 事务包，实现跨 domain 互连 |

## 关键特性

- **统一协议**：单一协议处理 memory、messaging、RPC、资源管理，消除协议转换开销
- **P2P 协调**：每个 UBPU 都是架构对等体，无需 host/proxy 即可直接发起事务
- **全资源池化**：计算/内存/互连资源按 Entity 粒度分配，支持弹性伸缩和异构编排
- **全栈协调**：每层协议提供多种可选模式，按 workload 精确调优
- **灵活拓扑**：集成交换能力，支持 nD-FullMesh、Clos、torus 等拓扑及混合拓扑
- **高可用**：物理层降速/降道、数据链路层重传、网络层多路径、传输层端到端重传 + RAS

## 协议栈（6 层）

```
┌─────────────────────┐
│   Function Layer    │  Load/Store 同步访问 + URMA 异步访问
├─────────────────────┤
│  Transaction Layer  │  Memory/Messaging/Maintenance/Management 事务
├─────────────────────┤
│   Transport Layer   │  RTP / CTP / UTP + TP Bypass
├─────────────────────┤
│   Network Layer     │  IP + CNA 寻址，多路径，per-packet/per-flow LB
├─────────────────────┤
│  Data Link Layer    │  CRC + 重传 + credit-based 流控 + Virtual Lane
├─────────────────────┤
│   Physical Layer    │  可定制速率，动态 FEC 切换，故障降速
└─────────────────────┘
```

横向组件：**UBFM**（Fabric Manager，集中管理 domain 资源）、**UMMU**（内存地址映射+权限验证）、**Security**（设备认证/隔离/CIP/TEE 扩展）。

## 编程模型

1. **Load/Store 同步访问**：UB Controller 与 NoC 协作，将 load/store 指令转换为事务操作
2. **URMA 异步访问**：通过 Jetty API 建立通信对，提交事务操作，查询响应（支持 many-to-many）
3. **URPC**：基于内存对象的远程过程调用，支持任意 UBPU 间直接 P2P 调用（详见 [Ub Urpc](/concepts/ub-urpc.md)）

## 事务服务模式

| 模式 | 可靠性 | 排序方 |
|------|--------|--------|
| ROI | 可靠 | Initiator（发送端排序） |
| ROT | 可靠 | Target（接收端排序） |
| ROL | 可靠 | Lower layer（下层排序） |
| UNO | 不可靠 | 无排序 |

## 内存管理

采用 **Home-User 访问模型**：Home 是内存拥有者，User 是访问者。UBMD (UB Memory Descriptor) 包含 EID + TokenID + UB Address，UMMU 将 UB Address 翻译为 Home 的物理地址。详见 [Ub Memory Management](/concepts/ub-memory-management.md)。

## 与其他互连技术对比

UB 的定位可类比 [Switching Principles](/concepts/switching-principles.md) 和 [Switching Networks](/concepts/switching-networks.md) 中描述的交换原理，但在 SuperPoD 规模上提供统一的 memory+messaging+RPC 语义。与 NVIDIA NVLink/NVSwitch 生态相比：
- UB 强调 **统一协议栈**（NVLink 分为 NVLink + NVSwitch + NVLink-C2C 多种协议）
- UB 提供 **内置 RPC**（URPC），NVLink 不直接支持
- UB 支持 **跨 domain Ethernet 互连**（UBoE）

## 安全模型

- 设备身份认证 (SPDM)
- 资源分区隔离 (UB Partition + Network Partition)
- 访问控制 (Token + 权限验证)
- 传输保密性和完整性保护 (CIP, AES-GCM)
- 跨设备 TEE 扩展 (EE_bits)

## Multi-Entity Coordination

单次函数调用 → UB 框架分解为多个底层事务 → 跨 UBPU 协调执行：
- **Fusion**：合并多个事务为统一操作（broadcast、multicast、task balancing、compound data + sync）
- **Collective Communication**：经典并行计算集合通信，硬件拓扑定制，最小化数据移动
- **Global Maintenance**：跨多 UBPU 的系统级维护（内存一致性、UMMU 同步更新、通信状态管理）

## 来源

- UnifiedBus™ (UB) Base Specification Revision 2.0, 2025-12-31, Huawei Technologies
- <https://www.unifiedbus.com>


## Nested Parallel 理论叙事（2026-09）

[Nested Parallel von Neumann / Nested BSP](/papers/nested-parallel-von-neumann-nested-bsp.md)（廖恒，arXiv:2609.16787）把 UB 写成 **Nested Parallel von Neumann Architecture** 的端到端 memory-semantic 总线：peer equality、physically sparse / logically tight，与 Nested BSP 软件嵌套及 [τ Scaling law](/papers/huawei-tau-chip-logicfolding-thermal.md) 配对；文称 SuperNode 以 Nested BSP 为理论根基。论述文，无新吞吐表——规范与书中数字仍以本页上文为准。

## 书 Ch.6.5.5 / 7.3：规模与延迟预算（2026-09）

规范页之上，[李博杰书](/entities/bojieli-ai-infra-book.md)用 OpenURMA 仿真给出可对照数字（作者参与 UB）：

- **状态**：256 KiB 片上缓存、每主机 8 端点。RoCE 式逐对 QP \(512A^2(H-1)\) 约 8 主机溢出；Jetty+通道 \(52A+56(H-1)\) 到四千主机。CloudMatrix384 的 192 主机：QP ~6 MiB vs UB ~11 KiB。目录式缓存一致（NVLink 类）两主机已 ~8 MiB，1024 主机 ~136 MiB——故 UB **不**做跨主机 cache coherence。
- **建连**：N=M=1024，QP 并行约 17 s，UB 约 16 ms。
- **64 B 读**（L=100 ns）：PCIe NIC 2.22 μs（五次 PCIe 1.65 μs）；UB 异步 0.75 μs；UB Load 0.42 μs（仿真 0.50 μs）。总时间 = 截距 + 2L。
- CloudMatrix384：384×910C + 192 CPU，域内 UB、域外 RDMA。昇腾 950 UB 双向合计 **2016 GB/s**（72×112 Gbit/s，单向 1008）；UBoE 与 UB Link 分同一组 SerDes。

章节：[Ch.6](/analyses/ai-infra-book/ch06-supernode.md)、[Ch.7](/analyses/ai-infra-book/ch07-datacenter-network.md)。

# Citations

[1] [raw/articles/UB-overview.md](raw/articles/UB-overview.md)
[2] [raw/articles/UB-FUN.md](raw/articles/UB-FUN.md)
[3] [raw/articles/UB-MEM.md](raw/articles/UB-MEM.md)
[4] [raw/articles/UB-RSC.md](raw/articles/UB-RSC.md)
[5] [raw/articles/UB-TA.md](raw/articles/UB-TA.md)
[6] [raw/articles/UB-TP-ch6.md](raw/articles/UB-TP-ch6.md)
[7] [raw/articles/UB-NETWORK-ch5.md](raw/articles/UB-NETWORK-ch5.md)
[8] [raw/articles/UB-DL-ch4.md](raw/articles/UB-DL-ch4.md)
[9] [raw/articles/UB-PHY-ch3.md](raw/articles/UB-PHY-ch3.md)
[10] [Ch.6.5.5](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/06-超节点.md) — 李博杰《AI Infra》UB 规模
[11] [AI-Infra-Book.pdf](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
