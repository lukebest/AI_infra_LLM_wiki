---
type: Raw Source
title: REACT — Tuning Collective Patterns to Alleviate Congestion in Shared AI Clusters
source_url: https://arxiv.org/abs/2609.04417
arxiv: '2609.04417'
ingested: 2026-09-08
sha256: f68154fefc61606d637798f59302d0910a582a07e133d344751ff99c0aad884d
---

# Tuning Collective Patterns to Alleviate Congestion in Shared AI Clusters（REACT）

**Authors:** Eashan Gupta, Yongzhou Chen, Apoorve Mohan, Pavlos Maniotis, Abdullah Kayi, Radhika Mittal
**Affiliations:** UIUC; Meta; IBM Research
**PDF:** [REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf](REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf)
**arXiv:** [2609.04417](https://arxiv.org/abs/2609.04417)（2026-09-03，cs.NI / cs.DC）

## 问题

共享云/学术集群里，单用户无法控制他方作业或背景流量造成的拥塞；现有方案多假设全局调度或交换机自适应路由，不适于「单边部署」。集体通信一轮里任一流变慢会拖垮整轮。

## 方法要点

- REACT：在 CCL/应用层（NCCL shim）用流级 FCT/吞吐统计检测拥塞，在保留集体语义前提下换集体 pattern（如 tree AllReduce 的聚合点、ring 上的邻居置换）。
- TEN（Time Expanded Network）建模；预计算安全 swap；反馈环按 epoch 批调参；无需基础设施支持。
- 覆盖 NCCL dual binary tree AllReduce、Ring AllReduce、recursive doubling AllGather。

## 摘录数字（仅论文给出）

- 实测：国家学术共享 GPU 集群；每服务器 4×A100 NVLink + 200Gbps Cray Slingshot；自适应路由与 GPU Direct RDMA 开启。
- 通信算法带宽（algorithm bandwidth）在拥塞下提升 **13%–38%**（Table 2  sweep）。
- ns-3 仿真跨多种拥塞/故障场景：算法带宽最高再升约 **75%**。
- 示例：拥塞下 collective 完成时间 656µs → 换 pattern 后 576µs（约 **14%**）。
