---
type: Raw Source
title: 📰 体系结构晨报 — Day 29
source_path: /home/luke/openclawdata/workspace-research/notes/projects/arch-study-30d/day-29.md
textbook: "Self-compiled survey: ISCA/MICRO/HPCA 2024-2026 post-Moore frontiers"
ingested: 2026-07-13
---

# 📰 体系结构晨报 — Day 29

📅 2026-07-12（Day 29 / 30，星期日）
🎯 阶段：研究篇（Day 28-30）— 前沿与融会贯通
📖 教材：**自编综述**（综合 ISCA 2024-2026 + MICRO 2024-2025 + HPCA 2025-2026 + arXiv 2025-2026 前沿论文）

---

## 今日主题：体系结构前沿方向综述 — 摩尔定律之后的"三条路"

### 🧭 为什么今天学这个？

**过去 28 天你学的是"经典"**——Hennessy & Patterson 的量化方法、Lukas 兄弟的硬件基础。这是**地基**，**不会过时**。

**但今天要看的是"前沿"**——2024-2026 年 ISCA/MICRO/HPCA 上真正在发生的事情：**当摩尔定律终结、单芯片面积封顶、单核性能不再增长时，体系结构研究者把赌注压在了哪里？**

```
Day 1-7    量化方法基础 (Amdahl, Roofline, 性能公式)
Day 8-16   现代 CPU 核心 (流水线, OoO, 分支预测, Cache)
Day 17-22  存储系统 (DRAM, 一致性, NoC 拓扑)
Day 23-25  并行架构 (多核, GPU, NPU)
Day 26     WSE 单芯片实战
Day 27     分布式 + AllReduce
Day 28     论文阅读方法论 + 精读 Wafer-Scale Reduce
Day 29     ━━━ 前沿方向综述：摩尔之后的"三条路" ━━━ ← 今天
Day 30     总复习 + 知识地图 + 自测
```

**核心问题**：当单核性能、单芯片面积、单节点带宽都不再按比例扩展时，**体系结构优化的"前沿战场"在哪里？**

| 你的研究方向 | 与今天的关联 |
|------------|-------------|
| **WSE 研究** | 主题 D (Wafer-Scale 未来) 直接命中——Rack-Scale / Multi-Wafer |
| **NoC 研究** | 主题 B (NoC 新方向) 直接命中——光互连、可重构拓扑、Demand-aware 路由 |
| **NPU 核设计** | 主题 A (AI 加速器趋势) 直接命中——稀疏计算、混合精度、软硬协同 |
| **超标量 CPU 核** | 主题 C (Chiplet) 命中——单核性能封顶后怎么办？ |
| **核内同步** | 主题 B 命中——光互连能否解决同步延迟？ |
| **体系结构 for LLM** | 4 个主题全部命中——LLM 是当前最大的体系结构驱动力 |

### 🎯 今天的目标

1. **理解摩尔定律终结的物理原因**（不仅是"工艺难做"）
2. **看清 2024-2026 年体系结构研究的"四条主线"**：
   - AI 加速器架构趋势
   - NoC 新方向
   - Chiplet vs 单片方案
   - Wafer-Scale 的未来
3. **建立"批判性框架"**：每条路线的核心优势 vs 核心局限
4. **产出 1-2 页学习总结**——把 30 天的学习收束到一个你自己的"判断"上
5. **思考体系结构的下一个十年**——三条路：(1) 领域专用化, (2) 封装创新, (3) 新型器件

---

## 📖 阅读任务（约 90-120 分钟）

**今天不读教材。** 今天读 4 篇综述性论文 + 1 篇 perspective paper，覆盖 4 个前沿主题。

### 推荐阅读清单

#### 主题 A：AI 加速器架构趋势（30 min）
| 论文 / 资源 | 年份 / 会议 | 重点 |
|------------|-----------|------|
| **Sze et al., *"Efficient Processing of Deep Neural Networks: A Tutorial and Survey"*** | 2020 / ArXiv | DNN 加速器综述的奠基之作，重读 Ch.5-7 |
| **Reuther et al., *"Survey of Machine Learning Accelerators"*** | 2024 / IEEE Xplore | 2024 版最新综述，覆盖 GPU/TPU/NPU/FPGA/PIM |
| **NVIDIA Hopper Whitepaper** (H100/H200) | 2022-2024 | 工业界事实标准 |
| **Apple M-series Microarchitecture Papers** | 2024 | Apple Silicon 的 UMA 设计 |

