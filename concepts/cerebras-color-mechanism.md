---
type: Concept
title: Cerebras Color Mechanism
description: WSE Color 虚拟通道机制：静态路由+独立缓冲+Color×4任务调度+独立反压，Fabric/Local Color 双类型
tags:
- cerebras
- wse
- fabric
- routing
- noc
- deterministic
- virtual-channel
- communication
timestamp: '2026-05-29T00:00:00Z'
created: 2026-05-29
sources:
- US10515303B2
- raw/papers/Near-optimal_wafer-scale_reduce.pdf
---

# Cerebras Color 机制

US10515303B2（Sean Lie, Cerebras Systems）描述的 Color 机制，是 WSE 晶圆级加速器片上通信的核心抽象。Color 同时充当**虚拟通道标识符**和**任务选择器**双重角色。

## 本质：Color = 虚拟网络

Color 是 Wavelet（片上通信包）中的字段，标识一个逻辑上独立的虚拟网络（virtual channel），叠加在同一套物理网络上。

- **Fabric Color**：PE 间虚拟通道，5-bit 整数（0-31）
- **Local Color**：PE 到自身的虚拟通道（自环回）
- 完整 Color 字段在某些实现中为 6-bit：高位区分 Fabric/Local 类型
- 典型配置：**16 个 Color**（c0...c15），也可配为 8、24 或 32 个
- Fabric 上有多个虚拟网络叠加在同一个物理网络上，每个虚拟网络即一个 Color
- 每个 Color 有**独立的物理缓冲**，共享**物理路由资源**
- 独立缓冲使 Colors 间**非阻塞**

## Wavelet 中的位置

Wavelet 格式：`Color | Control Bit | 可选 Index | Data`

- **Sparse Wavelet**：Control Bit + Index（Lower/Upper Bits）+ Sparse Data + Color
- **Dense Wavelet**：Control Bit + Dense Data（多个元素）+ Color
- Control 字段互斥地指示 **Control 状态** 或 **Data 状态**
- 所有字段在**同一个时钟周期**内接收

## 静态固定路由

这是 Color 机制最核心的设计决策：

- 每个 Color 关联一个**编译时静态确定的路由模式**，由 Placement Server 软件计算
- **运行时没有动态路由决策** — 属于同一 Color 的数据始终按固定路径流动
- 这匹配了神经网络的通信模式（神经元连接是静态指定的）
- 固定路由 → 硬件面积更低、延迟可预测

### 为什么静态路由可行
- 神经网络层间连接在编译时已知
- 每个 Color 只有一个 active input source（软件层面协调）
- 单 source 意味着同一 Color 内**无拥塞**

## 路由器中的实现

路由器（Router 600）为每个 Color 维护独立资源：

### Data Queues（650）
- 每个 Color **2 个 entry**
  - Entry 1：解耦输入/输出
  - Entry 2：捕获 parallel stall 时的 inflight data
- 总存储：`16 colors × 27 bits × 2 entries = 864 bits`（或 33-bit 版为 1056 bits）
- 通过寄存器/register file 实现

### Dest（661）— 目标方向查找表
- 每个 Color 的静态目标方向：`16 colors × 7 directions = 112 bits`
- 按 Color 查找，返回 bit vector 指示输出方向
- 支持**多播**：单个 Color 可配置多个输出方向
- 路由器将 incoming wavelet **复制到所有配置的输出方向**

### Sent（662）
- 追踪每个 Color 的已发送状态

### Stall 信号
- 每个方向、每个 Color 有独立的 **stall/ready 信号**
- 每个 core clock cycle 更新

## 任务调度 — Color 驱动计算

Color 最巧妙的设计：**Color 直接决定执行哪段代码**。

```
收到 Data Wavelet  → 指令起始地址 = Base_Register + Color × 4
收到 Control Wavelet → 指令起始地址 = Base_Register + Index_Lower_Bits
```

### 任务启动流程（Flow 900）
1. **Select Ready Wavelet**（Picker 830）：从 Input Queues 中选择 ready 的 wavelet
   - Ready 条件：Active Bit asserted 且 Block Bit deasserted
   - 调度策略：Round-Robin 或 Pick-from-Last
2. **Control/Data 判断**：检查 Control Bit
3. **计算指令地址**：Data→Color×4+Base；Control→Index+Base
4. **Fetch & Execute**：从计算出的地址取指执行，直到 Terminate 指令
5. **后续同 Color wavelet 作为 operand 消费**，直到任务终止

