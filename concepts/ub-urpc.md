---
title: URPC (UB 远程过程调用)
created: 2026-05-09
updated: 2026-05-09
type: concept
tags: [interconnect, scale-up, rpc, memory, programming-model]
sources: [raw/articles/UB-FUN.md]
---

# URPC (Unified Remote Procedure Call)

[[unifiedbus-ub]] 基于 UB 事务层能力和直接内存访问的 RPC 协议，支持任意 UBPU 间直接 P2P 远程函数调用。

## 功能角色

| 角色 | 职责 |
|------|------|
| **Client** | 发起端/调用方，向 Server 发起远程函数调用 |
| **Server** | 接收端/分发方，接收请求并分配给 Worker |
| **Worker** | 执行方，触发函数执行并将结果返回给 Server → Client |
| **Caller** | 应用层调用者 |
| **Callee** | 函数实现者（可与 Worker 合并） |

## 协议流程

```
Caller → Client → URPC Request (function ID + args) → Server
                                                    Server → URPC ACK (args received) → Client
                                                    Server → 分配 Worker
                                                    Worker → 执行函数 → Server
                                                    Server → URPC Response (result) → Client → Caller
```

- Client 可指示是否需要 URPC ACK
- Server **可合并 ACK + Response** 为单条消息（函数执行完成后再返回）
- 每个 URPC Request 携带唯一的 function ID

## 参数传递方法

### Pass-by-value (inline)
- 参数数据封装在 URPC Request 中
- **0.5 RTT**（仅需请求+响应）
- 受 URPC Request 最大大小限制
- 适用：小参数（< 40KB），如存储场景

### Pass-by-value (external)
- 发送参数数据地址，Server 主动 Read/Lod 拉取完整数据
- **1.5 RTT**
- 不受请求大小限制
- Server 拉取后 Client 即可释放内存
- 适用：大参数（> 40KB）

### Pass-by-reference
- 发送参数数据地址，Server 转发给 Worker
- Worker 在**函数执行开始后**按需 Read/Load 拉取数据
- **1.5 RTT**，但传输时机由 Worker 控制
- 数据直接从 Client → Worker（不经 Server 中转）
- Client 在 Worker 实际取走数据后才释放内存
- 适用：**参数传输与函数执行时间接近的场景**（如 AI 训练/推理中数据传输与 NPU 计算重叠）

### 对比

| 方法 | RTT | 数据路径 | 内存释放时机 | 典型场景 |
|------|-----|----------|-------------|---------|
| Inline | 0.5 | Client→Server→Worker | ACK 后 | 小数据 (<40KB) |
| External | 1.5 | Client→Server→Worker | Server 拉取后 | 大数据 |
| By-reference | 1.5 | Client→Worker | Worker 取数据后 | 计算传输重叠 |

## P2P 架构

Client/Server/Worker 均可实现在不同 UBPU 的 Entity 上。利用 UB 的 P2P 架构，任意 UBPU 可直接发起远程函数调用。

**典型应用**：NPU 直接发起 RPC 将数据写入 SSU（存储单元），AI 训练/推理数据从 NPU 直接到 SSU 存储执行，无需 CPU 中转。

## 与其他 RPC 机制对比

- **vs gRPC**：URPC 绕过 OS 内核栈，基于硬件直接内存访问，延迟极低
- **vs RDMA RPC**：URPC 原生支持 pass-by-reference，Worker 可控制数据拉取时机，实现计算-通信重叠
- **vs [[m2n-communication]]**：M2N 专用于 disaggregated inference 的 M:N 通信，URPC 更通用
- 类似于 [[unifiedbus-ub]] 的 UBoE 跨 domain 场景，URPC 也可扩展到跨 domain 调用

## 来源

- UB Base Specification Rev 2.0, §8.5 URPC
