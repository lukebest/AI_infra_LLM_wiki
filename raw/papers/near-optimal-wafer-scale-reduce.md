---
source_url: https://arxiv.org/abs/2404.15888
ingested: 2026-06-20
sha256: b0b027ffd4070c22120fda3f3769f45b8a1efd5f972f25c91e06ec4be9e8832a
---

# Near-Optimal Wafer-Scale Reduce (arXiv:2404.15888v4)

**Authors:** Piotr Luczynski, Lukas Gianinazzi, Patrick Iff (ETH Zurich); Leighton Wilson (Cerebras Systems); Daniele De Sensi (Sapienza University of Rome); Torsten Hoefler (ETH Zurich)

**Venue:** HPDC 2024
**Code:** https://github.com/spcl/spatial-collectives

## Motivation
- Reduce/AllReduce 是 HPC 中最常用的 collective，对 GEMV/GEMM、深度学习、生物信息、物理模拟至关重要
- Cerebras WSE 的 2D mesh + multicast + pipelining 特性使得传统 α-β 模型不适用
- 现有实现仅优化极端向量长度，中间/可变长度 HPC 场景性能差

## WSE 架构背景
- CS-2: ~750K PE，2D grid，每 PE 48KB SRAM
- 每 cycle: 128-bit read, 64-bit write, 8×16-bit ops
- Router: 5 bidirectional links (4 neighbors + ramp)，32 bits/cycle/direction
- Wavelet = 32-bit packet，1 cycle/hop
- TR (ramp latency) ≈ 2 cycles (WSE-2)，之前文献误报为 7
- Color-based routing: 每个 color 独立路由配置，支持 multicast（免费复制）
- 每 router 每 color 存 4 种路由配置，control wavelet 可运行时切换
- 数据流架构：task 由 wavelet arrival 激活
- DSD (Data Structure Descriptor): 硬件级向量化操作描述符

## 性能模型

| 符号 | 含义 |
|------|------|
| E | Energy: 所有 wavelet 的总跳数 |
| L | Distance: 最大单 wavelet 跳数 |
| D | Depth: 最长依赖链 |
| C | Contention: 单 PE 最大收发数 |
| N | 使用的 link 总数 |
| TR | Ramp latency (PE↔router) |
| P | PE 数量 |
| B | 向量长度 (wavelet 数) |

**核心公式:**
```
T = max(C, E/N) + L + (2*TR + 1)*D
```

- C 主导 → PE 成瓶颈（pipeline 行为，网络延迟可忽略）
- E/N 主导 → 网络拥塞
- L 主导 → 长距离延迟
- D 主导 → 串行依赖链

## 1D Reduce 算法

### Star Reduce
- 所有 PE 直接发给 root，depth=1
- T = B*(P-1) + 2*TR + 1
- 适合 B=1（标量），大 B 时灾难性

### Chain Reduce
- PE 依次向左邻居传递，pipelined，depth=P-1
- T = B + (2*TR+2)*(P-1)
- 适合 B ≫ TR*P（大向量），小 B 时深度太大

### Tree Reduce（新）
- 二叉树归约，log2(P) 轮，每轮减半活跃 PE
- T = max(B*log2(P), B*P/(2*(P-1))*log2(P) + P - 1 + (2*TR+1)*log2(P))
- 适合小到中等 B，大 B 时 contention 高

### Two-Phase Reduce（新）
- Phase 1: 每 √P 个 PE 一组做 Chain Reduce
- Phase 2: 剩余 √P 个 PE 再 Chain Reduce
- Depth = 2*√P - 2（vs Chain 的 P-1）
- Contention = 2B（仅比 Chain 差 2×）
- 适合中间范围 B，最多 2.4× 于最优

### Auto-Gen Reduce（新）
- 性能模型驱动，自动搜索最优 reduction tree
- 递归计算 min energy for given (P, B, D, C)
- O(P^4) 计算最优 pre-order tree，自动生成代码
- **最多 1.4× 于下界**，严格优于所有固定算法

### Lower Bound
- T*(P,B) ≥ min_D [B * E*(P,1,D)/(P-1) + P-1 + D*(2*TR+1)]
- 通过动态规划 O(P^3) 计算 E*(P,1,D)
- 1D 场景下 Auto-Gen 严格接近最优

## 1D AllReduce

### Reduce-then-Broadcast
- T = T_Reduce + T_Bcast
- Broadcast = flooding（multicast 使然），T_Bcast = B + P + 2*TR

### Ring AllReduce
- 两种 ring 映射（simple / distance-preserving），性能相同
- T = 2(P-1)*B/P + 4P - 6 + 2(P-1)*(2*TR+1)
- 利用双向链路，2(P-1) links
- 大 B 时优于 Reduce-then-Broadcast

## 2D Collectives (M×N = P)

### 2D Broadcast
- 利用 multicast: x 轴 broadcast + y 轴 multicast 同时
- T = B + M + N - 2 + 2*TR + 1
- √P×√P grid: 2√P + 2*TR - 1 + B，远优于 1D 的 P

### 2D Reduce
- **X-Y Reduce**: 先 x 轴 reduce 再 y 轴 reduce
- **Snake Reduce**: chain 按 snake 形状映射 2D grid，T ≈ T_chain
- Lower bound: T* ≥ max(B, B*P/8 + M + N - 1 + 2*TR + 1)
- B ≫ P 时 Snake 接近最优

### 2D AllReduce
- 2D Reduce + 2D Broadcast 最优
- 不同 (B,P) 区域最佳算法不同（类似 1D）

## 实验结果
- 平台: CS-2 @ 850 MHz, 40GB SRAM
- Reduce: Two-Phase/Auto-Gen 比 Cerebras vendor 方案快 **3.27×**
- AllReduce: 快 **2.56×**
- 模型预测误差 **< 4%**
- 1D 实现: ≤3 colors; 2D: ≤5 colors（共 24 个可用）
- 测量方法: 时钟同步 + wait parameter (α) 校准

## 关键洞察
1. **Multicast 使 flooding broadcast 最优** — 颠覆传统网络中 broadcast 需要树的认知
2. **Ring AllReduce 在 WSE 上不总最优** — 小/中向量时 Reduce-then-Broadcast 更快（因 multicast）
3. **模型驱动 > 试错** — 性能模型可在 O(P^4) 内自动生成接近最优的代码
4. **2D 收益有限** — 单 port（processor↔router）限制了两维并行度，但仍显著降低 broadcast 延迟
5. **Color 数量是约束** — 复杂 collective 消耗 colors，24 个总 colors 中 1D 用 3 个、2D 用 5 个
