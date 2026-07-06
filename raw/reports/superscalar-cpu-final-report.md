---
type: Raw Source
title: Superscalar CPU 研究综述 — 最终报告
source_path: /home/luke/openclawdata/workspace-research/notes/reports/superscalar-cpu/FINAL-report.md
ingested: 2026-07-03
---

# Superscalar CPU 研究综述 (2023-2026) — 最终报告

> **研究流程**: Scout → Analyst → Writer → Critic (7.7/10) → Writer v2 (8.2-8.4/10) → APPROVED
> **研究时间**: 2026-07-03
> **执行模型**: minimax/MiniMax-M3 (Orchestrator 协调)
> **位置**: `notes/reports/superscalar-cpu/`

---

## 📊 流程总览

| Phase | 角色 | 输出 | 状态 |
|-------|------|------|------|
| 1 | Scout | `01-papers.md` (13 候选 + 5 趋势) | ✅ |
| 2 | Analyst | `02-analysis.md` (6 篇深度 + 5 insights + 5 gaps) | ✅ |
| 3 | Writer | `03-report.md` (~2300 字综述) | ✅ v1 + v2 |
| 4 | Critic | `04-review.md` (7.7/10 → REVISE_REPORT) | ✅ |
| 5 | Writer v2 | `03-report.md` (P0/P1 全部完成) | ✅ |

**迭代次数**: 2 (一次 Critic 反馈 → Writer 修订)
**最终综合评分**: **8.2-8.4/10** (Analyst 8.2 + Report 8.5 + Luke 关联 8.0)

---

## 🎯 一句话总结

**2023-2026 超标量 CPU 研究的主线是"用异构旁路子系统 + 软硬件协同消除/跳过无效访问"，而非传统"堆容量、挖 ILP"——LLM 推理的 memory-bound 特性把 load 消除、时序预取、前端 H2P 推到顶会中心，RISC-V 工业级超标量核 (CVA6S+) 已可用作可控 baseline。**

---

## 📁 完整产出

| 文件 | 大小 | 内容 |
|------|------|------|
| `01-papers.md` | 14 KB | 13 篇候选论文 + 5 条趋势 + Top 5 推荐 |
| `02-analysis.md` | 32 KB | 6 篇论文深度分析 (含 arXiv ID 校正) + 5 个跨论文 insight + 5 个研究 gap |
| `03-report.md` | 22 KB | ~2300 字结构化综述 (含 P0/P1 修订) |
| `04-review.md` | 14 KB | Critic 详细评审 (7.7/10 + 11/11 数据核验通过) |
| `FINAL-report.md` | (本文件) | 最终汇总 + 行动建议 |

---

## 🔑 核心洞察 (5 条 + 性质标注)

### Insight 1: 🔀 **组合** — "用旁路子系统解决主表退化"是新范式
Constable 用 likely-stable tracker 旁路主调度、Bullseye 用 HIT 表旁路 TAGE、Prophet 用 hints 旁路 metadata — 异构子系统是 2024-2026 微架构设计的统一答案。

### Insight 2: 🔁 **复用** — 开源 + 工业双轨结合 = 研究工业核最优路径
CVA6S+ (开源 RTL) + Apple M1 RE (商业逆向) 是同一研究问题的两面 — 优先 fork CVA6S+ + 用 M1 RE 校准参数。

### Insight 3: 🔀 **组合** — 内存子系统 + 前端 是真正瓶颈，OoO 深度边际饱和
继续扩大 ROB/issue queue 收益已微; Zen 5 仍维持 6-wide issue 但加大前端 prefetch 与 L2 带宽。

### Insight 4: 💡 **提案** — LLM 推理催生"memory-bound 优化"复兴
Constable + Prophet + NPU+CPU 分工都指向 memory-bound 优化; WSE 天然优势 → 研究 "WSE 上 LLM 推理核专用 ISA"。

### Insight 5: 💡 **提案** — 安全研究反向推动硬件透明度
WSE 应把"微架构透明度"作为差异化优势 — 开源 RTL + 公开 BP/L1/L2 参数。

---

## 📚 Top 5 论文 (经 arXiv 验证)