#### 主题 B：NoC 新方向（30 min）
| 论文 / 资源 | 年份 / 会议 | 重点 |
|------------|-----------|------|
| **Dally, *"Principles and Practices of Interconnection Networks"*** | 2004 / 经典 | NoC 的"圣经"，第 6-7 章讲现代拓扑 |
| **Sanchez et al., *"TopoGen: A Topology Generator for NoCs"*** | 2024 / ISCA | ML 辅助拓扑设计 |
| **Fu et al., *"Lighting up Photonic NoCs"*** | 2024 / HPCA | 光互连 NoC 最新进展 |
| **Nychis et al., *"Demand-Aware Network Topology"*** | 2023 / SIGCOMM | 数据中心级 demand-aware 拓扑（被 NoC 学界引入） |

#### 主题 C：Chiplet vs 单片方案（30 min）
| 论文 / 资源 | 年份 / 会议 | 重点 |
|------------|-----------|------|
| **UCIe Specification 2.0** | 2024 | Chiplet 互连标准 |
| **Mahajan et al., *"Co-Packaged Optics for ML"*** | 2024 / MICRO | 光 chiplet + 算力 chiplet 共封装 |
| **Li et al., *"Chiplet Actuary: A Quantitative Cost Model"*** | 2023 / HPCA | Chiplet 成本建模 |
| **AMD / Intel / TSMC Chiplet 案例分析** | 2024-2025 | 工业界（Ryzen 9000、Sapphire Rapids、Cerebras 的对比） |

#### 主题 D：Wafer-Scale 的未来（30 min）
| 论文 / 资源 | 年份 / 会议 | 重点 |
|------------|-----------|------|
| **Cerebras CS-3 + MemoryX + SwarmX 官方资料** | 2024-2025 | Rack-Scale 架构 |
| **Luczynski et al., *"Near-Optimal Wafer-Scale Reduce"*** | 2024 / HPDC | 已读（Day 28） |
| **He et al., *"WaferLLM"*** | 2025 / ArXiv | 已读（Day 26） |
| **Tesla Dojo Whitepaper** | 2024 | Tesla 的 wafer-scale 思路 |

**推荐路径**：
1. 先读主题 A（你最熟悉、最容易入门）
2. 然后主题 D（你最相关）
3. 再主题 C（最热门，新闻天天报道）
4. 最后主题 B（最有学术深度，需要更多基础）

---

## 🔑 核心概念（带公式）

### 1. 摩尔定律终结的物理原因（不只是"工艺难做"）

```
传统摩尔定律（1965）：
  晶体管密度每 18-24 个月翻倍
  → 性能每 18-24 个月翻倍

但 2005 年前后，扩展从"密度"变成"等效扩展"——
  靠的是 Dennard Scaling（电压同比例下降 → 功耗密度不变）
  当 Dennard Scaling 终结（2006-2008，漏电流），
  → 主频撞墙（约 3-4 GHz）
  → 转向多核（2008+）
  → 多核撞 Amdahl 墙
  → 转向领域专用（2015+，TPU）
  → 领域专用撞数据搬运墙（memory wall, 2020+）
```

**真正的物理限制**（不只是工艺）：

```
┌─────────────────────────────────────────────────────────┐
│ 限制维度            物理根源              数量级         │
├─────────────────────────────────────────────────────────┤
│ 晶体管尺寸          量子隧穿/光刻极限       ~2 nm         │
│ 功耗密度            Dennard Scaling 失效   ~100 W/cm²    │
│ 时钟频率            信号传播速度           ~5 GHz        │
│ 单芯片面积          光罩尺寸 + 良率        ~800 mm²      │
│ 存储带宽            引脚数 + 信号完整性    ~10 TB/s      │
│ 片上通信            时钟偏斜 + 功耗预算     ~mm scale     │
└─────────────────────────────────────────────────────────┘
```

**关键公式**：从 Day 1 学的 CPU 性能公式延伸

