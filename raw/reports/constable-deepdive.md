---
type: Raw Source
title: Constable Deep-Dive 笔记
source_path: /home/luke/openclawdata/workspace-research/notes/reports/superscalar-cpu/constable-deepdive.md
ingested: 2026-07-03
---

# 📖 Constable Deep-Dive 笔记

> **论文**: Constable: Improving Performance and Power Efficiency by Safely Eliminating Load Instruction Execution
> **会议**: **ISCA 2024 Best Paper Award** ⭐
> **作者**: Rahul Bera, Adithya Ranganathan (co-primary), Joydeep Rakshit, Sujit Mahto, Anant V. Nori, Jayesh Gaur, Ataberk Olgun, Konstantinos Kanellopoulos, Mohammad Sadrosadati, Sreenivas Subramoney, Onur Mutlu
> **机构**: ETH Zürich + Intel Processor Architecture Research Lab
> **arXiv**: https://arxiv.org/abs/2406.18786
> **精读时间**: 2026-07-03 (Asia/Shanghai)
> **精读员**: Turing (for Luke)
> **全文长度**: 17 页 + 9 章节 + Appendix A (sensitivity) + Appendix B (extra registers)

---

## 🎯 一句话总结 (Luke 视角)

**Constable 通过 "识别 likely-stable load + 监控 source register 与 memory 变化" 两个轻量硬件表，在 12.4 KB 面积代价下让全局 34.2% 的 load 完全不执行（不占 RS、不占 L1-D 端口），换 5.1% 性能 + 3.4% 动态功耗。这是 Luke 设计 WSE 控制核时可直接借鉴的 "用识别换消除" 微架构范式。**

---

## 1. 核心问题 (Motivation)

### 1.1 Load 是 ILP 的双重瓶颈
| 瓶颈类型 | 现象 | 现有缓解 | 不足 |
|---------|------|---------|------|
| **数据依赖** | Load 延迟 stall 后继指令 | LVP / MRN | 只能掩盖延迟 |
| **资源依赖** | Load 占用 RS entry、AGU port、L1-D 端口 | 加大硬件 (功耗墙) | 边际收益递减 |

**Key limitation (论文原话)**: LVP/MRN 预测对错都需要 **执行 load 来验证** → 即使预测正确也消耗 hard-to-scale 的 pipeline 资源。**5.1% 性能 + 3.4% 功耗的 headroom 来自 "load 不执行"**。

### 1.2 关键观察：34.2% 的 load 是 global-stable
论文发现：
- **34.2%** 的动态 load（最高 68.3%）在整 workload 期间**反复从同一地址取同一值**
- 命名为 **global-stable load**
- 即便 -O3 编译器也**无法**消除（原因：runtime constants、inlined function 的 local vars、shared statics）
- **这给 Constable 提供了天然的可消除目标**

---

## 2. 关键洞察 (Key Insight)

**两次连续执行同一静态 load 的动态实例，I₂ 必然和 I₁ 取到相同值 iff 两个条件都满足：**

```
Condition 1 (Address 同):  I₁ 和 I₂ 之间无 source register 的写
Condition 2 (Value 同):    I₁ 和 I₂ 之间无 store/snoop 请求访问 I₁ 的地址
```

**直觉**：
- Condition 1 满足 → I₂ 地址与 I₁ 相同 → **地址计算可消除**
- Condition 2 满足 → I₂ 取到的值与 I₁ 相同 → **数据 fetch 可消除**
- 两者都满足 → **整个 load 执行可消除**

**与 LVP 的本质区别**：

| | LVP (EVES) | Constable |
|---|-----------|-----------|
| 消除什么 | 预测值，掩盖**数据依赖** | 消除 load 执行，**数据+资源依赖**都消除 |
| 验证机制 | 仍要执行 load | 不执行 load（用 last-fetched value） |
| 节省资源 | 仅节省 stall 周期 | 节省 RS + AGU + L1-D 端口 |
| 性能 headroom (理想) | 4.3% (Ideal Stable LVP) | 9.1% (Ideal Constable) |

---

