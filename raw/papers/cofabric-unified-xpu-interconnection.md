---
type: Raw Source
title: "Co-Fabric: Breaking Host-Domain Boundaries for Unified xPU Interconnection"
description: "Co-Fabric 原始论文来源：跨 host 的 bus-based 四层 xPU scale-up 互连协议。"
timestamp: '2026-09-25T00:00:00Z'
source_url: https://arxiv.org/abs/2609.25560
arxiv: '2609.25560'
ingested: 2026-09-25
sha256: 6f28399329abf4e70958aee38e8a402a634ef6257cc6b58c355a982dadd889b9
---

# Co-Fabric: Breaking Host-Domain Boundaries for Unified xPU Interconnection

**Authors:** Zhen Peng, Jiaming Huang, Chaofan Chen, Zhao Zhang, An Wu, Baoyang Liu, Xinglong Wang, Tanlong Ci, Jinfeng Li, Xueke Duan, Hao Wang, Xi Chen, Shunshun Zhang, Zhiyuan Su, Zhu Cao, Zhichong Dou, Shaohua Wu, Lu Jing, Yue Yuan  
**Affiliation:** IEIT SYSTEMS Co., Ltd.  
**PDF:** [CoFabric_Unified_xPU_Interconnection_2026.pdf](CoFabric_Unified_xPU_Interconnection_2026.pdf)  
**arXiv:** [2609.25560](https://arxiv.org/abs/2609.25560)（2026-09-22，cs.DC）

## 问题

超节点要把跨 host 的 xPU 做成统一地址空间与原生 memory 语义。RoCE 等网络栈跨域可达但延迟/封装重；NVLink 类总线语义好但难跨 host。

## 方法要点

- 四层栈：Media (ML) → Link (LL, credit + 链路重传) → Fabric (FL, Port-ID 路由/地址映射) → Semantic (SL, load/store/atomic)。
- shadow-device 自动枚举形成跨 OS 的统一地址空间；拓扑可从 full-mesh 弹性到带 Co-Fabric Switch 的超节点。
- 评测：64-xPU 3D-Mesh 相对 64-xPU RoCE（8 卡 OAM + 以太交换机）。

## 摘录数字（仅论文给出）

- 节点间延迟 **over 50%** 降低；带宽 **2–5×**；DeepSeek R1 推理 **+30%–80%**。
- 互连成本最高 **−80%**、功耗约 **−5%**。
- AllReduce：小包（<4MB）延迟为 RoCE 的 **10%–20%**、带宽 **5–15×**；大包（>4MB）延迟为 RoCE 的 **15%–50%**、带宽 **2–5×**。

**Working page:** [Co-Fabric](/papers/cofabric-unified-xpu-interconnection.md)  
**Related:** [Protocol Stack](/concepts/interconnection-network-protocol-stack.md)、[AI Infra Supernode](/concepts/ai-infra-supernode.md)
