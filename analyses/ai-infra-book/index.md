# Summary

李博杰《深入理解 AI Infra》章节摘要（工作层，非正文转载）。实体：[深入理解 AI Infra](../../entities/bojieli-ai-infra-book.md)。源 stub：[raw/articles/bojieli-ai-infra-book.md](../../raw/articles/bojieli-ai-infra-book.md)。

* [Ch.0 前言](ch00-preface.md) - 从约束推导设计；五个数据搬移问题
* [Ch.1 初识 AI Infra](ch01-intro.md) - 容量/算力/带宽/延迟；MFU/MBU
* [Ch.2 模型架构](ch02-model-architecture.md) - 权重/KV/MoE 公式
* [Ch.3 推理与训练负载](ch03-workloads.md) - 到达、Agent、6ND、RL
* [Ch.4 加速器架构](ch04-accelerators.md) - Roofline 与三代架构
* [Ch.5 算子与运行时](ch05-operators-runtime.md) - 分块、融合、Graph
* [Ch.6 超节点](ch06-supernode.md) - 并行、集体、NVLink/TPU/UB、Engram
* [Ch.7 数据中心网络](ch07-datacenter-network.md) - 分层梯度、Clos、UB 延迟、1024 卡
* [Ch.8 推理优化](ch08-inference-optimization.md) - 批处理、分页 KV、推测解码
* [Ch.9 分布式推理](ch09-distributed-inference.md) - PD/AF 配比与共享 KV
* [Ch.10 训练系统](ch10-training-system.md) - 16B/param、ZeRO、checkpoint
* [Ch.11 资源调度](ch11-scheduling.md) - 工具环境与成组分配
* [Ch.12 端边云](ch12-edge-cloud.md) - WAN/无线下的同一套预算