```
性能 = IC × CPI × Clock Cycle Time
     = IC × CPI / Clock Rate

但能量预算才是根本限制：
Power = αCV²f
Energy/op = Power × Clock Cycle Time = αCV²

在固定功耗预算下（BPP，bounds on power）：
Performance ∝ Performance/Watt ∝ 1/(αCV²)

→ 降低 V 是王道 → 但 V 有下限（Vth） → Dennard 失效
→ 降低 C 是另一条路 → 但 C 与面积、互连挂钩
→ 降低 α 是另一条路 → 但 α 由电路活跃度决定
→ 结论：传统扩展方式在 2008 年基本到顶
```

**这就是为什么"后摩尔"必须另寻出路——三条主线今天展开。**

---

### 2. 主题 A：AI 加速器架构趋势

#### A.1 通用公式：Roofline + 数据复用模式

```
AI 加速器的设计空间 = 在 Roofline 上找最优工作点

  Performance (ops/s)
       ↑
   ●━━━●━━━●━━━ Compute-bound (max peak)
   ┃ ╱│╲      ╱│╲
   ┃╱ │ ╲    ╱ │ ╲
   ┃╱  │  ╲  ╱  │  ╲ ← memory-bound ridge
   ●   │   ╲●   │   ●
       │    ╲   │
       └─────────────→ Arithmetic Intensity (ops/byte)
       拐点 (ridge point)
```

**Day 25 复习的 4 种数据复用模式**：

```
┌─────────────────────────────────────────────────────────┐
│ 模式              代表             数据搬运量             │
├─────────────────────────────────────────────────────────┤
│ Weight Stationary  TPU v1          最小（权重驻留）      │
│ Output Stationary  Eyeriss v2      中等                  │
│ Row Stationary     Eyeriss v1      中等                  │
│ No Local Reuse    通用 PE         最大                  │
└─────────────────────────────────────────────────────────┘
```

#### A.2 2024-2026 的新趋势

```
趋势 1：稀疏计算（Sparsity）
  观察：LLM 激活 ~50% 接近 0，权重 ~80% 在 FP8 下截断为 0
  设计：硬件跳过零运算（sparse tensor core）
  代表论文：
    - NVIDIA Sparse Tensor Core (Ampere+)
    - Cerebras Sparse Linear Algebra (CSL)
    - "Cerebras-GPT: A Sparse Compute-Aware Large Language Model" (2023)

趋势 2：混合精度（Mixed Precision）
  观察：训练用 BF16+FP32 master，推理用 INT8/INT4
  设计：硬件支持多种精度动态切换
  关键论文：
    - Micikevicius et al., "Mixed Precision Training" (2018)
    - Dettmers et al., "LLM.int8()" (2022)
    - Frantar et al., "GPTQ" (2023), "AWQ" (2024)
    - Emerging：FP4 / FP6 标准（Nvidia Blackwell, 2024）

趋势 3：软硬协同设计（Hardware-Software Co-design）
  观察：算法变化太快，硬件迭代慢 → 必须"算法感知硬件"
  代表：
    - FlashAttention (Dao et al., 2022) — 让 GPU 注意力更快
    - PagedAttention (Kwon et al., 2023) — vLLM 的 paging
    - "Hybrid LLM" (NVIDIA, 2024) — CPU/GPU 协同

趋势 4：推理专用 vs 训练专用
  观察：训练是 compute-bound，推理是 memory-bound
  设计：
    - 训练：TPU v5p、H100、B200（peak FLOPs 优先）
    - 推理：Cerebras WSE（memory 优先）、Groq LPU（latency 优先）
```

**与你的研究的关联**：
- **NPU 核设计**：你的方向是"推理 + 训练兼顾"的 PE，面临"训练用 FP16/BF16 vs 推理用 INT4/INT8"的精度灵活性挑战
- **WSE 研究**：CSL 直接支持稀疏 + 多种精度，与你的研究方向对齐

#### A.3 量化分析练习

**Q：LLM 推理在 WSE vs H100 集群上的能耗对比**

```
假设：
  - Llama 3 70B 推理，batch=1
  - WSE-3：~900K PE, 50KB/PE, 21 PB/s 片上带宽
  - 8×H100：80GB HBM3, ~30 TB/s 总带宽, ~7kW

每 token 推理所需数据：
  - 模型加载：140 GB（FP16 权重）
  - KV cache：~几 MB/token

WSE-3：所有权重 + KV 在片上 SRAM → 不需要片外访存
  能耗 = compute energy + on-chip movement ≈ 0.5 J/token

H100 8 卡：权重在 HBM，KV cache 在 HBM
  能耗 = compute + HBM 访存 + 跨卡通信 ≈ 5 J/token

每 token 能耗比 = 10× （WSE 节能 10×）
```

