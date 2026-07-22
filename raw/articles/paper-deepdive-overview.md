---
type: Raw Source
title: Paper Deep-Dive Overview
source_path: /home/luke/openclawdata/workspace-research/notes/projects/paper-deepdive/OVERVIEW.md
project: paper-deepdive
ingested: 2026-07-22
---

# 论文精读专项 📚 — Paper Deep-Dive

> 阶段：**30 天体系结构学习 → 阶段二**（输入 → 输出 转换期）
> 开始：**2026-07-14**（Day 1）
> 计划：6 周（~30 篇论文）+ 月度轮换
> 节奏：**每天早晨 08:00 Asia/Shanghai** 自动推送
> Cron：`paper-daily`（TBD）

---

## 🎯 目标

把 **Day 28 论文方法论** 用起来 —— 系统精读顶会论文，建立"顶级论文肌肉记忆"：

```
Day 28 学了：5 步精读法 + 4 大量化武器 + 5 大红旗
            ↓
接下来 6 周：用这个方法，**每天一篇顶会论文实战**
            ↓
目标：能用 2-3 小时读懂任何 ISCA / MICRO / HPCA / DAC 论文
```

## 📚 论文清单（每日更新）

### 第一阶段（Week 1-2）：NoC 经典 + Wafer-Scale 奠基（6 篇）

| # | 论文 | 年份 | 主题 | 优先级 |
|---|------|------|------|--------|
| 1 | Luczynski et al. *Near-Optimal Wafer-Scale Reduce* | 2024 | WSE Reduce 算法（FRED/FREDR）| ⭐⭐⭐ |
| 2 | Dally & Towles *Route Packets, Not Wires* | 2001 | NoC 奠基论文 | ⭐⭐⭐ |
| 3 | Hoskote et al. *A 5GHz Mesh Interconnect for a Teraflops* | 2007 | 80 核 NoC 工业实践 | ⭐⭐⭐ |
| 4 | Balfour & Dally *Design Tradeoffs for Tiled CMP On-Chip Networks* | 2006 | CMP NoC 设计权衡 | ⭐⭐ |
| 5 | Dally *Virtual-Channel Flow Control* | 1992 | VC 流控奠基 | ⭐⭐ |
| 6 | Kim, Dally, Abts *Adaptive Routing in High-Radix Clos Network* | 2006 | 高基数路由 | ⭐⭐ |

### 第二阶段（Week 3-4）：现代 LLM 加速器网络（6 篇）

| # | 论文 | 年份 | 主题 | 优先级 |
|---|------|------|------|--------|
| 7 | TPU v4 / v5 Pod Networking 报告 | 2023-24 | Google TPU 拓扑 | ⭐⭐⭐ |
| 8 | NVIDIA Hopper/Blackwell NVLink 报告 | 2022-24 | GPU 网络拓扑 | ⭐⭐⭐ |
| 9 | Groq LPU 白皮书 / 报告 | 2022-23 | 时序确定性推理 | ⭐⭐ |
| 10 | SambaNova SN40L 白皮书 | 2024 | RDU 数据流 | ⭐⭐ |
| 11 | Cerebras WSE-3 公开资料 | 2024 | WSE 第三代 | ⭐⭐⭐ |
| 12 | Tesla Dojo 白皮书 | 2023 | Dojo 训练架构 | ⭐⭐ |

### 第三阶段（Week 5-6）：前沿方向（6 篇）

| # | 论文 | 年份 | 主题 | 优先级 |
|---|------|------|------|--------|
| 13 | Theseus (arXiv 2024) | 2024 | Wafer-Scale 互连路由 | ⭐⭐ |
| 14 | WaferLLM (arXiv 2025) | 2025 | WSE LLM 框架 | ⭐⭐⭐ |
| 15 | Demand-Aware Reconfigurable Networks | 2023-24 | 可重构 NoC | ⭐⭐⭐ |
| 16 | Photonic NoC Papers (Henderson/Miller 系列) | 2020-23 | 硅光子 NoC | ⭐ |
| 17 | UCIe Chiplet 互联规范 | 2024 | Chiplet 互联 | ⭐ |
| 18 | FRED / FREDR 后续工作 | 2024-25 | Reduce 算法演进 | ⭐⭐ |

**待补充**：随着研究深入持续更新。

## 📖 Day-N 模板（每篇论文的固定结构）

```
00. 信息卡
    - 标题 / 作者 / 会议 / 年份 / arXiv ID
    - 一句话定位
    - 我为什么要读这篇

01. 5 步精读法实战
    - Step 1: Abstract & Intro（动机）
    - Step 2: Background（问题定义）
    - Step 3: Method（核心创新）
    - Step 4: Evaluation（实验设计）
    - Step 5: Conclusion（贡献 + 局限）

02. 核心贡献 1-2-3（要点）

03. 方法详解（自己的话）
    - 问题建模
    - 算法 / 电路 / 架构
    - 关键公式推导

04. 实验复盘
    - 关键图表（自制缩略版）
    - 性能数据回算
    - 与 SOTA 对比

05. 4 大量化武器应用
    - Roofline 分析（如适用）
    - Amdahl 公式（扩展性）
    - 几何均值（公平汇总）
    - 信噪比 / 敏感度

06. 5 大红旗检测
    - baseline 公平？
    - benchmark 完整？
    - 工艺/工艺节点
    - 统计显著性
    - 可复现性

07. 与 WSE / NoC / NPU 研究的关联
    - 可借鉴的方法
    - 可改进的地方
    - 与未来研究方向的关系

08. 5 个深度思考题（自己出 + 自己答）

09. 笔记：最有启发的 1 个洞察
```

## 🔗 与其他项目的关系

```
30 天体系结构 (Day 28 方法论)
   ↓ 提供方法
论文精读 (paper-deepdive) ← 当前阶段
   ↓ 提供素材
WSE-NoC 专项 (wse-noc-deepdive)
   ↓ 提供实战
NPU 核 / Superscalar CPU 核 (下一阶段)
   ↓ 输出
研究 / 论文 / 系统设计
```

## 📊 追踪指标

- 每周读完论文数（计划 5-6 篇）
- 每月输出一份月度复盘
- 6 周后累计 18-20 篇，方法论熟练度应到 90%+
- 一年内累计 60-80 篇

## ⏰ Cron 节奏

| 项 | 时间 | 任务 |
|---|------|------|
| **每日论文晨报** | 每天 08:00 Asia/Shanghai | 推送当日 Day-N 论文精读晨报 |
| **每周 WSE-NoC 综述** | 每周一 08:00 Asia/Shanghai | 推送本周 WSE-NoC 综述 |

两份 cron 互不干扰，并行执行。

---

*创建时间：2026-07-14*
*阶段：30 天体系结构完成 → 论文精读 + WSE-NoC 专项*
