---
title: UB 事务层
created: 2026-05-09
updated: 2026-05-09
type: concept
tags: [interconnect, scale-up, fabric, protocol, hardware]
sources: [raw/articles/UB-TA.md]
---

# UB 事务层

[[unifiedbus-ub]] §7 Transaction Layer。位于传输层之上，为上层编程模型（load/store 同步访问和 [[ub-programming-models|URMA]] 异步访问）提供事务服务和事务操作。

## 概览

事务层接收上层事务操作，协调底层协议在 Initiator 和 Target 之间执行和完成事务操作。核心设计目标：

1. **统一事务操作**：为不同编程模型提供统一的事务接口
2. **多种服务模式**：满足不同可靠性和排序需求
3. **安全机制**：Token 验证确保事务操作安全执行
4. **高效传输**：TP Bypass 模式 + Compact 包头优化 load/store 同步访问

## 四类事务

| 类型 | TAOpcode | 说明 |
|------|----------|------|
| **Memory** | Write(0x3), Read(0x6), Atomic(0x7-0xF), Write_with_notify(0x5), Write_with_be(0x14), Writeback(0x17), Writeback_with_be(0x18) | 对 Target 内存段的读写和原子操作 |
| **Message** | Send(0x0), Send_with_immediate(0x1), Write_with_immediate(0x4) | 基于 Jetty 消息队列的通信 |
| **Maintenance** | Prefetch_tgt(0x15) | 目标端数据预取，优化后续 Read 延迟 |
| **Management** | Management(0x10) | 携带管理命令，见 [[ub-resource-management]] |

每种事务操作由唯一 TAOpcode 标识，包含至少一个请求包，可选一个响应包。

## 事务包头

### BTAH (Basic Transaction Header)

所有请求包必须包含，有 Full 和 Compact 两种格式：

| 字段 | Full BTAH | Compact BTAH |
|------|-----------|--------------|
| TAOpcode (8-bit) | 操作类型 | 同左 |
| TAver (2-bit) | 协议版本，当前为 0 | 同左 |
| EE_bits (2-bit) | 执行环境安全属性 (non-TEE/TEE) | 同左 |
| TV_EN (1-bit) | 是否包含 TVETAH（Token 验证头） | 同左 |
| Poison (1-bit) | 载荷是否含 poisoned 数据 | 同左 |
| UD_Flag (1-bit) | 是否包含用户自定义头 | 同左 |
| INI_TASSN (16-bit) | Initiator 事务段序列号 | 同左 |
| ODR (3-bit) | 排序属性 (NO/RO/SO + TCO) | **无** |
| INI_RC_Type/ID | 发送上下文类型和标识 | **无** |
| No_TAACK | 是否跳过事务确认 | **无** |

**Compact BTAH 仅用于 TP Bypass 模式**，省略排序和上下文字段以减少开销。

### ATAH (Acknowledge Transaction Header)

所有响应包必须包含，同样有 Full/Compact 格式：
- TAOpcode：TAACK(0x11)、Read_response(0x12)、Atomic_response(0x13)
- Status (Compact) / RSPST+RSPINFO (Full)：事务完成状态
- INI_TASSN：回传 Initiator 的序列号以匹配请求
- INI_RC_ID：回传 Initiator 的上下文标识

### 扩展包头

| 扩展头 | 用途 | 携带信息 |
|--------|------|----------|
| **MAETAH** | Memory Address，Memory 事务必选 | Address(64-bit) + TokenID(20-bit) + Length |
| **MTETAH** | Message Target，Message 事务必选 | TGT_TC_ID (目标接收队列) + Hint (负载均衡) |
| **TVETAH** | Token Value，安全验证时必选 | TokenValue(32-bit) 用于 Target 端权限检查 |
| **TAIDETAH** | Task ID | TAID(16-bit)，请求→响应原样回传 |
| **OFSTETAH** | Offset，多包事务分段 | Offset(24-bit)，粒度 1KB |
| **IMMETAH** | Immediate Data | 8 字节立即数据 + TokenValue + Msg_Length |
| **NTFETAH** | Notify Data (Write_with_notify) | 通知数据 + 目标地址 + 访问凭证 |
| **BEETAH** | Byte Enable (Write_with_be) | 64~1024-bit 字节有效位图 |
| **UDETAH** | User Defined，厂商自定义 | 4 字节 |
| **MGMTETAH** | Management 事务必选 | 管理命令净荷 |

