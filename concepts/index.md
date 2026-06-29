# Concept

* [3D-Stacked AI Chip](3d-stacked-ai-chip.md) - 3D 堆叠 AI 芯片：TSV 垂直堆叠 DRAM bank 于 AI core 之上，分布式内存与专用总线带来带宽扩展与利用率新挑战
* [Architecture Benchmark Methodology](architecture-benchmark-methodology.md) - 体系结构量化评估方法论：几何均值、Speedup 计算、SPEC/MLPerf 原则与常见数据陷阱
* [Branch Prediction](branch-prediction.md) - 分支预测：1-bit/2-bit 饱和计数器、局部与全局历史、TAGE/BTB、分支惩罚对 CPI 的量化影响
* [Cerebras Color Mechanism](cerebras-color-mechanism.md) - WSE Color 虚拟通道机制：静态路由+独立缓冲+Color×4任务调度+独立反压，Fabric/Local Color 双类型
* [CMX & STX](cmx-stx.md) - NVIDIA 推理存储平台：CMX（Tier G3.5 NVMe KV cache）+ STX（BF-4 存储 rack 参考架构）
* [Core Group (DRAM Access Synchronization)](core-group-dram-access.md) - 3D AI 芯片 core group：物理相邻 core 组内通过 hardware tracker 同步 DRAM 访问，缓解 row-buffer 冲突
* [CPU Pipeline Fundamentals](cpu-pipeline-fundamentals.md) - 五级流水线（IF/ID/EX/MEM/WB）、三大冒险（结构/数据/控制）、Forwarding 与分支惩罚
* [CSA and HCA (Hybrid Attention)](csa-hca.md) - 两级压缩注意力：CSA 温和压缩+稀疏选择，HCA 激进压缩+dense attention
* [Deterministic Execution](deterministic-execution.md) - 编译器控制时序、消除 jitter 的执行范式
* [Disaggregated Inference](disaggregated-inference.md) - 解耦推理：attention/FFN 分离部署，独立扩展，batch 聚合
* [DSA Processor Design Tradeoffs](dsa-processor-design-tradeoffs.md) - 领域专用处理器设计取舍：现代 CPU 传统武器（OoO/Cache/分支预测/TLB）的能力代价矩阵 vs WSE SLA 核
* [DSec Sandbox Platform](dsec-sandbox.md) - DeepSeek Elastic Compute 沙箱平台，4 种执行基板，数十万并发
* [Flattened Butterfly 拓扑](flattened-butterfly-topology.md) - Flattened Butterfly 片上拓扑：高基数路由器降低直径，concentration + bypass channel，2-hop 直径，38% 功耗降低
* [FP4 Quantization-Aware Training](fp4-qat.md) - FP4 量化感知训练，无损 FP4→FP8 反量化
* [Heterogeneous Inference](heterogeneous-inference.md) - GPU + LPU 异构推理，分别优化 prefill/decode
* [Inference Capacity Trap](inference-capacity-trap.md) - 推理容量陷阱：KV cache 饱和导致 preemption + recomputation，throughput 崩溃
* [Instruction-Level Parallelism](instruction-level-parallelism.md) - 指令级并行 ILP：超标量 vs VLIW、真依赖与名称依赖、静态/动态多发射权衡
* [Interconnection Network Cost Model](interconnection-network-cost-model.md) - 互连网络开销与性能模型：节点/链路/交换成本、零负载延迟公式、注入带宽与二分带宽上界、直连网络 d≈O(log N)
* [Interconnection Network Design Space](interconnection-network-design-space.md) - Dally & Towles 互连网络四层设计空间（应用→拓扑/路由/流控→微架构）、基本术语与三大应用域
* [Interconnection Network Protocol Stack](interconnection-network-protocol-stack.md) - 互连网络四层协议栈（物理/链路/网络/传输）、Network Interface 边界，与 NoC 及 UB 的对应关系
* [Interconnection Topology Metrics](interconnection-topology-metrics.md) - 互连拓扑度量：度/直径/平均距离/二分带宽/对称性，k-ary n-cube 公式，Mesh vs Torus 对比
* [ISA Design Principles](isa-design-principles.md) - 指令集设计原则：Load/Store、RISC-V 编码、CISC vs RISC 历史教训、寄存器与条件码权衡
* [LPU Architecture](lpu-architecture.md) - Groq LPU 推理专用架构：SRAM-first、显式数据搬运、编译器调度
* [M2N Communication](m2n-communication.md) - M2N 不对称通信模式，disaggregated inference 核心，4.2× NCCL 优化
* [Manifold-Constrained Hyper-Connections (mHC)](mhc.md) - 流形约束超连接，Birkhoff polytope 约束残差映射
* [MegaMoE Kernel (Expert Parallelism Overlap)](megamoe-kernel.md) - MoE 专家并行 mega-kernel，wave-based 通信计算全重叠
* [Memory Hierarchy and Cache](memory-hierarchy-cache.md) - 内存墙、存储层次、Cache 映射与 3C 模型、AMAT 优化框架、与 WSE SRAM-only 设计的对比
* [Multi-plane Clos Topology for AI Training](multi-plane-clos-topology.md) - 多平面 CLOS 拓扑：2-tier 131K GPU，低延迟高冗余，MRC 容错，Z3 形式化分析，bitwise reproducibility
* [Muon Optimizer](muon-optimizer.md) - 矩阵正交化优化器，Hybrid Newton-Schulz 迭代
* [NoC Router 微架构](noc-router-microarchitecture.md) - NoC Router 微架构：链路级流控/EB/credit、Switch/仲裁器（RR/2D 矩阵）、WH/VC 流水线 Router、VA/SA 分配器优化
* [Numeric Formats for AI Hardware](numeric-formats-ai-hardware.md) - IEEE 754 浮点与 AI 数据格式（FP32/FP16/BF16/FP8/INT8）的精度、动态范围与硬件面积权衡
* [NVIDIA CPO Roadmap](nvidia-cpo-roadmap.md) - NVIDIA CPO 用于 scale-up 的路线图：Rubin NVL576 测试 → Feynman NVL1152 volume ramp
* [Out-of-Order Execution](out-of-order-execution.md) - 乱序执行：Tomasulo 算法、保留站、ROB 顺序提交、寄存器重命名与指令窗口 IPC 收益递减
* [Parallelism Transition Point](parallelism-transition-point.md) - 并行度切换点：32B 是 DP→TP inflection，MoE 需 hybrid PP+TP
* [Prefill-Decode Resource Divergence](prefill-decode-divergence.md) - Prefill（compute-bound）vs Decode（bandwidth-bound）资源需求正交，>99% 时间在 decode
* [Quantitative Architecture Fundamentals](quantitative-architecture-fundamentals.md) - Hennessy & Patterson 量化体系结构基石：CPU 性能公式、Amdahl 定律、局部性、功耗墙、Dennard Scaling 终结与暗硅
* [Reasoning Cliff](reasoning-cliff.md) - 推理悬崖：KV 线性增长使 HBM 饱和，scheduler 进入 convoy mode
* [SRv6 Source Routing for AI Supercomputers](srv6-source-routing.md) - AI 超算静态源路由：SRv6 uSID uN 转发，禁用动态路由，与 MRC 协同
* [Switching Elements](switching-elements.md) - 交换单元：空分/时分交换，开关阵列与共享存储器/总线，性能指标
* [Switching Networks](switching-networks.md) - 交换网络：CLOS 三级网络（严格/可重排无阻塞），TST 网络，Banyan 网络
* [Switching Principles](switching-principles.md) - 交换原理基础：电路/报文/分组/虫孔交换，历史演进，三对基本概念，交换系统结构
* [TileLang DSL](tilelang.md) - Kernel 开发 DSL
* [UB 事务层](ub-transaction-layer.md) - UB 事务层：四类事务（Memory/Message/Maintenance/Management）、Full/Compact 包头、安全 Token 验证、四种服务模式（ROI/ROT/ROL/UNO）
* [UB 传输层机制](ub-transport-layer.md) - UB 传输层：四种模式（RTP/CTP/UTP/TP Bypass）、PSN 机制、Go-Back-N/Selective 重传、TPG 多路径负载均衡、LDCP/CAQM/DCQCN 拥塞控制、ROL 模式事务-传输联动
* [UB 内存管理](ub-memory-management.md) - UB 内存管理：Home-User 模型、UBMD、UMMU 两阶段地址翻译+权限检查、UB Decoder
* [UB 数据链路层机制](ub-data-link-layer.md) - UB 数据链路层：Flit/DLLDP/DLLCB 封装、CRC/Non-CRC 双模式、4 阶段链路状态机、Init Block 参数协商、16 VL 虚通道、Credit 流控（Exclusive/Sharing）、Go-Back-N 重传 + Retry Buffer 管理、双状态机（RETRY_REQ_SM/RETRY_ACK_SM）
* [UB 物理层机制](ub-physical-layer.md) - UB 物理层：PCS FEC RS(128,120) T=2/4、eBCH-16 AMCTL、PMA SerDes NRZ/PAM4、LMSM 10 态链路训练、QDLWS 动态宽度切换、3 种均衡模式、FEC/CRC 动态切换
* [UB 编程模型与 URMA](ub-programming-models.md) - UB 编程模型：Load/Store 同步、URMA 异步访问（Jetty/事务队列/内存池化/死锁避免）
* [UB 网络层机制](ub-network-layer.md) - UB 网络层：CNA/IP 双格式寻址、RT 路由（per-flow/per-packet）、SL-VL QoS、CAQM/FECN/FECN_RTT 拥塞标记、NPI 网络隔离、死锁避免、ICRC 完整性保护
* [UB 资源管理](ub-resource-management.md) - UB 资源管理：UBFM、Entity 模型/池化/虚拟化、配置空间、管理命令、三级复位+三级错误 RAS
* [URPC (UB 远程过程调用)](ub-urpc.md) - URPC 远程过程调用：Client/Server/Worker，pass-by-value/reference，P2P 架构
* [Virtual Memory and TLB](virtual-memory-tlb.md) - 虚拟内存四作用、页表与 TLB、巨页与 TLB Shootdown、AMAT 含地址转换、WSE 无 MMU 的工程权衡
* [Voxel Simulator](voxel-simulator.md) - Voxel：编译器感知的 3D AI 芯片端到端仿真框架，支持 compute paradigm / mapping / NoC / DRAM 协同探索
* [WSE Performance Model](wse-performance-model.md) - WSE 通信性能模型：T=max(C,E/N)+L+(2TR+1)D，四瓶颈项（contention/energy/distance/depth），<4% 预测误差
* [WSE Reduce Algorithms](wse-reduce-algorithms.md) - WSE Reduce/AllReduce 算法族：Star/Chain/Tree/Two-Phase/Auto-Gen，模型驱动选择，Auto-Gen ≤1.4× 下界
* [智能体辅助编程的信息论价值模型](information-theoretic-value-model.md) - 智能体辅助编程的信息论价值模型：V ∝ I(S;K)，知识与任务的匹配度决定 Agent 价值