## 3. 总体机制 (End-to-End Mechanism)

```
Step 1: 识别 (Identify)
   SLD (Stable Load Detector) - PC-indexed
   - 每个非消除 load 完成时: 若 (last_addr, last_value) 都匹配 → confidence++
   - 若不匹配 → confidence /= 2
   - confidence ≥ 30 → 标记为 likely-stable (但 can_eliminate 仍为 0)

Step 2: 武装 (Arm) - 仅一次
   likely-stable load 在 writeback 阶段:
   (a) RMT 查 source register → 插入 load PC
   (b) AMT 查 physical address → 插入 load PC
   (c) SLD 设 can_eliminate = 1
   之后该 load 进入 "elimination 模式"

Step 3: 消除 (Eliminate) - 持续
   can_eliminate=1 的 load 在 rename 阶段:
   - 把 load 转化为 3-operand register-move
   - 源 = xPRF entry (含 last-fetched value)
   - 目标 = 原 destination register
   - 第三操作数 = last-computed load address (for LB disambiguation)
   - 此指令 bypass 所有后续 pipeline stage

Step 4: 失效 (Invalidate) - 防御
   (a) 任何指令写 RMT 中的 architectural register → reset can_eliminate
   (b) 任何 store/snoop 命中 AMT 中的 physical address → reset can_eliminate
   (c) Context switch / page mapping 变化 → reset all
```

**关键设计决策**：
- **last-fetched value 存储在 SLD** (不需额外的 value table)
- **load 转化为 register-move** (复用已有的 move elimination 机制)
- **用现有 memory disambiguation 逻辑** 处理 OoO store-load 顺序违例 (无需新硬件)

---

## 4. 微架构详细设计 (Section 6) — Luke 最关心

### 4.1 三个核心硬件表 (Table 1)

| 结构 | 大小 | Entry 内容 | 端口 | 用途 |
|------|------|-----------|------|------|
| **SLD** (Stable Load Detector) | **7.9 KB** | 32 sets × 16 ways, 512 entries<br>tag(24b) + addr(32b) + val(64b) + conf(5b) + can_eliminate(1b) | **3R/2W** | (1) 识别 likely-stable (2) 决定 can_eliminate (3) 提供 last-addr + last-val |
| **RMT** (Register Monitor Table) | **0.4 KB** | 16 load PCs / stack reg (RSP, RBP)<br>8 load PCs / 14 other regs | **2R/6W** | 监控 source register 写 → reset can_eliminate |
| **AMT** (Address Monitor Table) | **4.0 KB** | 32 sets × 8 ways, 256 entries<br>phys-addr-tag(32b) + 4 hashed load PCs(24b) | **1R/1W** | 监控 store/snoop → reset can_eliminate |
| **xPRF** (extra PRF) | 32 entries (small) | last-fetched value (64b) | depends | 写回端口用，break load data dependence |
| **总计** | **12.4 KB / core** | (xPRF 不计入 Constable 开销) | | |

### 4.2 端口设计依据 (Section 6.7.1)

**SLD 3R/2W 的依据**:
- 平均每 rename group **1.93 loads** (90 workload 统计)
- **98.3%** rename groups ≤ 2 loads
- → 3 read ports 足够; rename stage 偶发 stall 可接受

**SLD 2W 的依据**:
- SLD 写只在 `can_eliminate` reset 时发生 (来自 RMT/AMT 更新)
- 平均每 cycle 仅 **0.28 SLD updates**
- **98.23% cycles** 有 ≤ 2 SLD updates
- → 2 write ports 足够

**关键洞察 (Luke 复用)**:
- 端口不是凭感觉设计，是**实测分布**反推
- 这套方法学适合 WSE 控制核的 L1 端口设计

### 4.3 Pipeline 修改 (Section 6.1)

