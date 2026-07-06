---
type: Raw Source
title: Superscalar CPU 研究综述 (2023-2026)
source_path: /home/luke/openclawdata/workspace-research/notes/reports/superscalar-cpu/03-report.md
ingested: 2026-07-03
---

# Superscalar CPU 研究综述 (2023-2026)

> 角色: Writer
> 基础: 02-analysis.md (深度分析)
> 修订: 2026-07-03 (Iteration 2 - REVISE_REPORT)
> 读者: Luke - 体系结构研究员

## 修订历史
- **v2 (2026-07-03)**: 修订 Critic P0/P1 建议
  - P0-1: AVM-BTB 显式降级为"未深分析"
  - P0-2: 5 条 Insights 标注性质 (🔁/🔀/💡)
  - P0-3: 核内同步 Gap 加负面论证 (02-analysis 同步更新)
  - P1-1: 关联矩阵加具体步骤
  - P1-2: Prophet 节补 Triangel 简述 (02-analysis 同步更新)
  - P1-3: Apple M1 RE 关联度降为 ⭐
- **v1 (2026-07-03)**: 初版

---

## 一句话总结

**2023-2026 超标量 CPU 研究的主线是"用异构旁路子系统 + 软硬件协同消除/跳过无效访问"，而非传统"堆容量、挖 ILP"——LLM 推理的 memory-bound 特性把 load 消除、时序预取、前端 H2P 推到顶会中心，RISC-V 工业级超标量核 (CVA6S+) 已可用作可控 baseline。**

---

## 研究背景

### 为什么超标量 CPU 在 2026 年仍然重要

- **NPU/GPU 不替代 CPU**：矩阵乘之外的控制流、稀疏访存、操作系统、Spectre 防护仍依赖超标量核。Apple M-series、AMD Zen、Intel Lion Cove 都在持续迭代。
- **RISC-V 工业化**：CVA6S+ (OpenHW Group + ETH) 证明开源 RISC-V 也能做出 +43.5% IPC 提升的工业级超标量核。
- **LLM 时代新角色**：CPU 跑 LLM 推理 (token 生成、speculative decoding host) 重新变成 memory-bound 优化主战场。
- **安全驱动透明度**：Spectre 之后，学术界开始用侧信道反向工程商业核 (Apple M1 RE)，倒逼微架构设计文档化。

### 四大挑战 (业界共识)

| 挑战 | 现象 | 代表性缓解 |
|------|------|-----------|
| **内存墙** | 算力增速 >> DRAM 带宽增速 | Constable 消除 load、Prophet 时序预取 |
| **前端墙** | TAGE-SC-L 自 2016 年仍是工业基线，剩余 mispredict 集中在 H2P | Bullseye HIT + 双感知器 |
| **能耗墙** | Dynamic frequency 边际收益递减，dark silicon 出现 | 减少执行 (Constable -3.4% 动态功耗) |
| **安全墙** | Spectre v1 / out-of-place mistraining 仍是威胁 | Apple M1 RE 显示商业核需 partial mitigations |

---

## 技术演进时间线

### 2023 (Gap) 
HPCA/MICRO 2023 是"AI 加速器主导"年，超标量 CPU 微架构论文相对稀少。

### 2024 (突破年)
- **Q2 ISCA**: **Constable (Best Paper Award)** ⭐ — load 消除重新成为顶会中心话题 (上次是 2017 年 value prediction 类)
- **Q2 ISCA**: AVM-BTB (Session 1A) — 多租户 BTB 隔离进入顶会 [未深分析 — 详见"未深分析"节]
- **Q4 MICRO**: "The Last-Level Branch Predictor" (Arm Research + Edinburgh) — Arm 公开 LLBP 设计细节

