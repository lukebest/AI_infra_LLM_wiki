---
title: SRv6 Source Routing for AI Supercomputers
created: 2026-05-13
updated: 2026-05-13
type: concept
tags: [routing, protocol, scale-up, switch, fabric, retransmission]
sources: [raw/articles/resilient-ai-supercomputer-networking-mrc-srv6.md]
---

# SRv6 Source Routing for AI Supercomputers

## 定义

在 AI 训练集群后端网络中，使用 IPv6 Segment Routing (SRv6) 的 micro-segment ID (uSID) 格式做**静态源路由**，替代传统动态路由协议（BGP/ECMP）。与 [[mrc]] 协同设计部署。

## 核心机制

### uSID uN 转发
- 目的 IPv6 地址 = 32-bit locator prefix + 序列 of 16-bit uSID
- 每个 uSID 对应路径上的一个交换机
- 交换机收到包后，uSID 部分左移 16 bit → 下一跳暴露到前 48 bit
- 查静态转发表确定出端口，线速处理
- 使用 uN (uNode) 风格，每跳显式命名

### EV → SRv6 地址映射
- QP 启动时查 node-specific 配置文件获取 SRv6 地址模板
- 模板中 dst uSID 填入最后一跳的 downlink 编号
- 每个 EV 包含 plane number 和 T0 uplink number
- 发包时：EV 的 plane number 填入所有 uSID，uplink number 填入 T1 uSID

### 为什么禁用动态路由
1. MRC 自己做自适应负载均衡，动态路由会干扰（两套机制冲突）
2. 高 radix 两层拓扑的 ECMP set 极大（256 条），维护困难
3. 链路故障导致每个目的地的可达 ECMP set 不同，转发引擎压力大
4. 静态路由 + MRC 容错 = 更简单的控制面

### 可观测性优势
- **Clustermapper** 探测包走精确已知的 SRv6 路径
- 与 ECMP hash 不同，探测路径 = 数据路径，无歧义
- T0 自探测 + T1 自探测 → 精确定位故障链路/交换机
- SRv6 探测走数据面（非 ICMP 控制面），支持高频探测

## 部署
- NVIDIA Spectrum-4/5 (Cumulus, SONiC)
- Broadcom Tomahawk 5 (Arista EOS)
- 交换机转发表在安装时配置，正常运行期间不更改

## 关系

- 为 [[mrc]] 提供确定性的路径映射
- 与 [[multi-plane-clos-topology]] 拓扑结构共同设计
- 相比传统 [[switching-networks]] 中的动态路由，追求极简控制面
- 参见 [[switching-principles]] 中电路交换/分组交换的基础对比
