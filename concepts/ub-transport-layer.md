---
type: Concept
title: UB 传输层机制
description: UB 传输层：四种模式（RTP/CTP/UTP/TP Bypass）、PSN 机制、Go-Back-N/Selective 重传、TPG
  多路径负载均衡、LDCP/CAQM/DCQCN 拥塞控制、ROL 模式事务-传输联动
tags:
- interconnect
- scale-up
- fabric
- transport
- congestion-control
- routing
timestamp: '2026-05-11T00:00:00Z'
created: 2026-05-09
sources:
- raw/articles/UB-overview.md
- raw/articles/UB-TP-ch6.md
---

# UB 传输层机制

[Unifiedbus Ub](/entities/unifiedbus-ub.md) 协议栈传输层（§6），位于事务层与网络层之间。提供端到端可靠/不可靠传输、多路径负载均衡、拥塞控制。

## 四种传输模式

| 模式 | 可靠性 | 负载均衡 | 拥塞控制 | 典型场景 |
|------|--------|----------|----------|----------|
| **RTP** | 端到端确认+重传 | TP Channel 粒度 | TP Channel 粒度 | 高可靠需求 |
| **CTP** | 依赖下层（链路层 hop-by-hop 重传） | Entity 粒度 | {Dest Entity, VL} 粒度 | 直连/高链路质量 |
| **UTP** | 无保证 | 无 | 无 | 带内连接建立等容忍丢包 |
| **TP Bypass** | N/A | N/A | N/A | Load/Store 同步内存访问 |

## 包格式体系

- **RTPH** (16B)：TPOpcode + NLP + SrcTPN(24b) + DstTPN(24b) + PSN(24b) + TPMSN(24b) + RSPST/RSPINFO
- **CTPH** (1B)：极简 — 仅 TPOpcode(2b) + Padding + NLP
- **UTPH** (16B)：保留字段为主，无 PSN/TPN
- **响应包**：TPACK/TPNAK/TPSACK（RTP），可选携带 CETPH（拥塞信息）或 SAETPH（选择性确认 BitMap）
- **CNP**：独立拥塞通知包（RTP/CTP 均可用）

## PSN 机制（RTP 核心）

- 24-bit 单调递增序号，范围 0–16M-1，溢出回绕
- 初始 PSN 随机协商，每个 TP Channel 独立 PSN 空间
- 最大在途窗口 ≤ 8M-1（半空间约束）
- 乱序接收范围可配：[128, 256, 512, 1024, 2048]
- 响应包（TPACK/TPNAK/TPSACK）不消耗 PSN

## 重传算法

### Go-Back-N
- **+Fast Retransmission**：收到 TPNAK 立即重传该 PSN 及之后所有包。适合 per-flow LB、极低丢包率
- **-Fast Retransmission**：仅 RTO 超时触发。适合 per-packet LB（避免乱序误触发）
- 实现简单但冗余重传多

### Selective Retransmission
- 仅重传 TPSACK BitMap 标识的缺失包
- 接收端维护 BitMap 记录每个 PSN 接收状态
- **MarkPSN 机制**：区分新包发送阶段与丢失包重传阶段，允许快速检测非首次丢包（避免等 RTO）
- **HighRtxPSN**：记录已重传的最大 PSN，防止重复重传
- 适合丢包率较高的链路

### RTO 超时策略
- **静态**：固定间隔 [512μs, 16ms, 128ms, 4s]
- **动态**：指数退避 `RTO = Base_time × 2^(N × Times)`，推荐 Base_time 正相关于 RTT
- 逐渐增大超时的好处：快速恢复尾部丢包、适配拥塞导致 RTT 增加、避免误判路径不可达

## 多路径负载均衡

### TPG (Transport Channel Group)
- 多个 TP Channel 组成一个 TPG，对事务层呈现为单一 Entity
- 事务操作 → TPG → 按 policy（如队列深度）选 TP Channel → 发送
- 不同 TP Channel 可绑定不同物理端口，最大化带宽利用

### Per-Flow LB
- 同一 TP Channel 的包走同一路径（通过 UDP 源端口或 LBF 字段区分）
- 每个 TP Channel 独立拥塞控制上下文