### Task Activating（Flow 920）
1. Activate Operation for Color(s) — 软件激活特定 Color
2. Activate Color(s) — 硬件设置 Active Bit
3. Picker Selects Color — 调度器选择 ready 的 Color
4. Initiate Task, Deactivate Color — 启动任务，清除 Active Bit

### Block/Unblock（Flow 940）
- **Block 指令**：设置 Block Bit，Picker 不再选择该 Color
- **Unblock 指令**：清除 Block Bit，Color 重新可被调度
- 用途：实现任务间依赖（等待前序任务完成）

## CE 内部 Color 状态

Compute Element（CE 800）为每个 Color 维护：

| 组件 | 功能 |
|------|------|
| Input Queues（897） | 每个 Fabric Color + Local Color 各一个虚拟/物理队列 |
| Active Bits（898） | 该 Color 队列是否有 wavelet 等待 |
| Block Bits（899） | 该 Color 是否被软件 block |
| Scheduling Info（896） | 管理所有 Color 的调度状态，向 Router 发送 stall 信息 |

## 反压（Backpressure）机制

Color 粒度的独立反压：

1. **CE 侧**：当某 Color 的 Input Queue 超过阈值（如 capacity-2），向 Router 发 stall
2. **Router 侧**：当某 Color 的 Data Queue 满或下游 stall，向邻居 Router 反向传播 stall
3. **上游 Router**：收到 stall 后停止该 Color 的数据发送，形成**分布式 in-fabric queue**
4. **Output Queue 侧**：CE 检测某 Color 的 Output Queue 满，stall 该 Color 的处理

关键特性：
- 反压**按 Color 独立**传播，不同 Color 互不影响
- Inflight 数据在 stall 时被第二个 entry 捕获，不丢失
- 每周期检查 queue 深度变化（接收+消费），动态响应

## 软件控制接口

Data Structure Descriptor 中与 Color 相关的字段：
- **AC（Activate Color）**：收到 wavelet 时激活对应 Color
- **SC（Specified Color, Normal Mode）**：指定 Color 模式
- **CH（Color, High Bits）**：Color 高位
- **Push/Pop (Activate) Color**：FIFO 操作时激活对应 Color

## 设计哲学总结

| 维度 | 设计 |
|------|------|
| 路由 | 静态固定，编译时确定，运行时零开销 |
| 复用 | 16+ 虚拟网络共享一套物理线路 |
| 隔离 | 每 Color 独立缓冲+独立反压，互不阻塞 |
| 计算映射 | Color 直接编码为指令地址偏移（Color×4），驱动任务选择 |
| 多播 | 静态配置，硬件级复制，支持高扇出 |
| 拥塞 | 单 Color 无拥塞（单源），Color 间竞争物理通道 |
| 可编程性 | Block/Unblock 实现任务依赖，Active/Inactive 控制就绪状态 |

## 与其他系统的对比

- vs [传统 NoC VC](/concepts/noc-router-microarchitecture.md)：传统 VC 用于避免死锁和 QoS，Color 同时驱动路由+任务调度
- vs [UB 16 VL](/concepts/ub-data-link-layer.md)：UB VL 是传输层抽象，Color 是物理+计算层联合抽象
- vs [Groq C2C](/entities/nvidia-groq-3-lpx.md)：Groq 用 plesiosynchronous 确定性，Color 用静态路由确定性，异曲同工

## 相关页面
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — checkerboard pass 自动 color 分配
- [Cerebras Wse](/entities/cerebras-wse.md) — Color 所在的晶圆级加速器
- [Deterministic Execution](/concepts/deterministic-execution.md) — Color 静态路由是确定性执行的物理实现
- [Noc Router Microarchitecture](/concepts/noc-router-microarchitecture.md) — Color 路由器的 NoC 理论基础
- [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md) — Color 与 VC 语义对照（Day 16）
- [Æthereal NoC](/concepts/aethereal-noc.md) — TDM slot 预约 vs Color 静态配置（对照）
- [Switching Principles](/concepts/switching-principles.md) — 电路交换 vs 分组交换，Color 本质是电路交换思想

# Citations

[1] [US10515303B2](US10515303B2)
[2] [raw/papers/Near-optimal_wafer-scale_reduce.pdf](raw/papers/Near-optimal_wafer-scale_reduce.pdf)