### 安全验证

通过 TVETAH 携带 TokenValue：
- **Memory 事务**：用 MAETAH.TokenID 检索 Target 端 Token 进行比对
- **Message 事务**：用 MTETAH.TGT_TC_ID 检索 Target 端 Jetty/JFR Token 进行比对
- 数据长度为 0 时：Memory 事务不需要验证，Message 事务仍需验证

## 事务可靠性

### 可靠事务

- 底层协议保证包传输可靠
- 支持重试处理资源短缺等可管理异常
- 不可解决异常上报上层处理
- 重试超限后通过 CQ 报告上层

### 不可靠事务 (UNO)

- 不依赖底层可靠性，不重传失败事务
- 载荷不得超过传输层 MTU
- 适用于 Prefetch_tgt、Management 等操作

## 事务排序

### TEO (Transaction Execution Order)

| 标志 | 含义 | 行为 |
|------|------|------|
| **NO** | 无排序要求 | 不受排序约束 |
| **RO** | 宽松排序 | 阻止后续 SO 事务提前执行 |
| **SO** | 强排序 | 等待前面所有 RO/SO 事务完成后执行 |

### TCO (Transaction Completion Order)

控制完成通知 (CQE) 的生成顺序：
- **Send Completion Order**：Initiator 端 CQE 生成顺序
- **Receive Completion Order**：Target 端 CQE 生成顺序
- 各自支持 in-order 和 out-of-order 两种

### Fence 机制

事务标记为 NO 但作为 Fence 使用：确保前面所有事务完成后才发送后续事务，但不影响自己的排序要求。

## 四种服务模式

### ROI (Reliable Ordered by Initiator)

```
Initiator 发送事务 → 等待前面 RO/SO 事务的 TAACK → 发送下一个 SO 事务
```

- **Initiator 负责排序**：发送 SO 事务前必须等待前面 RO/SO 事务完成
- 支持多路径传输（TPG / 多 TP Channel / 网络层负载均衡）
- 适合排序依赖简单、Initiator 有足够状态信息的场景

### ROT (Reliable Ordered by Target)

```
Initiator 连续发送所有事务（不等待）→ Target 维护排序 → 按序执行
```

- **Target 负责排序**：Initiator 无需等待即可连续发送
- 比 ROI 节省一次往返延迟
- Target 需要额外资源：**Sequence Context (SC)**
- SC 资源可静态配置或动态申请（BTAH.Alloc=1）

**SC 动态分配流程**：
1. Initiator 发送 Alloc=1 的请求
2. Target 分配 SC，返回 SCID（ATAH.SV=1 表示成功）
3. Initiator 后续请求使用 SCID（INI_RC_Type=SC）
4. Target 响应时通过 SC 映射回 RCID

### ROL (Reliable Ordered by Lower Layer)

```
Initiator 连续发送 → 底层协议保证有序 → Target 按序接收执行
```

- **底层协议负责排序**：要求传输层/网络层保证包有序
- RTP 模式：同一 TP Channel 传输有排序要求的事务
- CTP/TP Bypass 模式：网络层必须使用 per-flow 负载均衡（单路径）
- 需要处理 Target NoC 内部可能的乱序

### UNO (Unreiable Non-ordered)

- 不保证可靠性或排序
- 载荷不超过 MTU
- 可配合 UTP/CTP/TP Bypass 使用

### 服务模式对比

| 特性 | ROI | ROT | ROL | UNO |
|------|-----|-----|-----|-----|
| 可靠性 | ✅ | ✅ | ✅ | ❌ |
| 排序责任 | Initiator | Target | 底层 | 无 |
| 多路径 | ✅ | ✅ | 受限 | ✅ |
| 额外资源 | 无 | SC (Target端) | TP Channel 绑定 | 无 |
| 延迟 | 等待 RTT | 无需等待 | 取决于底层 | 最低 |