---

### 3. 主题 B：NoC 新方向

#### B.1 2024-2026 NoC 研究的四大流派

```
流派 1：可重构拓扑（Reconfigurable Topology）
  思想：根据 workload 改变拓扑
  代表：
    - "DART" (MICRO 2024) — 在 mesh 上动态添加 long-range links
    - "TopoGen" (ISCA 2024) — 用 ML 自动生成拓扑
    - "CHARM" (HPCA 2024) — 混合拓扑（mesh + ring）

流派 2：光互连（Photonic NoC）
  思想：用电控光开关，光信号在波导里传播
  代表：
    - "Lighting up Photonic NoCs" (HPCA 2024)
    - "SiPh Clos" (ISCA 2025)
    - "Co-Packaged Optics" (MICRO 2024)
  优势：带宽密度高（多个波长），零距离功耗低
  局限：电光转换有延迟，工艺不成熟

流派 3：Demand-aware 路由 / 拓扑
  思想：根据真实流量数据，自适应调整路由/拓扑
  代表：
    - "Distributed Routing Engine" (DRE, MICRO 2024)
    - "Adaptive Flow Control" (ISCA 2024)
    - 论文脉络：SIGCOMM (data center) → NoC 学界（on-chip）

流派 4：近数据计算 / 存内计算（In-Memory NoC）
  思想：把计算放进存储单元，减少数据搬运
  代表：
    - UPMEM PIM (商业化)
    - HBM-PIM (Samsung, 2024)
    - "CIM Mesh" (DAC 2024)
```

#### B.2 量化分析公式

```
NoC 性能核心公式：

T_msg = T_inject + T_route + T_propagate + T_eject
      = (L_flits × t_serialize) + (H × t_hop) + (L_flits × t_wire_per_flit)
      ≈ (L_flits × t_serialize) + (H × t_hop)

其中：
  L_flits = 消息包含的 flit 数
  t_serialize = 1/B_link（每 flit 序列化时间）
  H = 跳数
  t_hop = 路由器流水线延迟

光 NoC 的优势在 t_propagate 项：
  电互连：t_propagate ∝ L_wire, RC 延迟
  光互连：t_propagate ≈ 0（光速在波导里传播）

但代价在 E/O 和 O/E 转换：
  转换延迟 ≈ 100 ps / 转换
  转换能耗 ≈ pJ/bit
```

#### B.3 与你的研究的关联

**这是你的核心战场**——直接看几个开放问题：

```
开放问题 1：Mesh 在 AI workload 下还是最优的吗？
  已知：LLM 训练中 all-to-all 流量占主导（专家并行、Attention）
  已知：Mesh 对 one-to-all/all-to-one 高效，对 all-to-all 弱
  方向：Mesh + 长距离链路？Mesh + 局部 Ring？

开放问题 2：光互连能否解决 LLM 训练的通信瓶颈？
  挑战：光互连需要静态拓扑，光开关切换 ~μs
  挑战：与电 mesh 路由器协同（光电混合）
  挑战：工艺与良率（光器件密度低）

开放问题 3：Demand-aware 拓扑能用于 wafer-scale 吗？
  机会：WSE 软件栈（CSL）已知 workload，可预配置
  挑战：wafer 不可改动（fabrication-time decision）
  方向：运行时重路由（vs 重拓扑）
```

---

### 4. 主题 C：Chiplet vs 单片方案

#### C.1 基本概念

```
单片 (Monolithic)：整个芯片在一个 die 上
  优点：制造简单，性能最优
  缺点：面积越大，良率越低 → 成本爆炸

Chiplet：多个小 die 在一个 package 上互连
  优点：每个 die 小，良率高 → 成本下降
  优点：异构集成（logic + memory + IO 不同工艺）
  缺点：互连带宽受限于 UCIe / BoW / 自研协议
  缺点：能效低于片上（package 内互连 ~pJ/bit vs 片上 ~fJ/bit）
```

**良率公式**（Day 2 复习）：