| # | 论文 | 会议 | 核心数字 | Luke 关联 |
|---|------|------|---------|----------|
| 1 | **Constable** | **ISCA 2024 Best Paper** ⭐ | +5.1% perf / -3.4% 动态功耗 / +8.8% SMT | ⭐⭐⭐ LLM + WSE + 超标量核 |
| 2 | **CVA6S+** | arXiv 2025 (ISCA/MICRO 预期) | +43.5% IPC vs scalar / +10.9% vs CVA6S | ⭐⭐⭐ RISC-V 开源 baseline |
| 3 | **Bullseye Predictor** | CBP-2025 (ISCA co-held) | 187 KB 总预算 / MPKI 3.4045 | ⭐⭐⭐ WSE 前端小面积高精度 |
| 4 | **AVM-BTB** ⚠️ | ISCA 2024 | [待验证 — 全文不可达] | ⭐⭐⭐ WSE 多租户 (降级) |
| 5 | **Prophet** | ISCA 2025 | +14.23% vs Triangel | ⭐⭐ WSE 片间预取 + KV cache |
| 附 | Apple M1 RE | arXiv 2025-02 | RE 类 / 非 Luke 主线 | ⭐ (已降级) |

**数据准确性**: 11/11 核心数据已通过 arXiv/官方页面交叉验证 (Critic 复核) ✅

---

## 🔗 Luke 研究的关联矩阵 (4 方向强关联 + 1 Gap)

| Luke 方向 | 关联论文 | 关键复用点 (含具体步骤) |
|----------|---------|------------------------|
| **超标量 CPU 核** | Constable, CVA6S+, Bullseye | (1) Constable likely-stable tracker 移植到 WSE 控制核 (2) `git clone openhwgroup/cva6s` 作为 baseline (3) Bullseye HIT 表 (28KB) + 双感知器集成 |
| **NPU 核** | CVA6S+, Prophet | (1) HPDCache (+74.1% L1 带宽) 用作 NPU 数据供给 (2) Prophet profile-guided hints 移植到 weight reuse 优化 |
| **Wafer Scale Engine** | AVM-BTB, Constable, Prophet | (1) AVM-BTB 多租户 BTB 隔离迁移到 WSE 跨 mesh BPU 共享 (2) Constable 消除 load = 省 NoC 跳 (3) Prophet profile-guided → WSE 片间预取 |
| **LLM 体系结构** | Constable, Prophet | (1) Constable likely-stable 复用 KV cache (2) gem5 中用 Prophet profile-guided 替换默认 L2 预取器 |
| **核内同步** | ⚠️ **Gap + 负面论证** | (1) Constable 思路迁移有 4 点障碍 (LR/SC vs load 失败模式差异) (2) 推测性方向: perceptron 预测 SC 失败 / LR 预取 / PAUSE hint |

---

## 🎯 行动建议 (4 条优先级排序)

### 1. 精读 Constable 全文 ⭐⭐⭐
- **理由**: ISCA 2024 Best Paper，Luke 在 WSE 控制核 + LLM 推理核两条线都要直接复用
- **目标**: 验证 likely-stable tracker 精确硬件开销、Section 7 敏感性研究
- **耗时**: 2-3 小时
- **产出**: "Constable 微架构改动 checklist" 用于 WSE spec

### 2. Fork CVA6S+ + 跑通仿真 baseline ⭐⭐⭐
- **理由**: Luke 最直接可用的开源工业 baseline
- **具体步骤**:
  - `git clone https://github.com/openhwgroup/cva6s`
  - 集成 HPDCache (OpenHW Core-V)
  - 在 gem5 中跑 CoreMark/MiBench 评估 Bullseye H2P 子系统加成
- **耗时**: 1-2 周
- **产出**: WSE 控制核 spec 初稿 + 仿真 baseline

### 3. 抓 ISCA 2024 AVM-BTB proceedings PDF
- **理由**: 补全多租户 BTB 隔离的真实性能/面积数据
- **DOI**: 10.1145/3695053.3730996 (推测, 待验证)
- **耗时**: 0.5-1 天
- **产出**: AVM-BTB 详细参数表

