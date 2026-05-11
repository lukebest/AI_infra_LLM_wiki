# Wiki Log

> 按时间顺序记录所有 wiki 操作。仅追加。
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-04-16] create | Wiki initialized
- Domain: AI 基础设施（scale-up 网络、加速器架构、确定性执行、推理系统）
- Structure created with SCHEMA.md, index.md, log.md

## [2026-04-16] ingest | NVIDIA Groq 3 LPX Blog Article
- Source: raw/articles/nvidia-groq3-lpx-blog-2026-04.md
- Created: entities/nvidia-groq-3-lpx.md, entities/nvidia-vera-rubin-nvl72.md, entities/cerebras-wse.md, concepts/deterministic-execution.md, concepts/lpu-architecture.md, concepts/heterogeneous-inference.md
## [2026-04-16] ingest | MegaScale-Infer + 3 analyses
- Ingest: papers/megascale-infer-2504.02263.md
- Created: analyses/wse-nom-contradiction-analysis.md (矛盾论六步)
- Created: analyses/cerebras-wse-vs-groq-network-comparison.md (全面对比)
- Updated: index.md (10 pages total)
- 使用《矛盾论》六步框架系统性分析 WSE Network-on-Wafer
- Created: analyses/wse-nom-contradiction-analysis.md
- 主要矛盾：物理均匀性 vs 通信异构性（通信异构性是主要方面）
- 关键洞察：color routing 是调和性缓解，非根本解决

## [2026-04-17] ingest | MegaScale-Infer 概念提取
- Created: concepts/disaggregated-inference.md, concepts/m2n-communication.md
- Updated: papers/megascale-infer-2504.02263.md (添加交叉引用)
- Updated: index.md (8 pages total)
## [2026-04-20] ingest | 信息论视角下的 AI Agent 价值模型
- Source: raw/papers/information-theory-ai-agents-2026-04.md
- Created: concepts/information-theoretic-value-model.md
- Updated: index.md (9 pages total)
- Topic: 互信息 I(S;K) 作为 Agent 价值的核心度量，有效性条件 I(S;K)/H(S) > 0.5 (α=2)，悖论区间，工程策略

## [2026-04-17] ingest | AI Tools Weekly Report (manual run)
- Report: notes/projects/ai-tools-weekly-2026-04-17.md
- Email sent: liuyingxyzabc@live.com (Foxmail SMTP, fixed From address)
- Topics: OpenClaw 2026.4.12, Cursor 3, Windsurf/Cognition, Claude Code rebuild, Opus 4.7

## [2026-04-28] ingest | DeepSeek-V4 Technical Report
- Source: DeepSeek_V4 PDF (54 pages)
- Files created:
  - entities/deepseek-v4.md — Model entity page
  - concepts/csa-hca.md — Hybrid attention architecture
  - concepts/mhc.md — Manifold-Constrained Hyper-Connections
  - concepts/muon-optimizer.md — Muon optimizer with Hybrid Newton-Schulz
  - concepts/fp4-qat.md — FP4 Quantization-Aware Training
  - concepts/megamoe-kernel.md — Expert Parallelism communication-computation overlap
  - concepts/tilelang.md — TileLang DSL for kernel development
  - concepts/dsec-sandbox.md — DSec sandbox platform
  - summaries/deepseek-v4.md — Paper summary with wiki cross-links
- Updated: index.md (22 pages total)
- Note: Merged from workspace wiki into ~/wiki/

## [2026-05-08] ingest | SemiAnalysis GTC 2026 – The Inference Kingdom Expands
- Source: raw/articles/GTC 2026 – The Inference Kingdom Expands.md
- Topics: LP30/LP35/LP40 路线图, LPX rack 架构 (FPGA Fabric Expansion Logic), C2C 三级网络拓扑, AFD (Attention FFN Disaggregation), Speculative Decoding on LPU, NVIDIA CPO roadmap (NVL576/NVL1152), Kyber rack 更新 (NVL144/NVL288), Vera ETL256, CMX/STX
- Created:
  - entities/kyber-rack.md — Kyber rack 架构 (144 GPU/rack, NVLink 7, midplane, NVL288/NVL1152)
  - concepts/nvidia-cpo-roadmap.md — CPO 路线图 (Rubin→Rubin Ultra→Feynman)
  - concepts/cmx-stx.md — CMX/STX 推理存储平台 (Tier G3.5, BF-4 DPU)
  - entities/vera-etl256.md — 256 CPU 独立 rack
