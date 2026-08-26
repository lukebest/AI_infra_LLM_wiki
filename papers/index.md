# Paper

* [Hot Chips 2026 Handy HBM Tutorial](hc2026-handy-hbm-tutorial.md) - Objective Analysis — HBM 吃 3× DDR 晶圆面积；DRAM 产能十年未涨；PIM/base-die 被推理推上台
* [Hot Chips 2026 Samsung HBM Base Die](hc2026-samsung-hbm-base-die.md) - Samsung — HBM4/4E B-die 改 4 nm logic；cHBM→aHBM→zHBM（WoW+HCB 取消 2.5D interposer）
* [Hot Chips 2026 SK hynix HBM Packaging](hc2026-skhynix-hbm-advanced-packaging.md) - SK hynix — HBM4 12Hi 量产/16Hi Qual；HyB 才能 ≥20Hi、pitch <18 μm；i-HBM 热阻 >30% ↓
* [Hot Chips 2026 d-Matrix Raptor 3D-DRAM](hc2026-dmatrix-raptor-3d-dram.md) - d-Matrix — 1-Hi logic-on-top；自称 ≈20× BW/mm²、13.5× 更好 mW/GB/s vs HBM4；ISCA 2026 指针
* [Hot Chips 2026 OXMIQ HBF](hc2026-oxmiq-hbf.md) - OXMIQ — HBF 是低 α/低 β 容量点；72-GPU 机柜 ~14× 容量 / ~0.6× 带宽；HBM for the rack
* [Hot Chips 2026 NVIDIA NVLink Fusion](hc2026-nvidia-riscv-nvlink-fusion.md) - NVIDIA — NVL72 全铜 72 GPU；3.6 TB/s per GPU、900 GB/s C2C、28.8 TB/s/switch tray；CHI Fusion
* [Hot Chips 2026 Pistil 20-Chiplet SLM](hc2026-pistil-20-chiplet-slm.md) - Harvard/Google/Lockheed — 16 nm 2.5D flower；512 MB / 51.2 GB/s；vs Jetson Nano 最高 7.6× 吞吐

* [HYDRA: Heterogeneous Chiplet DSE for Hybrid LLM Serving](hydra-heterogeneous-chiplet-dse-hybrid-llm.md) - UW–Madison/Ulsan — 2.5D 异构 chiplet 上 Hybrid LLM serving 的宏架构+运行时联合 DSE；平均 1.55× 吞吐、TTFT −43.7%，最高 2.3×
* [HCCL: Collective Communication for Meta MTIA 300](hccl-meta-mtia-300-collective-communication.md) - SC 2026 自称 — 包内 NIC chiplet + ME/NMC 卸载集体；机柜内最高 940 GB/s，重叠 GEMM 降幅 <0.5%；推理 PUT 集体 <6 μs
* [ReXpert: ReRAM Near-Memory FFN Pool for Disaggregated MoE](rexpert-reram-nmc-disaggregated-moe.md) - HKUST/阿里云 — 驻留 expert + core 内组播；occupancy 0.328→0.519；iso-compute vs H20 FFN 9.5×、权重搬运能 20×
* [DASH: Dual-Path HBF for MoE LLM Inference](dash-dual-path-hbf-moe-inference.md) - KAIST — GPU–HBF 直连 + HBM 基座中继；五模型几何均值吞吐 1.90× vs RelayOnly；代表负载 1.94× 吞吐 / 1.90× E2E

* [DICE: Detailed Inter-Chiplet End-to-End PHY Modeling](dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) - Uppsala — gem5 运行时 QC-LDPC/PAM4 chiplet PHY；相对 HeteroGarnet IPC 平均偏移 6.8%、最高 27.6%；9454P 跨 die 最大 C2C RMSE 89.5 vs 141.2 cycle
* [C2C-Explorer: Chip-to-Chip Interconnect DSE for LLM Systems](c2c-explorer-chip-to-chip-interconnect-llm.md) - DAC 2026 — LLM 轨迹驱动的 scale-up C2C 仿真+贝叶斯 DSE；FPGA 时序误差 2.46–8.23%；DeepSeek combine goodput +44.1%、buffer −98.4%
* [Fovea: Physical-Implication-Aware Wafer-Scale DSE](fovea-physical-implication-aware-wafer-scale-dse.md) - 清华 — 物理可行域 + Decision Domain；70 对 LLM 训练全部找回参考最优，相对穷尽参考平均 4.13×、最高 7.80×
* [ThAME: 3D Memory-Enabled Heterogeneous Accelerator for LLM MoE](thame-3d-memory-enabled-heterogeneous-moe.md) - WSU ESWEEK-26 — FeFET-NAND PNM 存 expert、DRAM-PNM 做 attention、分层树 NoC；相对 H3D-T 最高 15.7× TBT、9.8× 能效