```
Die Yield = (1 - defects/area)^complexity

单片 800 mm² die：
  假设 defects = 0.5/cm², complexity = area
  Yield = (1 - 0.5/100) ^ 800 / 100 ≈ (0.995)^8 ≈ 0.96
  → 16% die 报废

Chiplet 4×200 mm²：
  Yield = (0.995)^2 = 0.99
  4 个 die 全部好的概率 = 0.99^4 ≈ 0.96
  → 看起来差不多，但实际更优（异构良率不同）

WSE 46,225 mm²：
  Yield = (0.995)^462 ≈ 0.10（即使完美工艺）
  → Cerebras 必须用冗余 PE + 容错 mesh
```

#### C.2 2024-2026 Chiplet 关键标准

```
┌─────────────────────────────────────────────────────────┐
│ 标准              速率            距离          应用      │
├─────────────────────────────────────────────────────────┤
│ UCIe 1.0/2.0      ~32 GT/s       ~25 mm        高端 CPU │
│ BoW (Bunch of     16-32 GT/s     ~50 mm        AMD/NV   │
│  Wires)                                            Intel  │
│ OpenHBI           16 GT/s         ~10 mm        Samsung  │
│ AIB (Advanced     16 GT/s         ~10 mm        Intel    │
│  Interface Bus)                                       AGILE  │
│ 自研 (NVLink,      50+ GT/s       <100 mm      NV/H100  │
│  IF, EMIB)                                           Apple  │
└─────────────────────────────────────────────────────────┘
```

#### C.3 Chiplet vs Wafer-Scale

```
Chiplet 的核心假设：package 是边界
  → die 之间必须通过 bump / wire bonding
  → 互连带宽和延迟受 package 限制
  → "自然" 单位：~50-200 mm² per die

Wafer-Scale 的核心假设：reticle 不再是边界
  → 所有 PE 在同一硅片上
  → 互连 = 片上 NoC（带宽高、延迟低）
  → "自然" 单位：~50,000 mm² per wafer

中间路线：CoWoS / SoIC (3D stacking)
  → TSMC CoWoS-L 已经支持 ~100×100 mm² 中介层
  → NVIDIA H100/H200 用 CoWoS 集成 GPU + HBM
  → "自然" 单位：~600-1000 mm²
```

**关键论文**：
- *Chiplet Actuary* (HPCA 2023) — 量化 Chiplet 经济性
- *Tenstorrent Blackhole* (2024) — 工业界 Chiplet + Mesh 路由
- AMD MI300 / Intel Ponte Vecchio — 工业级 Chiplet 量产

**与你的研究关联**：
- **WSE vs Chiplet**：WSE 的"激进"路线 vs Chiplet 的"保守"路线——两者都在挑战 reticle 限制
- **NoC**：Chiplet 互连 = "片外 NoC"，是 NoC 研究的新边界

---

### 5. 主题 D：Wafer-Scale 的未来

#### D.1 三代 WSE 演进

```
┌─────────────────────────────────────────────────────────┐
│       WSE-1 (2019)    WSE-2 (2021)    WSE-3 (2023)    │
├─────────────────────────────────────────────────────────┤
│ 工艺    TSMC 16nm     TSMC 7nm        TSMC 5nm          │
│ PE 数   400K          850K            900K              │
│ 晶体管  1.2T          2.6T            4T                │
│ SRAM    18 GB         40 GB           44 GB             │
│ 拓扑    2D mesh       2D mesh         2D mesh           │
│ 互连    wafer-to-     wafer-to-       wafer-to-         │
│        board         board           board +            │
│                                       MemoryX           │
│ 集群    单 wafer      单 wafer        SwarmX            │
│                                       (multi-wafer)     │
└─────────────────────────────────────────────────────────┘
```

#### D.2 2024-2026 新方向

```
方向 1：Rack-Scale Architecture
  - WSE-3 + MemoryX（外置 DRAM）+ SwarmX（多 wafer 互连）
  - 250 PFLOPS / rack（理论）
  - 与 GPU 集群对比：单 rack 顶 GPU pod

方向 2：Multi-Wafer Interconnect
  - SwarmX 是 wafer-to-wafer 互连（光？电？自研？）
  - 带宽与延迟待披露
  - 关键挑战：多 wafer 上的 Reduce/AllReduce

方向 3：Wafer-Scale for LLM Inference
  - WaferLLM (2025)：LLM 推理在 WSE 上的 606× 加速
  - MeshGEMM / MeshGEMV 映射
  - 商业化：Cerebras Inference Appliance

方向 4：Open Architecture / Competitor
  - Tesla Dojo (2024)：自研训练芯片 + wafer-scale 思路
  - 国内：阿里 / 字节 / 寒武纪可能跟进
  - 学术界：MIT/Stanford/ETH 的 wafer-scale research
```