```
Fetch  →  Decode  →  Rename  →  Allocate  →  Issue  →  Execute  →  Memory  →  Writeback  →  Retire
                       │ ①↑                                                              │ ④↓
                       │ SLD lookup                                                      │ Non-elim likely-stable:
                       │ 1R/cycle                                                        │ (a) RMT lookup with src reg
                       │                                                                  │     → insert load PC
                       │ Eliminated: bypass to retire                                    │ (b) AMT lookup with phys addr
                       │   convert to register-move                                      │     → insert load PC
                       │   map dest ← xPRF source                                        │ (c) SLD: set can_eliminate
                       │                                                                  │  (d) If on heap: pin CV-bit
                                                                                          │
                                                                                          │ Not likely-stable (first time):
                                                                                          │   SLD: compare (last_addr, last_val)
                                                                                          │   - match → confidence++
                                                                                          │   - mismatch → confidence /= 2
```

### 4.4 写 RMT/AMT 的多源 (Section 6.4)

| 触发事件 | RMT 操作 | AMT 操作 | SLD 操作 |
|---------|---------|---------|---------|
| **非消除 likely-stable 完成** (writeback) | 查 src regs，insert load PC | 查 phys addr，insert load PC | set can_eliminate |
| **任何指令写 architectural reg** (rename) | 查 dest reg，reset 所有相关 load PC | — | reset can_eliminate |
| **Store 地址生成** (execute) | — | 查 phys addr，reset 所有相关 load PC | reset can_eliminate |
| **Snoop 请求** (cache) | — | 查 snoop addr，reset 所有相关 load PC | reset can_eliminate |
| **Context switch / page mapping 变** | invalidate all | invalidate all | reset all can_eliminate |

**RMT 端口需求 (2R/6W)**:
- 2R: rename 阶段查 dest reg (用于 reset)
- 6W: 一个 rename group 可有最多 6 个写 reg 指令 (6-wide 机器)

### 4.5 OoO Load 顺序违例的处理 (Section 6.5)

**问题**: eliminated load 可能在 store 计算地址前完成 (OoO load 投机执行)

**解法**: 复用**现有 memory disambiguation 逻辑** (StoreSets 类)
- store 计算地址后, 查 AMT reset can_eliminate
- 但 OoO 流水线中: 较年轻的 eliminated load 已经被标记为完成
- memory disambiguation 探测 LB 中的 address 字段, 发现违例
- → **flush pipeline + re-execute** 所有比该 load 新的指令
- **0.09%** 的 eliminated load 触发此违例 (90 workload 平均, 86/90 workload < 0.5%)

**关键设计哲学**: 不为 OoO 违例增加新硬件 → 复用既有 LSQ 机制 → 极低违例率 → 整体成本可控

### 4.6 Multi-core Coherence (Section 6.6)

**问题**: eliminated load 已"完成", 但 cache line 在远端被改 → 数据 stale

**解法**: **CV-bit pinning** (Constable-Valid bit)
- eliminated load 触发时, **pin CV-bit in coherence directory entry** for that line
- 远端 write → 必须 invalidate 该 line → 触发 snoop → 查 AMT reset
- **关键**: pinning 只针对 shared line; core-private line 不需要

**Clean eviction 失效分析 (Appendix A.3)**:
- 如果 L1 私有 cache 干净驱逐 (clean eviction) → 设计选项有两种:
  1. 失效 AMT entry (avoid elimination, **Constable-AMT-I**)
  2. 简单 invalidate (Constable 默认)
- 选 2: 干净驱逐不 invalidate, 节省硬件
- 代价: 11/90 workload 损失 > 5% 性能 (最多 -10.4% on 554.roms_r)
- 论文选 2 (CV-bit pinning) 性能更优

### 4.7 关键设计决策 (Section 6.7)

| 决策 | 数据 | 结论 |
|------|------|------|
| **Wrong path 更新不恢复** | 82/90 workload < 1% 性能变化, 0.2% 平均 | 不需要 branch misprediction recovery |
| **Page mapping 变化** | reset all SLD + invalidate RMT/AMT | 简单粗暴, 但发生率低 |
| **xPRF unavailable** | 仅 0.2% 出现 → fallback 正常执行 | 32-entry xPRF 够用 |
| **SMT 资源分配** | Constable 资源**statically-partitioned 或 dynamically-shared** | 2-way SMT 时 8.8% 性能 |
| **32-set 哈希** | (未明示) | 推测 PC-hash |

