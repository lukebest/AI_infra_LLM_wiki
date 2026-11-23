---
type: Raw Source
title: "GNoF: A Low-SM-Overhead GPU-Native NVMe-over-Fabrics Completion Path for Data-Intensive GPU Workloads"
source_url: https://arxiv.org/abs/2611.21288
pdf: GNoF_GPU_Native_NVMeoF_2026.pdf
retrieved: 2026-11-23
ingested: 2026-11-23
org: National University of Defense Technology
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.21288)

GPUs are the main compute engine for data-intensive workloads whose datasets exceed device memory and reside on remote flash. The conventional host CPU orchestrates every NVMe-over-Fabrics (NVMe-oF) transaction and stages data through host memory, costing high CPU usage, repeated CPU-GPU synchronization, and redundant data movement. GPU-initiated storage removes the CPU from the I/O path, but existing designs leave two problems: synchronous lock-step completion pins streaming multiprocessors (SMs) in spin-polling, wasteful over a 10-100 microsecond RDMA round trip, and current GPU-native remote systems focus on target-side firmware while using per-command doorbells and periodic CQ polling. We present GNoF, a GPU-native NVMe-oF/RDMA data path where GPU threads build command capsules, post send work-queue elements, ring doorbells, and reap completions entirely on the device; the CPU only handles one-time connection setup, the admin queue, and a keep-alive thread. Three mechanisms target long fabric round trips: a doorbell mover that coalesces a burst's doorbells into one MMIO ring; a batched CQ poller with a lock-free fast peek and monotonic completion counters that cannot lose a wakeup; and a set-associative, reference-pinned GPU page cache with split fetch/wait pipelining and orphan-fill takeover. GNoF needs no target or firmware change and runs against an unmodified SPDK target. On a 200 Gb/s InfiniBand fabric, GNoF reaches 1.77 million 4 KB IOPS per client at 0.37% host CPU and about 1% SM occupancy, versus 40% CPU for kernel nvme-rdma and about 100% SM occupancy for lock-step polling. Against three existing baselines (kernel nvme-rdma, BaM over a BlueField-3 DPU, and BaM on a local SSD) under identical workloads, we show 10-22x gains on selective column I/O, CPU-burn immunity, and the regime where bulk staging is faster.

# Excerpts / key facts

- Authors: Lei Tian, Wenhao Gu（National University of Defense Technology）。arXiv:2611.21288，cs.DC / cs.AR，提交标注 16 Nov 2026。
- 测试床：200 Gb/s InfiniBand；客户端为 Ada 一代数据中心 GPU（算力能力 8.9，46 GB 显存）与 BlueField-3；目标端为未改动的 SPDK NVMe-oF 与企业级 SSD。GPU 与网卡跨 NUMA（NVIDIA 拓扑中的 SYS 类）。
- 峰值约 1.77 M 4 KB 随机读 / 约 1.0 M 写 IOPS；C=1024 时主机 CPU 0.37%、显存 8702 MiB。SM throughput 占用 0.03–1.07%。严格 in-flight=1 时 4 KB 读 RTT 约 98 µs，p99 为 135 µs（kernel nvme-rdma 为 197 µs）。
- 纽约出租车列扫描冷启动 224–804 ms，对照整图批量装载约 5 s，为 10–22×。8.5 GB 图 BFS 上批量装载为 9873 ms，GNoF 为 11870 ms。