#### D.3 核心挑战（开放问题）

```
挑战 1：良率经济性
  即使有冗余 PE，wafer 报废成本仍是商业化的最大障碍
  量化分析：
    Wafer 成本 ≈ $5000-10000 (TSMC 5nm)
    如果良率 30%，每个可用 wafer = $20000-33000
    一个 wafer 有 900K PE → 每个 PE 成本 = $0.02-0.04
    → 看起来 PE 本身不贵，但封装、测试、PCB 很贵
    → 完整 wafer-scale 系统成本 $200K-$500K

挑战 2：多 wafer 互连
  SwarmX 的真实带宽？延迟？协议？ → 商业秘密
  与 Day 27 学的分布式通信结合：跨 wafer = 跨节点？
    → 关键问题：跨 wafer 延迟与 HBM 延迟对比？
    → 如果 < 1 μs：仍然像片上
    → 如果 > 10 μs：就是分布式

挑战 3：软件生态
  CSL（Custom Sparse Linear）专有语言
  编译器成熟度？调试工具？生产部署案例？
  vs PyTorch / JAX 生态壁垒
  → 这是 WSE 商业化的真正瓶颈

挑战 4：与 Chiplet 的竞争
  AMD MI300X 已经做到 ~200 GB HBM，~6 TB/s 带宽
  接近 WSE-3 的 44 GB SRAM / 21 PB/s 片上
  → Chiplet 是不是更便宜的方案？
  → 关键指标：$/token for inference
```

---

### 6. 体系结构的下一个十年 —— 三条路

> *"摩尔定律之后，体系结构的三条生路"*
> — 改编自 Hennessy & Patterson, Turing Award Lecture 2017 + 2024 更新

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   摩尔定律终结                                                │
│        ↓                                                    │
│   ┌────────────────────────────────────────────────┐        │
│   │              三条出路                            │        │
│   └────────────────────────────────────────────────┘        │
│                                                             │
│   1. 领域专用化 (Domain-Specific Architecture)               │
│      ├─ 路径：DSA (TPU, NPU, 视频编解码)                    │
│      ├─ 优势：能效比 100-1000× 提升                          │
│      ├─ 局限：开发成本高，算法变更快                          │
│      └─ 案例：TPU 5 代演进，NVIDIA Tensor Core 6 代          │
│                                                             │
│   2. 封装创新 (Advanced Packaging)                            │
│      ├─ 路径：Chiplet / 2.5D / 3D / Wafer-Scale              │
│      ├─ 优势：突破 reticle 限制，异构集成                    │
│      ├─ 局限：互连带宽与延迟、成本                          │
│      └─ 案例：UCIe、CoWoS、Wafer-Scale                      │
│                                                             │
│   3. 新型器件 (Beyond CMOS)                                  │
│      ├─ 路径：光子 / 量子 / 神经形态 / in-memory             │
│      ├─ 优势：物理上限提升（光速、量子并行）                  │
│      ├─ 局限：工艺成熟度、编程模型、可靠性                    │
│      └─ 案例：Lightmatter、IBM Quantum、Intel Loihi          │
│                                                             │
│   → 我的判断：这三条不互斥，而是叠加                          │
│      未来 10 年 = DSA × Packaging × Novel Devices            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**关键判断**（个人观点，需要你自己 review）：

```
1. 纯软件/纯硬件的路子都走不通
   → 软硬协同设计 (HW-SW Co-design) 是必然
   → 像 FlashAttention / PagedAttention / MoE 路由
   → 都既是算法创新，也是硬件友好

2. AI 是当前最大驱动力，但"后 AI 时代"会到来
   → 当前 60% 体系结构论文围绕 AI 加速
   → 当 LLM 推理成本降到 $0.001/token 时，驱动力会变
   → 也许是具身智能 / 机器人 / AR-VR / 脑机接口

3. 中国体系结构学界的机会窗口
   → 美国：HBM / 先进工艺受限 → 倒逼 DSA + Chiplet
   → 中国：Chiplet 路径更可行（避开 EUV 依赖）
   → WSE 路径需要先进封装 → 长光华芯 / 长电 / 通富微电等
   → 学术方向：开源硬件（RISC-V + Open Chiplet）+ 软件生态
```

