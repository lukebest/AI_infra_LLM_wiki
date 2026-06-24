---
type: Concept
title: UB 资源管理
description: UB 资源管理：UBFM、Entity 模型/池化/虚拟化、配置空间、管理命令、三级复位+三级错误 RAS
tags:
- interconnect
- scale-up
- fabric
- virtualization
- hardware
timestamp: '2026-05-09T00:00:00Z'
created: 2026-05-09
sources:
- raw/articles/UB-RSC.md
---

# UB 资源管理

[Unifiedbus Ub](/entities/unifiedbus-ub.md) §10 Resource Management。定义 UBFM 如何管理 UB domain 内的互连、通信和计算资源，以及 Entity 生命周期、虚拟化和 RAS 机制。

## UBFM (UB Fabric Manager)

UB domain 的管理员，管理所有 Entity 和端口的互连、通信和计算资源。

### 关键能力
- 通过 GUID 识别和调度资源
- 管理每个 Entity 的 EID，使 Entity 间可通过 EID 直接访问
- 将 Entity 分配到 UB Partition，实现访问隔离
- 动态处理系统运行事件
- 管理 CNA (Compact Network Address) 配置和路由表

### 部署模型
- 大型 UB domain 可部署**多个 UBFM 实例**，每个管理一个 sub-domain
- Sub-domain 不可重叠，所有 UBFM 实例协同工作
- 在服务器中，host 系统软件可承担 UBFM 功能

## 协议组件模型

### UB Controller vs UB Switch

| | UB Controller | UB Switch |
|--|---------------|-----------|
| 拓扑位置 | 叶节点 | 非叶节点 |
| 核心功能 | 为本地 UBPU 提供远程内存访问/消息服务 | 路由转发，互连 UB Controller |
| 扩展功能 | 内存池化、Entity 池化、虚拟化、中断 | 路由、访问隔离、中断报告 |

### 配置管理模型

每个 UB Controller/Switch 由以下结构组成：
- **N 个 Entity**（≤65,536，从 0 编号，Entity 0 必选）
- **M 个 Port**（≤16,384，从 0 编号，Port 0 必选）
- Port 包含物理端口和虚拟端口 (vPort)，被所有 Entity 共享

Entity 0 负责管理其他 Entity 和共享资源（网络层/数据链路层/物理层）。

### 资源管理模型

**MUE (Management UB Entity)**：从 Entity 0 开始的连续 Entity 集合，提供共享资源（如 TP Channel）和管理接口。其他 Entity 可使用但不可管理这些共享资源。在虚拟化场景中，MUE 为多个 Entity 托管资源，最小化 VM 攻击面。

## Entity 访问与隔离

### EID (Entity Identifier)

128-bit 地址空间，在 UB domain 内唯一标识 Entity。链路上可携带完整 128-bit EID 或缩短的 20-bit EID。EID 0 保留，不分配。

EID 与网络地址绑定。Entity 迁移时需重新绑定到新位置的网络地址。

### 访问流程

```
Initiator Entity → Request (SEID + DEID + Token + UBA) → Target Entity
                                                              │
                                                        DEID 确定处理 Entity
                                                        Token 认证访问请求
```

### UB Partition 隔离

- 每个 Entity 恰好属于一个 UB Partition
- **UPI (UB Partition Identifier)**：15-bit 或 24-bit，支持可信配置和防欺骗
- UPI=0 的 Entity 不能与其他 Entity 通信
- 发送方在包中添加 UPI，接收方验证，不匹配则丢弃

## 函数调用方式