### 2025 (协同设计主流化)
- **Q1 HPCA**: "Architecting Value Prediction around In-Order Execution" (Kalray/Perais) — VP 思路延伸至 in-order 核
- **Q2 ISCA (Tokyo)**:
  - Bullseye (CBP-2025 workshop, UBC) — 异构子系统 + H2P 专用感知器
  - Prophet (Session 4B, HKUST + Intel) — Profile-guided 软硬件协同时序预取
- **Q2 ISCA**: CVA6S+ 论文投递 (arXiv 2025-04/05 预印本)

### 2026 展望
- **预测 1**: WSE 专用 LLM 推理核进入主流 (Cerebras WSE-3 已先行)
- **预测 2**: Apple M3/M4 RE 论文出现 (侧信道研究持续推进)
- **预测 3**: RISC-V 工业超标量核 (SiFive P870, Andes, Tenstorrent) 与 CVA6S+ 路径竞争
- **预测 4**: Constable 风格"value elimination"扩展到 branch/store elimination

---

## 核心方案分类

> ⚠️ **方法分类原则**: 本节仅纳入"经精读、有可信数字"的论文。**AVM-BTB 因全文不可访问，不作为方法类别**，单列"未深分析"节。

### 类别 1: 微架构优化 (数据通路)

| 论文 | 核心思想 | 关键数字 | 优 | 缺 |
|------|---------|---------|---|---|
| **Constable** (ISCA'24 Best Paper) | 动态识别 likely-stable load，依赖未变时**完全跳过 load 执行** (不占 LSQ/issue port/ROB) | **+5.1% perf / -3.4% 动态功耗** (基础 baseline 含 MRN+move-elim)；2-way SMT 下 **+8.8%**；与 EVES LVP 组合再 +3.7% | 轻量改、5% 几乎免费、与 LVP 正交 | 只对 stable 访问有效；硬件开销数字 [待验证] |

**Luke 复用路径**: LLM 推理 KV cache 访问高度规律 → 直接移植 likely-stable 思路到 LLM 核。

---

### 类别 2: 前端优化 (分支预测)

| 论文 | 核心思想 | 关键数字 | 优 | 缺 |
|------|---------|---------|---|---|
| **Bullseye** (CBP-2025) | TAGE-SC-L 旁加 H2P 识别表 (HIT) + 双感知器；H2P PC 停止更新 TAGE 避免污染 | 187 KB 总预算 (159 KB TAGE + 28 KB H2P)；MPKI **3.4045** | 主表不增、并行运行、动态阈值 | vs 纯 TAGE baseline 的 MPKI 减少 [待验证] |
| **Apple M1 RE** (arXiv 2025-02) | 侧信道驱动反向工程 Apple M1 BPU；发现 M1 有 **partial cross-ASID mistraining mitigations** | N/A (RE 类) | 公开文献中**唯一**对 Apple 商业核 BP 的实证 | 仍基于 TAGE 假设；M2/M3/M4 未验证 [待验证]；**非 Luke 安全研究主线** |

**Luke 复用路径**:
- Bullseye: 28 KB H2P 子系统是 WSE 小核前端"小面积+高精度"蓝图
- Apple M1 RE: 仅作工业微架构参数参考 (BP entries/set, history length 等)，不深入安全研究

---

### 类别 3: 内存子系统

| 论文 | 核心思想 | 关键数字 | 优 | 缺 |
|------|---------|---------|---|---|
| **Prophet** (ISCA'25 Session 4B) | Profile-guided hints 注入 + counter-based profile + 与现有硬件预取器协同；相比 Triangel 改进 on-chip metadata 利用率 | **+14.23% perf** vs state-of-the-art **Triangel** (ISCA'24 on-chip metadata 预取器)；对先前 profile-guided 失败的复杂时序模式仍有效 (vs 0.1%) | 软硬件协同；profile 开销可忽略 | 需重编译/注入 hints；纯 pointer-chasing 可能仍不足 [推测] |
| **CVA6S+ HPDCache** (集成模块) | 集成 OpenHW Core-V HPDCache | **+74.1% L1 带宽** vs legacy CVA6 cache | 开源、NPU 数据供给关键 | 与商业 cache (SiFive, Andes) 缺横向对比 |

**Luke 复用路径**:
- Prophet: profile-guided 思路迁移到 WSE 跨芯片 (inter-mesh) 预取
- HPDCache: GEMM tile 数据供给直接受益

---

### 类别 4: 工业参考实现

| 论文 | 核心思想 | 关键数字 | 优 | 缺 |
|------|---------|---------|---|---|
| **CVA6S+** (arXiv 2025-04) | 改进 BP + 增强寄存器重命名 + 增强操作数转发 + 集成 HPDCache | **+43.5% IPC** vs 标量 CVA6；**+10.9% IPC** vs 已有 CVA6S；**9.30% 面积**开销 | 工业级开源 RISC-V、面积效率优秀 | **3 页 short paper** [待精读验证]；无商业 RISC-V (SiFive/Andes) 横向对比 |

**Luke 复用路径**: CVA6S+ 是 WSE 控制核最直接的可 fork 开源 baseline。

---

### 类别 5: 未深分析 (Top 5 提名保留)

| 论文 | 状态 | 原因 | Luke 关联 |
|------|------|------|----------|
| **AVM-BTB** (ISCA'24 Session 1A) | ❌ **未深分析** | 无 arXiv preprint；ISCA 2024 proceedings PDF 全文未访问 (DOI: 10.1145/3695053.3730996 [推测])；所有数字 [待验证] | 仅作 WSE 多租户场景的**方向性参考**，不进入方法分类 |

**何时补全**: 待 ISCA 2024 proceedings PDF 全文获取后，由 Critic/Analyst 优先精读。

---

## 关键 Insights (5 条，跨论文)

> 每条 Insight 顶部标注**性质**，帮助 Luke 判断"复用已有方法"vs"新研究提案"的可信度：
> - 🔁 **复用已知方法** — 直接搬过来用
> - 🔀 **组合已有方法** — 把 A 和 B 组合
> - 💡 **新研究提案** — 这是新方向，需要验证

### Insight 1: 🔀 **组合** — "用旁路子系统解决主表退化"是新范式

- **现象**: Constable 用 likely-stable tracker 旁路主调度、Bullseye 用 HIT 表旁路 TAGE、Prophet 用 hints 旁路 metadata 存储 — 三篇都在说同一件事。
- **重要性**: 主硬件资源已饱和，再用"加大"思路边际收益递减。**正确做法是识别"特殊情况"并用低成本专用子系统处理**。
- **对 Luke 启发**: WSE 上任何子模块 (NoC 路由、前端 BP、内存控制器) 都应优先考虑"旁路子系统"架构而非"加大容量"。
- **复用方式**: WSE NoC 路由器可加"high-fanout 旁路缓存"；前端 BP 加"H2P 旁路" (Bullseye-style)；L2 预取器加"pattern-based 旁路"。
- **性质解释**: 组合 Constable/Bullseye/Prophet 三者方法 + Luke 在 WSE 上的复用。

### Insight 2: 🔁 **复用** — 开源 + 工业双轨已成熟，但商业核仍是黑盒

- **现象**: CVA6S+ (开源 RTL) + Apple M1 RE (商业闭源逆向) 是同一研究问题的两面。
- **重要性**: Luke 能从 CVA6S+ 拿到 RTL 级代码、从 Apple M1 RE 拿到硬件参数 — **两边结合才是研究工业核微架构的最优路径**。
- **对 Luke 启发**: WSE 控制核设计应:
  1. 优先 fork **CVA6S+** 作 baseline (开源、可改)
  2. 用 Apple M1 RE + AMD Zen 白皮书 + Intel patents 做工业参数校准
  3. 仿真器用"实际参数"而非"学术假设"
- **复用方式**: 仿真平台优先选 CVA6S+ fork，参数标定以 M1 RE 为锚点。
- **性质解释**: 直接 fork CVA6S+ + Apple M1 RE 参数，无新方法创新。

### Insight 3: 🔀 **组合** — 内存子系统 + 前端 是真正瓶颈，OoO 深度已边际饱和

- **现象**: Constable (load 消除) + Bullseye (前端 H2P) + Prophet (时序预取) 三篇都指向同一现象。**继续扩大 ROB/issue queue 收益已微**。
- **重要性**: 论文开始从"减少访问"和"减少 stall"角度突破。这是工业界 (Apple M3/M4, AMD Zen 5) 真实方向 — Zen 5 仍维持 6-wide issue 但加大前端 prefetch 与 L2 带宽。
- **对 Luke 启发**: WSE 控制核设计应**保守 OoO 深度** (例如 4-wide issue, ROB ≤ 256) 而**激进前端** (大 BTB/BP + Prophet-style 预取) + **激进内存子系统** (HPDCache-style 高带宽 L1)。
- **复用方式**: 这套组合是当前性价比最高的设计选择，Luke 应在 spec 阶段就定下"4-wide + 大前端 + 大 L1 带宽"基调。
- **性质解释**: 论文证据 + 工业事实 (Zen 5) 的组合推论。

### Insight 4: 💡 **提案** — LLM 推理催生"memory-bound 优化"复兴

- **现象**: Constable (load 消除) + Prophet (不规则访存预取) + Intel/AMD 的 NPU+CPU 分工 — 都在说"memory-bound 是 LLM 时代主战场"。
- **重要性**: 2025 年 LLM 推理优化已不只是 KV cache + quantization — 硬件侧也开始专门优化。**Constable 直接给 WSE 上的 LLM 推理核提供硬件思路**。
- **对 Luke 启发**: WSE 天然优势是"内存就在边上" — Luke 应研究 **"WSE 上 LLM 推理核的专用 ISA"** 或 **"专用 LLM prefetcher"**。
- **复用方式**: 把 Constable 的 likely-stable tracker 移植到 LLM 推理核 (KV cache attention score reuse 场景)。
- **性质解释**: "WSE 上 LLM 推理核的专用 ISA"是新研究方向，非 Constable 直接复用。

### Insight 5: 💡 **提案** — 安全研究反向推动硬件透明度

- **现象**: Apple M1 RE 表明学术界正通过侧信道攻击"反向工程"商业核。Spectre/Meltdown 之后的持续趋势。
- **重要性**: 未来可能扩展到 NVIDIA Hopper/Blackwell、Apple M3/M4 等新一代核。**透明 vs 黑盒是研究型 vs 产品型 CPU 的分水岭**。
- **对 Luke 启发**: WSE 设计应**把"微架构透明度"作为差异化优势** — 开源 RTL + 公开 BP/L1/L2 参数。这与 Cerebras 当前"黑盒"路线相反，但能吸引学术合作 (类似 RISC-V 成功)。
- **复用方式**: 在 WSE 控制核 spec 中明确"开源 BP 设计与参数文档化"作为对外学术合作卖点。
- **性质解释**: WSE 差异化优势是战略建议，非已知方法复用。

---

## 未解决问题 (Open Questions)

1. **AVM-BTB 真实性能数字**？论文无 arXiv，ISCA 2024 全文未访问；多租户 BTB 隔离对 WSE 跨 mesh BPU 共享的实际收益未知 — **本综述已将其降级为"未深分析"**。
2. **Constable 硬件开销精确数字**？摘要未给面积/功耗详细拆分；与 baseline 配置强耦合，跨研究对比困难。
3. **RISC-V 阵营的 BP 安全研究空白**？Apple M1 RE 显示 TAGE 容易被攻击，CVA6S+ 等 RISC-V 核的 Spectre 类威胁评估几乎缺位 — 商业核未公开、RISC-V 核未受关注。
4. **WSE 上分支预测器的特殊设计**？6 篇论文都假设"单芯片 + 有限核数"前端设计；WSE"大量小核共享前端"是新场景，缺乏针对性论文。
5. **AI 训练侧的微架构瓶颈**？6 篇都关注 inference (memory-bound) 或传统 workload；训练侧 (compute-bound + gradient sync) 的微架构瓶颈未被深入研究。
6. **核内同步方向的微架构优化**？6 篇论文均未涉及 LR/SC/AMO；**且负面论证指出 Constable 思路未必直接适用** (cache coherence 主导失败模式 ≠ load 失败模式)。真正可行的方向 (SC retry 预测、LR 预取、PAUSE hint) 均为**推测性**，需仿真验证。

---

## 未来方向

### 短期 (1-2 年)
- **WSE-aware Constabulary**: 把 Constable 思想扩展到 WSE — 不是"跳过 load"而是"跳过远程 mesh 访问"。当 NoC 跳数代价 > 本地访存时，跳过远端 load 直接用 cached value。
- **CVA6S+ + Bullseye 集成**: 在 RISC-V 上集成 Bullseye 风格 HIT + 双感知器，评估 RISC-V 实际能拿到的精度增益 (CVA6S+ 3 页 short paper 的扩展方向)。
- **RISC-V Secure TAGE**: 把 Morrison 的搜索空间缩小技术移植到 RISC-V BP — 填补 RISC-V 安全研究空白。

### 中期 (3-5 年)
- **Apple M-style BTB for WSE**: 基于 Morrison 论文的 TAGE 参数 + WSE 多核共享前端需求，设计 WSE 专用 BTB (Bullseye + AVM-BTB 思路融合)。
- **LLM 推理微架构 Benchmark**: 当前没有标准 benchmark 评估 CPU 微架构优化对 LLM 推理的影响。Luke 可推动建立 "LLMCPU-Mark"。
- **Tightly-coupled NPU dispatch**: 研究 CPU 核如何与 NPU 核交互时的微架构开销 (矩阵指令 dispatch、tile 状态同步)；用 Constable-style elimination 减少 NPU 指令的 load stalls。

---

## 与 Luke 研究的关联

| Luke 方向 | 关联论文 | 关联强度 | 关键复用点 + **具体步骤** |
|----------|---------|---------|-------------------------|
| **超标量 CPU 核** | Constable, CVA6S+, Bullseye | ⭐⭐⭐ 强 | (1) **Constable likely-stable tracker**: 在 gem5 中复刻 likely-stable 识别 + dirty tracker 模块，用 SPEC CPU 2017 trace 验证是否能复现 +5% (2) **CVA6S+**: 直接 git clone OpenHW CVA6 仓库，checkout CVA6S+ 分支，作为 WSE 控制核 baseline (3) **Bullseye HIT 表**: 在 CVA6S+ 之上加 28 KB H2P 子系统，运行 CBP-2016 trace 测 MPKI 减少 |
| **NPU 核** | CVA6S+, Prophet | ⭐⭐ 中 | (1) **HPDCache**: 把 CVA6S+ 集成的 HPDCache 移植到 NPU 控制核，验证 GEMM tile 数据供给是否真的受益 (+74.1% L1 带宽是否在 NPU 工作负载下成立待验证) (2) **Prophet profile-guided**: 用 NPU weight reuse profile 注入 hints 到预取器，类比 Prophet 思路 |
| **Wafer Scale Engine** | AVM-BTB (未深分析), Constable, Prophet | ⭐⭐⭐ 强 | (1) **AVM-BTB 思路** (方向性参考): 待 ISCA 2024 全文访问后，提取多租户 BTB 隔离的具体机制 (2) **Constable 扩展**: 在 WSE 上实现 "WSE-aware Constabulary" — 跳过远程 mesh 访问而非本地 load，需 NoC 跳数感知的依赖追踪 (3) **Prophet 思路迁移**: 用 profile-guided hints 优化 WSE 跨 mesh 预取，metadata 存在 fabric 上的分布式 SRAM |
| **LLM 体系结构** | Constable, Apple M1 RE, Prophet | ⭐⭐⭐ 强 | (1) **Constable → LLM 核**: 在 LLM 推理核中加 likely-stable tracker，针对 KV cache attention score reuse 模式 (2) **Apple M1 BP 参数校准**: 在 gem5 中用 RE 论文附录的 BTB entries per set / history length 替换 LLM 核默认参数，运行 LLM inference trace 验证预测精度 (3) **Prophet 优化 KV cache 预取**: 为 KV cache 访问模式生成 profile-guided hints，结合 RadixAttention 的访问统计，注入到 Prophet 兼容的 binary 中 |
| **核内同步** | ⚠️ **无直接论文** | ❌ **Gap** + ⚠️ **负面论证** | (1) 6 篇论文均未涉及 LR/SC/AMO 微架构优化 (2) **Constable 思路未必直接适用** — LR/SC 失败模式由 cache coherence 主导 ≠ load 失败模式 (3) 可尝试方向 (推测性): **SC retry 预测** (用 perceptron 预测 SC 失败概率，提前 abort) / **LR 预取** / **PAUSE hint 增强**；均需 gem5 仿真验证 |

---

## 行动建议

Luke 接下来可以：

1. **精读 Constable 全文 (Section 5 + 7)** — 验证 likely-stable tracker 精确硬件开销、敏感性研究
   - **理由**: Constable 是本综述最强基线方法 (ISCA'24 Best Paper)；Luke 在 WSE 控制核 + LLM 推理核两条线都要直接复用
   - **预计耗时**: 2-3 小时 (精读 + 笔记)
   - **产出**: 一份"Constable 微架构改动 checklist"用于 WSE spec

2. **Fork CVA6S+ 并跑通仿真 baseline** — 在 WSE 仿真器中集成 HPDCache + 评估 Bullseye H2P 子系统加成
   - **理由**: CVA6S+ 是 Luke 最直接可用的开源工业 baseline；Bullseye 是 WSE 前端的"现成解决方案"
   - **预计耗时**: 1-2 周 (含 RTL 集成 + 仿真)
   - **产出**: WSE 控制核 spec 初稿 + 仿真数据 baseline

3. **抓 ISCA 2024 AVM-BTB proceedings PDF** — 补全多租户 BTB 隔离的真实性能/面积数据
   - **理由**: AVM-BTB 是 WSE 多租户场景最直接相关的论文，目前所有数字 [待验证]；Luke 写论文时需精确引用
   - **预计耗时**: 0.5-1 天 (DOI: 10.1145/3695053.3730996 [推测])
   - **产出**: AVM-BTB 详细参数表

4. **探索"核内同步"研究 gap — 但需先验证 Constable 思路是否适用** — 在 gem5 中做"baseline LR/SC 行为 profile"，判断 SC retry 失败模式是否真的可预测
   - **理由**: 6 篇论文中无一篇直接讨论 LR/SC/AMO 微架构优化；负面论证指出 Constable 思路可能不直接适用，需先做 profile 再设计
   - **预计耗时**: 1-2 周 (profile + 方案初稿)
   - **产出**: 一份 "LR/SC 失败模式 profile 报告" + research proposal 草稿

---

## 参考论文

| # | 标题 | 会议/年份 | arXiv/DOI | 一句话贡献 | 与 Luke 关联度 |
|---|------|----------|----------|-----------|---------------|
| 1 | **Constable**: Likely-Load-Aware Store-Load Forwarding | **ISCA 2024 Best Paper Award** ⭐ | arXiv:2406.18786 / DOI:10.1145/3695053.3731015 | Likely-stable load 完全跳过执行: +5.1% perf, -3.4% 动态功耗 | ⭐⭐⭐ (LLM 推理 + WSE + 超标量核) |
| 2 | **CVA6S+**: 工业级 RISC-V 超标量变体 | arXiv 2025-04/05 (预期 ISCA/MICRO 2025) | arXiv:2505.03762 | BP + 重命名 + 转发 + HPDCache 集成: +43.5% IPC vs 标量 CVA6, +10.9% vs CVA6S | ⭐⭐⭐ (RISC-V 开源 baseline + NPU 带宽) |
| 3 | **Bullseye Predictor**: H2P 专用感知器旁路 TAGE | **CBP-2025** (ISCA 2025 co-held) | arXiv:2506.06773 | HIT 表 + 双感知器 + TAGE 更新抑制: 187 KB 总预算, MPKI 3.4045 | ⭐⭐⭐ (WSE 前端小面积高精度) |
| 4 | **AVM-BTB**: 自适应虚拟化多级 BTB | **ISCA 2024 Session 1A** | 无 arXiv / DOI: 10.1145/3695053.3730996 [推测] | 多级 BTB + ASID/VMID 租户隔离 + 自适应替换 [未深分析] | ⭐⭐ (WSE 多租户方向参考) |
| 5 | **Apple M1 Conditional Branch Predictor RE** | arXiv 2025-02 | arXiv:2502.10719 | 反向工程 M1 BPU + 发现 partial cross-ASID mitigations | ⭐ (Apple 工业参考 + 安全，非 Luke 主线) |
| 6 | **Prophet**: Profile-Guided Temporal Prefetching | **ISCA 2025 Session 4B** | arXiv:2506.15985 | Profile-guided hints + 协同调度: +14.23% vs Triangel | ⭐⭐ (WSE 片间预取 + LLM KV cache) |

---

## 已知局限 (诚实标注)

1. **AVM-BTB 全部数字 [待验证]** — 无 arXiv，ISCA 2024 全文未访问；**本综述 v2 已将其降级为"未深分析"**，不进入方法分类
2. **CVA6S+ 细节 [待精读]** — 是 3 页 short paper，BTB 大小、rename table 拓扑等需查后续 ISCA/MICRO 全文
3. **Constable/Bullseye/Prophet vs baseline 百分比 [待验证]** — 摘要给主指标，缺与 baseline 直接对比
4. **Apple M1 RE 具体参数 [待验证]** — 摘要说"reverse engineer M1 BPU parameters"但未列出具体数字；**已降级为 Luke 关联度 ⭐，非主线**
5. **核内同步方向无直接论文 + Constable 思路未必适用** — 6 篇论文均未涉及 LR/SC/AMO 微架构优化；**02-analysis 已加负面论证** (cache coherence 主导失败模式 ≠ load 失败模式)
6. **5 条 Insights 中含 2 条研究提案** — Insight 4 (WSE LLM 推理核专用 ISA) 和 Insight 5 (WSE 微架构透明度战略) 为新研究方向，非已知方法复用；Luke 应按"提案"对待

---

> **Writer 备注 (v2)**:
> - 本报告完全基于 Analyst 的 02-analysis.md 整合 + Critic 的 P0/P1 修订建议
> - 关键数字 (+5.1%, +43.5%, +14.23%, MPKI 3.4045, -3.4% 动态功耗, +74.1% L1 带宽) 全部保留并标注
> - [待验证] 标注一律保留，未假装 Analyst 已确认
> - **P0 全部完成**: AVM-BTB 显式降级 + 5 Insights 标注性质 + 核内同步 Gap 加负面论证
> - **P1 全部完成**: 关联矩阵加具体步骤 + Prophet 节补 Triangel 简述 (02-analysis) + Apple M1 RE 关联度降为 ⭐
> - 关联 Luke 研究方向时**诚实标注 Gap** (核内同步方向无直接论文 + 负面论证)
> - 报告结构、表格、emoji 均按要求增强可读性
> - 长度目标 1500-2500 字 (实际 ~2400 字)