- Updated:
  - entities/nvidia-groq-3-lpx.md — LP30 规格, LPX rack, C2C 网络拓扑, AFD, speculative decoding
  - concepts/lpu-architecture.md — LPU 世代对比 (Gen1-Gen4), slice 架构, SRAM 权衡
  - concepts/heterogeneous-inference.md — AFD 两种模式 (AFD + speculative decoding)
  - concepts/disaggregated-inference.md — NVIDIA LPX 产品化 AFD
  - entities/nvidia-vera-rubin-nvl72.md — NVL 系统谱系, Kyber 更新
  - index.md (27 pages total)

## [2026-05-08] ingest | 浅谈交换原理（1）——概述
- Source: raw/articles/浅谈交换原理（1）——概述.md
- Created:
  - concepts/switching-principles.md — 交换原理基础（电路交换/分组交换，三对基本概念，交换系统结构）
- Updated: index.md (28 pages total)
- Note: 基础概念文章，单来源，创建一个综合性 concept 页面。关联 deterministic execution、scale-up fabric 设计选择。

## [2026-05-08] ingest | 浅谈交换原理（2）——交换单元
- Source: raw/articles/浅谈交换原理（2）——交换单元.md
- Created:
  - concepts/switching-elements.md — 交换单元（空分S接线器/时分T接线器，开关阵列/共享存储器/共享总线，性能指标）
- Updated: index.md (29 pages total)
- Note: 交换原理系列第2篇。空分交换 ↔ NVLink crossbar，时分交换 ↔ 共享总线，集中型/扩散型 ↔ disaggregated inference M:N 模式。

## [2026-05-08] ingest | 浅谈交换原理（3）——交换网络
- Source: raw/articles/浅谈交换原理（3）——交换网络.md
- Created:
  - concepts/switching-networks.md — 交换网络（单级/多级，阻塞/无阻塞，CLOS 三级网络 (m,n,r)，TST 网络，Banyan 网络）
- Updated: index.md (30 pages total)
- Note: 交换原理系列第3篇。CLOS 是理解 scale-up fabric 多级交换的基础（NVLink switch ≈ CLOS），TST 对应时分+空分组合（C2C 确定性调度）。

## [2026-05-09] ingest | UnifiedBus (UB) Base Specification Rev 2.0
- Source: /home/luke/workspace/Vibe-UB-Switch/docs/UB-overview.md
- Created:
  - entities/unifiedbus-ub.md — Huawei UB 高性能互连协议（SuperPoD-scale, 统一协议栈, 全资源池化, 6层协议栈）
  - concepts/ub-transport-layer.md — UB 传输层机制（RTP/CTP/UTP, TP Channel, 多路径LB, 拥塞控制）
  - concepts/ub-programming-models.md — UB 编程模型（Load/Store, URMA, URPC, Jetty）
- Updated: index.md (34 pages total)
- Note: UB 规范 45KB，6层完整协议栈。与 NVLink 对比：统一协议（vs 多协议）、内置 RPC（URPC）、跨 domain Ethernet 互连（UBoE）。

## [2026-05-09] ingest | UB Transaction Layer (UB-TA.md)
- Source: /home/luke/workspace/Vibe-UB/docs/UB-TA.md (2355 lines, §7 Transaction Layer full chapter)
- Created:
  - concepts/ub-transaction-layer.md — 四类事务（Memory/Message/Maintenance/Management）、Full vs Compact 包头体系（BTAH/ATAH/MAETAH/MTETAH/TVETAH 等）、安全 Token 验证、TEO/TCO 排序机制、四种服务模式（ROI/ROT/ROL/UNO）、Atomic 9 种原子操作、Write_with_notify 即时通知、Prefetch_tgt 预取
- Updated:
  - entities/unifiedbus-ub.md — 添加 source 引用
- Updated: index.md (38 pages total)
- Key: ROT 模式通过 Target 端 Sequence Context 实现无等待排序，比 ROI 省一次 RTT；Atomic 保证单包原子性和仅执行一次；Writeback 强制非阻塞防止死锁

