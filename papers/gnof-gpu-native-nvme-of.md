---
type: Paper
title: "GNoF: Low-SM-Overhead GPU-Native NVMe-over-Fabrics"
description: "国防科大 — 200 Gb/s InfiniBand 实测；每客户端最高约 1.77 M 4 KB IOPS，主机 CPU 0.37%、SM throughput 占用约 1%；列扫描相对整图装载 10–22×"
tags:
- gpu
- storage
- ssd
- flash
- rdma
- memory
- throughput
- latency
- hardware
- interconnect
created: 2026-11-23
updated: 2026-11-23
timestamp: '2026-11-23T00:00:00Z'
paper_author: [Lei Tian, Wenhao Gu]
year: 2026
venue: preprint
arxiv: '2611.21288'
sources:
  - raw/papers/GNoF_GPU_Native_NVMeoF_2026.pdf
  - raw/papers/gnof-gpu-native-nvme-of.md
---

# GNoF：把 NVMe-oF 补全路径放到 GPU 上，还把 SM 轮询压下去

## 一句话结论
国防科技大学的 GNoF 让 GPU 线程在设备上完成 NVMe-oF/RDMA 的建囊、发门铃和收完成，主机只保留建链、管理队列和保活线程。在 200 Gb/s InfiniBand 测试床上，每客户端最高约 1.77 M 次 4 KB 读 IOPS，主机 CPU 为 0.37%，SM throughput 占用约 1%；对照 kernel nvme-rdma 的主机 CPU 约 40%，以及 BaM 式锁步轮询约 100% 的 SM issue。

## 动机
图分析、推荐与列存这类数据密集负载，数据集常常超过显存，要经 NVMe-oF 读远端闪存。常规路径由主机 CPU 编排每一笔事务并经主机内存中转，CPU 占用高，还反复做 CPU–GPU 同步。已有 GPU 发起存储（BaM、libnvm）多针对本地 PCIe SSD，完成路径是锁步自旋，在 10–100 µs 的织物往返上会把 SM 钉住；远程方案又往往把创新放在目标端固件，客户端仍用逐条门铃和周期性 CQ 轮询。

## 方案
三条面向长织物往返的客户端机制：门铃合并器（把一次突发里连续写好的门铃收成一次 MMIO）；批量 CQ 收取（无锁快窥、一把锁排空整批，完成计数单调递增、不清除标志，避免丢掉唤醒）；集合关联、引用钉住的 GPU 页缓存，拆出发送与等待，并用 orphan-fill 接管。设计不改目标端或 SSD 固件，对着未修改的 SPDK NVMe-oF 目标运行。原型是 CUDA C++ 加用户态 rdma-core/verbs 与 mlx5 Direct Verbs，用 peer-memory 模块做网卡到显存的 DMA。

测试床：客户端为 Ada 一代数据中心 GPU（算力能力 8.9，46 GB 显存）与 BlueField-3；目标端挂企业级 NVMe SSD。GPU 与网卡跨 NUMA（NVIDIA 拓扑中的 SYS 类）。对照四个方案：P1 kernel nvme-rdma + fio/io_uring（数据到主机内存）；P2 GNoF；P3 BaM over BlueField-3 SNAP（队列深度受 SNAP MQES=64 限制）；P4 本地 SSD 上的 BaM。按在途请求总数 C 对齐，直接 I/O，每方案单独跑，三次重复。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 4 KB 吞吐 | 织物上的 P1/P2/P3 随并发到 **1.2–1.8 M IOPS**；GNoF 峰值约 **1.77 M 读 / 1.0 M 写**。本地 BaM 随机读平台期仅约 55 K（同盘 fio 为 1.76 M） | Fig. 3 / §6.3 |
| 资源（C=1024） | GNoF 主机 CPU **0.37%**、GPU 利用率 19/100、显存 **8702 MiB**；P1 主机 CPU **40.3%**；P3 另加 DPU Arm **24.8%** | Table 3 / Fig. 4 |
| SM 占用 | GNoF 的 SM throughput 为 **0.03–1.07%**，warps-active ≤16.67%；BaM（P3/P4）在各线程数上 SM issue ≈100% | Table 2 / Fig. 2 / §6.2 |
| 单次延迟（in-flight=1，4 KB 读） | GNoF 与 P1 的端到端 RTT 都约 **98 µs**；GNoF 的 p99 为 **135 µs**（P1 为 197 µs），主机 CPU 为 0.2%（P1 为 17.6%） | §6.4 |
| 主机核争用 | 钉死 0–72 个主机核时，GNoF/P3/P4 归一化吞吐保持约 1.00 直到 36 核；P1 在 56 核之后降到 0.84–0.94 | Fig. 5 / §6.5 |
| 应用 | 纽约出租车列扫描（38.3 M 行，2.85 GB，6 个查询）冷启动 **224–804 ms**，对照整图装载约 5 s，为 **10–22×**。2.13 GB 图 BFS：GNoF 1975 ms，装载 2567 ms，主机路径 3998 ms。8.5 GB 图 BFS：装载 **9873 ms**，GNoF **11870 ms**，主机路径 16798 ms——在约 965 MB/s 的织物上，粗粒度装载更快 | Table 4 / §6.7 |

评测负载是图分析与列存扫描。页缓存从 1 GiB 增到 16 GiB 时，BFS 时间从 61.3 s 降到 9.65 s。向量加这条写多、规则的路径上，GNoF 没有超过最好的装载流水线。

## 与已有页的增量
[uGDS](/papers/ugds-userspace-gpu-direct-storage.md) 走用户态 GPU Direct Storage，编排仍在主机一侧。[Janus](/papers/janus-agentic-ssd-sparse-kv.md) 把智能体稀疏 KV 放到 SSD 路径上，数字来自服务延迟。本篇把 NVMe-oF 客户端的完成路径放到 GPU 上，并在 200 Gb/s 织物上给出相对 kernel nvme-rdma 与 BaM 的 IOPS、CPU、SM 占用和应用时间。负载与对照都不同，倍数不宜直接横比。

## 与 wiki 的关系
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — 远端 NVMe-oF 与 GPU 发起的闪存路径
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 数据集超出显存后的存储访问
- [uGDS](/papers/ugds-userspace-gpu-direct-storage.md) — 同属 GPU 与 NVMe 之间的数据通路，编排位置不同
- [KIWI](/papers/kiwi-reverse-offload-gpu-initiated.md) — GPU 发起的通信；本篇是存储织物上的完成路径

## 开放问题
- 评测平台是单客户端、跨 NUMA 的 Ada GPU + 200 Gb/s InfiniBand，未给出多客户端争用或 LLM 权重/KV 卸载数字。
- P3 的并发被 SNAP MQES=64 卡住；本地 BaM 读路径远低于同盘 fio，作者把它记为锁步读路径的限制。
- 大图 BFS 上粗粒度装载更快，作者把这写成明确的适用边界。
- 严格单飞行的 BaM 百分位延迟，文中留作后续工作。

# Citations
- [arXiv:2611.21288](https://arxiv.org/abs/2611.21288) — Tian, Gu（National University of Defense Technology）
- [raw stub](/raw/papers/gnof-gpu-native-nvme-of.md)
- [PDF](/raw/papers/GNoF_GPU_Native_NVMeoF_2026.pdf)
