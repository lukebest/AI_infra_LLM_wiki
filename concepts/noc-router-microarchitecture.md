---
type: Concept
title: NoC Router 微架构
description: NoC Router 微架构：链路级流控/EB/credit、Switch/仲裁器（RR/2D 矩阵）、WH/VC 流水线 Router、VA/SA
  分配器优化
tags:
- noc
- routing
- flow-control
- arbitration
- router
- switch
- virtual-channel
- wormhole
- credit
timestamp: '2026-05-14T00:00:00Z'
created: 2026-05-14
sources:
- raw/articles/片上网络Router的微架构---设计师视角.md
- raw/papers/Near-optimal_wafer-scale_reduce.pdf
- raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf
---

# NoC Router 微架构

片上网络 Router 的完整设计方法论：从链路级流控到 VC-based 流水线 Router 的电路级描述。来源为设计师视角的系统教材，覆盖 9 大主题。

## 1. NoC 基础

### 物理媒介
- 片上导线组织在多层金属中：低层高密度短距离，高层低阻长距离
- 2.5D/3D 封装提供 TSV 跨 chip 连接
- 片上光互联尚在研究中

### 协议分层
- **事务层**：读写操作（如 AXI），端到端语义，不约束实现
- **传输层**：NI 封装事务为 packet（header + payload），request/response 分离避免死锁
- **网络层**：Router 负责路由、仲裁、竞争处理

### 核心问题
- **连接性**：任意 IP core 可交换信息
- **竞争**：共享 channel 需要仲裁/mux/buffer

## 2. 链路级流控与 Buffer

### Elastic Buffer (EB)
- **HBEB**（半带宽）：1-slot 寄存器 + RS 触发器，每拍只能 push 或 pop，引入气泡
- **2-slot EB**：时分复用实现全带宽，隔离上下游 valid/ready 时序
- **PEB**（pipelined EB）：写端口并行性，引入 ready 组合环路
- **BEB**（bypass EB）：读端口并行性，引入 data bypass 组合逻辑

### Credit-based 流控
- 将 slot counter 放在发送方，发送方显式追踪 credit
- 流水线链路中：EB 替换打拍寄存器可显著降低 buffer 开销（从 $N_f + N_b$ 降至 max($N_f$, $N_b$) + 1）
- Credit-based 下保证满吞吐所需 buffer 深度 = RTT

### 宽消息传输
- **Virtual Cut Through (VCT)**：下游须容纳整个 packet
- **Wormhole (WH)**：下游只需一个 flit，buffer 开销低

### req-ack 与无 buffer 流控
- 乐观发送 + ack/nack 重传
- Bufferless 流控：接收方直接丢弃，上层协议重传（设计复杂度高）

## 3. Switch 模块与 Router

### 多对一 / 一对多 / 多对多
- **outAvailable / outLock** 信号控制 packet 级锁定
- Credit-based 流控下每个输出端口需要 credit counter
- **Unroll datapath**：每个输出端口独立仲裁器 + mux，满带宽

### 头阻（Head-of-Line Blocking）
- 核心性能瓶颈：同一输入端口的不同目的 flit 被阻塞
- N×N switch 单输出吞吐量理论极限：$1-(1-1/N)^N$，N→∞ 趋近 0.63
- 只能通过 VC（允许并发多 flit）缓解

### 路由计算 (RC)
- 查找表实现：根据 head flit 地址计算输出端口
- **前瞻路由 (LRC)**：在前一跳并行计算下一跳路由，消除 RC 串行延迟

### 层次化 Switch
- 2:1 仲裁器级联，适用于 XY 路由等规则拓扑，可选择性裁剪资源

## 4. 仲裁逻辑

### 固定优先级 (FPA)
- 静态优先级，二叉树结构实现并行 grant 生成

### Round-Robin (RR)
- 每次仲裁后最高优先级转移至相邻端口
- HP/LP 分区实现：HP 内 FPA + LP 内 FPA，HP 空时才查 LP

### 2D 优先级矩阵仲裁器
- $N \times N$ 矩阵表示端口间优先级关系（$m_{ij}=1$ 表示 i 优先于 j）
- 不同更新策略：
  - **Least Recently Granted**：授权后置最低
  - **Most Recently Granted**：授权后置最高
  - **Incremental RR**：最高优先级周期性递降
  - **Hybrid FCFS+LRU**：新请求优先，授权后置最低

## 5. 流水线 Wormhole Router

### 单周期 Router
- 三阶段：RC → SA → ST（+ CC/SU 并行）
- Control path 关键路径：RC→SA→grant→ST
- Data path：input buffer mux + crossbar

### 流水线优化
| 阶段 | 仅控制路径 | 控制路径 + EB |
|------|-----------|--------------|
| RC | 有气泡 | 无气泡 |
| SA | grant 打拍引入气泡 | 输入侧 EB 对齐消除 |
| RC+SA | 2+ 气泡 | 全流水无气泡 |

- **RC 截断无气泡**：添加 1-slot EB 对齐数据
- **SA 非头 flit 优化**：body/tail 继承已有 grant，减少一拍

## 6. VC 流控与缓冲

### 动机
- 解决 WH 的 HOL blocking 和协议死锁（如 MOESI 需 3 个虚拟网络）
- 流量隔离、提高链路利用率