### 4. 探索"核内同步 + Constable-style elimination" Gap
- **理由**: 6 篇论文中无一篇直接讨论 LR/SC/AMO 微架构优化 — **真正的研究空白**
- **思路**: "Speculative lock elision at hardware level" + perceptron 预测 SC 失败
- **耗时**: 1-2 周 (文献调研 + 方案初稿)
- **产出**: research proposal 草稿

---

## 📈 未来方向 (按时间线)

### 短期 (1-2 年)
- **WSE-aware Constabulary**: 把 Constable 思想扩展到 WSE — 不是"跳过 load"而是"跳过远程 mesh 访问"
- **CVA6S+ + Bullseye 集成**: 在 RISC-V 上评估 H2P 子系统实际增益
- **RISC-V Secure TAGE**: 把 Morrison 的搜索空间缩小技术移植到 RISC-V BP

### 中期 (3-5 年)
- **Apple M-style BTB for WSE**: 基于 M1 RE 参数 + WSE 多核共享前端需求
- **LLMCPU-Mark**: 推动建立 CPU 微架构优化对 LLM 推理影响的 benchmark
- **Tightly-coupled NPU dispatch**: 用 Constable-style elimination 减少 NPU 指令的 load stalls

### 长期 (5+ 年)
- WSE 专用 LLM 推理核进入主流 (Cerebras WSE-3 先行)
- Apple M3/M4 RE 论文出现
- Constable 风格"value elimination"扩展到 branch/store elimination

---

## 🏆 关键发现 (本次研究最重要的产出)

### 1. **数据校正** (Analyst 表现)
Scout 报告的 5 个 arXiv ID 中 **4 个是错的** — Analyst 逐一验证纠正，避免整个研究建立在错误引用上。

### 2. **Constable = ISCA 2024 Best Paper** (Analyst 二次核验)
Scout 漏掉了最高权重信号 — Analyst 独立从 ISCA 2024 官方公告确认。这是"分析超越扫描"的标志性贡献。

### 3. **核内同步 = 真实 Gap** (诚实标注)
5 大 Luke 方向中，**只有核内同步无直接论文** — Analyst 写出负面论证 (4 点障碍 + 3 个推测性方向)，避免 Luke 错配研究方向。

### 4. **5 条 Insights 性质分类** (Writer 修订)
- 🔁 复用: Insight 2 (fork CVA6S+)
- 🔀 组合: Insight 1 (旁路子系统) + Insight 3 (OoO 边际饱和)
- 💡 提案: Insight 4 (WSE LLM ISA) + Insight 5 (微架构透明度)
让 Luke 知道哪些是已知方法复用、哪些是研究提案。

---

## ⚠️ 已知局限 (诚实标注)

1. **AVM-BTB 全部数字 [待验证]** — 无 arXiv，ISCA 2024 全文未访问
2. **CVA6S+ 细节 [待精读]** — 是 3 页 short paper，BTB/rename table 拓扑需查后续 ISCA/MICRO 全文
3. **Constable 硬件开销精确数字 [待验证]** — 摘要未给面积拆分
4. **Apple M1 RE 具体参数 [待验证]** — RE 论文未列出 BPU 详细数字
5. **HPCA 2024/2026 未深抓** — 仅验证 HPCA 2025 可访问
6. **核内同步方向无直接论文** — Gap + 负面论证 (4 障碍) 已写入

---

## 📌 下一步建议 (给 Luke)

**立即可做 (本周)**:
- 精读 Constable 全文 (2-3 小时)
- 浏览 CVA6S+ 代码 (1 小时)

**本周完成**:
- `git clone openhwgroup/cva6s` 跑通仿真
- 抓 ISCA 2024 AVM-BTB proceedings PDF

**本月完成**:
- 把 Constable likely-stable tracker 移植到 CVA6S+
- 评估 Bullseye 28KB H2P 子系统在 RISC-V 的实际增益
- 启动"核内同步 + Constable-style elimination"研究 gap 探索

---

*本报告由 OpenClaw Orchestrator 协调 Scout → Analyst → Writer → Critic 完成, 2 次迭代达 8.2-8.4/10 综合评分。*  
*模型: minimax/MiniMax-M3 | 时间: 2026-07-03 10:30 CST*
