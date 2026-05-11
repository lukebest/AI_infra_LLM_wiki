---
title: UB 物理层机制
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [interconnect, scale-up, fabric, physical-layer, serdes, fec, link-training]
sources: [raw/articles/UB-PHY-ch3.md]
---

# UB 物理层机制

[[unifiedbus-ub]] 协议栈物理层（§3），由 PCS（物理编码子层）、PMA（物理介质附件）、链路状态管理三部分组成。核心功能：FEC 编解码、加扰、链路训练、均衡协商、动态模式切换。

## 端口/通道/链路模型

- **Port** = 1 TX + 1 RX，全双工
- **Lane** = 一对高速差分信号线
- TX/RX 各支持 x1/x2/x4/x8 lanes
- **非对称链路**：TX 和 RX lane 数可不同（系统初始化时配置）
- 支持电互联和光互联

## 双物理层模式

| | PHY Mode-1 | PHY Mode-2 |
|---|-----------|-----------|
| 数据速率 | 4.0 Gbit/s 或自定义 | 2.578125 / 25.78125 / 53.125 / 106.25 Gbit/s |
| 调制 | NRZ (4.0) / NRZ+PAM4 (自定义) | NRZ (低速) / PAM4 (高速) |
| 最大速率/lane | 118 Gbit/s | 106.25 Gbit/s |
| 最大插损 | 背板 40dB / DAC 42dB | 同左 |

## PCS（物理编码子层）

### FEC（前向纠错）

**RS(128, 120)** 编码，有限域 GF(2^8)：
- **T=4 模式**：纠正 4 个 symbol 错误（默认）
- **T=2 模式**：纠正 2 个 symbol 错误（低延迟）
- 两种模式生成 8 个 parity symbol（T=2 仅用前 4 个校正，后 4 个验证）
- 本原多项式：x^8+x^4+x^3+x^2+1
- FEC bypass 模式：跳过编码/解码

**FEC 交织**：
- 单编码器（non-interleaved）或双编码器（interleaved）
- 交织模式将两个 FEC 编码器的 output 交替分布到各 lane

### 加扰

- Per-lane additive scrambling
- Seed 从 AMCTL 中的 Lane ID 获取
- EEIB 和 AMCTL 不加扰；LTB 和数据必须加扰

### Gray 编码（PAM4 必需）

PAM4 四电平映射：00→Level 0, 01→Level 1, 10→Level 2, 11→Level 3（Gray 编码后）
- 确保相邻电平误判只产生 1-bit 错误

### Precoding

- NRZ：Tn = Pn ⊕ Tn-1（XOR）
- PAM4：Tn = (Pn - Tn-1) mod 4
- 防止突发错误传播

### AMCTL（对齐标记控制）

40-symbol 结构，独立于 FEC，使用 **eBCH-16** 编码保护：
- 检测 7-bit 错误，纠正 3-bit 错误 + 部分 4-bit 错误
- Hamming 距离 8，32 个合法 codeword

**AMCTL 结构**：
| 字段 | 符号 | 功能 |
|------|------|------|
| BODY | 0–11 | CW21+CW28 重复 3 组，辅助锁定 |
| END | 12–15 | CW22 重复 2 组，标识 AMCTL 边界 |
| LID | 16–23 | Lane ID（scrambling seed + lane 重排） |
| CTRL_TYPE | 24–31 | 控制命令类型 |
| CTRL_DETAIL | 32–39 | 控制命令参数 |

**控制命令**：FEC 开关、Link Width 切换（x0/x1/x2/x4/x8）、EEI（电气空闲）、AMCTL 插入周期控制、远端 TX 宽度切换指示

**AMCTL 锁定过程**：`Lock_Init → AMCTL_Slip → AMCTL_Align → AMCTL_Confirm → AMCTL_Lock → AMCTL_Lock_Count`

### 低功耗机制

无数据时 PCS 可关闭 FEC + scrambling，发送 PRBS23 流保持远端 CDR 锁定。通过 AMCTL FEC Control 命令协调开关。

## PMA（物理介质附件）

- 并行→串行转换 + CDR（时钟数据恢复）
- TX：pre-emphasis + 均衡 → 补偿高频损耗 + 降低 ISI
- 介质无关接口，支持多物理链路
- PAM4 必须经过 Gray 编码和 precoding

## 链路状态管理（LMSM）

### LMB（链路管理块）

16-symbol 块，所有 active lane 同时发送相同内容：

| LMB 类型 | 功能 |
|---------|------|
| **DLTB** (Discovery) | 锁定 symbol、交换初始化信息、TX/RX link width、广播数据速率/FEC 支持 |
| **CLTB** (Config) | 协商均衡模式、FEC 模式 |
| **RLTB** (Retrain) | 切换数据速率、调整 link width、链路错误恢复 |
| **EEIB** (Exit Electrical Idle) | 低频 pattern 通知远端退出电气空闲 |

