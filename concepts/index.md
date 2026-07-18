# Concept

* [3D-Stacked AI Chip](3d-stacked-ai-chip.md) - 3D 堆叠 AI 芯片：TSV 垂直堆叠 DRAM bank 于 AI core 之上，分布式内存与专用总线带来带宽扩展与利用率新挑战
* [Adaptive Routing for NoC](adaptive-routing-noc.md) - D&T Ch.6-7 自适应路由：最小/非最小、Valiant VRR、VC 与拥塞感知；Duato 逃逸子网预告；DOR vs 自适应选型与 WSE/AllReduce
* [Architecture Benchmark Methodology](architecture-benchmark-methodology.md) - 体系结构量化评估方法论：几何均值、Speedup 计算、SPEC/MLPerf 原则与常见数据陷阱
* [Architecture Paper Reading Methodology](architecture-paper-reading-methodology.md) - 体系结构论文 5 步精读法 + 四大量化武器（归因/Roofline/敏感性/Pareto）；以 Luczynski HPDC'24 Wafer-Scale Reduce 为范例
* [Basic Data-Flow Processor](basic-data-flow-processor.md) - Dennis & Misunas (1975) 基本数据流处理器：token/actor 图、Instruction Cell + 仲裁/分发网络、decider/T-gate/merge 条件与迭代、Cell Block 两级存储作活跃指令 cache
* [Branch Prediction](branch-prediction.md) - 分支预测：1-bit/2-bit 饱和计数器、局部与全局历史、TAGE/BTB、分支惩罚对 CPI 的量化影响
* [Butterfly and MIN Topology](butterfly-min-topology.md) - 多级互连网络（MIN）：k-ary n-fly Butterfly、完美洗牌、自路由；Omega/Banyan/Delta 同构；Batcher-Banyan 无阻塞；与 Clos 路径多样性对比
* [Cache Coherence](cache-coherence.md) - 多核 Cache 一致性：MESI/MOESI 状态机、Snooping vs Directory、False Sharing，与 WSE 无共享地址空间的对比
* [Cerebras Color Mechanism](cerebras-color-mechanism.md) - WSE Color 虚拟通道机制：静态路由+独立缓冲+Color×4任务调度+独立反压，Fabric/Local Color 双类型
* [Clos and Fat-Tree Topology](clos-fat-tree-topology.md) - 间接网络：终端/交换分离、Clos C(n,m,r) 无阻塞条件、Fat-Tree 代价等价与 Beneš RNB，及 InfiniBand/Jupiter 与 WSE 规模分界
* [CMX & STX](cmx-stx.md) - NVIDIA 推理存储平台：CMX（Tier G3.5 NVMe KV cache）+ STX（BF-4 存储 rack 参考架构）
* [Collective-Capable NoC](collective-capable-noc.md) - FlooNoC 扩展：AXI 多地址 mask、XY fork 组播、并行/宽归约；DCA 范式（互连借 FPU 做 in-network 算术归约，router +16.9%、tile <1%）
* [Constable Load Elimination](constable-load-elimination.md) - ISCA 2024 Best Paper：SLD/RMT/AMT 识别 likely-stable load 并跳过执行；12.4 KB/core、+5.1% perf、-3.4% 动态功耗、SMT +8.8%；与 LVP 正交
* [Core Group (DRAM Access Synchronization)](core-group-dram-access.md) - 3D AI 芯片 core group：物理相邻 core 组内通过 hardware tracker 同步 DRAM 访问，缓解 row-buffer 冲突
* [CPU Pipeline Fundamentals](cpu-pipeline-fundamentals.md) - 五级流水线（IF/ID/EX/MEM/WB）、三大冒险（结构/数据/控制）、Forwarding 与分支惩罚
* [CSA and HCA (Hybrid Attention)](csa-hca.md) - 两级压缩注意力：CSA 温和压缩+稀疏选择，HCA 激进压缩+dense attention
* [CXL Tiered Memory](cxl-tiered-memory.md) - CXL 扩展内存分层 — 页迁移（M5）、解耦内存数据通路（CosMoS）、fabric（Aurelia）；把冷页/容量迁出本机 DRAM
* [Deadlock-Free Routing CDG and Dally Theorem](deadlock-free-routing-cdg-dally.md) - D&T Ch.8.1-8.4：通道依赖图 CDG、Dally & Seitz 无死锁定理、虫孔易死锁、Torus dateline/≥2 VC、Mesh 单 VC；WSE 选型
* [Deterministic Execution](deterministic-execution.md) - 编译器控制时序、消除 jitter 的执行范式
* [Deterministic Routing and DOR](deterministic-routing-dor.md) - 确定性路由与维序路由（DOR）：XY/Y-first、e-cube、源路由 vs 分布式；Mesh/Hypercube 最短路径与 CDG 无死锁直觉；WSE 工业选型
* [Disaggregated Inference](disaggregated-inference.md) - 解耦推理：attention/FFN 分离部署，独立扩展，batch 聚合
* [Distributed GEMM Algorithms](distributed-gemm-algorithms.md) - 分布式内存矩阵乘算法谱系：Cannon（2D mesh ring-shift）、SUMMA（broadcast 外积）、2.5D/3D SUMMA（通信–内存权衡）；α+β 代价模型、SBP 切分 vs 映射放置；T10 rTensor 形式化 Cannon
* [DNN Accelerator Systolic Dataflow](dnn-accelerator-systolic-dataflow.md) - H&P Ch.7 DSA：脉动阵列、WS/OS/RS 数据复用、Roofline for NPU、TPU vs GPU vs WSE SLA；晶体管从控制迁到 MAC
* [DRAM and Memory System](dram-memory-system.md) - DRAM 访问时序与 Row Buffer、Channel/Bank 并行、DDR/HBM 带宽公式、内存墙与 Roofline Ridge Point、WSE 分布式 SRAM 对 HBM 的绕过
* [DSA Processor Design Tradeoffs](dsa-processor-design-tradeoffs.md) - 领域专用处理器设计取舍：现代 CPU 传统武器（OoO/Cache/分支预测/TLB）的能力代价矩阵 vs WSE SLA 核
* [DSec Sandbox Platform](dsec-sandbox.md) - DeepSeek Elastic Compute 沙箱平台，4 种执行基板，数十万并发
* [DSpark Speculative Decoding](dspark-speculative-decoding.md) - DeepSeek 半自回归 speculative decoding：并行 DFlash backbone + Markov sequential head、confidence-scheduled 负载感知 verify，V4 生产 +60–85% 单用户速度
* [Duato Escape VC Deadlock-Free Routing](duato-escape-vc-deadlock-free-routing.md) - D&T Ch.8.5-8.8：Duato 定理（逃逸子网）、自适应+逃逸 VC、避免 vs 恢复、协议层 Request/Response 死锁；Dally 的推广
* [End-to-End Memory Data Path](end-to-end-memory-data-path.md) - 存储篇综合（Day 17-22）：load 全路径 AMAT 层级展开、内存墙时间线、一致性决策树、同步成本量级、WSE 消除 off-chip 的简化路径
* [Eyeriss Accelerator](eyeriss-accelerator.md) - MIT 65nm CNN 加速器：168 PE 空间阵列、Row Stationary (RS) 可重构 dataflow、四级存储层次、GIN 单周期组播 NoC、RLC 压缩与 PE data gating；AlexNet 83.1 GMAC/s/W
* [FEATHER Accelerator](feather-accelerator.md) - 可重构 DNN 加速器：NEST 2D PE 阵列 + BIRRD 蝶形归约/重排网络，RIR 在归约中隐藏 layout 切换，Layoutloop 联合 dataflow-layout 搜索
* [FlashAttention](flashattention.md) - IO-aware 精确 attention：SRAM tiling + online softmax + 反向重算；O(N) 内存、HBM 访问 IO-optimal；GPT-2 attention 7.6×、训练最高 3×
* [FlashAttention-2](flashattention-2.md) - IO-aware 精确 attention 第二代：减 non-matmul FLOP、序列维并行、warp 级 split-Q；相对 FlashAttention ~2×，A100 最高 73% 峰值 TFLOPs/s、训练 225 TFLOPs/s
* [FlashAttention-3](flashattention-3.md) - Hopper H100 IO-aware attention 第三代：TMA/WGMMA 异步 producer-consumer、GEMM-softmax 流水线、FP8 block quant+incoherent processing；FP16 740 TFLOPs/s、相对 FA2 1.5–2×
* [FlashDecoding++](flashdecoding-plus-plus.md) - GPU LLM 推理引擎：统一 max 值的异步 partial softmax、M 维 pad-8 flat GEMM+双缓冲、FastGEMV/CUTLASS 启发式 dataflow；相对 FlashDecoding 平均 1.37×、HF 最高 4.86×
* [FlashMoE Kernel](flashmoe-kernel.md) - NeurIPS 2025 单 persistent GPU kernel 融合分布式 MoE：actor 调度、NVSHMEM 设备端 RDMA、payload-efficient dispatch；8×H100 相对 SOTA 最高 6× 延迟、5.7× 吞吐、93% SM 利用率
* [Flattened Butterfly 拓扑](flattened-butterfly-topology.md) - Flattened Butterfly 片上拓扑：高基数路由器降低直径，concentration + bypass channel，2-hop 直径，38% 功耗降低
* [Flow Control Fundamentals](flow-control-fundamentals.md) - Dally & Towles Ch.9 — Message/Packet/Flit/Phit；电路/报文/虫孔/VCT 延迟公式；HoL blocking；与死锁的关系
* [FP4 Quantization-Aware Training](fp4-qat.md) - FP4 量化感知训练，无损 FP4→FP8 反量化
* [GEMM vs GEMV in LLM Inference](gemm-vs-gemv.md) - 矩阵乘 vs 矩阵-向量乘：算子形状、算术强度（AI）、Roofline 类别、Prefill/Decode 对应关系；GEMM compute-bound（AI~1000），GEMV bandwidth-bound（AI~2）；H100 decode <1% 峰值 FLOPS，理论时间 vs 实际时间差 100×
* [GPU SIMT Architecture](gpu-simt-architecture.md) - H&P Ch.4 GPU/SIMT：Warp 锁步、Warp Divergence、Occupancy 延迟隐藏、H100 内存层次、Tensor Core；与 CPU OoO / WSE MIMD 对比
* [Heterogeneous Inference](heterogeneous-inference.md) - GPU + LPU 异构推理，分别优化 prefill/decode
* [Inference Capacity Trap](inference-capacity-trap.md) - 推理容量陷阱：KV cache 饱和导致 preemption + recomputation，throughput 崩溃
* [Instruction-Level Parallelism](instruction-level-parallelism.md) - 指令级并行 ILP：超标量 vs VLIW、真依赖与名称依赖、静态/动态多发射权衡
* [Interconnection Network Cost Model](interconnection-network-cost-model.md) - 互连网络开销与性能模型：节点/链路/交换成本、零负载延迟公式、注入带宽与二分带宽上界、直连网络 d≈O(log N)
* [Interconnection Network Design Space](interconnection-network-design-space.md) - Dally & Towles 互连网络四层设计空间（应用→拓扑/路由/流控→微架构）、基本术语与三大应用域
* [Interconnection Network Protocol Stack](interconnection-network-protocol-stack.md) - 互连网络四层协议栈（物理/链路/网络/传输）、Network Interface 边界，与 NoC 及 UB 的对应关系
* [Interconnection Topology Metrics](interconnection-topology-metrics.md) - 互连拓扑度量：度/直径/平均距离/二分带宽/对称性，k-ary n-cube 公式，Mesh vs Torus 对比
* [ISA Design Principles](isa-design-principles.md) - 指令集设计原则：Load/Store、RISC-V 编码、CISC vs RISC 历史教训、寄存器与条件码权衡
* [Linear and Ring Topology](linear-ring-topology.md) - 线形阵列与环形拓扑：度/直径/二分带宽度量，双向环即 1-D Torus，NoC/SAN/Die-to-Die 应用与 Chordal Ring 扩展
* [LLM Distributed Training Collectives](llm-distributed-training-collectives.md) - H&P Ch.6/10 语境下 LLM 训练集体通信：AllReduce/AllGather/All-to-All；Ring vs Tree；DP/TP/PP/EP 配方；通信-计算重叠与 WSE 片上 vs 跨 wafer
* [LPU Architecture](lpu-architecture.md) - Groq LPU 推理专用架构：SRAM-first、显式数据搬运、编译器调度
* [M2N Communication](m2n-communication.md) - M2N 不对称通信模式，disaggregated inference 核心，4.2× NCCL 优化
* [Manifold-Constrained Hyper-Connections (mHC)](mhc.md) - 流形约束超连接，Birkhoff polytope 约束残差映射
* [MegaMoE Kernel (Expert Parallelism Overlap)](megamoe-kernel.md) - MoE 专家并行 mega-kernel，wave-based 通信计算全重叠
* [Memory Consistency Model](memory-consistency-model.md) - 内存一致性模型：Coherence vs Consistency、SC/TSO/ARM 重排规则、fence 契约、CAS/LL-SC 与 MCS 锁，及 WSE/NPU 同步设计
* [Memory Fence and Barrier](memory-fence-barrier.md) - 内存屏障：ISA 顺序语义、Store Buffer/Invalidate Queue 排空、NoC coherence 路径、x86/ARM/RISC-V 变体与 WSE 无 coherence 对照
* [Memory Hierarchy and Cache](memory-hierarchy-cache.md) - 内存墙、存储层次、Cache 映射与 3C 模型、AMAT 优化框架、与 WSE SRAM-only 设计的对比
* [Mesh and Torus Topology](mesh-torus-topology.md) - 2-D Mesh/Torus 与 k-ary n-cube：度/直径/二分带宽、Dally 维度-延迟-吞吐量权衡、XY 维序路由，及 WSE/Blue Gene 选型
* [Mixed Precision Training](mixed-precision-training.md) - FP16/BF16 混合精度训练经典配方 — FP32 master weights、loss scaling、FP32 accumulate；现代 LLM 训练默认基线
* [MPI Reduce/AllReduce Algorithms](mpi-reduce-allreduce-algorithms.md) - Rabenseifner ICCS 2004 五类 MPI 归约算法：二叉树、recursive doubling、halving&doubling、binary blocks、ring；α+nβ 代价模型与 (p,n) 自适应选择；MPICH-2 长向量基础
* [Multi-plane Clos Topology for AI Training](multi-plane-clos-topology.md) - 多平面 CLOS 拓扑：2-tier 131K GPU，低延迟高冗余，MRC 容错，Z3 形式化分析，bitwise reproducibility
* [Multicore SMT and NUCA](multicore-smt-nuca.md) - H&P Ch.5.7-5.9：Fine/Coarse/SMT 多线程、SMT 1.2-1.3× 收益、Amdahl+通信/一致性 Overhead、NUCA 非均匀 Cache、WSE 反 Amdahl 哲学
* [Muon Optimizer](muon-optimizer.md) - 矩阵正交化优化器，Hybrid Newton-Schulz 迭代
* [NoC Fundamentals (H&P Appendix F)](noc-fundamentals-hp-appendix-f.md) - H&P 附录 F 互连网络五问：拓扑/路由/流控/路由器/性能；直连 vs 间接、虫孔+VC、饱和吞吐与 WSE-scale 扩展指标
* [NoC Router Pipeline and Allocators](noc-router-pipeline-allocators.md) - Dally & Towles Ch.11–12 — RC/VA/SA/ST/LT 五级流水；Crossbar；RR / Matrix / iSLIP / Wavefront 仲裁
* [NoC Router Pipeline Optimizations](noc-router-pipeline-optimizations.md) - Dally & Towles Ch.12–13 — Speculative SA、Look-ahead Routing、Bypass、Shared Buffer、动态 VC、High-Radix、CMesh
* [NoC Router 微架构](noc-router-microarchitecture.md) - NoC Router 微架构：链路级流控/EB/credit、Switch/仲裁器（RR/2D 矩阵）、WH/VC 流水线 Router、VA/SA 分配器优化
* [Numeric Formats for AI Hardware](numeric-formats-ai-hardware.md) - IEEE 754 浮点与 AI 数据格式（FP32/FP16/BF16/FP8/INT8）的精度、动态范围与硬件面积权衡
* [NVIDIA CPO Roadmap](nvidia-cpo-roadmap.md) - NVIDIA CPO 用于 scale-up 的路线图：Rubin NVL576 测试 → Feynman NVL1152 volume ramp
* [Out-of-Order Execution](out-of-order-execution.md) - 乱序执行：Tomasulo 算法、保留站、ROB 顺序提交、寄存器重命名与指令窗口 IPC 收益递减
* [PagedAttention and vLLM Serving](pagedattention-vllm.md) - vLLM 服务系统的核心 KV cache 内存管理：借鉴 OS 虚拟内存与分页机制，将 KV cache 切为 fixed-size block 跨请求共享/重映射；解决 KV cache fragmentation 与不可共享
* [Parallelism Transition Point](parallelism-transition-point.md) - 并行度切换点：32B 是 DP→TP inflection，MoE 需 hybrid PP+TP
* [Plasticine Accelerator](plasticine-accelerator.md) - Stanford ISCA 2017 CGRA：PCU/PMU 空间阵列直接支持 Map/FlatMap/Fold/HashReduce parallel patterns；28nm 112.8mm²、12.3 TFLOPS、相对 FPGA 最高 76.9× Perf/W
* [Post-Moore Architecture Frontiers](post-moore-architecture-frontiers.md) - 摩尔/Dennard 之后的体系结构主线：AI 加速器、NoC 新方向、Chiplet、Wafer-Scale；三条路 DSA × Packaging × Novel devices
* [Prefill-Decode Resource Divergence](prefill-decode-divergence.md) - Prefill（compute-bound）vs Decode（bandwidth-bound）资源需求正交，>99% 时间在 decode
* [Quantitative Architecture Fundamentals](quantitative-architecture-fundamentals.md) - Hennessy & Patterson 量化体系结构基石：CPU 性能公式、Amdahl 定律、局部性、功耗墙、Dennard Scaling 终结与暗硅
* [Reasoning Cliff](reasoning-cliff.md) - 推理悬崖：KV 线性增长使 HBM 饱和，scheduler 进入 convoy mode
* [SpaDA Programming Language](spada-programming-language.md) - 空间数据流编程语言：place/dataflow/compute 三构造、async/await、GT4Py→CSL 编译管线与 checkerboard 路由/task 融合优化，WSE-2 上 14× 减码、260 TFlop/s stencil
* [SRv6 Source Routing for AI Supercomputers](srv6-source-routing.md) - AI 超算静态源路由：SRv6 uSID uN 转发，禁用动态路由，与 MRC 协同
* [SSD and NVMe Storage System](ssd-nvme-storage-system.md) - 片外存储：NAND/FTL/GC/写放大、RAID 0/1/5/6 写惩罚、NVMe 多队列与 PCIe 带宽、read() 延迟分解与 io_uring；WSE memoryX 与 CMX KV tier
* [Superscalar CPU Research (2023-2026)](superscalar-cpu-research-2023-2026.md) - 2023-2026 超标量 CPU 顶会综述：异构旁路子系统（Constable/Bullseye/Prophet）、CVA6S+ 开源 baseline、OoO 边际饱和与 LLM memory-bound 优化；WSE/NPU 关联矩阵与核内同步 Gap
* [Switching Elements](switching-elements.md) - 交换单元：空分/时分交换，开关阵列与共享存储器/总线，性能指标
* [Switching Networks](switching-networks.md) - 交换网络：CLOS 三级网络（严格/可重排无阻塞），TST 网络，Banyan 网络
* [Switching Principles](switching-principles.md) - 交换原理基础：电路/报文/分组/虫孔交换，历史演进，三对基本概念，交换系统结构
* [TileLang DSL](tilelang.md) - Kernel 开发 DSL
* [TileLoom Compiler](tileloom-compiler.md) - NUS TileLoom：MLIR 端到端 dataflow planning，Triton/Helion → spatiotemporal mapping + df 硬件模型；Tenstorrent 2-D mesh 上 FlashAttention ~2× TTNN
* [Topology Optimization Variants](topology-optimization-variants.md) - 拓扑变体与优化：Folding、Concentrated/Collapsed Mesh、Express Cube、Dally 1990 最优维度定律、高基数路由器；Compression vs Expansion 权衡
* [UB 事务层](ub-transaction-layer.md) - UB 事务层：四类事务（Memory/Message/Maintenance/Management）、Full/Compact 包头、安全 Token 验证、四种服务模式（ROI/ROT/ROL/UNO）
* [UB 传输层机制](ub-transport-layer.md) - UB 传输层：四种模式（RTP/CTP/UTP/TP Bypass）、PSN 机制、Go-Back-N/Selective 重传、TPG 多路径负载均衡、LDCP/CAQM/DCQCN 拥塞控制、ROL 模式事务-传输联动
* [UB 内存管理](ub-memory-management.md) - UB 内存管理：Home-User 模型、UBMD、UMMU 两阶段地址翻译+权限检查、UB Decoder
* [UB 数据链路层机制](ub-data-link-layer.md) - UB 数据链路层：Flit/DLLDP/DLLCB 封装、CRC/Non-CRC 双模式、4 阶段链路状态机、Init Block 参数协商、16 VL 虚通道、Credit 流控（Exclusive/Sharing）、Go-Back-N 重传 + Retry Buffer 管理、双状态机（RETRY_REQ_SM/RETRY_ACK_SM）
* [UB 物理层机制](ub-physical-layer.md) - UB 物理层：PCS FEC RS(128,120) T=2/4、eBCH-16 AMCTL、PMA SerDes NRZ/PAM4、LMSM 10 态链路训练、QDLWS 动态宽度切换、3 种均衡模式、FEC/CRC 动态切换
* [UB 编程模型与 URMA](ub-programming-models.md) - UB 编程模型：Load/Store 同步、URMA 异步访问（Jetty/事务队列/内存池化/死锁避免）
* [UB 网络层机制](ub-network-layer.md) - UB 网络层：CNA/IP 双格式寻址、RT 路由（per-flow/per-packet）、SL-VL QoS、CAQM/FECN/FECN_RTT 拥塞标记、NPI 网络隔离、死锁避免、ICRC 完整性保护
* [UB 资源管理](ub-resource-management.md) - UB 资源管理：UBFM、Entity 模型/池化/虚拟化、配置空间、管理命令、三级复位+三级错误 RAS
* [URPC (UB 远程过程调用)](ub-urpc.md) - URPC 远程过程调用：Client/Server/Worker，pass-by-value/reference，P2P 架构
* [Virtual Channel Flow Control](virtual-channel-flow-control.md) - Dally & Towles Ch.10 — VC 缓解 HoL；VC Allocator；Credit / On-Off / Window 流控选型；VC 与逃逸通道
* [Virtual Memory and TLB](virtual-memory-tlb.md) - 虚拟内存四作用、页表与 TLB、巨页与 TLB Shootdown、AMAT 含地址转换、WSE 无 MMU 的工程权衡
* [Voxel Simulator](voxel-simulator.md) - Voxel：编译器感知的 3D AI 芯片端到端仿真框架，支持 compute paradigm / mapping / NoC / DRAM 协同探索
* [WaferLLM System](waferllm-system.md) - Edinburgh/MSR 晶圆级 LLM 推理：PLMR 设备模型、MeshGEMM/MeshGEMV、KV shift、prefill/decode 百万 core parallelism；WSE-2 上 10–20× SGLang/A100 集群
* [WSE Performance Model](wse-performance-model.md) - WSE 通信性能模型：T=max(C,E/N)+L+(2TR+1)D，四瓶颈项（contention/energy/distance/depth），<4% 预测误差
* [WSE Quantitative Architecture Analysis](wse-quantitative-architecture-analysis.md) - arch-study Day 26：用 Amdahl/Roofline/Mesh 指标量化 WSE-3；片上 vs 片外带宽矛盾、良率容错、WaferLLM GEMV 606× 边界
* [WSE Reduce Algorithms](wse-reduce-algorithms.md) - WSE Reduce/AllReduce 算法族：Star/Chain/Tree/Two-Phase/Auto-Gen，模型驱动选择，Auto-Gen ≤1.4× 下界
* [Æthereal NoC](aethereal-noc.md) - Philips Æthereal — contention-free TDM 电路交换实现 Guaranteed Services；GS+BES；slot table；分布式/集中编程与路由器代价谱系
* [智能体辅助编程的信息论价值模型](information-theoretic-value-model.md) - 智能体辅助编程的信息论价值模型：V ∝ I(S;K)，知识与任务的匹配度决定 Agent 价值
