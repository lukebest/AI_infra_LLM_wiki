---
type: Paper
title: "ARK: Avoiding Routing Collisions for KV Cache Transfer in Disaggregated LLM Inference"
description: "Georgia Tech NAIC’26 — 解耦推理 KV 大象流路径预留；QPS=25 mean/P95 FCT −27.3%/−34.0%，mean TTFT 最高 −12.9%"
tags:
- inference
- disaggregated-inference
- kv-cache
- serving
- networking
- rdma
- load-balancing
- latency
- llm
- fabric
created: 2026-11-05
updated: 2026-11-05
timestamp: '2026-11-05T00:00:00Z'
paper_author: [Hung-Chun Lin, Ting-Wei Hsu, Chung-En Ho, Ahmed Saeed]
year: 2026
venue: ACM SIGCOMM NAIC ’26
arxiv: '2610.41160'
sources:
  - raw/papers/ARK_KV_Path_Reservation_Disagg_Inference_2026.pdf
  - raw/papers/ark-kv-path-reservation-disagg.md
---

# ARK：解耦推理 KV 转移的路径预留

## 一句话结论
Prefill–decode 解耦把百毫秒至秒级、可达数十 GB 的 KV 做成 spine 上的 mega elephant flow；无状态 ECMP 哈希碰撞会让一条 spine 过载、其它空闲。ARK 在端主机上分布式预留路径：协调发送端选 source port，使并发流 hash 到不同 spine，**不改交换机、不需接收侧重排**。包级 RDMA 仿真在中等负载下 mean / P95 FCT 最高降 **27.3% / 34.0%**，mean TTFT 最高降 **12.9%**。

## 动机
- DistServe / Splitwise 等把 prefill 与 decode 拆到不同 GPU 池；vLLM、SGLang、Dynamo、llm-d 与 Mooncake / DeepSeek 部署已落地该模式。
- LLaMA-3.1-405B 单条 100K-token KV 约 **48 GB**，在 **400 Gbps** 上可占满约 **960 ms**，FCT 直接抬高 TTFT。
- ECMP 按五元组钉路径，对大象流尺寸无感；现有避碰方案常要改硬件或专用软件栈。

## 方案
1. **大象流路径预留**：各 host 维护复制的预留表，记录 spine 占用。
2. **选源端口对齐 hash**：发送端选使 ECMP hash 落到空闲 spine 的 source port。
3. **纯端侧、商品交换机**：数据平面不动；长寿命流摊薄一次协调开销。
4. **评测**：包级 RDMA 仿真；扫 QPS，报 FCT 与端到端 TTFT（TTFT = 𝑇prefill + 𝑇KV + 𝑇decode-1）。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| QPS=25 mean FCT | **−27.3%** |
| QPS=25 P95 FCT | **−34.0%** |
| mean TTFT（最高） | **−12.9%** |
| QPS=5 mean TTFT | 约 **−2%**（随负载拉开） |

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — PD 拆分后的跨池 KV 交接；ARK 专攻 fabric 侧大象流避碰
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — KV 出卡后的网络段时延进入 TTFT 预算
- [HAWK](/papers/hawk-gpu-npu-heterogeneous-kv-transfer.md) — 异构设备间布局感知 RDMA；ARK 同属 KV 转移，聚焦多路径 hash 碰撞
- [Ofan](/papers/ofan-destination-aware-load-balancing.md) — 训练侧胖树目的地感知喷洒；ARK 面向推理 KV 大象流的端侧预留

## 开放问题
- 仿真负载与生产 Mooncake / Dynamo 流量形状的偏差仍待实测闭环。
- 与交换机侧可编程 LB（如 PCM）或目的地感知方案的联合部署空间未展开。

# Citations
- [arXiv:2610.41160](https://arxiv.org/abs/2610.41160) — Lin, Hsu, Ho, Saeed, Georgia Tech, NAIC ’26
- [raw stub](/raw/papers/ark-kv-path-reservation-disagg.md)