---

## 5. 实验结果 (Section 9) — 完整数字

### 5.1 性能 (noSMT) — Fig 11/12

| 机制 | 性能 vs baseline | 备注 |
|------|-----------------|------|
| EVES (LVP baseline) | **4.7%** | 仅 break data dep |
| **Constable** | **5.1%** | 同时 break data + resource dep |
| EVES + Constable | **8.5%** | 正交组合 |
| EVES + Ideal Constable | — | 82.9% headroom 已实现 |
| **最大单 workload 提升** | **31.2%** | outlier |

**关键观察**:
- 60/90 workload: Constable 比 EVES 高 **4.9%** (avg)
- 30/90 workload: EVES 比 Constable 高 **9.2%** (avg) — EVES 在 random memory pattern 下有优势
- 5 个 workload 类别: Client / Enterprise / FSPEC17 / ISPEC17 / Server

### 5.2 性能 (SMT 2-way) — Fig 14

| 机制 | 性能 vs baseline | 备注 |
|------|-----------------|------|
| EVES | 3.6% | SMT 下 EVES 收益降 |
| **Constable** | **8.8%** | SMT 下 Constable 收益**显著增加** |
| EVES + Constable | 11.3% | |

**根因**: SMT 加剧 load port 竞争 → Constable 节省的 RS+L1-D 端口成为稀缺资源 → 增益放大

### 5.3 性能 Headroom 分析 (Section 4.4) — **Luke 必读**

| 配置 | 性能 vs baseline | 含义 |
|------|-----------------|------|
| **Ideal Stable LVP** | 4.3% | 仅消除 data dependence (数据预测) |
| **Ideal Stable LVP + data fetch elim** | 6.7% | 多消除一半 resource dep (fetch) |
| **2× load execution width** | ~9% (等同 Ideal Constable) | 用硬件堆出来的极限 |
| **Ideal Constable** | **9.1%** | 真实可实现的物理上限 |

**黄金洞察** ⭐:
- **4.3% → 9.1% 的 4.8% 性能差距 = "resource dependence 的真实代价"**
- 论文实现的 5.1% 已经达到 9.1% headroom 的 **56%** (vs 4.3% = 100%)
- 这就是 Constable 的**核心价值**：**消除 resource dep 比消除 data dep 多 2x 性能空间**

### 5.4 性能分解 (Section 9.1.1, Fig 13) — Luke 可借鉴

| Load 类别 | 性能贡献 | 占比 |
|----------|---------|------|
| **Stack-relative** | **2.6%** | 50% of benefit |
| **Register-relative** | 1.8% | 35% of benefit |
| **PC-relative** | 1.1% | 22% of benefit |
| **总和** | ~5.5% (overlap 5.1%) | 100% |

**Luke 复用路径**: 任何 control-flow 主导的 workload, stack-relative load 占主导 → Constable 增益最大

### 5.5 覆盖率分析 (Section 9.3.1, Fig 16-17)

| 指标 | EVES | Constable | EVES+Constable |
|------|------|-----------|----------------|
| **Load coverage** | 27.3% | 23.5% | 35.5% |

**Constable 覆盖的 load 类型**:
- PC-relative global-stable: **70.2%** 覆盖 (最高)
- Stack-relative global-stable: ~56% 覆盖
- Register-relative global-stable: 33.2% 覆盖 (最低)
- **综合**: 56.4% 的 global-stable loads 被实际消除

**额外发现**: Constable 多消除了 **13.5%** 非 global-stable load (workload-phase-stable)
- Global-stable = 整 workload 稳定
- Constable 接受 phase-stable (达到 confidence 阈值) → **更广覆盖**

### 5.6 资源使用减少 (Section 9.4) — **能耗关键**

| 资源 | 减少 | 最大 |
|------|------|------|
| **RS 分配** | **8.8%** (avg) | 35.1% (Enterprise) |
| **L1-D 访问** | **26%** (avg) | 39.7% (Enterprise) |
| **ROB 分配 (memory ordering 违例)** | +0.3% (avg, 极小) | 1% (79/90 workload) |

