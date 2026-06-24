# Concept

* [Cerebras Color Mechanism](cerebras-color-mechanism.md) - WSE Color 虚拟通道机制：静态路由+独立缓冲+Color×4任务调度+独立反压，Fabric/Local Color 双类型
* [CMX & STX](cmx-stx.md) - NVIDIA 推理存储平台：CMX（Tier G3.5 NVMe KV cache）+ STX（BF-4 存储 rack 参考架构）
* [CSA and HCA (Hybrid Attention)](csa-hca.md) - 两级压缩注意力：CSA 温和压缩+稀疏选择，HCA 激进压缩+dense attention
* [Deterministic Execution](deterministic-execution.md) - 编译器控制时序、消除 jitter 的执行范式
* [Disaggregated Inference](disaggregated-inference.md) - 解耦推理：attention/FFN 分离部署，独立扩展，batch 聚合
* [DSec Sandbox Platform](dsec-sandbox.md) - DeepSeek Elastic Compute 沙箱平台，4 种执行基板，数十万并发
* [Flattened Butterfly 拓扑](flattened-butterfly-topology.md) - Flattened Butterfly 片上拓扑：高基数路由器降低直径，concentration + bypass channel，2-hop 直径，38% 功耗降低
* [FP4 Quantization-Aware Training](fp4-qat.md) - FP4 量化感知训练，无损 FP4→FP8 反量化
* [Heterogeneous Inference](heterogeneous-inference.md) - GPU + LPU 异构推理，分别优化 prefill/decode
* [Inference Capacity Trap](inference-capacity-trap.md) - 推理容量陷阱：KV cache 饱和导致 preemption + recomputation，throughput 崩溃
* [LPU Architecture](lpu-architecture.md) - Groq LPU 推理专用架构：SRAM-first、显式数据搬运、编译器调度
* [M2N Communication](m2n-communication.md) - M2N 不对称通信模式，disaggregated inference 核心，4.2× NCCL 优化
* [Manifold-Constrained Hyper-Connections (mHC)](mhc.md) - 流形约束超连接，Birkhoff polytope 约束残差映射
* [MegaMoE Kernel (Expert Parallelism Overlap)](megamoe-kernel.md) - MoE 专家并行 mega-kernel，wave-based 通信计算全重叠
* [Multi-plane Clos Topology for AI Training](multi-plane-clos-topology.md) - 多平面 CLOS 拓扑：2-tier 131K GPU，低延迟高冗余，MRC 容错，Z3 形式化分析，bitwise reproducibility
* [Muon Optimizer](muon-optimizer.md) - 矩阵正交化优化器，Hybrid Newton-Schulz 迭代
* [NoC Router 微架构](noc-router-microarchitecture.md) - NoC Router 微架构：链路级流控/EB/credit、Switch/仲裁器（RR/2D 矩阵）、WH/VC 流水线 Router、VA/SA 分配器优化
* [NVIDIA CPO Roadmap](nvidia-cpo-roadmap.md) - NVIDIA CPO 用于 scale-up 的路线图：Rubin NVL576 测试 → Feynman NVL1152 volume ramp
* [Parallelism Transition Point](parallelism-transition-point.md) - 并行度切换点：32B 是 DP→TP inflection，MoE 需 hybrid PP+TP
* [Prefill-Decode Resource Divergence](prefill-decode-divergence.md) - Prefill（compute-bound）vs Decode（bandwidth-bound）资源需求正交，>99% 时间在 decode
* [Reasoning Cliff](reasoning-cliff.md) - 推理悬崖：KV 线性增长使 HBM 饱和，scheduler 进入 convoy mode
* [SRv6 Source Routing for AI Supercomputers](srv6-source-routing.md) - AI 超算静态源路由：SRv6 uSID uN 转发，禁用动态路由，与 MRC 协同
* [Switching Elements](switching-elements.md) - 交换单元：空分/时分交换，开关阵列与共享存储器/总线，性能指标
* [Switching Networks](switching-networks.md) - 交换网络：CLOS 三级网络（严格/可重排无阻塞），TST 网络，Banyan 网络
* [Switching Principles](switching-principles.md) - 交换原理基础：电路交换/分组交换，三对基本概念，交换系统结构
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
* [WSE Performance Model](wse-performance-model.md) - WSE 通信性能模型：T=max(C,E/N)+L+(2TR+1)D，四瓶颈项（contention/energy/distance/depth），<4% 预测误差
* [WSE Reduce Algorithms](wse-reduce-algorithms.md) - WSE Reduce/AllReduce 算法族：Star/Chain/Tree/Two-Phase/Auto-Gen，模型驱动选择，Auto-Gen ≤1.4× 下界
* [智能体辅助编程的信息论价值模型](information-theoretic-value-model.md) - 智能体辅助编程的信息论价值模型：V ∝ I(S;K)，知识与任务的匹配度决定 Agent 价值