### VC Buffer
- 简单实现：每 VC 独立 EB + arbiter（buffer 浪费严重）
- **共享 buffer**：私有 buffer + 共享 buffer，链表维护 flit 顺序
- **ElastiStore**：V 个 VC 只用 V+1 个 buffer（节省面积但拥塞时限带宽）

### 流水线链路中 VC
- Valid/ready 寄存器 slice：每个 VC 需保留 $N_f + N_b$ 深度 buffer
- Credit-based：每 VC 私有 buffer 深度 1 即可安全运行 → **现代 VC 设计默认 credit 流控**

## 7. VC-based Switch 与 Router

### 关键状态变量
- 输出端口：每 VC 一个 credit counter + outAvailable[VC]
- 输入端口：每 VC 维护 outVCLock / outVC

### VC 分配器 (VA)
- **VA1**（per input VC）：V:1 仲裁，选择一个候选 output VC
- **VA2**（per output VC）：N×V:1 仲裁，选择一个 input VC
- 两级分离：input 独立选 VC → output 端冲突消解

### Switch 分配器 (SA)
- **SA1**（per input）：local 仲裁选择哪个 VC 出去
- **SA2**（per output）：input-to-output 映射

### Wavefront 分配器
- 集中式 N×N 矩阵分配，对角线扫描，行/列互斥

## 8. 高速分配器优化

### 虚拟网络降复杂度
- 禁止跨虚拟网络 VC 变换 → VA 拆分为独立小 VA → VA1 可完全消除

### 组合分配器（省 VA2）
- VA1 输出给 SA1 → SA2 顺带完成 VA2 功能
- **并行组合**：VA1 与 SA1 并行执行（VA1 结果在 SA2 才使用）

### 预测 SA (Speculative SA)
- SA 和 VA 并行执行，4 种结果：双失败 / VA 成 / SA 成 / 双成
- **预测失败**（SA 成但 VA 失败）：需引入气泡重试
- 引入两个独立 SA 降低预测失败代价

### Input-Speedup
- 多个 VC 直接连 crossbar，提高分配效率
- 极端情况：禁止跨 VC + 最大 input speedup → VA 完全消除

## 9. 流水线 VC-based Router

### 4 级流水线
- RC → VA → SA → ST（各阶段可独立打拍）

### 气泡问题
- RC/SA 可通过 EB 消除气泡
- **VA 不能用 EB**：两个 packet 连续到达同一 input VC → 可能死锁（tail 未发但 head 已获 output VC → 循环依赖）
- VA 气泡在以下场景出现：连续 packet 到同一 input VC + 去同一 output VC

### 常见流水线组织
| 组织 | 气泡源 | 延迟 |
|------|--------|------|
| RC/VA/SA-ST | VA | 3 cycles |
| RC-VA/SA/ST | VA | 3 cycles |
| RC/VA/SA/ST | VA | 4 cycles |

## 与 Wiki 其他概念的关系

- **[Switching Elements](/concepts/switching-elements.md)**：Router 是交换单元在片上的具体实现，空分交换 ↔ crossbar，时分交换 ↔ 共享 buffer
- **[Switching Networks](/concepts/switching-networks.md)**：CLOS 多级网络是 scale-up fabric 的基础，Router 是其中的节点
- **[Switching Principles](/concepts/switching-principles.md)**：电路交换/分组交换的基本概念在 NoC 中的体现
- **[Cerebras Wse](/entities/cerebras-wse.md)**：WSE 900K 核心的 NoC 使用 24-color 确定性路由，直接应用本文描述的 Router 微架构
- **[Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md)**：WSE Color 机制的完整解析——虚拟通道+静态路由+任务调度
- **[Ub Data Link Layer](/concepts/ub-data-link-layer.md)**：UB 的 Credit 流控/Go-Back-N 与 NoC credit-based 流控原理一致
- **[Ub Transport Layer](/concepts/ub-transport-layer.md)**：UB 传输层的 PSN/重传机制是 NoC router 流控在网络层的扩展
- **[Deterministic Execution](/concepts/deterministic-execution.md)**：编译器确定性调度依赖 NoC Router 的确定性行为
- **[Collective-Capable NoC](/concepts/collective-capable-noc.md)** — FlooNoC 扩展：XY fork 组播、in-network reduction、**DCA 借 FPU**（MLSys 2026）
- **[Eyeriss Accelerator](/concepts/eyeriss-accelerator.md)** — CNN 加速器 **GIN/GON/LN** custom multicast（单周期 tag 组播 vs 通用 mesh router）
- **[WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md)** — WSE mesh collective 算法与性能模型
- **[Lpu Architecture](/concepts/lpu-architecture.md)**：LPU 的 SRAM-first 架构中片上互联设计参考了 NoC Router 微架构
- **[Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md)**：FBFLY 拓扑利用高基数 Router 降低片上网络直径，bypass channel 减少非最小路由开销
- **[Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md)** — XY/DOR 路由算法与 VC 死锁避免（D&T Ch.4–5）
- **[NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md)** — 虫孔/VC/5-stage pipeline（H&P App.F）

# Citations

[1] [raw/articles/片上网络Router的微架构---设计师视角.md](raw/articles/片上网络Router的微架构---设计师视角.md)
[2] [raw/papers/Near-optimal_wafer-scale_reduce.pdf](raw/papers/Near-optimal_wafer-scale_reduce.pdf)
[3] [raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf](raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf) — FlooNoC collective + DCA（MLSys 2026）