| 方式 | 说明 |
|------|------|
| **MMIO** | 将 Entity 资源空间映射到处理器 MMIO 地址空间，通过读写 MMIO 调用函数 |
| **消息通信** | 通过本地 UB Controller 的消息接口发送命令，Entity 解析执行 |
| **[URPC](#ub-urpc\)** | 通过 URPC 直接调用远程函数 |

UBPU 可将访问凭证授予其他 Entity，使其通过 DMA 等方式远程调用。

## 中断机制

### USI (UB Signaled Interrupt)

基于 Write 类型事务语义发送中断。目标地址与中断子系统指定的地址一致。

### 两种中断实现

| | Type 1 | Type 2 |
|--|--------|--------|
| 向量数 | ≤32 | ≤N+1 (可配置) |
| 地址表 | 单一 Interrupt Address | 多地址表（M+1 entries） |
| 向量表 | 固定 | 可配置 Vector Table |
| 粒度 | 每 Entity 一组寄存器 | 支持 vector 共享 address |
| Pending | 32-bit bitmap | 可扩展 bitmap |

## 配置空间结构

### CFG0 vs CFG1

| 空间 | UBFM 权限 | User 权限 |
|------|-----------|-----------|
| **CFG0** | 读写 | 只读 |
| **CFG1** | 读写 | 读写 |

### Slice 结构

配置空间分为多个 slice（版本化），每个 slice 1KB（ROUTE_TABLE 1GB）：
- **CFG0_BASIC** — 基础信息、GUID、EID
- **CFG0_CAP** — 能力位图（错误记录/EMQ/安全等）
- **CFG1_BASIC** — Entity 基础配置
- **CFG1_CAP** — Decoder/Jetty/中断/内存能力
- **CFG0_PORTx** — 端口基础/链路/数据速率/LTSM/错误
- **CFG0_ROUTE_TABLE** — 路由表

## 管理命令

### 枚举管理

在设备未配置 CNA 时，通过**源路由 (Scan Header)** 转发枚举消息：
- **Topology Query**：发现设备拓扑（端口数、端口信息、设备能力、邻居 GUID）
- **CNA Configuration**：配置网络地址（primary CNA / port CNA）
- **CNA Query**：查询网络地址配置

响应使用 TLV 格式（Type-Length-Value）。

### 配置管理

| 命令类型 | Code | 功能 |
|----------|------|------|
| Error Message | 0 | 向 UBFM 报告 class-C 错误 |
| Link Change | 1 | Link Up/Down 事件通知 |
| Configuration | 2 | 读写 CFG0/CFG1 寄存器 |
| VDM | 3 | MCTP over UB / 厂商自定义消息 |
| Entity Info Exchange | 4 | 资源空间信息交换/Entity 信息查询/邻居查询 |
| Device Security | 5 | SPDM 设备认证/Token 检查配置 |
| Pooled Resource | 6 | Entity 注册/注销/Bus Instance 创建/销毁/配置完成通知/端口复位通知 |

## 池化 Entity 管理

### 注册流程

```
UBFM → 配置 EID/UPI/UEID → 发送 Entity Registration → User UB Bus Driver 注册
→ OS 创建设备 → 加载驱动 → 使用设备
```

### 注销流程

```
UBFM → 发送 Entity Deregistration → User 注销设备资源 → 销毁 OS 设备 → 响应
→ UBFM 复位 Entity → 回收
```

### 替换流程

Entity 发生不可纠正错误时，UBFM 可选择另一个 Entity，迁移配置后注册给 User 作为替换。

## 通信控制

管理员可启用 UBPU 间通信控制。标准传输模式下：

```
① UBPU 申请通信 → ② UBFM 策略判定 → ③ TP Channel 协商 → ④ 报告协商结果
→ ⑤ UBFM 激活 TP Channel → ⑥ 开始通信
```

CTP/TP Bypass 模式下通过控制路由表条目实现。

## 远程内存注册控制

管理员可启用集中控制的远程内存注册：UBFM 查询 Entity 资源空间地址 → 写入 UB Controller Decoder MATT → 处理器核心通过 load/store 访问远程内存。

## 虚拟化

### 硬件辅助设备虚拟化

- Entity 可通过 hypervisor 直通到 VM
- UBFM 可将池化 Entity 分配给指定 VM
- Entity 可从一个 VM 卸载后重新分配给另一个 VM（需安全处理）

### 虚拟化机制

```
Hypervisor:
  ├── 数据面直通 VM（资源空间访问、中断、设备功能数据流）
  └── 管理面由 Hypervisor 接管（配置空间访问）
  
  支持 UB Bus，模拟基于拓扑的互连结构呈现给 VM
```

VM 启动时创建独立 Entity 作为总线访问入口，分配 EID 和 UPI。不同 VM 通过 UB Partition 隔离。

## RAS (Reliability, Availability, Serviceability)

### 三级复位

| 级别 | 范围 | 触发方式 |
|------|------|----------|
| **Device-Level** | 所有 Entity、功能、端口恢复初始状态 | 管理命令 / Pin 信号 |
| **Entity-Level** | CFG1 + 资源空间恢复初始状态，不影响公共资源 | 管理命令 / User 命令 |
| **Port-Level** | 指定端口恢复初始状态，需重新配置 | 管理命令 |

### 三级错误分类

| 级别 | 影响范围 | 报告路径 | 处理方式 |
|------|----------|----------|----------|
| **Class-A** | 单个事务，Fabric 拓扑完好 | CQ → 编程接口 | 事务重试 / Jetty 复位 / TP Channel 复位 / Entity 复位 |
| **Class-B** | Entity/TP Channel/Jetty 级别，Fabric 拓扑完好 | EQ → 设备驱动 | Jetty 复位 / TP Channel 复位 / Entity 复位 |
| **Class-C** | 设备/端口公共资源，可能影响 Fabric 拓扑 | Error Message → 本地固件 → UBFM | 端口/设备复位 |

Class-C 进一步分为：Correctable（自恢复不影响服务）和 Uncorrectable（需软件干预）。Uncorrectable 细分为 NFUE 和 FUE。

### Class-A 典型错误
- 不支持的 Opcode、长度错误、权限验证失败
- 远程请求不支持/中止、数据 Poison
- 事务重试超限、事务响应超时

### Class-C 典型错误
- **可纠正**：Block Align Unlock、Elasticity Buffer、Lane-to-Lane Deskew、CRC、链路降速/降道
- **不可纠正**：数据链路协议错误、重传状态机错误、包长度错误、ICRC 校验、接收缓冲区溢出、流控溢出

## 与其他概念关联

- [Unifiedbus Ub](/entities/unifiedbus-ub.md) — UB 整体架构，资源管理是其核心子系统
- [Ub Memory Management](/concepts/ub-memory-management.md) — UMMU 地址翻译和权限检查
- [Ub Programming Models](/concepts/ub-programming-models.md) — Jetty/队列/URMA 是资源管理的用户面
- [Switching Networks](/concepts/switching-networks.md) — UB Switch 的路由服务对应多级交换网络
- [Deterministic Execution](/concepts/deterministic-execution.md) — RAS 机制确保确定性执行的基础

## 来源

- UB Base Specification Rev 2.0, §10 Resource Management

# Citations

[1] [raw/articles/UB-RSC.md](raw/articles/UB-RSC.md)
