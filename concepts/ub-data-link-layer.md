---
title: UB 数据链路层机制
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [interconnect, scale-up, fabric, data-link, flow-control, retransmission]
sources: [raw/articles/UB-DL-ch4.md]
---

# UB 数据链路层机制

[[unifiedbus-ub]] 协议栈数据链路层（§4），位于物理层与网络层之间。提供可靠的、保序的、点到点包传输。核心功能：封装/解析、CRC 校验、VL 虚通道、Credit 流控、点到点重传。

## 链路状态机

| 状态 | 说明 | 上报网络层 |
|------|------|-----------|
| **DLL_Disabled** | 初始/复位态，物理层未就绪 | Status_Down |
| **DLL_Param_Init** | 物理层 LinkUp，交换 Init Block 协商参数 | Status_Down |
| **DLL_Credit_Init** | 参数协商完成，交换 Crd_Ack Block 初始化 credit | Status_Down |
| **DLL_Normal** | 正常通信，发送/接收 DLLDP + DLLCB | Status_Up |

Entity 复位不触发 DLL_Disabled；仅物理层 LinkUp==0 触发。

## 包格式体系

### 基本单元
- **Flit** = 20 字节（不可分割的物理传输单元）
- **DLLDP**（数据包）：1–512 flits，分 1–16 个 DLLDB（每个 DLLDB ≤ 32 flits）
- **DLLCB**（控制块）：1–32 flits，不可插入 DLLDB 中间

### 双封装模式

| | CRC 模式 | Non-CRC 模式 |
|---|---------|-------------|
| 校验 | BCRC（CRC-30）per DLLDB | END 字段（仅尾部） |
| 物理层 FEC | 可选 | **必须启用** |
| 检错触发 | FEC 失败 **或** CRC 失败 → 重传 | 仅 FEC 失败 → 重传 |
| 延迟 | 略高（CRC 计算） | 更低 |
| 切换 | 由物理层发起 BER 检测 → Block_Mode_Chg Block 协调切换 |

### LPH（链路包头）
4 字节，首个 DLLDB 的首个 flit：`CRD(1) | ACK(1) | CRD_VL(4) | VL(4) | CFG(4) | RT(2) | PLENGTH(14)`

关键字段：
- **CRD/ACK**：credit 返回 + retry buffer 释放标志
- **CFG**：0=DLLCB, 3/4/5/6/7/9=DLLDP（上层定义）
- **PLENGTH**：14-bit 编码 DLLDB 数量 + 最后 DLLDB flit 数 + payload 边界

### LBH（链路块头）
2 字节，中间/最后 DLLDB 的首个 flit。结构与 LPH 类似但更紧凑。

### BCRC
每个 DLLDB 尾部：CRC-30 + ERROR_FLAG(1) + Reserved(1)。CRC 多项式：x^30+x^28+x^26+...+1。

### DLLCB 类型

| 类型 | CTRL/SUB_CTRL | 功能 | 平面 |
|------|--------------|------|------|
| Null Block | 0000/0000 | 链路空闲填充 | 数据 |
| No_Operation Block | 0000/0001 | 小包节流（满足 PACKET_MIN_INTERVAL） | 数据 |
| Retry_Idle Block | 0001/0000 | 隔离 Retry_Req/Ack 与 DLLDP | 数据 |
| Retry_Req Block | 0001/0001 | 重传请求（携带 RcvPtr） | 数据 |
| Retry_Ack Block | 0001/0010 | 重传确认（携带 RdPtr/WrPtr/NumFreeBuf） | 数据 |
| Crd_Ack Block | 0010/0100 | Credit 返回 + ACK 返回 | 数据 |
| Param_Exchg Block | 0011/0000 | 邻居通告（网络层信息交换） | 控制 |
| Lane_Manage Block | 0100/0001 | 动态 lane 增减（X1/X2/X4/X8） | 控制 |
| Block_Mode_Chg Block | 0101/0000 | CRC ↔ Non-CRC 模式切换 | 控制 |
| Init Block | 1100/1000 | 初始化参数协商（5–32 flits） | 控制 |

## 初始化自协商

DLL_Param_Init 状态下交换 Init Block，协商以下参数（取两端支持的**最小交集**）：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| DATA_CREDIT_GRAIN_SIZE | DLLDP 中 CRD 字段返回 credit 粒度（per VL） | 4 cells |
| CTRL_CREDIT_GRAIN_SIZE | Crd_Ack Block CRD_NUM 返回 credit 粒度（per VL） | 1 cell |
| FEATURE_ID | 协议版本 | 1 |
| RXBUF_VL_SHARE | 接收端 buffer 是否支持 VL 共享 | 不共享 |
| DATA_ACK_GRAIN_SIZE | DLLDP ACK 返回粒度 | 32 flits |
| CTRL_ACK_GRAIN_SIZE | Crd_Ack ACK_NUM 返回粒度 | 1 flit |
| FLOW_CTRL_SIZE | 1 cell = ? flits | 8 flits |
| VL_ENABLE | 启用哪些 VL（VL0 必须启用） | VL0 only |
| RETRY_BUF_DEPTH | 重传 buffer 深度 | 直接采用对端值 |
| PACKET_MIN_INTERVAL | 连续 DLLDP 最小间隔 | 直接采用对端值 |