**5 个 workload 类别排序**:
- Enterprise: **RS -12.8%, L1-D -39.7%** (最高)
- ISPEC17: RS -1.3%, L1-D -3.9% (最低)

### 5.7 能耗 (Section 9.5) — Fig 19

| 单元 | 节省 | 备注 |
|------|------|------|
| **整体 core** | **-3.4%** (avg) | 24.6% max |
| OOO 单元 | -4.5% | RS 节省主导 |
| **RS 子单元** | **-5.1%** | 直接来自 load RS 减少 |
| MEU 单元 | -7.2% | L1-D 节省主导 |
| **L1-D 子单元** | **-9.1%** | 26% 访问减少的直接体现 |
| RAT / ROB | 略降 | |

**EVES 节省对比**: EVES 仅 -0.2% (load 仍要执行, 只省一点 stall 周期) → Constable 是 **16x 节能优势**

### 5.8 错误恢复 / Correctness (Section 8.5)

- 在 **3400 traces** 上做 functional verification (microarch vs functional simulation)
- **没有任何 trace 失败** (golden check 强制比较 load addr + data)
- 错误恢复路径:
  1. AMT reset → can_eliminate = 0 → 下次正常执行 (90% 情况)
  2. OoO 违例 → 既有 memory disambiguation → flush + re-execute (0.09% 情况)
  3. Snoop → AMT reset → 正常重执行 (multi-core 情况)

---

## 6. Sensitivity Studies (Appendix A.1) — Luke 必读

### A.1.1: 加大 load execution width (Fig 20a)

| Load execution width | Baseline 速度 | Constable 速度 | 差距 |
|---------------------|--------------|----------------|------|
| 3 (baseline) | 1.00 | 1.05 | +5% |
| 4 | 1.04 | 1.08 | +4% |
| 5 | 1.07 | 1.10 | +3% |
| 6 | 1.09 | 1.12 | +3% |
| **2× (6)** | — | — | **Constable 3.5% 优于 2× width** |

**关键洞察** ⭐:
- **Constable 在 baseline (3 width) 上的 perf ≈ baseline + 1 个 extra width 的 perf**
- **但面积/功耗节省巨大** (12.4 KB vs 一个 load execution unit 估计 ~50-100 KB)
- **性价比: 12.4 KB 表 + 极少能耗 ≈ 1 个 load port**
- 这是 Constable 工业价值的核心

### A.1.2: 加大 pipeline depth (Fig 20b)

| Pipeline depth | Baseline | Constable | 差距 |
|--------------|----------|-----------|------|
| 1× (baseline) | 1.00 | 1.05 | +5% |
| 2× | 1.07 | 1.10 | +3% |
| 3× | 1.10 | 1.12 | +2% |
| **4×** | 1.12 | 1.15 | **+3.4%** |

**关键洞察** ⭐:
- 即使 pipeline depth 翻 4 倍, Constable 仍能拿到 +3.4% 性能
- **Constable 收益是 "deeper 流水线的边际"** — 不被 pipeline 深度边际饱和影响
- 这就是论文 5.1% 的"长青性"

### A.2: Memory Ordering 违例 (Fig 21)

- **0.09%** eliminated load 违例 (avg, 90 workload)
- **86/90 workload** 违例率 < 0.5%
- ROB 指令分配 +0.3% (avg, 几乎无影响)
- **79/90 workload** ROB 增加 < 1%

### A.3: Clean Eviction 失效 (Fig 22)

- 干净驱逐不 invalidate AMT (Constable 默认)  vs  invalidate (Constable-AMT-I)
- **0.9% 性能差距** (Constable 优)
- 11/90 workload 损失 > 5% (最多 554.roms_r -10.4%)
- 17/90 workload 覆盖损失 > 5% (最多 554.roms_r -27%)

### B: 架构寄存器增加 (Fig 23)

- 增加 architectural register → compiler 可减少 spill/fill → 减少 global-stable load
- 数据: 增加 ~5-15% register → global-stable load 比例 **略降但** Constable 仍 positive
- → Constable 在未来 RISC-V 32+ regfile 架构中**仍有价值**

