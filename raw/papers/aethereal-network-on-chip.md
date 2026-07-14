---
source_url: https://doi.org/10.1109/MDT.2005.99
ingested: 2026-07-14
sha256: e7d9f698ba631779ff7c1506a2d02a6eaac623db874ec67dc8ba95ae6af7d15a
zotero_key: 4PFJG7KE
---

# Æthereal Network on Chip: Concepts, Architectures, and Implementations

**Authors:** Kees Goossens, John Dielissen, Andrei Rădulescu (Philips Research Laboratories)

**Venue:** IEEE Design & Test of Computers, Sept.–Oct. 2005, pp. 414–421  
**DOI:** 10.1109/MDT.2005.99

## Motivation
- SoC IP 增多 → 总线不够，NoC 成为通信中心
- 许多 IP 需要**硬保证**吞吐/延迟（实时流、中断），纯 BES 不够
- 片外网络难给 100% 保证（丢包、深流水线）；片上可无丢包 + 流控
- 争用是不可预测性主因；大缓冲的 deadline/rate 仲裁对 NoC 太贵

## 核心思想：Contention-free routing
- **流水线 TDM 电路交换**（pipelined time-division-multiplexed circuit switching）
- 连接打开时预约 **线 + 缓冲 + 时隙**；关闭时释放
- 保证：同一时刻同一资源最多一个块 → **无争用 by construction**
- 相对纯电路交换：更少导线；路由器缓冲最小（每输入 1 block）
- 相对优先级方案：多媒体多流「同等重要」→ 优先级失效；TDM 可给不同带宽预约

## Slot table
- 路由器 arity N：表 T 有 S 行（时隙）× N 列（输出）
- 逻辑全局同步：全网同一固定时长 slot
- `T(s, o) = i`：时隙 s 时输入 i → 输出 o；空表示未预约
- 每 slot 每端口最多读写一块；下一 slot 转发 → **store-and-forward，无死锁**
- 每跳延迟 = 1 slot；带宽 = 块大小的整数倍 / S slots
- GS 块**无 header**（路径由 slot 表决定）→ 效率高

## 同步实现
- 集中时钟 + waterfall / SLD 等；或
- **分布式**：每 slot 每输出先产 token、再消费每输入 token（SDF actor）→ 与邻居同步，全网同 slot，速度受最慢路由器限制

## BES（Best-Effort）
- 传统虫孔 + 输入排队；RR 仲裁，粒度 3 words = 1 flit
- 链路级流控防溢出；**源路由**（header 含路径，每跳剥 log₂N bit）
- 无多缓冲类 → 可死锁，靠路由策略避免
- GS-BE 组合：GS∥BES 并行；BES **低优先级**，仅无空闲/未用预约时隙

## 编程模型
| | **Distributed** | **Centralized** |
|--|-----------------|-----------------|
| 机制 | BES 系统包 SetUp / TearDown / AckSetUp（类 ATM） | 根进程 / MMIO 直接写 NI（及可选路由表） |
| 可扩展 | 好 | 小 NoC 够用 |
| 成本 | 高（slot 表遍布路由器） | 低（可去掉路由器 slot 表，GS 带 header） |
| 拓扑假设 | 路径可逆（TearDown 回退） | 较弱 |

- 两模型可用**相同** slot 分配；用 NoC 自身编程，无需另建配置网
- SetUp 沿数据路径下行；成功则任意路径回 Ack；失败 TearDown 清半连接
- 设计时冲突无关分配 → 运行时任意顺序仍确定性可编程

## 四种路由器实现（0.13 µm）

| 实现 | 服务 | 编程 | Switch | Area (mm²) | Freq |
|------|------|------|--------|------------|------|
| GS-BE distributed | GS+BES | Distributed | N×N | **0.24** | 500 MHz → 2 GB/s/port |
| GS-BE centralized | GS+BES | Centralized | 2N×N | 0.175 | 500 |
| GS-BE centralized | GS+BES | Centralized | N×N | **0.13** | 500 |
| **GS-only centralized** | GS | Centralized | N×N | **0.033** | **1 GHz** → 4 GB/s/port |

- Mesh：5 I/O + 1 内部 → 有效 6×6 开关
- GS queue = 1 flit（最小）；BES queue = 8 flits；datapath 34b（32+2 ctrl）
- 寄存器实现队列时队列占 **~80%** 面积 → 专用 FIFO + 最小 GS 队列是正确选择
- GS-only：2× 性能、约 1/4 面积（相对 GS-BE）；但纯 GS 承载“类 BES”可能需更多路由器/导线

## 设计取舍收束
- 频谱两端：GS-BE + 分布式系统包（可扩展、面向未来）↔ GS-only + 集中 + DSM（快、便宜、贴近当时实践）
- 系统架构师在 **编程模型 × 性能 × 面积 × 全局线数** 上平衡

## 与本 wiki 的关联点
- TDM/电路交换 ↔ [Switching Principles](/concepts/switching-principles.md)、[Flow Control Fundamentals](/concepts/flow-control-fundamentals.md)
- GS 确定性预约 ↔ [Deterministic Execution](/concepts/deterministic-execution.md)、[Cerebras Color](/concepts/cerebras-color-mechanism.md)（不同机制，同属预配置确定性通信）
- BES 虫孔 + credit ↔ [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md)、[NoC Router 微架构](/concepts/noc-router-microarchitecture.md)
