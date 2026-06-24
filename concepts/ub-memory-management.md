---
type: Concept
title: UB 内存管理
description: UB 内存管理：Home-User 模型、UBMD、UMMU 两阶段地址翻译+权限检查、UB Decoder
tags:
- interconnect
- scale-up
- memory
- hardware
- virtualization
timestamp: '2026-05-09T00:00:00Z'
created: 2026-05-09
sources:
- raw/articles/UB-MEM.md
---

# UB 内存管理

[Unifiedbus Ub](/entities/unifiedbus-ub.md) §9 Memory Management。定义了跨 UBPU 的内存共享、地址翻译和权限验证机制。

## 核心设计目标

- **全局统一内存描述**：UBMD (UB Memory Descriptor) 全局唯一标识内存段
- **Home-User 访问模型**：Home 拥有物理内存，User 通过 UBMD 访问
- **UMMU**：Home 端地址映射 + 权限检查，可安全委托给非特权软件
- **UB Decoder**：User 端门户，将本地 PA 翻译为 UBMD

## Home-User 访问模型

```
User (发起方)                           Home (内存拥有方)
    │                                        │
    │  UBMD {EID, TokenID, UBA}              │
    ├─────────── Memory Access Request ──────→│
    │                                        │ UMMU: UBMD → PA + 权限验证
    │                                        │
    │←────── Response ───────────────────────┤
```

User 获取 UBMD 的两种方式：
1. **UB Decoder**：从 PA 查表获得 UBMD（Load/Store 同步访问路径）
2. **编程接口**：用户通过 URMA API 提供 UBMD（异步访问路径）

## UBMD (UB Memory Descriptor)

| 字段 | 说明 |
|------|------|
| **EID** | 标识目标内存所属 Entity |
| **TokenID** | 标识 UBA 空间及其权限集 |
| **UBA** | 64-bit 虚拟地址，Home 提供给 User 用于访问 |

UBA 空间 = 一组 UBA → Home 端 PA 的映射集合。

## UMMU (UB Memory Management Unit)

Home 端核心组件，处理内存访问的 4 步流程：

### 处理流程

```
UBMD → ① 配置查找 → ② 上下文查找 → ③ 地址翻译 → ④ 权限检查 → PA
```

### ① 配置查找 (Configuration Lookup)

查找 **TECT (Target Entity Configuration Table)**，基于 EID 索引，获取 TECTE。

TECTE 关键字段：
- **ST_MODE**：地址翻译阶段模式（仅 S1 / 仅 S2 / S1+S2 / 禁用）
- **MAPT_EN**：是否启用权限检查
- **MEM_ATTR_SEL**：内存属性选择机制
- **SECURE_SEL / PRIV_SEL / INST_SEL**：安全/特权/指令属性覆写
- **S2_VMID**：Stage 2 虚拟机标识
- **TCT_PTR / TCT_NUM / TCT_FMT**：上下文表指针、大小、格式
- **S2_MATT**：Stage 2 地址翻译表基址（Secure / Non-Secure 各一份）
- **MTM_ID / MTM_GP**：内存流量监控标识

### ② 上下文查找 (Context Lookup)

基于 TokenID 查找 **TCT (Target Context Table)**，获取 TCTE。

TCT 支持两种格式：
- **Linear TCT**：直接用 TokenID 索引连续 TCTE
- **Two-level TCT**：L1 TCT (TokenID 高位索引) → L2 TCT (TokenID 低 6 位索引)，支持更多 TokenID

TCTE 关键字段：
- **MATTBA**：Stage 1 地址翻译表基址
- **SZ / TGS**：UBA 最大位数 / 翻译粒度
- **MAPT_MODE**：权限表模式（单条目 / 多级）
- **MAPT_BBA / MAPT_BTA**：权限表基块地址 / 权限块表地址
- **HAF / HDF**：硬件自动更新 Access/Dirty 标志
- **MATTWD**：禁用 MATT walk（TLB miss 直接报事件）
- **GPAS**：Guest PA 大小（32/36/40/42/44/48 bit）

### ③ 地址翻译 (Address Translation)

支持**两阶段翻译**（虚拟化场景）：

```
UBA ──[Stage 1: MATT]──→ IPA ──[Stage 2: MATT]──→ PA
```

