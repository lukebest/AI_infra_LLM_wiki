---
title: UB 网络层机制
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [interconnect, scale-up, fabric, routing, congestion-control, networking]
sources: [raw/articles/UB-NETWORK-ch5.md]
---

# UB 网络层机制

[[unifiedbus-ub]] 协议栈网络层（§5），位于数据链路层之上，为传输层和事务层提供服务。核心功能：寻址、路由、QoS、拥塞标记、网络隔离、死锁避免、ICRC 完整性保护。

## 网络地址管理

- **双格式**：32-bit / 128-bit 完整地址 + 16-bit / 24-bit CNA（Compact Network Address）
- 完整地址用于 IP 通信（域内/跨域），CNA 用于域内高效通信
- UB Controller 有 Primary CNA（设备级）+ Port CNA（端口级）
- UBFM 根据互联拓扑管理地址和路由配置

### 路由规则
- Primary CNA 寻址 → 可从任意端口接收
- Port CNA 寻址 → 仅从对应端口接收
- 响应包可复用请求包的源地址，确保回到发起端口

## 包头格式（NTH）

### 16-bit CNA 格式 (CFG=6)
`RT(2) | SCNA(16) | DCNA(16) | CCI(16) | LBF(8) | SL(4) | Mgmt(1) | NLP(3)`

### 24-bit CNA 格式 (CFG=7/9)
`RT(2) | SCNA(24) | DCNA(24) | CCI(16) | RSVD(8) | LBF(8) | SL(4) | NLP(3)`

### IP 地址格式 (CFG=3/4)
`RT(2) | CCI(16) | RSVD(14) | NPI(25) | IP Header | UDP/TCP/...`
- 兼容 IPv4/IPv6，UB 字段插入标准 IP 头之前
- UDP 目的端口 4792（IANA 注册）
- IPv4 不支持分片（Flags=0b010）

## 路由机制

### RT（Routing Type）字段

| RT | LB 模式 | 路径选择 |
|----|---------|----------|
| 00 | Per-flow | 所有可用路径 |
| 01 | Per-packet | 所有可用路径 |
| 10 | Per-flow | 仅最短路径 |
| 11 | Per-packet | 仅最短路径 |

- 需要保序 → 必须用 per-flow；否则可用 per-packet
- 路由模块返回一组出端口（可选 cost），RT + LBF 决定最终端口
- UB Switch 可配单一管理地址，从所有端口捕获发往自身的包

## QoS

- **SL（Service Level）**：4-bit 优先级标识
- **SL→VL 映射**：每个 SL 映射到一个 Virtual Lane
- **Inter-VL 调度**：保证高优先级优先转发
- UB Controller 负责 SL-VL 映射 + VL 间调度；UB Switch 负责 VL 间调度

## 拥塞标记

### CAQM（CCI.Mode=000）
- 发送端设 I bit 请求增带宽 + Hint 字段指示增量
- 交换机逐跳审批：C bit 标拥塞、I bit 批准/拒绝增量、可修改 Hint
- LoC 标识拥塞位置（中间交换机 vs 最后跳交换机）
- 与 [[ub-transport-layer|传输层]] CAQM 拥塞控制联动

### FECN（CCI.Mode=100）
- 2-bit FECN 字段：00=不可标记、01=轻度拥塞、10=无拥塞、11=严重拥塞
- 交换机仅在源拥塞端口标记（可选，防拥塞扩散误标记）
- 与 IP ECN 互通：发送时 ECN→FECN，接收时 FECN→ECN

### FECN_RTT（CCI.Mode=010）
- 在 FECN 基础上增加 Timestamp 字段
- 接收端通过 CNP 将时间戳回传发送端，用于 RTT 测量

## 网络隔离（NPI）

- **NPI（Network Partition Identifier）**：25-bit = Permission(1) + ID(24)
- 不同 NPI → 流量隔离
- 同 ID：Permission=0（高特权）可与任何节点通信；Permission=1（低特权）之间不可通信
- UB Controller 两种模式：
  - **Mode-S（Strict）**：不信任软件栈，单 Entity 下所有接口同一 NPI，硬件强制
  - **Mode-L（Loose）**：信任软件栈，不同接口可不同 NPI，UB Controller 辅助过滤+防 DoS
- UB Switch：按端口配置 NPI 过滤规则，可选 NPI 替换

## 死锁避免

Credit-based 流控的 hop-by-hop 反压可能形成环形缓冲依赖导致死锁。四种机制：

1. **路由算法预防**：特定路由算法消除环路条件（如维度序路由）
2. **自适应路由**：绕开拥塞区域
3. **VL 切换**：在特定节点配置 Input VL→Output VL 映射，打破环形依赖
4. **超时丢包**：队列超时未调度则丢弃所有包，解除死锁

此模型与 [[switching-networks|CLOS 网络]] 中多级交换的缓冲依赖问题同源——InfiniBand 也使用 VL 切换+自适应路由防死锁。

## ICRC 完整性保护

- CRC-32（多项式 0x04C11DB7），初始值 0xFFFFFFFF
- 覆盖包中不可变字段；CCI/LBF/IP TTL/ToS/Checksum 等可变字段替换为全 1 后计算
- 逐字节 bit-reverse → CRC → bit-reverse + 取反 = ICRC
- CFG=3/4：从 IP header 开始保护；CFG=6/7：从 NTH 开始

## 与传输层联动

- NTH.LBF 字段由发送端生成，传输层 per-packet/per-flow LB 使用
- CCI 字段在网络层承载拥塞信息，传输层 CAQM/LDCP/DCQCN 消费
- SL→VL 映射在网络层，传输层 TPG 跨 channel 聚合在 VL 之上
- ICRC 保护跨网络层端到端完整性，传输层重传处理丢包恢复

## 与其他协议对比

| 特性 | UB | InfiniBand | Ethernet/RoCE |
|------|-----|-----------|---------------|
| 地址格式 | CNA(16/24b) + IP(32/128b) | LID(16b) + GID(128b) | MAC+IP |
| 路由 | RT 2-bit 自适应 | LID 路由 + LMC | ECMP |
| 拥塞标记 | CAQM + FECN + FECN_RTT | ECN + FECN/BECN | ECN + DCQCN |
| 网络隔离 | NPI（25-bit） | PKey（16-bit） | VLAN/VxLAN |
| 死锁预防 | 路由+VL切换+超时 | VL映射+自适应路由 | 通常不处理 |
| 完整性 | ICRC（不可变字段） | ICRC + VCRC | FCS（链路级） |
| UDP 封装 | 端口 4792 | 不适用 | 端口 4791 |

## 来源

- UB Base Specification Rev 2.0, §5 Network Layer（完整章节）
