---
type: Concept
title: UB 编程模型与 URMA
description: UB 编程模型：Load/Store 同步、URMA 异步访问（Jetty/事务队列/内存池化/死锁避免）
tags:
- interconnect
- scale-up
- rpc
- memory
- programming-model
timestamp: '2026-05-09T00:00:00Z'
created: 2026-05-09
sources:
- raw/articles/UB-overview.md
- raw/articles/UB-FUN.md
---

# UB 编程模型与 URMA

[Unifiedbus Ub](/entities/unifiedbus-ub.md) Function Layer 提供的两种编程模型及其上层抽象。

## 编程抽象层次

```
Application
    │
    ├── [URPC](/concepts/ub-urpc.md) (远程过程调用)
    │      └── Client/Server/Worker, Pass-by-reference
    │
    ├── Multi-Entity Coordination (融合/集合通信/全局维护)
    │
    ├── URMA (异步内存访问/消息)
    │      └── Jetty API (Standard/One-sided/Group)
    │
    └── Load/Store (同步内存访问)
           └── 硬件自动转换，TP bypass 优化
```

## Load/Store 同步访问

最基础的编程模型。UB Controller 与 NoC 协作，将 CPU/加速器的 load/store 指令自动转换为 UB 事务操作。

### 跨层协调优化

- **TP Bypass 模式**：服务器/机架/小集群内，跳过传输层，依赖数据链路层重传保证可靠性，降低延迟，节省传输层资源
- **TP Channel 模式**：数据中心规模，传输层提供独立的可靠端到端管道
- 支持将 UB 事务作为指令集原生组件：many-to-many 消息发送、事件通知、有序信息传递、全局同步
- 仅支持 ROI 和 ROL 事务服务模式

## URMA (Unified Remote Memory Access)

高性能异步通信库，提供 UB 语义的异步内存访问和双边消息通信。

### Jetty 模型

Jetty 是 URMA 的基本抽象，提供对事务层的访问。每个 Jetty 关联一个或多个事务队列。

#### Jetty 类型

| 类型 | 说明 |
|------|------|
| **Standard Jetty** | 绑定 SQ（发送）+ RQ（接收），双向通信 |
| **One-sided JFS** | 仅绑定 SQ，单向发送 |
| **One-sided JFR** | 仅绑定 RQ，单向接收 |
| **Jetty Group** | 仅存在于 target 端，包含多个 Jetty，绑定 RQ Group，硬件自动分发 |
| **JFC** | Completion Jetty，绑定 CQ，轮询获取完成状态 |
| **JFCE** | Completion Event Jetty，绑定 JFC + EQ，中断通知 |
| **JFAE** | Asynchronous Event Jetty，绑定 EQ，报告异常事件 |

#### Jetty Group 调度策略

Jetty Group 在 target 端实现无 CPU 干预的请求分发：
1. **Hash**：基于 initiator 提供的 Hint 字段哈希选择
2. **Round-robin**：轮询分发
3. **Dynamic load balancing**：基于 RQ 深度动态负载均衡

优势：offload CPU 分发开销，避免跨 NUMA 访问（选择 NUMA 亲和的 Jetty）。

#### Jetty 通信模式

- **Many-to-many**：无一对一绑定，initiator Jetty 可与任意 target Jetty 通信。支持 Standard 和 One-sided Jetty。initiator 发送时需指定 target Jetty。
- **One-to-one**：一对一绑定，仅 Standard Jetty 可用。

#### Jetty 状态机

```
Reset ←→ Ready → Suspend → Error
  ↑                              │
  └──────────────────────────────┘
```

- **Reset**：初始状态，所有资源已分配，属性已初始化。收到的包静默丢弃
- **Ready**：通信协商完成后进入。正常处理事务
- **Suspend**：可恢复传输故障（如 TP channel 故障）时进入。exception_suspend 模式下暂停新 WR，等待已分发 SQE 完成，flush SQ
- **Error**：严重错误（如 Jetty 上下文损坏）。停止 SQE 分发，静默丢弃收到的包。可通过 API 恢复到 Reset

exception_continue 模式下跳过 Suspend 状态，保持 Ready。

### 事务队列