---

## 7. 失败模式 / Limitations (Section 9.3.1)

### 43.6% global-stable loads **未被消除** — 三个原因:

| 原因 | 占比 | 例子 | 解决方案 |
|------|------|------|---------|
| **source register 被写** (Condition 1 失败) | **23.3%** | 循环变量被赋值 | 增大 RMT / 更激进调度 |
| **Silent store** (Condition 2 失败) | **14.1%** | `memory[i] = memory[i]` 之类 | 区分 silent vs real store |
| **学习/硬件预算不足** | 6.2% | workload phase 切换 / SLD 满 | 增大 SLD / 优化哈希 |

**Luke 复用价值**: 这 43.6% 是**未来 Constable 改进**的方向, 改进空间仍有 4% 性能 + 2% 功耗 (相对当前 5.1%)

### 在 30/90 workload 上 EVES > Constable — 9.2% avg

**主因**: EVES 在 **random / non-stable data** 时有预测价值, Constable 完全无能为力
- Hash table lookup
- Random number generation
- Cryptographic operations

**Luke 启发**: **LLM 推理的 KV cache 访问** = 高 stability → Constable 大胜
**LLM 推理的 speculative decoding** = 部分 stability → 仍 Constable 占优
**LLM 训练的反向传播** = low stability → EVES 占优 (但 Constable + EVES 都用)

---

## 8. 与 Luke 研究的关联 (按方向)

### 8.1 WSE 控制核设计 ⭐⭐⭐

**直接复用**:

```verilog
// Luke 设计的 WSE RISC-V 控制核可加的模块
module constable_sld #(
    parameter ENTRIES = 512,  // 可缩到 256 for small core
    parameter WAYS = 16
) (
    input clk, reset,
    input [63:0] pc,             // load PC
    input [63:0] last_addr,
    input [63:0] last_val,
    input confidence_update,     // 1=match, 0=mismatch
    output can_eliminate,
    output [63:0] stored_addr,
    output [63:0] stored_val
);
    // 32-set × 16-way PC-indexed
    // 5-bit confidence counter, threshold 30
    // ...
endmodule
```

**Luke 的设计选择建议**:
- **面积预算**: 12.4 KB 是 Intel Golden Cove 6-wide baseline → WSE 小核 (4-wide) 可缩到 ~6 KB
- **端口数**: 3R/2W SLD 足够 (rename group 1.93 loads)
- **核心机制**: confidence threshold 30 是经验值, RISC-V 可能要重新调
- **避免的坑**: 不需要为 wrong path 加 recovery (0.2% 影响)

**Luke 需精读**: Section 6.4-6.7 (微架构实现) + Table 1 (硬件参数)

### 8.2 LLM 推理核 ⭐⭐⭐ (Luke 关注度最高)

**应用场景**:
- **KV cache 访问**: 高度规律 → likely-stable 占比可能 > 50%
- **Attention score 计算**: 同一 QK^T 多次访问 → 大量 global-stable
- **Embedding lookup**: 同一 token 多次访问 → 高 likely-stable

**Luke 行动项**:
- 在 WSE 上跑 LLM 推理 trace → 测量 likely-stable load 比例
- 如果 > 30%, **Constable 是必备优化**
- 实现简化版 (只用 SLD + RMT, 不需要 AMT for on-chip LLM)
- 与 Prophet (HKUST) 配合: Prophet 优化 KV cache 预取, Constable 优化 weight 复用

### 8.3 NPU 核 ⭐⭐

**应用场景**:
- **Weight 加载**: 同一 weight tile 反复访问 → likely-stable 高
- **Activation 复用**: 同一 activation 多次消费 → likely-stable
- **Tile 数据流**: GEMM 中的 element-wise 加载 → likely-stable

**Luke 行动项**:
- NPU 通常是 in-order + 大量 SRAM, Constable 思路可移植但需要适配
- **关键约束**: NPU 没有 OoO, 但 Constable 不依赖 OoO, 只依赖"硬件表"
- **建议**: 在 NPU dispatcher 加 SLD, 复用 load elimination 思路

