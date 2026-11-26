---
type: Raw Source
title: "Making Protocol Effects Explicit: LLM-to-Packet Simulation for Superpod Interconnect Exploration"
source_url: https://arxiv.org/abs/2611.30191
pdf: ProtoBridge_LLM_to_Packet_Superpod_2026.pdf
retrieved: 2026-11-26
ingested: 2026-11-26
org: Tsinghua / MetaX / Infinigence-AI / HKUST / SJTU
venue: HPCA 2027
---

# Abstract (verbatim gist, arXiv:2611.30191)

Exploring superpod designs requires accurate interconnect simulation, as communication latency is jointly determined by link technologies, topologies, and scale-up protocol-stack choices. Latency-bandwidth models fail to capture contention and protocol effects, resulting in errors of up to 40%. Packet-level simulators like ns-3 model routing, queueing, and packet timing, but require protocol-specific LLM-to-packet implementations, and high simulation time hinders end-to-end evaluation.

ProtoBridge is an ns-3-based LLM-to-packet simulator. It introduces two abstraction layers over ns-3: an operation-to-packet (OTP) layer that captures protocol-specific packet exchanges and dependencies, and a packet-execution (PEX) layer that applies shared packet-level mechanisms to the ns-3 event system. ProtoBridge achieves average latency error of 17.8% on H200 NVLink4 and 10.3% on C500 MetaXLink. A surrogate model that combines OTP parameters with analytical models of PEX mechanisms reduces the mean absolute percentage error (MAPE) from 55.7% of latency-bandwidth models to 11.8%, and reduces evaluation time from 2.38–75.70 s to 20.5 µs per operation. Using the surrogate-to-simulator workflow, the authors explore 38,232 superpod designs across topologies, link technologies, and protocol configurations in one hour, and analyze scale-up memory pools and co-packaged optics (CPO) interconnects.

# Excerpts / key facts

- Authors: Yu Zhu, Xinhao Yang, Zhaoshi Li, Baodong Wu, Boxun Li, Wenxue Li, Guohao Dai, Hongyang Jia, Shuwen Deng, Huazhong Yang, Yuan Xie, Zhenhua Zhu, Yu Wang。清华、MetaX、无问芯穹、港科大、上海交大。arXiv:2611.30191，HPCA 2027。
- 硬件对照：H200（8 GPU，NVLink4/NVSwitch）；C500（4 GPU，MetaXLink 全互连）；另对 NVL72 开源数据与 ns-3-UB 参考。
- 包级仿真平均 MAPE：H200 17.76%，C500 10.33%，NVL72 1.76%，UB 2.77%；同期最好的 ASTRA-sim 后端为 52.01%、28.85%、15.62%、18.49%。UB AllToAll 上 ProtoBridge 为 8.65%。
- 860 组配置上，代理模型 MAPE 13.4%，延迟-带宽模型 60.6%；95% 预测误差小于 34.9%，正确排序 87.8% 的候选对；平均仿真 31.6% 的候选即可找到最低延迟设计（延迟-带宽模型需 99.2%）。
- 相对 SimAI，DeepSeek-V3 端到端 TGS / TTFT / TPOT 的 MAPE 为 4.5–7.9%；代理约 21 µs/操作，SimAI 约 16 ms。
- 案例：128 张 H200，GLM-5.2 在百万 token 上下文上，G1 点用 46 节点 HBF KV 池，交互性与 TGS 均为 1.31×。128×800 Gb/s CPO 相对光电：TTFT 降 0.42–7.58%；DeepSeek-V3 / GLM-5.2 的 TPOT 降 2.93% / 9.36%，Qwen3-235B 的 TPOT 升 2.50%。