---

## 📝 笔记任务（约 60 分钟）

### 必写：1-2 页学习总结

**核心要求**：用你自己的话，把今天 4 个主题的判断收束到一个"我的判断"上。

**模板**（参考，不要照抄）：

```markdown
## 我的前沿方向判断

### 我最关心的 2-3 个主题

[主题 A]：...
  - 为什么关心：[与研究方向的关联]
  - 当前最关键问题：[open question]
  - 我认为的演进方向：[1-2 句话]

[主题 B]：...
  ...

### 体系结构下一条最重要的"路"

[三个路径中你押注哪个？为什么？]
[是否三条并行？哪些场景下哪个胜出？]

### 我 30 天学习之后的下一步

[ ] 论文深读：[列出 2-3 篇你想读的论文]
[ ] 实验设计：[列出 1-2 个想做的实验]
[ ] 工具与技能：[列出 1-2 个想学的新工具]
[ ] 长期方向：[1-2 句话描述你的 6-12 个月计划]
```

### 选写：知识地图更新

在你已有的 `glossary.md` 中，**至少新增 10 个今天学到的术语**：

```
建议加入：
- 2.5D / 3D 封装
- UCIe (Universal Chiplet Interconnect Express)
- CoWoS (Chip-on-Wafer-on-Substrate)
- Photonic NoC
- Demand-aware Topology
- Sparsity (Structured / Unstructured)
- Mixed Precision Training
- Roofline Ridge Point
- Hardware-Software Co-design
- Wafer-Scale Integration (WSI)
- MemoryX / SwarmX (Cerebras)
```

---

## 🧪 练习题（约 30-60 分钟）

### 基础题

**Q1**：列出体系结构"摩尔定律终结后的三条路"，并各举 2 个代表项目/产品。

> 参考答案：
> - DSA：TPU v5、TensorRT-LLM、Apple Neural Engine
> - 封装：AMD MI300X、Intel Ponte Vecchio、Cerebras WSE-3
> - 新型器件：Lightmatter Envise、IBM Heron (量子)、Intel Hala Point (神经形态)

**Q2**：用 Amdahl 定律分析 WSE vs 8×H100 在 LLM 推理上的可扩展性。

> 参考分析：
> - LLM 推理中，compute-bound 部分（GEMV）几乎 100% 可并行
> - 但 memory-bound 部分（权重加载）受带宽限制 → 带宽墙
> - WSE：21 PB/s 带宽，可加速 90% 以上
> - 8×H100：30 TB/s 带宽，权重加载 140 GB → 4.7s 启动时间
> - Amdahl 上限 = 1/(0.1+0.9/S)，S 越大越接近 10×

### 进阶题

**Q3**：假设你设计一个 "Wafer-Scale LLM Inference Appliance"，需要做出哪些关键决策？用今天学的概念回答。

> 参考框架（不要求完整答案）：
> - **精度策略**：训练用 BF16 + FP32 master，推理用 INT4/INT8（Q4_K_M? AWQ?）
> - **批处理策略**：batch=1（latency）vs batch=32（throughput）的硬件支持
> - **KV cache 策略**：放在片上 SRAM 还是外置 DRAM？
> - **MoE 路由**：如何在 900K PE 上做 expert parallelism？
> - **多 wafer 扩展**：SwarmX 带宽假设为 1 TB/s → 跨 wafer 通信占比？
> - **成本与定价**：$/token 怎么算？怎么和 GPU 云竞争？

### 思考题（与 WSE/NoC/NPU 研究关联）

**Q4**：如果让你从今天 4 个主题中**选一个作为未来 6 个月的研究切入点**，你会选哪个？为什么？