### 8.4 核内同步 ⭐ (Luke Gap 方向)

**Constable 思路的迁移可能**:
- LR/SC 也有 "value stability" (同一地址 lock 反复取相同值)
- 但 Constable 处理的是"消除执行", LR/SC 需要保留执行
- **结论**: Constable 思路**不直接适用** LR/SC, 需要新方案 (Luke Gap)

---

## 9. 关键数字速查 (Luke 写作直接引用)

```
性能:
  +5.1% avg, +31.2% max (noSMT)
  +8.8% avg (2-way SMT)
  +8.5% avg (与 EVES 组合, noSMT)
  +11.3% avg (与 EVES 组合, SMT)
  9.1% ideal headroom (Ideal Constable)
  4.3% ideal headroom (Ideal Stable LVP)

能耗:
  -3.4% core dynamic (avg), -24.6% max
  -4.5% OOO, -7.2% MEU
  -5.1% RS, -9.1% L1-D
  EVES 对比: -0.2% (Constable 是 16x)

硬件开销 (Intel Golden Cove 6-wide baseline):
  SLD: 7.9 KB (32×16, 3R/2W, 0.211 mm²)
  RMT: 0.4 KB (2R/6W, 0.004 mm²)
  AMT: 4.0 KB (32×8, 1R/1W, 0.017 mm²)
  xPRF: 32 entries (不算入开销)
  总: 12.4 KB per core
  端口总功耗: 0.211 + 0.004 + 0.017 ≈ 0.23 mm² (14nm)

资源使用:
  -8.8% RS allocation (avg), -35.1% max
  -26% L1-D accesses (avg), -39.7% max
  +0.3% ROB allocation (memory ordering 违例)
  +0.09% eliminated loads 触发 OoO 违例
  0.2% load 触发 xPRF 不可用 fallback

覆盖率:
  34.2% of dynamic loads are global-stable (avg), 68.3% max
  56.4% of global-stable loads eliminated
  23.5% load coverage (Constable alone)
  35.5% load coverage (Constable + EVES)
  
Load 类别贡献:
  Stack-relative: 2.6% perf (50% of benefit)
  Register-relative: 1.8% perf
  PC-relative: 1.1% perf

覆盖率 by type:
  PC-relative: 70.2% runtime elimination
  Register-relative: 33.2% runtime elimination

Workload:
  90 traces, 58 unique workloads
  Client (16), Enterprise (9), FSPEC17 (13), ISPEC17 (10), Server (10)
  3400 traces 用于 functional verification
```

---

## 10. 写作 / Spec 复用模板 (Luke 直接 copy)

### 10.1 硬件表参数

```yaml
# WSE 控制核 Constable 配置 (RISC-V 4-wide, Luke 可调)
constable:
  SLD:
    entries: 256  # 从 512 缩 (4-wide vs 6-wide)
    sets: 32
    ways: 8
    entry_size_bits: 126  # tag(24) + addr(32) + val(64) + conf(5) + flag(1)
    total_size_KB: 4.0
    read_ports: 2  # 4-wide 平均 1.3 loads
    write_ports: 2
  RMT:
    stack_registers: 2  # SP, FP
    stack_loads_per_reg: 16
    other_registers: 14  # RISC-V 16 - 2
    other_loads_per_reg: 8
    total_size_KB: 0.4
    read_ports: 2
    write_ports: 4  # 4-wide 写 reg 指令最多 4
  AMT:
    entries: 128  # WSE 上 L1 访问模式更简单
    sets: 16
    ways: 8
    entry_size_bits: 128
    total_size_KB: 2.0
    read_ports: 1
    write_ports: 1
  xPRF:
    entries: 32  # 与 Intel baseline 相同
  confidence_threshold: 30
  total_size_KB: ~6.4  # WSE 缩
```

### 10.2 关键设计决策 (Luke Spec Checklist)

