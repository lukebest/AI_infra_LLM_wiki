---
type: Paper
title: "HAWK: Heterogeneity-Aware KV Cache Transfer for GPU-NPU Phase-Disaggregated LLM Inference"
description: "Georgia Tech/ETRI — GPU prefill + Tenstorrent NPU decode；布局感知 RDMA KV 传输；同 SLO 下相对 GPU-only 吞吐差距 ≤7.88%，功耗效率最高 1.26×、成本效率最高 1.72×"
tags:
- disaggregated-inference
- kv-cache
- npu
- gpu
- prefill
- decode
- serving-system
- rdma
- architecture
- inference
created: 2026-10-23
updated: 2026-10-23
timestamp: '2026-10-23T00:00:00Z'
paper_author: [Junhyeok Park, Jungeun Yoon, Kyungmin Kim, Hunsoon Lee, Shinyoung Ahn, Kangho Kim]
year: 2026
arxiv: '2610.29873'
sources:
  - raw/papers/HAWK_GPU_NPU_Heterogeneous_KV_Transfer_2026.pdf
  - raw/papers/hawk-gpu-npu-heterogeneous-kv-transfer.md
---

# HAWK：GPU–NPU 相位解耦推理的异构感知 KV 传输

## 一句话结论
把 prefill 放 GPU、decode 放 NPU 能同时要性能和能效，但跨厂商 KV 传输与张量布局不一致是卡点。HAWK 用公共 RDMA 栈 + 传输期布局对齐，在真实 A100×Tenstorrent 系统上把异构 PD 做到相对同构 GPU 在同 SLO 下吞吐差距 ≤**7.88%**，功耗效率最高 **1.26×**、成本效率最高 **1.72×**。

## 动机
- Prefill 偏 GEMM、decode 偏 GEMV：A100 上 QKV 投影 prefill tensor core ≈92.9%、DRAM ≈19.3%；decode 则 ≈35.9% / 64.1%，板级功耗却几乎不随利用率下降。
- 商用对比（Llama 3.1 70B，512/128，BS=32，TP=4）：A100 vs Tenstorrent p150a prefill **2.52×**，decode 仅 **1.16×**；NPU decode 功耗效率 **1.39×**、成本效率 **5.88×**。
- 同构 GPU 有 NIXL/Mooncake 直传；异构则常走 host staging，且 GPU 连续布局 vs NPU 按 DRAM channel 分块的布局强制二次重排。

## 方案
1. **公共 RDMA 路径**：GPU peermem + 扩展 NPU peer memory client，接 Linux ib_core/libibverbs；用户态叠 Mooncake Transfer Engine。
2. **布局感知 NPU RDMA 缓冲**：每个 DRAM channel 一块连续缓冲，转移后可直接当 NPU 张量用，避免跨 channel 重排与碎片化 OOM。
3. **传输感知变换**：在 prefill 侧先把 KV 维序部分对齐到「按目标 channel 成块」，再一次大块 RDMA 填满各 channel；小消息也能摊薄协议开销。
4. 原型：vLLM 0.10.0 + Tenstorrent 插件；4×A100 prefill / 4×p150a decode；200 Gbps HDR IB。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 异构直传 vs host staging | 最高 **27.69×**；相对 GPU↔GPU RDMA 延迟差 **0.65%** |
| 大消息（1280 MB）GN-HAWK / GN-Host | 延迟降至 **14.69%** |
| 90% SLO 请求率 vs GG-Direct | Chatbot TTFT 差 **2.90%**，Summarization **5.90%**；Summarization SLO 请求率差 **7.69%** |
| 输出吞吐差距（90% SLO） | Chatbot **0.48%**，Summarization **7.88%** |
| 功耗 / 成本效率 vs GG-Direct | 最高 **1.26×** / **1.72×**（Chatbot）；Summarization **1.15×** / **1.61×** |
| vs H100 decode（GGH-Direct） | 吞吐差 ≤**6.53%**；功耗 **1.03×**；成本最高 **2.76×** |

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 相位解耦从同构 GPU 扩到 GPU–NPU
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构轴从 GPU+LPU/AFD 扩到商用 NPU decode + 跨设备 KV
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 用实测利用率支撑「prefill 吃算力、decode 吃带宽/数据流」
- [DuoPD](/papers/duopd-hybrid-gpu-pnm-pd-disaggregation.md) — 同机 HBM 逻辑 die 内解耦；HAWK 是跨节点异构器件解耦
- [M2N Communication](/concepts/m2n-communication.md) — 解耦 serving 的跨实例传输语境

## 开放问题
- 评测绑定 Llama 3.1 70B 与当前 Tenstorrent 模型–设备数耦合；其他 NPU（TPU/Gaudi/Ascend）需改布局缓冲映射。
- 功耗用 ASIC 估算（NPU 监控仅报核功耗）；成本价取自公开市价，随行情变。
- 算子级异构（attention@GPU / FFN@NPU）时激活更小、重叠空间更少，HAWK 声称可扩展但未实测。

# Citations
- [arXiv:2610.29873](https://arxiv.org/abs/2610.29873) — Park et al., 2026