| 模式 | ST_MODE | 说明 |
|------|---------|------|
| 仅 S1 | 3'b101 | UBA → PA（非虚拟化） |
| 仅 S2 | 3'b110 | UBA 直接做 IPA → PA |
| S1+S2 | 3'b111 | UBA → IPA → PA（虚拟化） |

S1 翻译信息在 TCTE，S2 翻译信息在 TECTE。S1 翻译每级前需对 MATT 基址做 S2 翻译。

具体 MATT 数据结构由 UBPU 架构定义（类似 ARM SMMU 的页表 walk）。

### ④ 权限检查 (Permission Check)

基于 **MAPT (Memory Address Permission Table)** 查找权限信息，与访问请求中的信息比对。

#### MAPT 两种模式

**单条目 MAPT**：
- 直接通过 TCTE.MAPT_BBA 获取唯一 UMAPTE
- 包含 UBA 范围 (Base/Limit) + 权限位 + TokenValue

**多级 MAPT**（支持 4KB / 2MB 两种粒度）：
- 4KB 粒度：最多 4 级（L0 用 UBA[47:39], L1 用 UBA[38:30], L2 用 UBA[29:21], L3 用 UBA[20:12]）
- 2MB 粒度：最多 3 级
- 每级 MAPTE 包含 UBA 范围，匹配则检查权限，不匹配且 T=0 则继续下一级，T=1 则终止

#### 权限检查项

| 检查项 | 说明 |
|--------|------|
| **TokenValue** | 双 TokenValue（primary + secondary），匹配任一即通过。支持 Positive PLB 优化 |
| **E_Bit (Exclusive)** | 两层检查（TCTE + MAPTE），exclusive 请求总是通过，非 exclusive 遇到 exclusive 目标被拒 |
| **Access Type** | Read/Write/Atomic 位图，对应位置 1 表示允许 |
| **MATT 权限** | 地址翻译过程中的权限也参与最终判定 |

#### MAPT 安全委托

- MAPT **可由非特权软件直接管理**，但操作范围限于 MAPT base block
- 特权软件分配 MAPT 物理内存并映射到非特权软件虚拟地址
- 该内存不会被 swap out，避免 page fault
- 非特权软件访问不得超出 MAPT block 大小

## UB Decoder (User 端)

User 端将本地 PA 翻译为 UBMD 的组件。

### PA → UBMD 翻译

两级页表查找：

```
PA → L0 Page Table (PA[43:35] 索引)
       ├── L0 PTE (8 个/64B bulk) → PA[34:32] 选一个 → L1 PT
       └── L0 PTRE (范围条目) → 检查 PA[34:20] 是否在范围
              ├── 在范围内 → 直接获得 UBA
              └── 不在范围内 → L1 PT (PA[34:20] 索引)

L1 Page Table → L1 PTE → UBA 计算
```

### UBA 计算

```
UBA = UBA_BASE:12'b0 + 29'b0:PA[34:0]
```

## 与其他架构对比

| 特性 | UB UMMU | ARM SMMU | Intel VT-d |
|------|---------|----------|------------|
| 两阶段翻译 | ✅ S1+S2 | ✅ S1+S2 | ❌ 单阶段 |
| 权限表独立 | ✅ MAPT 独立于 MATT | ❌ 权限嵌入页表 | ❌ 权限嵌入页表 |
| 非特权软件管理 | ✅ MAPT 安全委托 | 部分 | ❌ |
| 全局内存描述 | UBMD (EID+TokenID+UBA) | StreamID+SubstreamID | PASID |
| 双 TokenValue | ✅ primary + secondary | ❌ | ❌ |

UB 的 MAPT 独立于 MATT 是独特设计——权限和地址翻译解耦，允许更灵活的权限管理（非特权软件可管理权限表而不影响地址翻译）。

## 与 Wiki 其他页面的关联

- [Unifiedbus Ub](/entities/unifiedbus-ub.md) — UB 整体架构
- [Ub Programming Models](/concepts/ub-programming-models.md) — 内存段的创建/使用/访问方式
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — UB 内存池化与解耦推理的内存共享理念类似
- [Switching Principles](/concepts/switching-principles.md) — UMMU 的地址翻译本质上是一种"交换"（UBA → PA 空间映射）

## 来源

- UB Base Specification Rev 2.0, §9 Memory Management

# Citations

[1] [raw/articles/UB-MEM.md](raw/articles/UB-MEM.md)