* [3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving](3dls-3d-logic-stacked-disaggregated-llm-serving.md) - KAIST IEEE CAL 2026 — logic-on-logic 把 KVT 与 decode AllReduce 物理隔离；相对共享 D2D 最高 1.49× 吞吐、60.2% 更低 E2E
* [Mozart: Modularized and Efficient MoE Training on 3.5D Wafer-Scale Chiplet Architectures](mozart-35d-wafer-scale-moe-training.md) - UNC/UMN 3.5D 晶圆级 NoP-Tree + 专家共激活布局；Qwen3/OLMoE/DeepSeek post-training 1.92× / 2.37× / 2.17×
* [Network Design for Wafer-Scale Systems with Wafer-on-Wafer Hybrid Bonding](network-design-wafer-scale-wow-hybrid-bonding.md) - ETH Iff et al. — WoW 放置即拓扑；相对 mesh-like baseline 吞吐最高 +250%、延迟 -36%、每字节能量 -38%

* [22580: From GPT-2 to Kimi K3, Explained](ali-22580-from-gpt2-to-kimi3.md) - Ali (@waterloo_intern, Baseten) 2026-07-27 X 长文；从 GPT-2 attention 一路演化到 Kimi K3；核心论点"过去七年 LLM 真正的变化不是规模 22,580×，而是 attention 状态空间从 O(N) 到 O(1) 的选择/衰减/reset 范式"
* [MegaScale-Infer](megascale-infer-2504.02263.md) - MegaScale-Infer：MoE disaggregated attention/FFN serving，ping-pong pipeline + M2N 通信库，1.90× 吞吐提升
* [Resilient AI Supercomputer Networking using MRC and SRv6](resilient-ai-supercomputer-networking-mrc-srv6.md) - MRC+SRv6+multi-plane Clos：三管齐下的 100K+ GPU AI 训练网络容错方案，OpenAI/Microsoft 生产验证

# Summary

