---
type: Paper
title: "KVCompass: Discovery Plane for Internet-Scale Prefix Cache Sharing"
description: "UCSC POMACS — 跨地域共享前缀 KV：KV 身份与放置解耦，边缘常数时间变长前缀查表，按复用/负载/网络距离联合打分转发；P99 TTFT 降 1.3–14×，吞吐最高 4.7×，峰值负载因子距 Oracle 2% 内"
tags:
- kv-cache
- prefix-cache
- geo-distributed
- serving-system
- routing
- prefill
- latency
- datacenter
- networking
created: 2026-10-21
updated: 2026-10-21
timestamp: '2026-10-21T00:00:00Z'
paper_author: [Shiyi Ling, Fei Fang, Chen Qian]
year: 2026
arxiv: '2610.24179'
venue: POMACS (accepted)
sources:
  - raw/papers/KVCompass_Internet_Scale_Prefix_Cache_Discovery_POMACS_2026.pdf
  - raw/papers/kvcompass-internet-scale-prefix-cache-discovery.md
---

# KVCompass：互联网规模的前缀 KV 发现平面

## 一句话结论
多地域部署同一模型时，各地域反复 prefill 同样的热门前缀；想跨地域复用，难点在于「找到谁手里有这段 KV」。KV 由服务过请求的 worker 产生、随淘汰变动，没法像 DHT 那样按 key 哈希定位，所以要把 KV 的身份和放置解耦，做一个专门的发现平面。

## 动机
- 前缀 KV 复用目前基本限于单集群内。
- 中心化目录：每次查询多一次广域往返，直接加到 TTFT。
- 哈希放置（一致性哈希/DHT）：要么把每条 KV 迁到哈希指定节点（每条几百 MB 广域带宽），要么只索引恰好落在指定节点上的条目，命中率低。

## 方案
1. **发现索引**：支持变长前缀查找，边缘处常数时间本地查表；索引值无键（keyless），有少量假命中（论文 §5.8 单独测）。
2. **分片维护单元**：所有写入由分片维护单元负责，读路径无锁、无跨节点协调。
3. **联合打分转发**：对所有 worker（不只持有者）按网络距离、排队延迟、缓存层级（HBM / host DRAM）、剩余 prefill 量打分，选最优目标。
4. 前缀长度按延迟推导（latency-derived prefix lengths），控制索引规模。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 仿真 | 64 worker 跨地域；每个按 A100-80GB 跑 Llama-3.1-8B BF16，32 GB VRAM + 128 GB host DRAM（PCIe 4.0 25 GB/s 回载），WAN 延迟取 CloudPing AWS 实测 |
| 实机 | 14 块 RTX 5090 跨三大洲（美 8、亚 4、欧 2），每卡一个 SGLang worker，跨地域走公网 |
| P99 TTFT | 比基线低 **1.3–14×** |
| P99 端到端延迟 | 最多低 **3.7×** |
| 吞吐 | 最高 **4.7×** |
| 负载均衡 | 峰值负载因子距 Oracle 下限 **2%** 以内 |

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 单机前缀缓存；KVCompass 把复用范围扩到跨地域
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 附录 C 讨论与 PD 分离的结合
- [Agentic KV Residency](/papers/agentic-kv-residency-m365-production.md) — 生产 trace 显示跨部署复用从 88.9% 跌到 29.0%，正是 KVCompass 要补的缺口
- [Remote KV Tier for PCP Prefill](/papers/remote-kv-tier-context-parallel-prefill.md) — 远端 KV 盈亏带宽分析，可用来判断跨地域取 KV 何时划算
- [Fancy Eviction for Prefix Cache](/papers/fancy-eviction-llm-prefix-cache.md)

## 开放问题
- 评测用 8B 模型；70B+ 或 MoE 模型的 KV 体积更大，跨地域搬 KV 与本地重算的盈亏点会移动。
- 跨地域取 KV 涉及数据驻留与隐私合规，论文未覆盖。

# Citations
- [arXiv:2610.24179](https://arxiv.org/abs/2610.24179) — Ling, Fang, Qian, POMACS 2026
- 代码：https://github.com/011shiyiLing/KVCompass
