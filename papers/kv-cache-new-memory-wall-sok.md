---
type: Paper
title: "The KV Cache Is the New Memory Wall (SoK)"
description: "Singh — KV 五域 taxonomy；Llama-3-70B@128k +42 GB；H100/B200/MI300X crossover；三区间结构"
tags:
- architecture
- llm
- inference
- kv-cache
- memory
- memory-bandwidth
- cache
- quantization
- compression
- serving
- formal-analysis
- comparison
- hbm
created: 2026-09-29
updated: 2026-09-29
timestamp: '2026-09-29T00:00:00Z'
paper_author: [Tejinder Singh]
year: 2026
arxiv: '2609.30854'
sources:
  - raw/papers/KV_Cache_New_Memory_Wall_SoK_2026.pdf
  - raw/papers/kv-cache-new-memory-wall-sok.md
---

# The KV Cache Is the New Memory Wall

## 一句话结论

SoK 把长上下文 decode 的瓶颈从「权重搬运」钉到 **KV cache**：给出上下文相关算术强度闭式、H100/B200/MI300X（含多 die 分带宽）拓扑实例化，以及量化/淘汰/分页/前缀/分层五域 taxonomy；中心结论是硬件相关 **crossover** 之下、之上与容量墙的三区间结构。

## 动机

- Llama-3-70B BF16 权重 **140 GB** 已超单卡 80 GB HBM；单条 **128k** 序列再加 **42 GB** KV；**10⁶** token 时约 **328 GB**（&gt;4×H100 聚合）。
- 文献里压缩/淘汰/分页/共享/卸荷增益口径不一；缺统一分析骨架与 derived vs reported 分证。

对照 [Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md)、[MeshKV](/papers/meshkv-noc-kv-cache-fabric.md)、[End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)。

## 方案

1. **闭式**：decode 算术强度随上下文衰减；批量抬权重侧强度、不抬 KV 侧。
2. **拓扑**：H100 单体；B200 2-die NV-HBI；MI300X 8-XCD；区分 aggregate vs per-die β（条带可收回聚合，钉死页则折半或更差）。
3. **五域**：quantization / token eviction / KV paging / prefix caching / heterogeneous tiering；统一协议下 128k 对比，**不混** derived 吞吐上界与 as-reported 质量差。

## 效果与推导数字（仅论文）

| 项 | 数字 |
|----|------|
| H100 ridge I\*（BF16 dense） | **≈295 FLOP/B**（989.5 TF / 3.35 TB/s） |
| Llama-3-70B KV | **0.33 MB/token**；128k → **≈42 GB** |
| Traffic crossover s\*(b)（70B BF16，Table 4） | b=1：**427.2k**；b=32：**13.4k**；b=256：**1.7k** |
| b≈295 时 70B crossover | 已落到 **≈1.4k** tokens（权重算力界与 KV 界冲突） |
| 长上下文 token 率天花板 R∞（70B） | H100 **10.2M** tok/s；B200 striped **24.4M**；… |
| 容量墙示例 | 70B 单卡 H100 @ **244k**；405B @ **155k** |
| PCIe Gen5 x16 vs H100 HBM | 约 **64 GB/s**，约 **50×** 慢；NVLink 900 GB/s 仍约 **3.7×** 慢 |

中心三区间：crossover 下权重仍可见；之上 KV 主导、各域用可测质量换带宽、逼近 roofline；再上触及容量墙。Paging/prefix 对输出无损；量化/淘汰有质量–带宽折中。

## 与 wiki 的关系

- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) / [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 分析骨架
- [Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md) — 前缀域生产实证；本文给 **跨域统一界**
- [MeshKV](/papers/meshkv-noc-kv-cache-fabric.md) — 片上 KV 流量轴，正交于压缩/淘汰

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.30854) — Singh, arXiv:2609.30854
[2] [raw stub](raw/papers/kv-cache-new-memory-wall-sok.md)