| 队列 | 说明 | 标识 |
|------|------|------|
| **SQ** (Send Queue) | 存储 SQE（事务请求） | RCID |
| **RQ** (Receive Queue) | 存储 RQE（接收上下文） | TCID |
| **CQ** (Completion Queue) | 存储 CQE（完成状态） | — |
| **EQ** (Event Queue) | 事件通知，中断机制 | — |

队列 FIFO 操作，同队列有序，跨队列无序。

### URMA 基本流程

1. 获取 EID，创建 URMA 上下文
2. 创建 Jetty/JFC/JFCE，建立通信关系（导入 target Jetty 和内存段，绑定事务队列）
3. 通过 Jetty API 向 SQ 提交事务请求
4. UB Controller 调度并转换为事务操作
5. 事务层完成操作
6. 完成信息报告到 CQ；异常报告到 EQ
7. 通过 JFC 轮询或 JFCE 中断获取结果

## 内存段 (Memory Segment)

连续地址空间，由 UBMD 标识（EID + TokenID + UBA）。UMMU 在创建时配置 MATT（地址翻译表）和 MAPT（地址权限表）。

### 访问方式
1. **映射方式**：将内存段映射到本地进程虚拟地址空间（MVA），支持同步/异步访问
2. **非映射方式**：直接异步内存访问

### 访问方法
- **地址+长度**：指定起始地址和长度，要求对齐
- **ByteEnable**：仅更新指定字节（Write_with_be）

## 内存借入与共享

基于 UB P2P 架构的内存池化。每个 UBPU 节点可动态切换为 borrower（借入）或 lender（借出）角色。

### 两种模式
- **Memory Borrowing**：借入的内存段被 borrower 独占访问
- **Memory Sharing**：一个内存段可被多个 user 共享

### 访问方式
- **Cacheable**：提供与本地内存相同的缓存一致性能力，适合强数据局部性场景（通常用于 borrowing）
- **Non-cacheable**：避免缓存一致性管理开销，适合通信密集型数据交换

### 所有权机制（软件/硬件协同缓存一致性）

共享内存 cacheable 访问时，每个节点维护独立的 ownership 状态：

| 状态 | 权限 |
|------|------|
| **Invalid** | 不能读写 |
| **Write** | 可读写（独占，其他节点必须 Invalid） |
| **Read** | 只读 |

状态转换操作：
- Write→Invalid：clean + invalidate cache
- Write→Read：clean cache（保留缓存加速后续读）
- Read→Invalid：invalidate cache
- 其他：无需操作

## 通信管理

Initiator 和 target 交换 Jetty/内存段信息的三种方式：
1. **UBFM 协助**：通过 Fabric Manager 交换
2. **Known Jetty**：预配置的 target Jetty（Jetty ID 0=传输层, 1=事务层, 2=Socket over UB, 32-1023=用户自定义）
3. **TCP/IP**：建立 TCP 连接交换信息

## 死锁避免

### 内存访问死锁（三种典型场景）

1. **Memory Pooling 死锁**：A 借 B 的内存，B 借 A 的内存，同时 Writeback 互相等待 TAACK → 循环依赖
2. **Page Table 死锁**：UMMU 页表位于借入内存中，页表读取和原始访问共享同一端口
3. **Page Fault 死锁**：page fault 处理触发二次访问（存储/其他 UBPU 内存），与原始访问共享电路

**解决机制**：请求重试、虚拟通道隔离、事务类型区分、页表本地化、消除无条件完成依赖

### 消息通信死锁

队列资源耗尽 + 环形依赖（A→B 和 B→A 的 RQ 互满）。

**三种基本机制**：
1. 传输层与事务层分离（事务层资源不足不阻塞传输层）
2. Initiator 端重试异常状态（RNR TAACK → 重试）
3. 超时机制释放资源

## 与其他互连对比

UB 的 URMA 类似 RDMA 但更通用（支持 many-to-many、Jetty Group 硬件分发）。Load/Store 的 TP bypass 类似 [Deterministic Execution](/concepts/deterministic-execution.md) 中短路径优化。内存池化所有权机制类似 [Disaggregated Inference](/concepts/disaggregated-inference.md) 中内存解耦，但 UB 在硬件层面提供 cache coherence 支持。

## 来源

- UB Base Specification Rev 2.0, §8 Function Layer

# Citations

[1] [raw/articles/UB-overview.md](raw/articles/UB-overview.md)
[2] [raw/articles/UB-FUN.md](raw/articles/UB-FUN.md)