协商失败 → 使用默认值。

## VL 机制

- 每条点到点链路最多 **16 个 VL**（Virtual Lane）
- 同一 DLLDP 的所有 DLLDB 走同一 VL
- 同 VL 内 FCFS；跨 VL 调度由实现决定
- DLLCB 不消耗 credit，不需要指定 VL
- 与 [[ub-network-layer|网络层]] SL→VL 映射配合实现端到端 QoS

## Credit 流控

### 基本模型
- 接收端按 VL 分配 credit 给发送端
- 发送端维护 per-VL credit 计数器：发送扣减，收到 credit 返回增加
- **Cell** 为最小单位：1 cell = n flits（n ∈ {1,2,4,8,16,32,64,128}，协商确定）
- 最大 credit 数：65535 cells
- DLLDP 消耗 credit = ⌈flits / flits_per_cell⌉

### Exclusive 模式
- 每个 VL 独占固定 credit，互不共享
- 简单可预测

### Sharing 模式
- 所有 VL 共享 SHARE_CRD 池 + 每个 VL 有最低 exclusive credit 保底
- 发送时优先使用共享 credit，不足时用 exclusive credit
- credit 返回时全部归入 SHARE_CRD，然后检测各 VL exclusive credit 是否低于阈值并补充
- 更高 buffer 利用率，适合流量不均匀场景

### Credit 返回途径
1. **DLLDP 内嵌**：LPH/LBH 的 CRD 字段（粒度 DATA_CREDIT_GRAIN_SIZE）
2. **Crd_Ack Block**：CRD_NUM 字段（粒度 CTRL_CREDIT_GRAIN_SIZE）
3. **阈值触发**：待返回 credit 达阈值 → 反压 + 强制发 Crd_Ack Block

## 重传机制

### Go-Back-N
- 接收端检测 CRC/FEC 错误 → 发 Retry_Req_Set（1 Retry_Idle + 32 Retry_Req）
- 发送端从 RcvPtr 开始重传所有后续 flit
- Retry Buffer：发送端缓存已发未确认的 flit

### Retry Buffer 管理
- **NumFreeBuf**：空闲空间
- **WrPtr**：最新写入位置
- **TailPtr**：最早未确认位置
- **RdPtr**：重传读取位置
- **RcvPtr**：接收端期望位置（对端 buffer 中的偏移）

### 双状态机

**RETRY_REQ_SM（接收端）**：
`NORMAL → REQ → WAIT → RETRAIN → ERROR`
- NORMAL 检测错误 → REQ 发 Retry_Req_Set → WAIT 等 Retry_Ack_Set
- 超时 → 回到 REQ 重试（NUM_RETRY++）
- NUM_RETRY 达阈值 → RETRAIN（触发物理层 retrain）
- NUM_PHY_REINIT 达阈值 → ERROR（需 UBFM 复位）
- 推荐：NUM_RETRY_THRESHOLD=15, NUM_PHY_REINIT_THRESHOLD=4

**RETRY_ACK_SM（发送端）**：
`NORMAL ↔ ACK`
- 收到 Retry_Req_Set → ACK 态，发 Retry_Ack_Set + 重传 flit → 回 NORMAL

### Retry Buffer 死锁预防
高误码率下两端 retry buffer 可能互锁（都满，无法发 ACK）。解决方案：NumFreeBuf < 阈值时停止发 DLLDP/其他 DLLCB，优先发 Crd_Ack Block 释放对端 buffer。

## 异常处理

| 异常 | 处理 |
|------|------|
| 接收 buffer 溢出 | 上报错误，等 UBFM 复位 |
| Credit 溢出 | 上报错误，等 UBFM 复位 |
| Credit 返回超时 | 上报错误，等 UBFM 复位 |
| Retry ACK 超时 | 自动重试 → retrain → ERROR |
| ERROR_FLAG 包 | 正常上传，在完整 DLLDP 处丢弃 |

## 封装模式切换流程

CRC ↔ Non-CRC 通过 Block_Mode_Chg Block 协调：
1. 物理层发起（BER 触发或软件请求）
2. 本端反压网络层 → 发 Block_Mode_Chg_REQ → 对端反压 → 发 Block_Mode_Chg_REQ
3. 双端 flush 待发 ACK → 发 Block_Mode_Chg_ACK
4. 物理层 retrain → 新模式生效 → 解除反压

## 与其他协议对比

| 特性 | UB | InfiniBand | PCIe |
|------|-----|-----------|------|
| 基本传输单元 | Flit (20B) | Flit (可变) | TLP |
| VL 数量 | 16 | 16 | 8 TC |
| 流控 | Credit-based per VL | Credit-based per VL | Credit-based per VC |
| 重传 | Go-Back-N + retry buffer | Go-Back-N | 重试机制不同 |
| 封装模式 | CRC / Non-CRC 动态切换 | 固定 CRC | 固定 LCRC/ECRC |
| Lane 管理 | 动态 X1/X2/X4/X8 | 静态宽度 | Link width 可配 |
| 链路初始化 | 4 阶段状态机 | 类似多阶段 | LTSSM |

## 来源

- UB Base Specification Rev 2.0, §4 Data Link Layer（完整章节）