## [2026-05-09] ingest | UB Resource Management (UB-RSC.md)
- Source: /home/luke/workspace/Vibe-UB/docs/UB-RSC.md (2689 lines, §10 Resource Management full chapter)
- Created:
  - concepts/ub-resource-management.md — UBFM domain 管理、Entity 模型（EID/GUID/Partition 隔离）、配置空间（CFG0/CFG1 slice 结构）、管理命令（枚举/配置/池化资源）、Entity 注册/注销/替换、通信控制、远程内存注册、硬件辅助虚拟化、RAS（三级复位 + A/B/C 三级错误分类）
- Updated:
  - entities/unifiedbus-ub.md — 添加 source 引用
- Updated: index.md (37 pages total)
- Key: UB Partition (UPI) 隔离 + Token 认证双保险；Entity 池化支持动态分配/迁移/替换；三阶段错误分级（A→事务/B→Entity/C→设备）对应不同处理路径

## [2026-05-09] ingest | UB Memory Management (UB-MEM.md)
- Source: /home/luke/workspace/Vibe-UB/docs/UB-MEM.md (1648 lines, §9 Memory Management full chapter)
- Created:
  - concepts/ub-memory-management.md — UB 内存管理：Home-User 模型、UBMD、UMMU 4步处理流程（配置查找→上下文查找→两阶段地址翻译→权限检查）、MAPT 独立于 MATT 的权限表设计、UB Decoder PA→UBMD 翻译、与 ARM SMMU/Intel VT-d 对比
- Updated:
  - entities/unifiedbus-ub.md — 内存管理引用更新
- Updated: index.md (36 pages total)
- Key insight: UB MAPT 独立于 MATT（权限与地址翻译解耦），支持非特权软件安全委托权限管理，双 TokenValue 机制

## [2026-05-09] ingest | UB Function Layer (UB-FUN.md)
- Source: /home/luke/workspace/Vibe-UB/docs/UB-FUN.md (982 lines, §8 Function Layer full chapter)
- Updated:
  - concepts/ub-programming-models.md — 大幅扩展：Jetty 类型/状态机/通信模式、事务队列 (SQ/RQ/CQ/EQ)、内存段管理、内存借入/共享 (cache coherence + ownership)、通信管理 (Known Jetty/UBFM/TCP)、死锁避免 (内存访问 3 场景 + 消息通信 3 机制)
  - entities/unifiedbus-ub.md — 添加 Multi-Entity Coordination (Fusion/Collective/Global Maintenance)
- Created:
  - concepts/ub-urpc.md — URPC 远程过程调用（Client/Server/Worker 角色、3 种参数传递方法 inline/external/by-reference、P2P 架构）
- Updated: index.md (35 pages total)

## [2026-05-08] ingest | CASSINI (arXiv:2308.00852)
- Source: raw/papers/cassini-network-aware-scheduling-2308.00852.pdf
- Created:
  - entities/cassini.md — Network-aware ML 集群调度器（几何抽象、统一圆、兼容性评分、Affinity 图、time-shift 交错）
- Updated: index.md (31 pages total)
- Key: 利用 DNN 训练周期性通信模式，通过 time-shift 交错不同 job 的 Up/Down 相位。vs Themis 1.5× avg / 2.2× tail，vs Pollux 1.6× avg / 2.5× tail。ECN 标记降低 33×。

## [2026-05-11] ingest | UB Transport Layer Full Chapter (UB-TP.md)
- Source: raw/articles/UB-TP-ch6.md (§6 Transport Layer 完整章节)
- Updated:
  - concepts/ub-transport-layer.md — 大幅扩展：PSN 24-bit 机制（半空间约束、乱序范围）、Go-Back-N 重传（±fast retransmission 场景图解）、Selective 重传（BitMap + MarkPSN + HighRtxPSN）、RTO 静态/动态策略、TPG 机制与 per-flow/per-packet 负载均衡、window-based (LDCP) / rate-based / CAQM / DCQCN 拥塞控制、RTP/CTP 传输流程、ROI/ROT/ROL 模式事务层交互、互连协议对比分析
- Updated: index.md (38 pages, 传输层摘要更新)
- Key: MarkPSN 机制区分新包发送与丢失包重传阶段，快速检测非首次丢包；CAQM 逐跳审批制窗口增长；ROL 模式 TPACK 承载 TAACK 节省 RTT

