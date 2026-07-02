# Paper

* [MegaScale-Infer](megascale-infer-2504.02263.md) - MegaScale-Infer：MoE disaggregated attention/FFN serving，ping-pong pipeline + M2N 通信库，1.90× 吞吐提升
* [Resilient AI Supercomputer Networking using MRC and SRv6](resilient-ai-supercomputer-networking-mrc-srv6.md) - MRC+SRv6+multi-plane Clos：三管齐下的 100K+ GPU AI 训练网络容错方案，OpenAI/Microsoft 生产验证

# Summary

* [A Lightweight High-Throughput Collective-Capable NoC for Large-Scale ML Accelerators](collective-capable-noc-ml-accelerators.md) - FlooNoC 扩展：multicast/归约/barrier + DCA 借 Snitch FPU；router +16.9% 面积，4×4 mesh 上 multicast 5.3×、reduction 2.8×，SUMMA GEMM 最高 3.8×
* [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](dspark-speculative-decoding.md) - DeepSeek 半自回归 speculative decoding + 负载感知 confidence verify；离线 τ +16–31%，V4 生产 per-user +57–85% vs MTP-1，开源 DeepSpec
* [FEATHER: A Reconfigurable Accelerator with Data Reordering Support for Low-Cost On-Chip Dataflow Switching](feather-reconfigurable-accelerator.md) - NEST+BIRRD 可重构加速器，RIR 在归约中做 arbitrary layout reorder；Layoutloop dataflow-layout 联合搜索，ResNet-50 1.27–2.89× 延迟、FPGA 2.65–3.91× 吞吐
* [Near-Optimal Wafer-Scale Reduce](near-optimal-wafer-scale-reduce.md) - WSE Reduce/AllReduce 首次系统研究：性能模型（<4% 误差）、5 种算法（Auto-Gen ≤1.4× 下界）、3.27× 快于 vendor
* [SpaDA: A Spatial Dataflow Architecture Programming Language](spada-spatial-dataflow-architecture.md) - 空间数据流语言 place/dataflow/compute + GT4Py→CSL 优化编译；WSE-2 14× 减码、collective 1.04× 手写 CSL、260 TFlop/s stencil、82× GEMV vs A100
* [Understanding Inference Scaling for LLMs](understanding-inference-scaling-for-llms.md) - Reasoning-centric LLM 推理系统瓶颈分析：Capacity Trap, Reasoning Cliff, DP→TP Transition, Prefill-Decode Divergence（8B-671B H200 实测）
* [Voxel: 3D-Stacked AI Chip Efficiency for LLM Inference](voxel-3d-stacked-ai-chip-llm-inference.md) - Voxel 编译器感知 3D AI 芯片仿真框架：LLM prefill/decode 软硬件协同探索，Graphcore IPU 验证误差 ≤6.8%
