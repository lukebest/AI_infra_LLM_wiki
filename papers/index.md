# Paper

* [MegaScale-Infer](megascale-infer-2504.02263.md) - MegaScale-Infer：MoE disaggregated attention/FFN serving，ping-pong pipeline + M2N 通信库，1.90× 吞吐提升
* [Resilient AI Supercomputer Networking using MRC and SRv6](resilient-ai-supercomputer-networking-mrc-srv6.md) - MRC+SRv6+multi-plane Clos：三管齐下的 100K+ GPU AI 训练网络容错方案，OpenAI/Microsoft 生产验证

# Summary

* [A Lightweight High-Throughput Collective-Capable NoC for Large-Scale ML Accelerators](collective-capable-noc-ml-accelerators.md) - FlooNoC 扩展：multicast/归约/barrier + DCA 借 Snitch FPU；router +16.9% 面积，4×4 mesh 上 multicast 5.3×、reduction 2.8×，SUMMA GEMM 最高 3.8×
* [A Preliminary Architecture for a Basic Data-Flow Processor](dennis-misunas-basic-data-flow-processor.md) - Dennis & Misunas (ISCA 1975) 基本数据流处理器：decider/T-gate/merge 条件迭代、Decision Units、Instruction Cell 两级存储作活跃指令 cache
* [Constable: Safely Eliminating Load Instruction Execution](constable-load-elimination.md) - ISCA 2024 Best Paper：likely-stable load 识别 + RMT/AMT 监控；12.4 KB/core；+5.1% perf、-3.4% 动态功耗、SMT +8.8%；与 EVES LVP 正交至 8.5%
* [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](dspark-speculative-decoding.md) - DeepSeek 半自回归 speculative decoding + 负载感知 confidence verify；离线 τ +16–31%，V4 生产 per-user +57–85% vs MTP-1，开源 DeepSpec
* [Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks](eyeriss-energy-efficient-cnn-accelerator.md) - MIT 65nm 168-PE CNN 加速器：Row Stationary dataflow、四级存储、GIN 组播 NoC、RLC+data gating；AlexNet 35 frames/s @278mW、0.0029 DRAM access/MAC
* [FEATHER: A Reconfigurable Accelerator with Data Reordering Support for Low-Cost On-Chip Dataflow Switching](feather-reconfigurable-accelerator.md) - NEST+BIRRD 可重构加速器，RIR 在归约中做 arbitrary layout reorder；Layoutloop dataflow-layout 联合搜索，ResNet-50 1.27–2.89× 延迟、FPGA 2.65–3.91× 吞吐
* [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](flashattention-2-faster-attention.md) - IO-aware 精确 attention 第二代：减 non-matmul、seq 维并行、warp split-Q；相对 FlashAttention ~2×，A100 73% 峰值 TFLOPs/s、GPT 训练 225 TFLOPs/s
* [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](flashattention-3-asynchrony-low-precision.md) - Hopper H100：TMA/WGMMA producer-consumer、2-stage GEMM-softmax 流水线、FP8 block quant+incoherent processing；FP16 740 TFLOPs/s、相对 FA2 1.5–2×
* [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](flashattention-io-aware-exact-attention.md) - IO-aware tiling + online softmax + 反向重算；O(N) 内存、IO-optimal HBM 访问；GPT-2 attention 7.6×、BERT 15% 快于 MLPerf 纪录、Path-X 16K 61.4%
* [FlashDecoding++: Faster Large Language Model Inference on GPUs](flashdecoding-plus-plus-llm-gpu-inference.md) - 异步 unified-max softmax + M=8 flat GEMM 双缓冲 + FastGEMV/CUTLASS 启发式 dataflow；decode 相对 HF 最高 4.86×、FlashDecoding 平均 1.37×，NVIDIA/AMD 双平台
* [FlashMoE: Fast Distributed MoE in a Single Kernel](flashmoe-fast-distributed-moe-single-kernel.md) - NeurIPS 2025：单 persistent GPU kernel 融合 MoE 计算与 NVSHMEM RDMA；actor 调度 + payload-efficient dispatch；8×H100 最高 6× 延迟、5.7× 吞吐、93% SM（FP32 vs FP16 基线）
* [Near-Optimal Wafer-Scale Reduce](near-optimal-wafer-scale-reduce.md) - WSE Reduce/AllReduce 首次系统研究：性能模型（<4% 误差）、5 种算法（Auto-Gen ≤1.4× 下界）、3.27× 快于 vendor
* [Optimization of Collective Reduction Operations](rabenseifner-collective-reduction-operations.md) - Rabenseifner ICCS 2004：MPI Reduce/AllReduce 五算法（tree、doubling、RHD、binary blocks、ring）与 (p,n) 选择；占 MPI 时间 >40%；长向量相对 vendor 最高 100×
* [Plasticine: A Reconfigurable Architecture For Parallel Patterns](plasticine-reconfigurable-parallel-patterns.md) - Stanford CGRA 直接支持 Map/FlatMap/Fold/HashReduce；64 PCU+64 PMU @28nm 112.8mm²、12.3 TFLOPS；相对 Stratix V 最高 76.9× Perf/W、DHDL 数分钟编译
* [SpaDA: A Spatial Dataflow Architecture Programming Language](spada-spatial-dataflow-architecture.md) - 空间数据流语言 place/dataflow/compute + GT4Py→CSL 优化编译；WSE-2 14× 减码、collective 1.04× 手写 CSL、260 TFlop/s stencil、82× GEMV vs A100
* [TileLoom: Automatic Dataflow Planning for Tile-Based Languages](tileloom-automatic-dataflow-planning.md) - MLIR 编译框架：Triton/Helion → spatiotemporal dataflow planning + df 硬件模型；Tenstorrent Wormhole/Blackhole 上 FlashAttention ~2× TTNN、Mamba Scan 最高 27× unfused
* [Understanding Inference Scaling for LLMs](understanding-inference-scaling-for-llms.md) - Reasoning-centric LLM 推理系统瓶颈分析：Capacity Trap, Reasoning Cliff, DP→TP Transition, Prefill-Decode Divergence（8B-671B H200 实测）
* [Voxel: 3D-Stacked AI Chip Efficiency for LLM Inference](voxel-3d-stacked-ai-chip-llm-inference.md) - Voxel 编译器感知 3D AI 芯片仿真框架：LLM prefill/decode 软硬件协同探索，Graphcore IPU 验证误差 ≤6.8%
