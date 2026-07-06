# Bundle Update Log

## 2026-07-03
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 8 → `raw/articles/interconn-study-21d-day-08.md`（源：`openclawdata/.../interconn-study-21d/day-08.md`）。
* **Creation**: [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md).
* **Update**: [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md), [Switching Networks](/concepts/switching-networks.md), [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md), [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Butterfly/Omega/Banyan/Batcher-Banyan 与 Clos/Mesh 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 20 → `raw/articles/arch-study-30d-day-20.md`（源：`openclawdata/.../arch-study-30d/day-20.md`）。
* **Creation**: [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md).
* **Update**: [DRAM and Memory System](/concepts/dram-memory-system.md), [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [Cerebras WSE](/entities/cerebras-wse.md), [CMX & STX](/concepts/cmx-stx.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — FTL/RAID/NVMe/io_uring、memoryX、KV tier 交叉引用。
* **Ingest**: 郑启航 知乎「分布式存储架构下的矩阵乘与编译器」→ `raw/articles/分布式存储架构下的矩阵乘与编译器.md`（已有 clippings；补 OKF frontmatter）。
* **Creation**: [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md), [summaries/distributed-gemm-and-compiler.md](/summaries/distributed-gemm-and-compiler.md).
* **Update**: [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [Linear and Ring Topology](/concepts/linear-ring-topology.md), [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md), [Parallelism Transition Point](/concepts/parallelism-transition-point.md), [Graphcore IPU](/entities/graphcore-ipu.md), [SpaDA Programming Language](/concepts/spada-programming-language.md) — Cannon/SUMMA/2.5D/3D GEMM 与 T10 rTensor 交叉引用。

## 2026-06-24
* **Ingest**: Rabenseifner 2004 MPI collective reduction ICCS PDF → `raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf`（Zotero: ICCS 2004, LNCS 3036）。
* **Creation**: [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md), [papers/rabenseifner-collective-reduction-operations.md](/papers/rabenseifner-collective-reduction-operations.md), `raw/papers/rabenseifner-collective-reduction-operations.md`.
* **Update**: [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md), [Linear and Ring Topology](/concepts/linear-ring-topology.md), [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md), [Parallelism Transition Point](/concepts/parallelism-transition-point.md), [Near-Optimal Wafer-Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md) — MPI Ring/RHD 与 WSE collective 谱系交叉引用。
* **Ingest**: Aimuyo et al. 2025 FlashMoE NeurIPS PDF → `raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf`（Zotero: arXiv:2506.04667）。
* **Creation**: [FlashMoE Kernel](/concepts/flashmoe-kernel.md), [papers/flashmoe-fast-distributed-moe-single-kernel.md](/papers/flashmoe-fast-distributed-moe-single-kernel.md), `raw/papers/flashmoe-fast-distributed-moe-single-kernel.md`.
* **Update**: [MegaMoE Kernel](/concepts/megamoe-kernel.md), [M2N Communication](/concepts/m2n-communication.md), [Disaggregated Inference](/concepts/disaggregated-inference.md), [Parallelism Transition Point](/concepts/parallelism-transition-point.md), [MegaScale-Infer](/papers/megascale-infer-2504.02263.md) — MoE EP kernel 栈交叉引用。
* **Ingest**: Shah et al. 2024 FlashAttention-3 PDF → `raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf`（Zotero: arXiv:2407.08608）。
* **Creation**: [FlashAttention-3](/concepts/flashattention-3.md), [papers/flashattention-3-asynchrony-low-precision.md](/papers/flashattention-3-asynchrony-low-precision.md), `raw/papers/flashattention-3-asynchrony-low-precision.md`.
* **Update**: [FlashAttention](/concepts/flashattention.md), [FlashAttention-2](/concepts/flashattention-2.md), [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [papers/flashattention-2-faster-attention.md](/papers/flashattention-2-faster-attention.md), [papers/flashdecoding-plus-plus-llm-gpu-inference.md](/papers/flashdecoding-plus-plus-llm-gpu-inference.md) — FA→FA2→FA3 谱系补全。
* **Ingest**: Dao et al. 2022 FlashAttention NeurIPS PDF → `raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf`（Zotero: arXiv:2205.14135, NeurIPS 2022）。
* **Creation**: [FlashAttention](/concepts/flashattention.md), [papers/flashattention-io-aware-exact-attention.md](/papers/flashattention-io-aware-exact-attention.md), `raw/papers/flashattention-io-aware-exact-attention.md`.
* **Update**: [FlashAttention-2](/concepts/flashattention-2.md), [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [papers/flashattention-2-faster-attention.md](/papers/flashattention-2-faster-attention.md), [papers/flashdecoding-plus-plus-llm-gpu-inference.md](/papers/flashdecoding-plus-plus-llm-gpu-inference.md) — FA→FA2→FlashDecoding 谱系交叉引用。
* **Ingest**: Dao 2023 FlashAttention-2 PDF → `raw/papers/FlashAttention2_Faster_Attention_2023.pdf`（Zotero: arXiv:2307.08691）。
* **Creation**: [FlashAttention-2](/concepts/flashattention-2.md), [papers/flashattention-2-faster-attention.md](/papers/flashattention-2-faster-attention.md), `raw/papers/flashattention-2-faster-attention.md`.
* **Update**: [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [papers/dspark-speculative-decoding.md](/papers/dspark-speculative-decoding.md) — prefill attention vs decode kernel 栈交叉引用。
* **Ingest**: Hong et al. 2024 FlashDecoding++ PDF → `raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf`（Zotero: arXiv:2311.01282）。
* **Creation**: [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [papers/flashdecoding-plus-plus-llm-gpu-inference.md](/papers/flashdecoding-plus-plus-llm-gpu-inference.md), `raw/papers/flashdecoding-plus-plus-llm-gpu-inference.md`.
* **Update**: [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md), [Heterogeneous Inference](/concepts/heterogeneous-inference.md), [papers/dspark-speculative-decoding.md](/papers/dspark-speculative-decoding.md) — decode kernel vs speculative/异构推理交叉引用。
* **Ingest**: Prabhakar et al. 2017 Plasticine ISCA PDF → `raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf`（Zotero: ISCA 2017, DOI 10.1145/3079856.3080256）。
* **Creation**: [Plasticine Accelerator](/concepts/plasticine-accelerator.md), [papers/plasticine-reconfigurable-parallel-patterns.md](/papers/plasticine-reconfigurable-parallel-patterns.md), `raw/papers/plasticine-reconfigurable-parallel-patterns.md`.
* **Update**: [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md), [SpaDA Programming Language](/concepts/spada-programming-language.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [FEATHER Accelerator](/concepts/feather-accelerator.md), [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — parallel patterns CGRA、dataflow 谱系交叉引用。
* **Ingest**: Chen et al. 2017 Eyeriss JSSC PDF → `raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf`（Zotero: JSSC 2017, DOI 10.1109/JSSC.2016.2616357）。
* **Creation**: [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md), [papers/eyeriss-energy-efficient-cnn-accelerator.md](/papers/eyeriss-energy-efficient-cnn-accelerator.md), `raw/papers/eyeriss-energy-efficient-cnn-accelerator.md`.
* **Update**: [FEATHER Accelerator](/concepts/feather-accelerator.md), [papers/feather-reconfigurable-accelerator.md](/papers/feather-reconfigurable-accelerator.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [Collective-Capable NoC](/concepts/collective-capable-noc.md), [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — RS dataflow、GIN 组播 NoC、FEATHER 固定基线交叉引用。
* **Ingest**: Dennis & Misunas 1975 basic data-flow processor PDF → `raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf`（Zotero: ISCA 1975, ACM 641675.642111）。
* **Creation**: [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md), [papers/dennis-misunas-basic-data-flow-processor.md](/papers/dennis-misunas-basic-data-flow-processor.md), `raw/papers/dennis-misunas-basic-data-flow-processor.md`.
* **Update**: [Deterministic Execution](/concepts/deterministic-execution.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md), [SpaDA Programming Language](/concepts/spada-programming-language.md), [Cerebras WSE](/entities/cerebras-wse.md) — 数据流架构历史交叉引用。
* **Update**: [Collective-Capable NoC](/concepts/collective-capable-noc.md), [papers/collective-capable-noc-ml-accelerators.md](/papers/collective-capable-noc-ml-accelerators.md) — 扩充 DCA 范式。
* **Ingest**: Colagrande et al. 2026 collective-capable NoC PDF → `raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf`（Zotero: MLSys 2026, arXiv:2603.26438）。
* **Creation**: [Collective-Capable NoC](/concepts/collective-capable-noc.md), [papers/collective-capable-noc-ml-accelerators.md](/papers/collective-capable-noc-ml-accelerators.md), `raw/papers/collective-capable-noc-ml-accelerators.md`.
* **Update**: [NoC Router 微架构](/concepts/noc-router-microarchitecture.md), [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md), [Memory Consistency Model](/concepts/memory-consistency-model.md), [Cerebras WSE](/entities/cerebras-wse.md) — FlooNoC multicast/reduction/DCA/barrier 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 19 → `raw/articles/arch-study-30d-day-19.md`.
* **Creation**: [Memory Consistency Model](/concepts/memory-consistency-model.md).
* **Update**: [Cache Coherence](/concepts/cache-coherence.md), [Memory Fence and Barrier](/concepts/memory-fence-barrier.md), [Out-of-Order Execution](/concepts/out-of-order-execution.md), [Deterministic Execution](/concepts/deterministic-execution.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [Cerebras WSE](/entities/cerebras-wse.md), [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — SC/TSO/ARM、fence、CAS/MCS 锁、WSE barrier 交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 7 → `raw/articles/interconn-study-21d-day-07.md`.
* **Creation**: [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md).
* **Update**: [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [Linear and Ring Topology](/concepts/linear-ring-topology.md), [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md), [Switching Networks](/concepts/switching-networks.md), [Multi-plane Clos Topology for AI Training](/concepts/multi-plane-clos-topology.md) — Clos 定理、Fat-Tree、间接网络交叉引用。
* **Ingest**: FEATHER 论文 PDF → `raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf`（Zotero: Tong et al. 2024, arXiv:2405.13170）。
* **Creation**: [FEATHER Accelerator](/concepts/feather-accelerator.md), [papers/feather-reconfigurable-accelerator.md](/papers/feather-reconfigurable-accelerator.md), `raw/papers/feather-reconfigurable-accelerator.md`.
* **Update**: [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [SpaDA Programming Language](/concepts/spada-programming-language.md) — dataflow/layout 可重构交叉引用。
* **Ingest**: SpaDA 论文 PDF → `raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf`（Zotero: Gianinazzi et al. 2026, arXiv:2511.09447）。
* **Creation**: [SpaDA Programming Language](/concepts/spada-programming-language.md), [papers/spada-spatial-dataflow-architecture.md](/papers/spada-spatial-dataflow-architecture.md), `raw/papers/spada-spatial-dataflow-architecture.md`.
* **Update**: [Cerebras WSE](/entities/cerebras-wse.md), [Deterministic Execution](/concepts/deterministic-execution.md), [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md), [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md), [Cache Coherence](/concepts/cache-coherence.md) — SpaDA/CSL 编程模型交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 6 → `raw/articles/interconn-study-21d-day-06.md`.
* **Creation**: [Mesh and Torus Topology](/concepts/mesh-torus-topology.md).
* **Update**: [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md), [Linear and Ring Topology](/concepts/linear-ring-topology.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 2-D Mesh/Torus、k-ary n-cube、Dally d_opt 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 18 → `raw/articles/arch-study-30d-day-18.md`.
* **Creation**: [Cache Coherence](/concepts/cache-coherence.md).
* **Update**: [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [Memory Fence and Barrier](/concepts/memory-fence-barrier.md), [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md), [Cerebras WSE](/entities/cerebras-wse.md) — MESI/Snooping/Directory/False Sharing 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 17 → `raw/articles/arch-study-30d-day-17.md`.
* **Creation**: [DRAM and Memory System](/concepts/dram-memory-system.md).
* **Update**: [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [Cerebras WSE](/entities/cerebras-wse.md) — DRAM/HBM/内存墙交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 5 → `raw/articles/interconn-study-21d-day-05.md`.
* **Creation**: [Linear and Ring Topology](/concepts/linear-ring-topology.md).
* **Update**: [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 1-D 基线、TileLink Ring 交叉引用。
* **Ingest**: DSpark 论文 PDF → `raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf`（Zotero: Cheng et al. 2026）。
* **Creation**: [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md), [papers/dspark-speculative-decoding.md](/papers/dspark-speculative-decoding.md), `raw/papers/dspark-speculative-decoding.md`.
* **Update**: [DeepSeek-V4](/entities/deepseek-v4.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — speculative decode 交叉引用。
* **Ingest**: Memory Fence 深度研究报告 → `raw/articles/memory-fence-hardware-2026-06-28.md`（源：`openclawdata/.../notes/reports/`）。
* **Creation**: [Memory Fence and Barrier](/concepts/memory-fence-barrier.md).
* **Update**: [Out-of-Order Execution](/concepts/out-of-order-execution.md), [Deterministic Execution](/concepts/deterministic-execution.md), [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [ISA Design Principles](/concepts/isa-design-principles.md), [Cerebras WSE](/entities/cerebras-wse.md) — fence/coherence 交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 3–4 → `raw/articles/interconn-study-21d-day-03.md`, `interconn-study-21d-day-04.md`.
* **Creation**: [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md), [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md).
* **Update**: [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Cerebras WSE](/entities/cerebras-wse.md) — 拓扑度量、延迟/B_b 模型、Mesh vs Torus 权衡。
* **Ingest**: 体系结构 30 天学习笔记 Day 15–16 → `raw/articles/arch-study-30d-day-15.md`, `arch-study-30d-day-16.md`.
* **Creation**: [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md).
* **Update**: [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [Cerebras WSE](/entities/cerebras-wse.md), [Deterministic Execution](/concepts/deterministic-execution.md) — TLB/核心篇总结交叉引用。
* **Ingest**: Hennessy & Patterson 30 天体系结构学习笔记 Day 1–14 → `raw/articles/arch-study-30d-day-*.md`（14 文件）。
* **Creation**: [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md), [ISA Design Principles](/concepts/isa-design-principles.md), [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md), [Architecture Benchmark Methodology](/concepts/architecture-benchmark-methodology.md), [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md), [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md), [Out-of-Order Execution](/concepts/out-of-order-execution.md), [Branch Prediction](/concepts/branch-prediction.md), [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md).
* **Update**: [Cerebras WSE](/entities/cerebras-wse.md), [Deterministic Execution](/concepts/deterministic-execution.md), [FP4 Quantization-Aware Training](/concepts/fp4-qat.md) — 与 CPU 体系结构概念交叉引用。
* **Schema**: 标签 taxonomy 新增 `isa`, `pipeline`, `cache`, `power`。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 1–2 → `raw/articles/interconn-study-21d-day-01.md`, `interconn-study-21d-day-02.md`.
* **Creation**: [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md).
* **Update**: [Switching Principles](/concepts/switching-principles.md) — 报文/虫孔交换、历史里程碑；[Cerebras WSE](/entities/cerebras-wse.md) — Mesh 度量与虫孔选型。
* **Schema**: 标签 taxonomy 新增 `interconnect`。
* **Cleanup**: 删除重复的 `references/raw/`（OKF 转换副本）；唯一原始资料目录为 `raw/`。`megascale-infer-2504.02263.pdf`、`cassini-network-aware-scheduling-2308.00852.pdf` 本就位于 `raw/papers/`（与 `references/raw/papers/` 为同内容副本），无需迁移。
* **Docs**: README 与 OKF skill 统一为仅使用 `raw/`。
* **Creation**: [Graphcore IPU](/entities/graphcore-ipu.md), [Core Group (DRAM Access Synchronization)](/concepts/core-group-dram-access.md).
* **Update**: [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [Voxel Simulator](/concepts/voxel-simulator.md), [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) — 交叉引用拆分页。
* **Schema**: 标签 taxonomy 新增 `graphcore`。
* **Ingest**: [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) from `raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf` (arXiv:2604.26821).
* **Creation**: [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [Voxel Simulator](/concepts/voxel-simulator.md).
* **Update**: [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 3D chip prefill/decode 设计空间差异。
* **Creation**: Converted LLM wiki at `/home/luke/wiki` to OKF v0.1 bundle (54 work pages + raw sources).
* **Source**: Karpathy-style LLM wiki (entities, concepts, papers, summaries, analyses).
* **Update**: Generated interactive `viz.html` (74 concepts, 237 cross-links).