### LMSM 状态机

```
Link_Idle → Probe → Discovery → Config → Send_NullBlock → Link_Active
                          ↑                                  ↓
                          ← Retrain ← Change_Speed ← Equalization
```

| 状态 | 功能 | 关键动作 |
|------|------|----------|
| **Link_Idle** | 初始态，所有 TX lane 电气空闲 | 初始化变量（Tx_M, Rx_N, LinkUp=0） |
| **Probe** | 检测远端 RX 是否存在 | 发检测脉冲，确定初始 link width + lane 0 位置 |
| **RXEQ_Optimize** | 固定速率模式 RX 均衡自适应 | 仅 fix_data_rate_mode 时进入 |
| **Discovery** | 交换链路能力，协商 link width | 端口类型协商（随机数比较）、lane reversal/polarity、广播数据速率支持 |
| **Config** | 协商 FEC 模式 + 均衡模式 | 三步握手 Active→Check→Confirm |
| **Send_NullBlock** | 验证链路可传数据 | AMCTL with SDF + null block 交换 |
| **Link_Active** | 正常工作态 | LinkUp=1，可传 flit |
| **Retrain** | 速率/宽度/FEC 模式切换 | Active→Confirm→Change_Speed/Equalization |
| **Change_Speed** | 物理切换数据速率 | TX 电气空闲 → 切换 → 回 Retrain.Active |
| **Equalization** | TX/RX 均衡参数调优 | Coarsetune → Passive/Active 交互 |

### QDLWS（快速动态链路宽度切换）

不中断服务数据的 link width 切换：
- **增 lane**：数据链路层 LM block 协商 → 新 lane 发 RLTB → 远端确认 → AMCTL 切换
- **减 lane**：类似反向过程，空闲 lane 进入电气空闲
- **快速降级**：RX 检测 lane 错误 → 通过 AMCTL Remote TX Link Width Switch 指示远端直接降宽（无需 Retrain）

### 数据速率协商

- 从 Data Rate 0 开始训练
- Discovery 阶段广播所有支持速率
- Retrain→Change_Speed 切换到共同最高速率
- 光链路模式固定速率，跳过速率协商

### 均衡模式

| 模式 | 说明 |
|------|------|
| **Skip_EQ** | 直接切到最高速率，不均衡（已存储参数） |
| **Only_Highest_Data_Rate_EQ** | 直接切到最高速率，仅在该速率均衡 |
| **Full_EQ** | 逐级切换速率，每级都均衡 |

均衡过程：Primary/Secondary 角色分工 → Coarsetune 粗调 → Active（请求端发送 preset/系数）+ Passive（响应端应用并确认）→ 24ms 内完成

### FEC/CRC 模式动态切换

- Link_Active 状态测量 pre-FEC BER
- 进入 Retrain 协商匹配当前 BER 的 FEC/CRC 模式
- FEC 和 CRC 可独立或同时切换

## RX 处理链路

1. **AMCTL 锁定**：检测 END → slip 对齐 → 连续确认 → 锁定
2. **Lane 对齐**：基于 AMCTL.SDF 消除 lane 间 skew
3. **Lane 重排**：AMCTL.LID 标识物理 lane 位置
4. **解交织**：分配到 FEC 解码器
5. **FEC 解码**：纠正 ≤T 个 symbol 错误；超出 → 报告失败
6. **链路质量监控**：FEC error counter → hi_FEC_BER 标志 → 触发 FEC 模式切换

## 与其他协议对比

| 特性 | UB | InfiniBand | PCIe 6.0/7.0 |
|------|-----|-----------|-------------|
| FEC | RS(128,120,T=2/4) | RS(528,514) / RS(272,257) | RS(28,24) + CRC |
| 调制 | NRZ + PAM4 | NRZ | NRZ + PAM4 (Flit mode) |
| 链路宽度 | x1/x2/x4/x8 非对称 | x1/x4/x12 非对称 | x1/x2/x4/x8/x16 对称 |
| 动态宽度切换 | QDLWS（不中断数据） | 不支持 | 不支持 |
| 最大速率/lane | 118 Gbit/s | 200 Gbit/s (XR) | 128 GT/s (PCIe 7.0) |
| 均衡 | 3 模式可选 + 动态协商 | 静态/自适应 | Preset + Coefficient |
| AMCTL 保护 | eBCH-16（纠 3-bit） | 无独立 AM 保护 | 无 |
| 低功耗 | PRBS23 保持 CDR | 类似 | L0s/L1 |

## 协议栈关联

- [[ub-data-link-layer]] — 物理层直接服务的数据链路层（FEC/CRC 模式切换由数据链路层协调触发）
- [[unifiedbus-ub]] — UB 协议整体架构（§3 物理层是协议栈最底层）

## 来源

- UB Base Specification Rev 2.0, §3 Physical Layer（完整章节）