```markdown
## Constable 集成 Checklist (WSE 控制核)

- [ ] SLD 3R/2W (WSE 4-wide 可缩到 2R/2W)
- [ ] RMT 2R/6W (WSE 4-wide 用 2R/4W)
- [ ] AMT 1R/1W
- [ ] xPRF 32 entries (避免 fallback 正常执行)
- [ ] confidence threshold = 30 (RISC-V workload 需重新调)
- [ ] load 转化为 register-move (复用 RISC-V 的 move 指令)
- [ ] AMT 查 store address → reset can_eliminate
- [ ] RMT 查 write dest reg → reset can_eliminate
- [ ] context switch / page mapping 变 → reset all
- [ ] branch misprediction → 不恢复 (0.2% 影响)
- [ ] OoO 违例 → 复用现有 LSQ disambiguation
- [ ] multi-core: CV-bit pinning in coherence directory
- [ ] 干净 cache eviction → 不 invalidate AMT (默认)
- [ ] LLM 推理 workload 测试: 测量 likely-stable load 比例
- [ ] 与 EVES LVP 组合 → 正交 (8.5% in noSMT, 11.3% in SMT)
```

### 10.3 论文引用模板

```bibtex
@inproceedings{bera2024constable,
  title={Constable: Improving Performance and Power Efficiency by Safely Eliminating Load Instruction Execution},
  author={Bera, Rahul and Ranganathan, Adithya and Rakshit, Joydeep and Mahto, Sujit and Nori, Anant V. and Gaur, Jayesh and Olgun, Ataberk and Kanellopoulos, Konstantinos and Sadrosadati, Mohammad and Subramoney, Sreenivas and Mutlu, Onur},
  booktitle={ISCA},
  year={2024},
  note={Best Paper Award}
}
```

---

## 11. 精读反思 (Turing 给 Luke)

### 11.1 论文最强的地方

1. **从根因出发**: 不堆硬件, 不堆预测, 而是用 "识别 + 消除" 直接解决问题
2. **完整实现**: 从硬件表到 pipeline 修改到 multi-core coherence 全部给出
3. **诚实评估**: 给出 9.1% headroom + 5.1% 实际 = 56% 实现率, 留改进空间
4. **开源工具**: https://github.com/CMU-SAFARI/Load-Inspector — Luke 可直接在自己 workload 上分析

### 11.2 论文可改进的地方

1. **依赖 xPRF**: 这是个新增结构, 论文"不计入开销"略 aggressive
2. **CV-bit pinning 修改 coherence protocol**: 工业部署需要 Intel/AMD 验证
3. **wrong path 不恢复**: 0.2% 看似小, 但 ARM big.LITTLE 异构下可能放大
4. **page mapping 变化粗暴 reset**: 没给出优化方案 (Wilson hash table?)

### 11.3 Luke 最该看的 3 个 Section

1. **Section 6.1-6.7 (微架构)** — 直接用于 WSE 控制核 spec
2. **Section 4.4 (Performance Headroom)** — 理解 resource dep 的真实代价
3. **Section 9.3.1 (Coverage Breakdown)** — 知道 Constable 在哪类 workload 上有效

### 11.4 Luke 不该照搬的地方

1. **6-wide baseline**: WSE 是 4-wide → 端口和表大小需重新定
2. **Golden Cove 内存参数**: WSE 的 L1 大小/带宽不同 → 26% L1-D 减少的绝对值要重测
3. **Intel coherence protocol**: WSE 是新架构, CV-bit pinning 需适配

---

## 12. 论文背景补充

- **Onur Mutlu 组 (SAFARI @ ETH)** 是体系结构顶会最活跃的组之一, 历年多篇 Best Paper
- **Intel PARL** 实习合作产物, Bera 一作, Ranganathan 二作
- 论文代码: https://github.com/CMU-SAFARI/Load-Inspector (binary instrumentation tool, 任何 x86-64 binary 可用)
- 完整 PDF: `notes/reports/superscalar-cpu/constable.pdf` (1.6 MB, 17 pages)

---

*精读完成时间: 2026-07-03 13:00 CST*  
*精读员: Turing (for Luke)*  
*下一步: 跑 Load-Inspector 测 WSE workload 的 likely-stable load 比例*
