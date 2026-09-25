---
type: Paper
title: "Co-Fabric: 打通 Host 域的统一 xPU 互连"
description: "IEIT bus-based 四层栈跨 host 统一地址；64-xPU 3D-Mesh vs RoCE：延迟超 50%↓、带宽 2–5×、R1 推理 +30–80%、互连成本 −80%。"
tags:
- architecture
- interconnect
- scale-up
- protocol
- fabric
- supernode
- llm
- inference
- networking
- gpu
created: 2026-09-25
updated: 2026-09-25
timestamp: '2026-09-25T00:00:00Z'
paper_author: [Zhen Peng, Jiaming Huang, Chaofan Chen, Zhao Zhang, An Wu, Baoyang Liu, Xinglong Wang, Tanlong Ci, Jinfeng Li, Xueke Duan, Hao Wang, Xi Chen, Shunshun Zhang, Zhiyuan Su, Zhu Cao, Zhichong Dou, Shaohua Wu, Lu Jing, Yue Yuan]
year: 2026
arxiv: '2609.25560'
sources:
  - raw/papers/CoFabric_Unified_xPU_Interconnection_2026.pdf
  - raw/papers/cofabric-unified-xpu-interconnection.md
---

# Co-Fabric：打通 Host 域的统一 xPU 互连

## 一句话结论

IEIT 的 Co-Fabric 用 **bus-based 四层协议栈**（Media / Link / Fabric / Semantic）把跨 host 的 xPU 收进同一互连域与统一地址空间。64-xPU 3D-Mesh 相对同规模 RoCE：节点间延迟 **超过 50%** 降低、带宽 **2–5×**；DeepSeek R1 推理 **+30%–80%**；互连成本最高约 **−80%**、功耗约 **−5%**。

## 动机：网络栈跨域 vs 总线栈不出域

大模型副本跨多 xPU、多 host。行业 scale-up 分裂为两派：网络派（RoCE/IB）跨域方便但封装与软件栈重、memory 语义粗；总线派（类 NVLink）延迟低、load/store 友好，却难跨 OS/host。论文提出六条原则：精简分层、内存一致性（非全缓存一致）、原生 memory 语义、超低延迟、够用带宽、链路级可靠。声称现有协议无法同时满足。

## 方案

### 1. 四层精简栈

自下而上：**Media Layer (ML)** 比特编码、铜/光介质抽象；**Link Layer (LL)** credit 流控 + 链路重传（可靠性停在单跳）；**Fabric Layer (FL)** 全局地址映射与 Port-ID 路由、上电发现；**Semantic Layer (SL)** load/store 与原子操作。数据单向 Semantic→Fabric→Link→Media，无软件中途缓冲。

### 2. 跨域 ID 路由与统一地址

路由信息嵌在包头；Switch 按 Domain/Port ID 转发。**Shadow device** 自动枚举让每个 OS 把超节点内全部 xPU 看成「本机设备」，扁平统一地址，可用单机编程模型写多卡代码。

### 3. 拓扑解耦与评测系统

小规模可 full-mesh；大规模用 Co-Fabric Switch 弹性扩展。评测系统：双柜 **64 xPU 3D-Mesh**；对照为 8 卡 OAM + 以太 NIC/交换机的 64-xPU RoCE（Table III）。

## 量化结果

均来自摘要与 §V（相对同规模 RoCE）：

- **基础通信（AllReduce）**：<4MB 小包，延迟为 RoCE 的 **10%–20%**、带宽 **5–15×**；>4MB 大包，延迟 **15%–50%**、带宽 **2–5×**。摘要概括节点间延迟 **over 50%** 降低、带宽 **2–5×**。
- **成本/功耗**：互连成本约 **−80%**；互连功耗约 **−5%**（Fig. 11）。
- **推理**：DeepSeek-R1 671B、SGLang、INT8 MLA、DP4 TP16 + MoE TP，1K/1K；吞吐相对 RoCE **+30%–80%**（Fig. 13）。
- **训练缩放**：文称 64-xPU 上大模型训练近线性；另有 AllGather/AllReduce 墙钟相对 RoCE 约 **75%** 压缩等 Table IV 数字（按场景读图）。

## 局限与解读

- 对照是「8 卡服务器 + RoCE 以太」而非 NVLink/UB 同级 bus fabric；增益部分来自产品档差。
- 延迟/带宽曲线依赖 Fig.12–14，正文以区间概括；成本 −80% 依赖其 BOM 假设（Retimer + Co-Fabric 交换 vs 以太 NIC/交换机）。
- 开源生态与多厂商互通未在文中展开。

Co-Fabric 对照 [NVLink/NVSwitch](../concepts/nvlink-nvswitch-scale-up-fabric.md) 的固定高带宽域，走的是 **跨 host 总线语义**；协议分层补强 [Interconnection Network Protocol Stack](../concepts/interconnection-network-protocol-stack.md)，也是 [AI Infra Supernode](../concepts/ai-infra-supernode.md) 的一种产品化路径。

# Citations

1. Peng, Z., Huang, J., Chen, C., Zhang, Z., et al. “Co-Fabric: Breaking Host-Domain Boundaries for Unified xPU Interconnection.” arXiv:2609.25560, 2026. [arXiv](https://arxiv.org/abs/2609.25560)
2. [本地原文 PDF](../raw/papers/CoFabric_Unified_xPU_Interconnection_2026.pdf)；[原始来源记录](../raw/papers/cofabric-unified-xpu-interconnection.md)
