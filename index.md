# Wiki Index

> 内容目录。每个 wiki 页面按类型分区列出，附一行摘要。
> 先读此文件找到相关页面。
> Last updated: 2026-05-08 | Total pages: 31

## Entities
- [[cerebras-wse]] — Cerebras 晶圆级 AI 加速器，24 color 确定性路由，900K 核心
- [[nvidia-groq-3-lpx]] — NVIDIA rack-scale 低延迟推理加速器，256 LPU，LP30 Samsung SF4，AFD，C2C 三级拓扑
- [[nvidia-vera-rubin-nvl72]] — NVIDIA Vera Rubin GPU 系统，含 NVL72/144/288/576/1152 系统谱系
- [[deepseek-v4]] — V4 模型系列：1.6T/284B MoE，百万 token 上下文，CSA+HCA 混合注意力
- [[kyber-rack]] — NVIDIA 第二种 rack 架构，144 GPU/rack，NVLink 7 switch，支持 NVL144/288/1152
- [[cassini]] — CASSINI 网络感知 ML 集群调度器：几何抽象交错通信相位，Affinity 图，1.6× 吞吐改善
- [[vera-etl256]] — 256 CPU 独立 rack，Spectrum-6 ETL switch，液冷，全 copper 互联

## Analyses
- [[wse-nom-contradiction-analysis]] — WSE NoW 矛盾分析：均匀性 vs 异构通信（主要矛盾），附六步框架 + 解决方案
- [[cerebras-wse-vs-groq-network-comparison]] — WSE 2D Mesh vs Groq High-radix Switched：拓扑、规模、MoE 场景、矛盾对比

## Concepts
- [[nvidia-cpo-roadmap]] — NVIDIA CPO 用于 scale-up 的路线图：Rubin NVL576 测试 → Feynman NVL1152 volume ramp
- [[cmx-stx]] — NVIDIA 推理存储平台：CMX（Tier G3.5 NVMe KV cache）+ STX（BF-4 存储 rack 参考架构）
- [[deterministic-execution]] — 编译器控制时序、消除 jitter 的执行范式
- [[disaggregated-inference]] — 解耦推理：attention/FFN 分离部署，独立扩展，batch 聚合
- [[heterogeneous-inference]] — GPU + LPU 异构推理，分别优化 prefill/decode
- [[information-theoretic-value-model]] — 智能体辅助编程的信息论价值模型：V ∝ I(S;K)，知识与任务的匹配度决定 Agent 价值
- [[lpu-architecture]] — Groq LPU 推理专用架构：SRAM-first、显式数据搬运、编译器调度
- [[m2n-communication]] — M2N 不对称通信模式，disaggregated inference 核心，4.2× NCCL 优化
- [[CSA-HCA]] — 两级压缩注意力：CSA 温和压缩+稀疏选择，HCA 激进压缩+dense attention
- [[DSec-sandbox]] — DeepSeek Elastic Compute 沙箱平台，4 种执行基板，数十万并发
- [[FP4-QAT]] — FP4 量化感知训练，无损 FP4→FP8 反量化
- [[MegaMoE-kernel]] — MoE 专家并行 mega-kernel，wave-based 通信计算全重叠
- [[mHC]] — 流形约束超连接，Birkhoff polytope 约束残差映射
- [[Muon-optimizer]] — 矩阵正交化优化器，Hybrid Newton-Schulz 迭代
- [[switching-principles]] — 交换原理基础：电路交换/分组交换，三对基本概念，交换系统结构
- [[switching-elements]] — 交换单元：空分/时分交换，开关阵列与共享存储器/总线，性能指标
- [[switching-networks]] — 交换网络：CLOS 三级网络（严格/可重排无阻塞），TST 网络，Banyan 网络
- [[TileLang]] — Kernel 开发 DSL，Z3 形式化分析，bitwise reproducibility

## Papers
- [[megascale-infer-2504.02263]] — MegaScale-Infer：MoE disaggregated attention/FFN serving，ping-pong pipeline + M2N 通信库，1.90× 吞吐提升

## Summaries
- [[deepseek-v4-summary]] — DeepSeek-V4 技术报告全文摘要，含 wiki 交叉链接

## Comparisons

## Queries
