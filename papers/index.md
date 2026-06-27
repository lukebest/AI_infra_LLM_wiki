# Paper

* [MegaScale-Infer](megascale-infer-2504.02263.md) - MegaScale-Infer：MoE disaggregated attention/FFN serving，ping-pong pipeline + M2N 通信库，1.90× 吞吐提升
* [Resilient AI Supercomputer Networking using MRC and SRv6](resilient-ai-supercomputer-networking-mrc-srv6.md) - MRC+SRv6+multi-plane Clos：三管齐下的 100K+ GPU AI 训练网络容错方案，OpenAI/Microsoft 生产验证

# Summary

* [Near-Optimal Wafer-Scale Reduce](near-optimal-wafer-scale-reduce.md) - WSE Reduce/AllReduce 首次系统研究：性能模型（<4% 误差）、5 种算法（Auto-Gen ≤1.4× 下界）、3.27× 快于 vendor
* [Understanding Inference Scaling for LLMs](understanding-inference-scaling-for-llms.md) - Reasoning-centric LLM 推理系统瓶颈分析：Capacity Trap, Reasoning Cliff, DP→TP Transition, Prefill-Decode Divergence（8B-671B H200 实测）
* [Voxel: 3D-Stacked AI Chip Efficiency for LLM Inference](voxel-3d-stacked-ai-chip-llm-inference.md) - Voxel 编译器感知 3D AI 芯片仿真框架：LLM prefill/decode 软硬件协同探索，Graphcore IPU 验证误差 ≤6.8%