* [A Cloud-Scale Characterization of Remote Procedure Calls](cloud-scale-rpc-characterization.md) - SOSP 2023 Google — 700 天 fleet 级 RPC 剖析：>10K 方法、毫秒级延迟、RPC/CPU 比年增 30%；尾延迟由 RPC tax 主导
* [A Lightweight High-Throughput Collective-Capable NoC for Large-Scale ML Accelerators](collective-capable-noc-ml-accelerators.md) - FlooNoC 扩展：multicast/归约/barrier + DCA 借 Snitch FPU；router +16.9% 面积，4×4 mesh 上 multicast 5.3×、reduction 2.8×，SUMMA GEMM 最高 3.8×
* [A Preliminary Architecture for a Basic Data-Flow Processor](dennis-misunas-basic-data-flow-processor.md) - Dennis & Misunas (ISCA 1975) 基本数据流处理器：decider/T-gate/merge 条件迭代、Decision Units、Instruction Cell 两级存储作活跃指令 cache
* [AI Accelerators for Large Language Model Inference: Architecture Analysis and Scaling Strategies](ai-accelerators-llm-inference.md) - 首篇 LLM 推理加速器跨架构定量横评：五类（GPU/Systolic/SRAM-centric/WSE/Deterministic pipeline）六大操作域评估；expert parallelism 8.4× 参数-计算比但 2.1× 延迟方差
* [Alibaba HPN: A Data Center Network for Large Language Model Training](alibaba-hpn-datacenter-network-llm.md) - SIGCOMM 2024 阿里云 — LLM 训练专用 2-tier dual-plane DCN，15K GPU/Pod；+14.9% 训练吞吐，non-stacked dual-ToR 防单点
* [Aurelia: CXL Fabric with Tentacle](aurelia-cxl-fabric-tentacle.md) - WORDS 2023 — 将寻址/路由/传输层 networking 化扩展 CXL fabric；解决 PBR 单路径与 PCIe 拥塞（RDMA 延迟可 spike 3×）
* [Batude Monolithic 3D Review 2011](batude-monolithic-3d-review-2011.md) - Batude et al. ICCAD 2011 *Low-Temperature 3D Sequential Integration*；Monolithic vs TSV-based 路线对比 + port 假设与商业现实剖析
* [Balfour Tiled CMP NoC Tradeoffs](balfour-tiled-cmp-noc-tradeoffs.md) - Balfour & Dally MICRO 2006 — CMP NoC area/energy/delay Pareto；wormhole、2-stage、mesh sweet spot
* [Cache-Resident LLM Inference in GB-Scale LLCs](cache-resident-llm-inference-llc.md) - KAUST cache-resident CPU inference — weight/attention domain split + sub-operator sync; 2.04–11.51× TPOT vs llama.cpp on Llama-3.2-3B/2-7B
* [CODE PLAN: Scaling Code-Form Planning for LLM Reasoning](code-form-planning-llm-reasoning.md) - Wen et al. — code-form pseudocode plans auto-mined at scale; 2M-example training; 25.1% relative gain on 13 multi-step reasoning benchmarks
* [Constable: Safely Eliminating Load Instruction Execution](constable-load-elimination.md) - ISCA 2024 Best Paper：likely-stable load 识别 + RMT/AMT 监控；12.4 KB/core；+5.1% perf、-3.4% 动态功耗、SMT +8.8%；与 EVES LVP 正交至 8.5%
* [CosMoS: Architectural Support for Cost-Effective Data Movement in a Disaggregated Memory Systems](cosmos-disaggregated-memory-data-movement.md) - ACM JETCAS 2025 — 解耦内存系统硬件热页预测/调度迁移，+20% vs SOTA、+86% vs 基线；保护关键路径 cache miss
* [Dally Virtual-Channel Flow Control](dally-virtual-channel-flow-control.md) - Dally IEEE TPDS 1992 — VC 原典；物理通道时分复用破死锁环；吞吐 vs VC 数
* [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](dspark-speculative-decoding.md) - DeepSeek 半自回归 speculative decoding + 负载感知 confidence verify；离线 τ +16–31%，V4 生产 per-user +57–85% vs MTP-1，开源 DeepSpec
* [DynaX: Dynamic X:M Sparse Attention Acceleration](dynax-sparse-attention-acceleration.md) - ASPLOS '25 DynaX — dynamic X:M structured attention pruning + block scheduling; 89–92% sparsity at <1% accuracy loss; 1.99× speedup vs Sanger on BERT
* [Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks](eyeriss-energy-efficient-cnn-accelerator.md) - MIT 65nm 168-PE CNN 加速器：Row Stationary dataflow、四级存储、GIN 组播 NoC、RLC+data gating；AlexNet 35 frames/s @278mW、0.0029 DRAM access/MAC
* [FEATHER: A Reconfigurable Accelerator with Data Reordering Support for Low-Cost On-Chip Dataflow Switching](feather-reconfigurable-accelerator.md) - NEST+BIRRD 可重构加速器，RIR 在归约中做 arbitrary layout reorder；Layoutloop dataflow-layout 联合搜索，ResNet-50 1.27–2.89× 延迟、FPGA 2.65–3.91× 吞吐
* [Feero & Stan 3D Mesh NoC](feero-3d-mesh-noc-stan-2008.md) - Feero et al. Microelectronics J. 2008 — 3-D Mesh NoC 拓扑基线：直径短 1/3、port 7、面积 +40%、TSV pitch vs KOZ trade-off
* [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](flashattention-2-faster-attention.md) - IO-aware 精确 attention 第二代：减 non-matmul、seq 维并行、warp split-Q；相对 FlashAttention ~2×，A100 73% 峰值 TFLOPs/s、GPT 训练 225 TFLOPs/s
* [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](flashattention-3-asynchrony-low-precision.md) - Hopper H100：TMA/WGMMA producer-consumer、2-stage GEMM-softmax 流水线、FP8 block quant+incoherent processing；FP16 740 TFLOPs/s、相对 FA2 1.5–2×
* [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](flashattention-io-aware-exact-attention.md) - IO-aware tiling + online softmax + 反向重算；O(N) 内存、IO-optimal HBM 访问；GPT-2 attention 7.6×、BERT 15% 快于 MLPerf 纪录、Path-X 16K 61.4%
* [FlashDecoding++: Faster Large Language Model Inference on GPUs](flashdecoding-plus-plus-llm-gpu-inference.md) - 异步 unified-max softmax + M=8 flat GEMM 双缓冲 + FastGEMV/CUTLASS 启发式 dataflow；decode 相对 HF 最高 4.86×、FlashDecoding 平均 1.37×，NVIDIA/AMD 双平台
* [FlashMoE: Fast Distributed MoE in a Single Kernel](flashmoe-fast-distributed-moe-single-kernel.md) - NeurIPS 2025：单 persistent GPU kernel 融合 MoE 计算与 NVSHMEM RDMA；actor 调度 + payload-efficient dispatch；8×H100 最高 6× 延迟、5.7× 吞吐、93% SM（FP32 vs FP16 基线）
* [FlexInfer: Flexible On-Device LLM Offloading](flexinfer-on-device-llm-offloading.md) - FlexInfer — async prefetch + balanced memory locking + flexible tensor retention for budget-adaptive edge LLM inference; 10.6–12.5× vs prior offload on Llama2-70B
* [HCache: Fast State Restoration in LLM Serving](hcache-fast-state-restoration.md) - EuroSys '25 HCache — restore conversational state from hidden activations; 6× less compute than recompute, 2× less I/O than KV offload; up to 5.73× TTFT gain
* [Heterogeneous Computing for AI Agent Inference](heterogeneous-computing-ai-agent-inference.md) - Zhao & Liu — OI/CF framework beyond roofline for agent inference; snowballing contexts (300K–1M tokens) expose memory capacity wall and system heterogeneity need
* [Hoskote 5GHz Mesh Polaris](hoskote-5ghz-mesh-polaris.md) - Intel Polaris 80-core 5GHz Mesh NoC（ISSCC/JSSC 2007–08）— 工业频率、message class、fault-tolerant XOR 路由
* [Hybrid Bonding 3D Integration Recent](hybrid-bonding-3d-integration-recent.md) - 综述整合：Cu-Cu 直接键合 ~1 μm pitch，TSMC SoIC/Samsung X-Cube/Intel Foveros/SK hynix HBM4 已量产；3D NoC 设计假设被根本改写
* [HyperMR: Efficient Hypergraph-enhanced Matrix Storage on Compute-in-Memory Architecture](hypermr-hypergraph-matrix-storage-cim.md) - SIGMOD 2025 — CIM 矩阵存储超图建模 + 两阶段划分，优化通信/累加成本；100% 矩阵有效优化，合成查询 +29.65%
* [Katti TSV Technology Roadmap 2010](katti-tsv-technology-roadmap-2010.md) - Katti et al. IEEE Comm. Mag. 2010 — TSV 综述原典：via-first/middle/last 工艺、KOZ、寄生 R/C、热密度、良率模型；3D NoC 物理层标准参考
* [Kim Adaptive Routing High-Radix Clos](kim-adaptive-routing-high-radix-clos.md) - Kim/Dally/Abts SC 2006 — high-radix Clos + DisPERoute；负载均衡自适应 vs mesh+DOR
* [Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective](llm-inference-acceleration-comprehensive-hardware-survey.md) - LLM 推理加速硬件最完整综述：HBM-assisted vs SRAM-based 双路线、Quantization/Sparse/Speculative/Paged 关键专题、典型 FPGA/SoC 数据点
* [LoopLynx: A Scalable Dataflow Architecture for Efficient LLM Inference](looplynx-scalable-dataflow-llm-inference.md) - FPGA hybrid spatial-temporal dataflow：Macro Dataflow Kernels + state-machine 调度 + multi-FPGA ring；解决"spatial dataflow 在 decode 串行依赖下利用率不足"；双节点 1.67× A100、四节点 2.52× A100
* [M5: Mastering Page Migration and Memory Management for CXL-based Tiered Memory Systems](m5-cxl-tiered-memory-page-migration.md) - ASPLOS 2025 — CXL 控制器内 HPT/HWT 硬件热页追踪平台，比 CPU 驱动 ANB/DAMON 识别更准（+47% 热度），内存密集型应用 +14% 性能
* [MAERI: Enabling Flexible Dataflow Mapping over DNN Accelerators via Reconfigurable Interconnects](maeri-flexible-dataflow-reconfigurable-interconnects.md) - ASPLOS 2018 首个 flexible interconnect DNN 加速器：ART + Distribution Tree + tiny switches；任何 layout/任意 dataflow 都能映射；8-459% 利用率提升
* [Mixed Precision Training](mixed-precision-training.md) - Micikevicius et al. (ICLR 2018) — FP16 training with FP32 master weights, loss scaling, and FP32 accumulation; ~2× memory savings, no hyperparameter change
* [MOCAP: Wafer-Scale Chunked Pipelining for Prefill-Only LLM Inference](mocap-wafer-scale-chunked-pipelining.md) - Tsinghua MOCAP — MBKR + LBCP chunked pipeline on wafer-scale chips for prefill-only workloads; 76.4% lower latency and 3.24× throughput vs GPipe
* [Multi-Branch Self-Drafting for LLM Inference Acceleration](multi-branch-self-drafting-llm-inference.md) - AAAI-25 Self-Draft — multi-branch in-model drafting without extra draft model; 2.0–3.2 tokens/step and ~2× throughput vs AR decode
* [Near-Optimal Wafer-Scale Reduce](near-optimal-wafer-scale-reduce.md) - WSE Reduce/AllReduce 首次系统研究：性能模型（<4% 误差）、5 种算法（Auto-Gen ≤1.4× 下界）、3.27× 快于 vendor
* [NVIDIA NVLink Hopper Blackwell](nvidia-nvlink-hopper-blackwell.md) - Hopper/Blackwell NVLink + NVSwitch — 固定 fat-tree、NVL72、每 GPU 带宽代际翻倍
* [Optimization of Collective Reduction Operations](rabenseifner-collective-reduction-operations.md) - Rabenseifner ICCS 2004：MPI Reduce/AllReduce 五算法（tree、doubling、RHD、binary blocks、ring）与 (p,n) 选择；占 MPI 时间 >40%；长向量相对 vendor 最高 100×
* [Optimizing the Parallelism of Communication and Computation in Distributed Training Platform](optimizing-comm-comp-parallelism-training.md) - ICA3PP 2023 — Torus-Ring 分层训练平台上重叠通信与计算，ResNet50 +23.8–25.6%，Transformer +11.7–12.8%
* [PANDA: Adaptive Prefetching and Decentralized Scheduling for Dataflow Architectures](panda-adaptive-prefetch-dataflow.md) - ACM TACO 2025 — 应用自适应 prefetch + PE 去中心化调度；相对 Plasticine 1.90×、REVEL 2.53× geomean 性能
* [pHost: Distributed Near-Optimal Datacenter Transport Over Commodity Network Fabric](phost-coflow-aware-packet-scheduling.md) - UC Berkeley CoNEXT 2015 — 主机端 RTS/token 分布式调度，商品交换机上接近 pFabric FCT（±4%），比 Fastpass 快 3.8×
* [Plasticine: A Reconfigurable Architecture For Parallel Patterns](plasticine-reconfigurable-parallel-patterns.md) - Stanford CGRA 直接支持 Map/FlatMap/Fold/HashReduce；64 PCU+64 PMU @28nm 112.8mm²、12.3 TFLOPS；相对 Stratix V 最高 76.9× Perf/W、DHDL 数分钟编译
* [PRESERVE: Prefetch Weights and KV-Cache in Distributed LLM Serving](preserve-prefetch-weights-kv-cache.md) - Huawei PRESERVE — overlap HBM→L2 weight/KV prefetch with collective comm; up to 1.6× E2E speedup; optimal L2 104 MB yields 1.25× perf/$
* [RDMA over Ethernet for Distributed AI Training at Meta Scale](rdma-over-ethernet-meta-training.md) - SIGCOMM 2024 Meta — 专用 backend RoCE 网络设计/运维：ECMP→流量工程，DCQCN→collective 库接收端准入；千级–32K GPU 集群
* [Route Packets, Not Wires](route-packets-not-wires.md) - Dally & Towles DAC 2001 — NoC 奠基；packet-switched on-chip vs dedicated wires；五决策话语体系
* [SambaNova SN40L: Scaling the AI Memory Wall with Dataflow and Composition of Experts](sambanova-sn40l-dataflow-coe.md) - SN40L RDU（TSMC 5nm, 1040 PCU+PMU, 638 BF16 TFLOPS, 520 MiB SRAM+64 GiB HBM+1.5 TiB DDR）+ Samba-CoE（150 个 8B expert, 1T 总参）；streaming dataflow 编译期融合数百 op；vs DGX H100 3.7× speedup
* [SIGMA: A Sparse and Irregular GEMM Accelerator with Flexible Interconnects for DNN Training](sigma-sparse-gemm-flexible-interconnects.md) - HPCA 2020 MAERI 团队的 sparse + training 延伸：Flex-DPE + FAN（Forwarding Adder Network）+ global NoC；任意 GEMM 形状 + 任意稀疏度；5.7× vs systolic、3× vs 稀疏加速器
* [SmartMem: Layout Transformation Elimination and Adaptation for Efficient DNN Execution on Mobile](smartmem-layout-transformation-elimination.md) - ASPLOS 2024 反向思路：编译期把 layout transformation 消除掉（不靠灵活 NoC）；4 类算子分类 + 2.5D 内存；2.8× vs DNNFusion、6.9× vs TVM、7.9× vs MNN
* [SpaDA: A Spatial Dataflow Architecture Programming Language](spada-spatial-dataflow-architecture.md) - 空间数据流语言 place/dataflow/compute + GT4Py→CSL 优化编译；WSE-2 14× 减码、collective 1.04× 手写 CSL、260 TFlop/s stencil、82× GEMV vs A100
* [SuperInfer: SLO-Aware Rotary Scheduling on Superchips](superinfer-slo-aware-rotary-scheduling.md) - UIUC SuperInfer — RotaSched + DuplexKV on GH200 NVLink-C2C; up to 74.7% higher TTFT SLO attainment under KV pressure vs PCIe offload stacks
* [TileLoom: Automatic Dataflow Planning for Tile-Based Languages](tileloom-automatic-dataflow-planning.md) - MLIR 编译框架：Triton/Helion → spatiotemporal dataflow planning + df 硬件模型；Tenstorrent Wormhole/Blackhole 上 FlashAttention ~2× TTNN、Mamba Scan 最高 27× unfused
* [TPU v4 Optically Reconfigurable](tpu-v4-optically-reconfigurable.md) - Jouppi et al. ISCA 2023 — TPU v4 pod OCS 可重构拓扑；4096-chip scale-up
* [Understanding Inference Scaling for LLMs](understanding-inference-scaling-for-llms.md) - Reasoning-centric LLM 推理系统瓶颈分析：Capacity Trap, Reasoning Cliff, DP→TP Transition, Prefill-Decode Divergence（8B-671B H200 实测）
* [Understanding Silent Data Corruptions in a Large Production CPU Population](silent-data-corruptions-production-cpu.md) - SOSP 2023 — 阿里云 >100 万 CPU、32 个月 SDC 实测：故障率 3.61‱；提出 Farron 优先测试 + 温控缓解
* [Venus: A Versatile Deep Neural Network Accelerator Architecture Design for Multiple Applications](venus-versatile-reconfigurable-accelerator.md) - DAC 2023 NoC fission/fusion 多 DNN 并行 serving：分布式 buffer + flexible NoC 按 workload 动态 morph；首个 runtime multi-tenancy 适配 layout 工作
* [Voxel: 3D-Stacked AI Chip Efficiency for LLM Inference](voxel-3d-stacked-ai-chip-llm-inference.md) - Voxel 编译器感知 3D AI 芯片仿真框架：LLM prefill/decode 软硬件协同探索，Graphcore IPU 验证误差 ≤6.8%
* [WaferLLM: Large Language Model Inference at Wafer Scale](waferllm-wafer-scale-llm-inference.md) - 首个晶圆级 LLM 推理系统：PLMR 设备模型 + MeshGEMM/MeshGEMV + KV shift；WSE-2 上 E2E 10–20× SGLang/A100 集群、MeshGEMV 606× 单 A100
* [Æthereal Network on Chip](aethereal-network-on-chip.md) - Philips Æthereal NoC（IEEE MDT 2005）— contention-free TDM 电路交换提供 GS；GS+BES 组合；分布式/集中编程；四种路由器面积对比