### Per-Packet LB
- 同一 TP Channel 的不同包可走不同路径（改变 LBF 或交换机启用 per-packet ECMP）
- 需配合乱序接收 + 仅超时重传（禁用 fast retransmission）
- TPSACK 仅在累积 N 个乱序包后发送（减少响应包开销）

### CTP 负载均衡
- Entity-based：多物理端口绑为一个 Entity，LBF 字段选择成员端口
- 支持 flow-based 和 packet-based 两种方式

## 拥塞控制

### Window-based（LDCP）
- 每个 TP Channel 独立拥塞窗口 (cw)
- `aval_win = cw - inflight`，包仅在 aval_win 足够时发送
- inflight = data_size_sent − data_size_recvd（通过 CETPH.Ack_seq 同步）
- Go-Back-N 重传时 inflight 清零；Selective 重传仅减去重传包大小
- RTO 超时直接 reset inflight = 0

### Rate-based
- 无拥塞窗口，直接调整发送速率
- 不需维护 inflight/aval_win，资源开销更低

### CAQM（Confined Active Queue Management）
- 发送端在包中携带窗口增长请求（C bit + I bit + Hint 字段）
- 交换机逐跳审批：根据自身资源决定批准/拒绝/削减
- 接收端通过 TPACK-CC/TPSACK-CC 回传审批结果
- 支持 coalesced acknowledgement（累积 C/I/Hint）
- 窗口调整规则：C>0 且 I=0 → 减窗；C>0 且 I=1 → 增 Hint − C；C=0 且 I=1 → 增 Hint；C=0 且 I=0 → 不变

### DCQCN 支持
- CNP 包携带 ECN 级别（minor 0x1 / severe 0x3）+ Loc 标志（中间节点 vs 最后跳交换机）
- 用于实现 RoCE v2 风格的基于优先级的拥塞控制

### Per-Packet LB 下的拥塞控制适配
- 仍以 TP Channel 粒度维护拥塞上下文
- 但仅当所有路径整体拥塞时才降速，避免单路径拥塞过度反应

## 传输流程

### RTP Sender
1. 事务层 → 选 TP Channel/TPG → 分段为 TP Packet（按 MTU）→ 分配 PSN → 设置 TPOpcode（last bit）
2. 收到 TPACK/TPNAK/TPSACK → 更新传输状态 → 触发重传（如需要）

### RTP Receiver
1. 按 DstTPN 找 TP 上下文 → PSN 验证（in-order/out-of-order/duplicate/invalid）
2. 提交 payload 到事务层 → 检查 last flag → 全部收到则通知事务层

### CTP
- 每个 TP Packet 携带完整事务操作（不分段）
- 无传输层确认，事务层响应（TAACK）作为数据包发送

## 与事务层交互（[事务层](/concepts/ub-transaction-layer.md) 关联）

### ROI/ROT 模式
- 传输层响应（TPACK）与事务层响应（TAACK）分离
- TAACK 作为独立 TP Packet 发送，需额外 TPACK 确认

### ROL 模式
- 事务层响应搭载在传输层 TPACK 中（TPACK 承载 TAACK）
- 最后一个 TP Packet 的 TPACK 延迟到事务层处理完成后才发送
- 节省一次 RTT（传输确认 + 事务确认合一）
- RSPST/RSPINFO 字段区分正常确认、RNR、Page Fault、Completer Error 等

## 与其他互连对比

- UB RTP ↔ Infiniiband RC QP（类似 PSN + 确认机制），但 UB 额外提供 TPG 多 channel 聚合
- UB CTP ↔ RoCE v2 DCT（轻量连接），依赖链路层可靠性
- UB per-packet LB + 乱序接收 ↔ [CLOS](/concepts/switching-networks.md) 多路径 + 自路由设计思想
- CAQM ↔ Quantized Congestion Notification (QCN, IEEE 802.1Qau)，但 CAQM 是逐跳审批制
- MarkPSN 机制在标准 RDMA 中无对应，是 UB 针对 non-initial loss 的创新优化

## 来源

- UB Base Specification Rev 2.0, §6 Transport Layer (完整章节，~250 行规范 + 大量场景图解)

# Citations

[1] [raw/articles/UB-overview.md](raw/articles/UB-overview.md)
[2] [raw/articles/UB-TP-ch6.md](raw/articles/UB-TP-ch6.md)