## [2026-05-11] ingest | UB Network Layer Full Chapter (UB-NETWORK.md)
- Source: raw/articles/UB-NETWORK-ch5.md (§5 Network Layer 完整章节)
- Created:
  - concepts/ub-network-layer.md — 网络层核心机制（CNA/IP 双格式寻址、NTH 包头三种格式、RT 路由 2-bit 四模式、SL-VL QoS 映射、CAQM/FECN/FECN_RTT 三种拥塞标记、NPI 网络隔离（Strict/Loose 模式）、死锁避免四种机制、ICRC CRC-32 完整性保护、与 IB/Ethernet 协议对比表）
- Updated:
  - entities/unifiedbus-ub.md — 添加 source 引用
- Updated: index.md (39 pages total)
- Key: NPI 隔离比 IB PKey 更细粒度（25-bit + Permission 层级）；FECN_RTT 时间戳回传是独特功能；CAQM 逐跳审批与传输层联动

## [2026-05-11] ingest | UB Data Link Layer Full Chapter (UB-DL.md)
- Source: raw/articles/UB-DL-ch4.md (§4 Data Link Layer 完整章节)
- Created:
  - concepts/ub-data-link-layer.md — 数据链路层核心机制（Flit/DLLDP/DLLCB 封装体系、CRC/Non-CRC 双模式动态切换、4 阶段链路状态机、Init Block 参数协商表、16 VL 虚通道、Credit 流控 Exclusive/Sharing 双模式、Go-Back-N 重传 + Retry Buffer 管理 + RETRY_REQ_SM/RETRY_ACK_SM 双状态机、异常处理与链路断连恢复）
- Updated:
  - entities/unifiedbus-ub.md — 添加 source 引用
- Updated: index.md (40 pages total)
- Key: Credit Sharing 模式允许 VL 间动态共享接收 buffer，比 IB 更灵活；封装模式可运行时切换（BER 触发物理层 retrain）；Retry Buffer 死锁预防通过优先发 Crd_Ack Block 解决互锁

## [2026-05-11] ingest | UB Physical Layer Full Chapter (UB-PHY.md)
- Source: raw/articles/UB-PHY-ch3.md (§3 Physical Layer 完整章节)
- Created:
  - concepts/ub-physical-layer.md — 物理层核心机制（PCS FEC RS(128,120) T=2/4 双模式、eBCH-16 AMCTL 40-symbol 控制结构、PMA SerDes NRZ/PAM4 + Gray 编码 + Precoding、LMSM 10 态链路训练状态机、QDLWS 快速动态宽度切换不中断数据、3 种均衡模式 Skip/Only_Highest/Full、FEC/CRC 运行时动态切换、低功耗 PRBS23 CDR 保持、端口类型随机数协商）
- Updated:
  - entities/unifiedbus-ub.md — 添加 source 引用
- Updated: index.md (41 pages total)
- Key: QDLWS 是 UB 独特功能（IB/PCIe 不支持不中断数据的动态宽度切换）；eBCH-16 对 AMCTL 提供比标准协议更强的独立保护；非对称 TX/RX 宽度支持功耗优化；最大 118 Gbit/s/lane

## [2026-05-11] lint | Wiki 健康检查
- 检查范围：39 页 + 15 raw + 2 PDF
- 修复项：
  - 修复 6 个 broken wikilinks（DeepSeek-V3, Muon Optimizer, spatial-execution, plesiosynchronous-protocol, scale-up, scale-up-fabric）
  - 修复 index.md 7 个大小写不匹配（CSA-HCA→csa-hca 等）
  - 修复 deepseek-v4 entity/summary 中 10+ 个 PascalCase wikilinks→lowercase
  - 补充 2 个 analysis 页面 frontmatter（wse-nom-contradiction-analysis, cerebras-wse-vs-groq-network-comparison）
  - 为 16 个 orphan 页面添加入站链接（UB 5 层交叉引用、DeepSeek V4 技术交叉引用、CASSINI→M2N、信息论→LPU）
  - 更新 SCHEMA.md taxonomy 新增 29 个 tag（transport, data-link, physical-layer, serdes, fec, huawei 等）
- 残余：
  - 0 broken wikilinks
  - 0 missing frontmatter
  - 0 index/filesystem 不一致
  - 3 个 residual orphan（cerebras-wse-vs-groq-comparison 分析页、ub-transaction-layer 伪孤儿、ub-physical-layer 新页待后续页面引用）
  - 4 个 oversize 页面（ub-resource-management 239行, ub-transaction-layer 249行, cerebras-wse-vs-groq 300行, wse-nom-contradiction 215行）
- Tag: 29 新 tag 加入 taxonomy，0 个未注册 tag