## Memory 事务详解

### Write 系列

| 操作 | TAOpcode | 特点 |
|------|----------|------|
| **Write** | 0x3 | 基础写入，支持分段 |
| **Write_with_notify** | 0x5 | 写入完成后附带通知数据到独立内存段 |
| **Write_with_be** | 0x14 | 字节使能，单包，仅写有效字节 |
| **Writeback** | 0x17 | Cache 写回，非阻塞（不可被普通读写阻塞，防死锁） |
| **Writeback_with_be** | 0x18 | Writeback + 字节使能 |

**Write_with_notify 流程**（以 ROI 为例）：
1. Initiator 发送 Write 包 → Target 更新内存返回 TAACK
2. 所有 Write TAACK 收到后，发送最后一个携带 NTFETAH 的包
3. Target 写入通知数据到独立内存段 → 返回 TAACK

### Read

- 支持 ROI/ROT/ROL
- 请求可分段，但**响应不可分段**（一个请求 TASSN 对应一个响应 TASSN）
- 响应通过 OFSTETAH.Offset 告知 Initiator 数据偏移
- TAIDETAH.TAID 帮助 Initiator 匹配请求和响应

### Atomic（9 种原子操作）

单包操作，保证原子性和仅执行一次：

| TAOpcode | 操作 | 行为 |
|----------|------|------|
| 0x7 | Compare_swap | operand2 == 本地数据 → 交换 operand1；返回本地数据 |
| 0x8 | Swap | operand1 与本地数据交换，返回交换前数据 |
| 0x9 | Store | 写入 operand1，无返回数据 |
| 0xA | Load | 返回本地数据，不修改 |
| 0xB | Fetch_add | 本地数据 += operand1，返回修改前数据 |
| 0xC | Fetch_sub | 本地数据 -= operand1，返回修改前数据 |
| 0xD | Fetch_and | 本地数据 &= operand1，返回修改前数据 |
| 0xE | Fetch_or | 本地数据 \|= operand1，返回修改前数据 |
| 0xF | Fetch_xor | 本地数据 ^= operand1，返回修改前数据 |

请求载荷包含两个等长 operand（operand2 不需要时忽略）。

## Message 事务详解

| 操作 | TAOpcode | 特点 |
|------|----------|------|
| **Send** | 0x0 | 发送消息到 Target 接收队列 (RQ)，每包消耗一个 RQE |
| **Send_with_immediate** | 0x1 | 发送消息 + 8 字节立即数据写入 Target CQE |
| **Write_with_immediate** | 0x4 | 写入数据 + 立即数据，仅携带立即数据的包消耗 RQE |

Message 事务通过 MTETAH 指定 Target 端接收队列 (TGT_TC_ID)，支持 TC Group 负载均衡。

## 维护事务

### Prefetch_tgt (0x15)

- UNO 模式，不保证可靠
- Target 自行决定是否预取
- Initiator 不重试，异常时静默丢弃
- 用于优化后续 Read 延迟

## 与其他概念关联

- [[unifiedbus-ub]] — UB 整体架构，事务层是协议栈核心层
- [[ub-transport-layer]] — 事务层位于传输层之上，使用 TP Channel/TPG 等传输服务
- [[ub-programming-models]] — load/store 和 URMA 编程模型直接调用事务层操作
- [[ub-memory-management]] — Memory 事务的地址翻译和权限检查由 UMMU 完成
- [[ub-resource-management]] — Management 事务携带管理命令；ROT 模式的 SC 资源由资源管理分配
- [[ub-urpc]] — URPC 建立在事务层消息语义之上

## 协议栈关联

- [[ub-transport-layer]] — 事务层依赖传输层的可靠/不可靠传输服务
- [[ub-programming-models]] — 事务层消息语义被 URPC 和 Jetty 编程模型使用
- [[unifiedbus-ub]] — UB 协议整体架构

## 来源

- UB Base Specification Rev 2.0, §7 Transaction Layer