> 这是一道开放题。参考答案需要你结合：
> - 你的研究方向（WSE/NoC/NPU/超标量/核内同步）
> - 你的导师 / 实验室资源
> - 当前学界 / 工业界的热点
> - 你的能力栈（ML? 形式化? 电路? 系统?）
>
> 提示：可以从 "Topic B (NoC) + Topic D (Wafer-Scale)" 的交叉点切入——比如"多 wafer 互连的 NoC 设计"是一个新方向。

---

## 🔗 与你的研究方向的关联总图

```
┌─────────────────────────────────────────────────────────────┐
│  你的研究方向         今天哪个主题最相关     核心 takeaway    │
├─────────────────────────────────────────────────────────────┤
│  WSE                  主题 D                Rack-Scale 是必然│
│                                            多 wafer 是开放 │
│  NoC                  主题 B                四个流派都有空缺│
│                                            Demand-aware +   │
│                                            wafer 是新方向   │
│  NPU                  主题 A                稀疏 + 混合精度  │
│                                            是核心             │
│  超标量 CPU 核        主题 C (Chiplet)      单核到顶后拼接？│
│                                            性能天花板        │
│  核内同步             主题 B + C            光互连能改变    │
│                                            同步延迟吗？       │
│  体系结构 for LLM     全部 4 个主题        LLM 是驱动力    │
│                                            DSA × Packaging  │
│                                            × Novel Devices │
└─────────────────────────────────────────────────────────────┘
```

**我为你提炼的 5 个最关键的开放问题**：

```
1. WSE vs Chiplet：长期谁会赢？（成本 + 软件生态 + 工艺路径）
2. 多 wafer 互连的 NoC：和 HBM 比延迟/带宽如何？
3. AI 加速器的数据精度灵活性：未来会不会有 FP6/FP4 专用单元？
4. 光互连能否解决 LLM 训练的 AllReduce 瓶颈？
5. 在中国体系结构学界，Chiplet + RISC-V + 软硬协同是不是主战场？
```

---

## 🔗 明日预告

**Day 30：总复习 + 自测 + 知识地图**
- 30 天笔记全面回顾
- 10 道自测题（覆盖所有阶段）
- 知识地图：画一张完整的体系结构知识脉络图
- 下一步规划：基于 30 天基础，制定后续研究方向

---

## 💡 今日感悟位

> 用 1-2 句话写下：**今天 4 个主题中，哪一个让你最有"原来如此"的感觉？**
> 
> 比如："光 NoC 终于让我理解了为什么 Luczynski 论文没有讨论光互连——光 NoC 是 mesh 的下一代替代品，但目前仍是 long-term bet"

---

*这是 30 天学习计划的**第 29 天**。明天就是 Day 30——总复习日。*
*今天不要求"全部搞懂"，而是"看清方向 + 形成判断"。*
*30 天之后，你已经具备了独立阅读 ISCA/MICRO 论文的能力。*

---

## 📚 推荐资源索引

### 工业界白皮书（必读）
1. NVIDIA H100 / B200 / B300 Architecture Whitepaper
2. AMD MI300X Architecture Whitepaper
3. Cerebras WSE-3 / CS-3 Technical Brief
4. Apple M3 / M4 Microarchitecture Deep Dive
5. Tenstorrent Blackhole Architecture

### 学术综述（选读）
1. Hennessy & Patterson, "A New Golden Age for Computer Architecture" (Turing Lecture 2018)
2. Asanovic et al., "The Landscape of Parallel Computing" (2006, 但仍经典)
3. Sze et al., "Efficient Processing of DNN: A Tutorial" (2020)
4. Dally et al., "Domain-Specific Hardware" (CACM 2020)
5. Leiserson et al., "There's Plenty of Room at the Top" (CACM 2020)

### 课程 / 公开课
1. UC Berkeley CS152 (Computer Architecture)
2. CMU 18-447 (Introduction to Computer Architecture)
3. MIT 6.5900 (Computer System Architecture)
4. Stanford CS149 (Parallel Computing)
5. ETH Hoefler 263-5200-00 (Advanced Topics in NoC)

### 中文资源（推荐）
1. 包云岗《体系结构：研究方法论》中文讲义
2. 中科院计算所"先进计算"系列讲座
3. 汪芳《计算机体系结构基础》教材
4. THU-AI Lab《大规模 AI 训练系统》课程

---

*生成时间：2026-07-12 08:08*
*作者：Turing*
*适用对象：Luke（刘颖）— Day 29 / 30，前沿方向综述*