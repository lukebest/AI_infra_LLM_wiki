---
type: Raw Source
title: 📰 体系结构晨报 — Day 20
source_path: /home/luke/openclawdata/workspace-research/notes/projects/arch-study-30d/day-20.md
textbook: "Computer Architecture: A Quantitative Approach (6th ed.) — Appendix D (Storage Systems)"
ingested: 2026-07-03
---

# 📰 体系结构晨报 — Day 20

📅 2026-07-03（Day 20 / 30，星期五）
🎯 阶段：存储篇（Day 17-22）
📖 教材：《计算机体系结构：量化方法》第6版 Ch.D（附录D — 存储系统）

---

## 今日主题：存储系统 + I/O（SSD / RAID / NVMe / I/O 路径）

### 🧭 为什么今天学这个？

昨天的 Day 19 解决了"内存级别"的同步与一致性问题——多个核对同一/不同地址的访问顺序。今天把视野往下沉到"存储级别"：**磁盘、SSD、RAID、NVMe**。

**为什么体系结构课程要看磁盘？**

> **AI 训练 = 数据加载 + 计算 + 通信**。
>
> 很多人把 GPU/NPU 当瓶颈，但实际上 **DataLoader 经常是真正的瓶颈**——尤其在大模型时代，一个 checkpoint 动辄几十 GB，一个 epoch 的 dataset 动辄 TB 级。

今天的核心问题：

```
1. SSD 为什么这么快？Flash cell、FTL、wear-leveling、GC 如何协同？
2. RAID 0/1/5/6 在不同工作负载下如何选择？
3. NVMe 协议如何把 PCIe 带宽榨干？
4. 从 user-space 发起一次 read() 到拿到数据，经历了哪些延迟？
```

**对你的研究（WSE / NPU / NoC）而言**，今天的概念是 **"AI 训练系统的完整 I/O 路径"**：
- WSE/NPU 通常 host 在传统服务器上，host 的 I/O 能力直接决定 dispatch / collect 的速度
- 大模型推理时 KV-cache 落盘（paged attention）涉及高速 SSD
- 多 NPU 训练时，权重 checkpoint 写入带宽需求巨大
- Cerebras 的 memoryX 用 NVMe SSD 做扩展——直接相关！

---

## 📖 阅读任务（约 60-90 分钟）

**《计算机体系结构：量化方法》第6版 附录 D (Appendix D)：Storage Systems**

### 核心阅读（60 min）：
1. **D.1 Introduction** — 存储系统分类、I/O 性能度量
2. **D.2 Advanced Topics in Disk Storage** — 磁盘物理、寻道时间、旋转延迟、调度算法
3. **D.3 Definition and Example of a RAID** — RAID 0/1/4/5/6 的 stripe 布局与故障恢复
4. **D.4 Features of Modern RAID** — 写策略、预读、后台重建
5. **D.5 Storage System Design Issues** — 存储系统的端到端延迟分解

### 推荐补充（30 min）：
- **《量化方法》Ch.2.6 (I/O and Storage)** — 与 D.5 互补
- **Samsung PM1743 / Kioxia CM7 NVMe SSD 白皮书** — 现代企业级 SSD 规格
- **NVMe 2.0 规范** 第五章（NVMe over PCIe）— 协议栈
- **ACM Queue "The Path to NVMe"** — NVMe 简史

### 选读：
- Intel SSD 670p / Samsung 990 PRO 消费级 datasheet
- Linux `blk-mq` 子系统源码（request allocation 部分）

---

## 🔑 核心概念（必须掌握）

### 1. 磁盘 (HDD) 性能模型（已渐弱但需理解）

```
磁盘访问时间 = T_seek + T_rot + T_transfer

T_seek      = 平均寻道时间（3-10 ms）
T_rot       = 1/2 × 旋转周期（7200 RPM → 4.17 ms）
T_transfer  = 扇区数 × (1 / (RPM/60) × 扇区数每圈)
```

**机械硬盘的"3 个数量级"差距**：
| 操作 | 延迟 |
|------|------|
| 顺序读 (1 MB) | ~1 ms |
| 随机读 (4 KB) | ~10 ms |
| 寻道 (seek only) | ~5 ms |

**关键洞察**：随机 I/O 和顺序 I/O 的性能差距是 **1000× 级别**——这正是 SSD 颠覆磁盘的根本原因。

### 2. SSD 物理与性能模型

**Flash Cell 原理**（NAND Flash）：
```
存储单元 = Floating Gate MOSFET
  写 (Program)：加高压电子穿过 oxide 注入 floating gate → 改变 V_th
  读：测量 V_th
  擦 (Erase)：反向电压抽出电子

限制：
  • Block-level erase only（不能单 byte 擦除）→ 必须 FTL 翻译
  • P/E cycle 有限（SLC ~100K, MLC ~10K, TLC ~1K, QLC ~500）
  • 写前必须擦（erase-before-write）→ 写放大 (Write Amplification)
```

**SSD 内部架构**：
```
┌──────────────┐
│ Host I/F     │  ← NVMe / SATA
├──────────────┤
│ FTL (Flash   │  ← 关键软件层！
│ Translation  │     • L2P mapping
│ Layer)       │     • Wear-leveling
│              │     • Garbage Collection
│              │     • Bad block 管理
├──────────────┤
│ Flash        │  ← 多 die / 多 plane / 多 channel
│ Controller   │     每个 channel 可独立读写
├──────────────┤
│ NAND dies    │  ← Block (256 KB - 4 MB) → Page (4-16 KB)
│              │     Page = 读写单位，Block = 擦除单位
└──────────────┘
```

**SSD 性能公式**（粗略）：
```
SSD 读延迟 ≈ 50-100 μs (page read + controller)
SSD 写延迟 ≈ 200-2000 μs (program + 可能要 erase)
SSD IOPS   ≈ 50K-1M (4 KB random read, 队列深度 = 32)
SSD 带宽   ≈ 500 MB/s - 14 GB/s (顺序, PCIe 5.0 NVMe)
```

### 3. FTL：Flash Translation Layer（SSD 软件核心）

**三大职责**：

**(a) Logical-to-Physical Mapping（L2P）**：
```
逻辑地址 LBA 0   → 物理地址 (die=0, block=42, page=5)
逻辑地址 LBA 1   → 物理地址 (die=1, block=10, page=12)
...
```
**为什么需要**：写不能原地改（要 erase）；FTL 写新数据到 free page，更新 mapping。

**(b) Wear-Leveling（磨损均衡）**：
```
目标：让所有 block 的 P/E cycle 接近平均
  - Dynamic WL：写热数据时换冷 block
  - Static WL：定期搬冷数据，让闲置 block 也被使用

寿命公式：
  SSD 寿命 (TBW) = NAND capacity × P/E cycles × (1 / WA)

  例：1 TB TLC SSD (1K P/E, WA=3) → TBW = 333 TB
```

**(c) Garbage Collection (GC)**：
```
问题：写新数据需要 free page；free page 来自死 page（已 invalidate 但未擦）
      但 erase 必须擦整个 block → 必须先合并多个死 page

流程：
  1. 选 victim block（死页最多）
  2. 把 block 里的活页搬到新 block
  3. 擦 victim block
  4. 加入 free pool

写放大 WA = (实际写入 NAND 的数据) / (主机写入的数据)
  理想 WA = 1；GC 不利时 WA = 3-5
```

**GC 的"写停顿"问题**：GC 期间，前台 I/O 被阻塞 → 突发 latency spike（百 ms 级）。这是企业级 NVMe 的核心优化目标。

### 4. RAID 各级对比

**RAID 0 (Striping)**：
```
Disk0:  A0  A2  A4
Disk1:  A1  A3  A5
→ 容量 = N × disk_size
→ 读 = 2×（条带并行）
→ 写 = 2×（条带并行）
→ 可靠性 = 0（任一盘坏 = 数据全丢）
→ 适用：临时数据、计算中间结果
```

**RAID 1 (Mirroring)**：
```
Disk0:  A0  A1  A2
Disk1:  A0' A1' A2'  ← 完全镜像
→ 容量 = 1 × disk_size
→ 读 = 2×（可从任一镜像读）
→ 写 = 1×（写两份，但只受最慢盘限制）
→ 可靠性 = 1 盘坏仍可工作
→ 适用：关键元数据
```

**RAID 5 (Striping + Single Parity)**：
```
Disk0:  A0   A1   A2   P3
Disk1:  B0   B1   P2   B3
Disk2:  C0   P1   C2   C3
Disk3:  P0   D1   D2   D3
→ 容量 = (N-1) × disk_size
→ 读 = (N-1)×（小写放大，因为 parity 占 1/N）
→ 写 = 4× I/O  Read-Modify-Write！(最致命弱点)
→ 可靠性 = 1 盘坏可恢复
→ 适用：读多写少
```

**RAID 6 (Striping + Double Parity)**：
```
→ 同 RAID 5，但有 P、Q 两个独立 parity
→ 容量 = (N-2) × disk_size
→ 可容忍 2 盘同时坏
→ 写 = 6× I/O（更糟）
→ 适用：超大阵列（>8 盘）
```

**RAID 性能表**（以 4 KB 随机 I/O，10 盘 RAID-5 为例）：

| 类型 | 顺序读 | 顺序写 | 随机读 | 随机写 |
|------|--------|--------|--------|--------|
| RAID 0 | 10× | 10× | 10× | 10× |
| RAID 1 | 2× | 1× | 2× | 1× |
| RAID 5 | 9× | 2× (read-modify-write) | 9× | **1× (灾难！)** |
| RAID 6 | 8× | 1.5× | 8× | **0.5×** |

**关键洞察**：**RAID 5/6 的随机写性能极差**——这是为什么企业用 SSD + RAID 10（或 erasure coding 软件方案）。

### 5. NVMe 协议：榨干 PCIe 带宽

**NVMe 关键创新**（vs 老的 AHCI / SATA）：
```
AHCI (SATA 时代)：
  - 1 个 command queue, 深度 32
  - 每次中断处理 1 个命令
  - 难以利用 SSD 并行性

NVMe (PCIe 时代)：
  - 最多 65535 个 I/O queues
  - 每个 queue 深度 65535
  - MSI-X 中断（多核友好）
  - Doorbell register 直接命令提交（无 I/O 寄存器读写）
```

**NVMe 命令提交流程**：
```
Host                            Device
  │                                │
  ├── 1. 写 Submission Queue ────→ │  (把命令放在 host memory 的 ring buffer)
  │                                │
  ├── 2. 写 Doorbell Reg ───────→ │  (敲 NVMe controller 寄存器通知有新命令)
  │                                │
  │   ... (device 处理命令)        │
  │                                │
  ├── 3. 写 Completion Queue ←─── │  (device 把完成状态写到 host memory)
  │                                │
  ├── 4. MSI-X 中断 ────────────→ │  (device 中断 host)
  │                                │
  └── 5. Host 处理中断             │
```

**NVMe over PCIe 带宽表**（单 SSD）：

| PCIe Gen | 通道数 | 理论带宽 | NVMe SSD 实测 |
|----------|--------|----------|---------------|
| Gen 3 | ×4 | 4 GB/s | ~3.5 GB/s |
| Gen 4 | ×4 | 8 GB/s | ~7 GB/s |
| **Gen 5** | **×4** | **16 GB/s** | **~14 GB/s** |
| Gen 5 | ×16 | 64 GB/s | (极少用) |

### 6. I/O 路径延迟分解（端到端）

**典型 read() 调用栈**：
```
用户态:  read(fd, buf, 4096)         ← syscall entry ~200 ns
   │
内核态:
   ├─ VFS layer                       ~200 ns (路径解析)
   ├─ Page cache lookup               ~500 ns
   │    ├─ Cache hit → memcpy        ~1 μs (4KB to user buf)
   │    └─ Cache miss → 启动 I/O
   │
   ├─ Filesystem layer                ~500 ns (ext4/xfs)
   │    (block 层地址映射)
   │
   ├─ Block layer (blk-mq)            ~500 ns
   │    (请求合并、调度、IO 调度器)
   │
   ├─ NVMe driver                     ~500 ns
   │    (PCIe 提交命令到 doorbell)
   │
硬件:
   ├─ PCIe 传输                       ~500 ns (TLP 包)
   ├─ NVMe controller 处理            ~5-10 μs
   ├─ NAND read (从 die)              ~50-100 μs
   │    └─ (如果需要 GC，额外 1-10 ms!)
   │
DMA 中断:
   ├─ MSI-X 中断返回                   ~500 ns
   ├─ NVMe 中断处理 (CQ polling)      ~1 μs
   │
内核态返回:
   └─ copy_to_user + syscall exit     ~500 ns
```

**总延迟**：
```
Page cache hit:  ~3-5 μs
NVMe SSD hit:    ~50-200 μs
NVMe SSD GC:     ~1-10 ms (!!!)
HDD:             ~5-20 ms
```

**关键洞察**：
1. **Software path 比 hardware 延迟更可观**：kernel 路径 ~3 μs vs NAND 本身 ~50 μs
2. **GC 是 latency killer**：突发 GC 让 SSD 延迟从 100 μs 跳到 10 ms
3. **io_uring 是游戏规则改变者**：绕过内核路径，用户态直接提交命令，延迟可降到 ~10 μs（仅硬件延迟）

### 7. 现代 I/O 技术趋势

**(a) io_uring**（Linux 5.1+）：
- 用户态/内核态共享 ring buffer
- 无 syscall 开销（最常用 submission 不需要 syscall）
- 批处理友好（一次提交 1024 个 I/O）

**(b) NVMe over Fabrics (NVMe-oF)**：
- 把 NVMe 命令包在 RDMA / TCP / FC 里
- 远程访问 SSD 像本地一样（延迟 ~10-20 μs over RoCE）

**(c) Computational Storage**：
- SSD 内部带 FPGA / ARM core
- 部分计算在 SSD 内完成（filter、compress、scan）
- 减少数据传输量

**(d) Zoned Namespaces (ZNS)**：
- 暴露 SSD 物理 block 布局
- Host 自己做 GC，更可控的延迟

---

## 📝 笔记任务（约 30 分钟）

1. **画出 SSD 内部架构图**：Host I/F → Controller (FTL) → NAND dies (channels × dies × planes × blocks × pages)
2. **手算 RAID-5 随机写放大**：为什么 RAID-5 4 KB 随机写需要 4 次 I/O？（read old data + read old parity + write new data + write new parity = 4）
3. **对比 NVMe vs AHCI 的 command queue 模型**：AHCI 1 queue × depth 32 = 32 commands；NVMe 64K queues × depth 64K = 4G commands in flight
4. **列出 5 个能减少 I/O 延迟的技术**（page cache、io_uring、NVMe-oF、prefetch、ZNS）
5. **思考**：如果 host 用 page cache 但 NPU 想 bypass cache 直写 SSD，会发生什么？（需要 O_DIRECT）

---

## 🧪 练习题（约 30-60 分钟）

### 基础题

**Q1**：某 SSD 标称 1 TB TLC NAND，P/E cycles 1000，平均写放大 WA=3。该 SSD 的总写入寿命 (TBW) 是多少？

> 答：
> TBW = (NAND capacity × P/E cycles) / WA = (1 TB × 1000) / 3 ≈ **333 TB**
> 厂商标称通常 300-600 TBW，与计算吻合。

**Q2**：10 盘 RAID-5 阵列做 4 KB 随机写。每块盘 IOPS 10000（机械盘）。计算阵列随机写 IOPS。

> 答：
> - 每次 4 KB 随机写 = 4 次 I/O（read old data + read parity + write data + write parity）
> - 每盘承担 4 次 I/O 中的部分，但每盘仍要处理至少 1 次 I/O 4 KB
> - 阵列 IOPS 受限于**最忙的那块盘**
> - 实际：RAID-5 随机写 IOPS ≈ 单盘 IOPS / 4 ≈ **2500 IOPS**
> - 对比：RAID-0 是 10 × 10000 = 100K IOPS（**40 倍差距！**）
> - 关键洞察：这就是为什么数据库（PostgreSQL / MySQL）严禁用 RAID-5 跑随机写。

**Q3**：NVMe SSD 标称顺序读 14 GB/s，4 KB 随机读 1M IOPS。计算 4 KB 随机读的"等效带宽"。

> 答：
> - 1M IOPS × 4 KB = 4 GB/s
> - 比顺序读 14 GB/s 低 **3.5×**
> - **原因**：随机读每个命令只读 4 KB（最小单位），NAND die 内部寻址 + DMA + 中断处理占大头
> - 对比：顺序读可以一条命令读几百 KB，NAND die 持续 streaming

**Q4**：解释"写放大 WA=3" 的具体含义。什么情况下 WA=1？

> 答：
> - **WA=3 含义**：主机写 1 GB，实际写到 NAND 的数据量 = 3 GB
> - **WA 来源**：
>   - GC 搬移活页（最常见）
>   - 静态磨损均衡（搬冷数据）
>   - 读改写（read-modify-write）— RAID 场景
> - **WA=1 条件**：
>   - 顺序写（host 顺序覆盖写，FTL 不用搬老数据）
>   - SSD 满前（大量 free block，无需 GC）
>   - 主机用 TRIM 主动释放（FTL 知道哪些 block 是死的）
> - **WA=1 是企业 SSD 的关键优化目标**——影响寿命 + 延迟稳定性。

### 进阶题

**Q5**：大模型训练时，DataLoader 经常是瓶颈。假设：
- GPU 训练吞吐：10000 samples/sec
- 每 sample 需要从 dataset 读 1 MB 数据（图片 / token 序列）
- 单块 NVMe SSD 顺序读带宽：7 GB/s

计算 DataLoader 是否成为瓶颈。如果想用 8 块 SSD 做并行读，需要怎样的软件改造？

> 答：
> - **数据需求**：10000 samples/sec × 1 MB = 10 GB/s
> - **SSD 能力**：7 GB/s (单盘)
> - **结论**：**DataLoader 是瓶颈！** 单盘只能提供 70% 所需带宽
> - **8 盘并行方案**：
>   1. **sharding**：把 dataset 分成 8 份，每盘一份（PyTorch `DistributedSampler`）
>   2. **prefetch**：开 4-8 个 worker，每个预先读下一 batch 到内存（`num_workers=8`）
>   3. **mmap + async I/O**：用 `aio` 或 `io_uring` 异步读，不阻塞 GPU
>   4. **NVMe-oF**：把 dataset 放在远端 NVMe over RoCE，扩展性更强
>   5. **压缩**：dataset 存为压缩格式（zstd/lz4），读时解压缩；CPU 解压 vs SSD 带宽的权衡
> - **终极方案**：用 memoryX-like 架构，把 dataset 缓存在 NPU 旁边的 NVMe SSD 池子，避免 PCIe 共享带宽

**Q6**：io_uring vs libaio 性能对比。假设 4 KB 随机读、队列深度 128、单线程。粗略估算二者 IOPS。

> 答（典型 Linux 系统实测）：
> - **libaio**（传统 POSIX AIO）：~200K IOPS
>   - 每次 I/O 提交 = 1 次 syscall（io_submit）+ 1 次 syscall（io_getevents）
>   - syscall 开销 ~1-2 μs，每次 2 次 → 总开销 ~3 μs/I/O
>   - 理论上限 = 1 / 3μs ≈ 330K IOPS（实测 ~200K）
> - **io_uring**（现代 Linux I/O）：~800K IOPS
>   - submission ring：用户态写 ring 即可（**不需 syscall**！）
>   - completion ring：轮询或单次 reap
>   - 理论上限接近 SSD 硬件上限 1M IOPS
> - **提升 ~4×**
> - **对 NPU/WSE 的启示**：WSE 的 host interface 应该用 io_uring 直接和 NVMe SSD 通信，绕过内核路径。这正是 Cerebras memoryX 的设计思路。

### 思考题（与 WSE/NoC/NPU 研究关联）

**Q7**：Cerebras WSE-3 的 memoryX 用 4 个 NVMe SSD 给 900K PE 提供扩展存储。如果用普通 NVMe SSD（顺序读 7 GB/s），4 块并行 = 28 GB/s。对比 WSE 内部 SRAM 的 21 PB/s 带宽。差多少倍？这种带宽差距对哪些工作负载致命？

> 答：
> - **带宽比**：21 PB/s ÷ 28 GB/s = **750,000×**
> - 即便乘以 4 块 SSD 的并行度，差距仍然是 **75 万倍**
> - **致命的场景**：
>   1. **KV-cache 读取**：LLM 推理时每 token 要读整个 KV-cache（GB 级），从 SSD 读会卡死
>   2. **大矩阵加载**：单层 transformer 权重就几 GB，从 SSD 加载延迟 1 秒（相对计算 10 ms，差 100×）
>   3. **多步迭代**：训练一个 step 要读数据 → 必须先 cache 到片上 SRAM
> - **可行的场景**：
>   1. **checkpoint 写入**：偶尔落盘，可接受
>   2. **冷启动数据加载**：一次性事件，可接受
>   3. **Streaming inference**：用 prefetch + 大 SRAM 吸收延迟
> - **关键洞察**：WSE 的 21 PB/s SRAM 是**唯一**真正匹配其算力的存储层次。任何外部存储都形成"内存墙"——只是墙的厚度不同。

---

## 🔗 与 WSE / NoC / NPU 研究的关联

### 1. AI 训练的 I/O 瓶颈分析

**完整数据路径**（以 GPT-3 训练为例）：
```
Dataset (PB级, 存于 HDD/对象存储)
   │  初次加载：~小时级
   ▼
NVMe SSD Pool (TB级, 顺序读 ~28 GB/s with 4盘)
   │  训练 step 数据：~秒级
   ▼
Host DRAM (GB级, ~100 GB/s)
   │  prefetch：~毫秒级
   ▼
GPU HBM (GB级, ~3 TB/s)
   │  forward/backward：~微秒级
   ▼
GPU SRAM (MB级, ~几十 TB/s)
   │  compute
   ▼
GPU ALUs
```

**每一层的"带宽悬崖"**：
- DRAM → HBM：~30×
- HBM → SRAM：~30×
- SRAM → ALU：~30×

**结论**：**每一层都可能成为瓶颈**，但瓶颈位置取决于工作负载：
- 训练大模型 → HBM 容量不够（不是带宽）
- DataLoader 慢 → SSD 不够
- 推理 KV-cache → DRAM 不够

### 2. WSE memoryX 的设计哲学

```
WSE-3 架构：

  ┌─────────────────────────────────┐
  │  Wafer (46,225 mm²)            │
  │  900K PE × 48KB SRAM = 43 GB   │  ← 片上 21 PB/s 带宽
  │  Mesh NoC                      │
  └─────────────────────────────────┘
        │  PCIe Gen5 ×16
        │  ~64 GB/s host link
        ▼
  ┌─────────────────────────────────┐
  │  memoryX (外置)                 │
  │  4× NVMe SSD = ~30 TB          │  ← 1-7 GB/s 顺序读
  │  DRAM 池                       │  ← 100 GB/s
  └─────────────────────────────────┘
        │
        ▼
  Host x86 CPU
```

**关键设计选择**：
- WSE **没有 L3/L4 cache**——片上 SRAM 就是 cache
- WSE **没有传统存储层次**——SRAM 到 DRAM 到 SSD 是完全分离的 tier
- memoryX 是"软件管理的存储 tier"——程序员（或编译器）显式搬运数据

**与 cache hierarchy 的对比**：
| 维度 | 传统 CPU/GPU | WSE |
|------|--------------|-----|
| Cache 层次 | L1/L2/L3/HBM/DRAM/SSD | 只有 SRAM / DRAM / SSD |
| 数据迁移 | 硬件自动 | 软件显式 |
| 一致性 | 硬件维护 | 软件维护 |
| 带宽 | 逐级 ~10× 衰减 | SRAM→DRAM 200× 衰减 |
| 延迟 | 逐级 ~10× 衰减 | SRAM→DRAM 1000× 衰减 |

**启示**：**WSE 是 dataflow 架构的极致——所有数据搬运都被显式调度**。这对编程模型（CSL/SpaDA）提出了巨大挑战。

### 3. NPU 的存储设计权衡

**Luke 研究的 NPU 核，假设架构**：
```
NPU Chip:
  ├─ 64× PE 阵列 (类似 TPU)
  ├─ 4 MB 片上 SRAM (~10 TB/s)
  ├─ HBM3 (~1 TB/s, 16 GB)
  └─ Host link (~64 GB/s)
```

**I/O 路径的关键问题**：
1. **权重加载**：每次推理开始要把权重从 HBM 搬到 SRAM
   - 16 GB / 10 TB/s = **1.6 ms** (理想)
   - 实际：~5 ms（HBM 带宽受限，DMA 开销）
2. **KV-cache 管理**：LLM 推理时 KV-cache 增长
   - 序列长度 100K × 80 层 × 32 head × 128 dim × 2 bytes = **1.3 GB per sequence**
   - 必须 spill 到 HBM：1.3 GB / 1 TB/s = **1.3 ms**
   - **这正是 Day 19 一致性问题的实际场景**——PE 写 KV-cache 到 HBM 需要 atomic ref count
3. **多 chip 训练**：权重梯度通过 host link 同步
   - 16 GB / 64 GB/s = **250 ms per step**
   - **梯度压缩 / overlap 计算通信是关键**

**对 Luke 研究的启示**：
- NPU 的存储层次设计**直接决定能跑多大的模型**
- 不能简单套用 GPU 方案——NPU 通常没有 large HBM，需要更激进的 SRAM 利用
- **软件管理的存储**（类似 WSE）是趋势，但**对编译器要求极高**

### 4. 一个具体的 NPU 存储优化方向

针对你的研究：

```
优化 1：双缓冲 + 软件预取
  - 推理 step N+1 所需权重，在 step N 计算时后台 DMA 到 SRAM
  - 隐藏 HBM 延迟

优化 2：权重压缩 (稀疏化 + 低精度)
  - 4-bit 量化权重：1.6 ms 加载 → 0.4 ms
  - 2:4 structured sparsity：再减半 → 0.2 ms
  - 总延迟降低 8×

优化 3：异构存储 tier
  - 热权重 (10%) 放 SRAM (10 TB/s)
  - 温权重 (60%) 放 HBM (1 TB/s)
  - 冷权重 (30%) 压缩后放 host DRAM (100 GB/s)
  - profile-driven 自动迁移

优化 4：in-SRAM compute
  - 把 KV-cache 留在 SRAM，永远不 spill 到 HBM
  - 代价：SRAM 容量限制单序列长度
  - 适合：短序列高频推理
```

---

## 🔗 明日预告

**Day 21：互连网络 (Interconnection Networks) — NoC 专题**
- 网络拓扑深度对比：Ring / Mesh / Torus / Fat Tree / Dragonfly
- 路由算法：维序路由（DOR）、自适应路由、死锁避免
- 流控技术：虫孔交换、虚通道、credit-based
- 拓扑评估指标：Bisection Bandwidth、Network Diameter、Node Degree
- **核心论文**：Dally & Towles "Principles and Practices of Interconnection Networks"
- **对你的研究而言**：这是 **Luke 的核心研究领域**！将教材理论与你的 NoC/WSE 知识库深度结合

**承上启下**：今天学了"存储级"的 I/O 系统（外置数据如何到达 CPU）。明天进入"芯片级"的互连网络（数据如何在片上/片间流动）——这是你 NoC 研究的硬件基础。

---

## 💡 今日感悟位

> *存储系统的"带宽悬崖"是体系结构永恒的主题——从 ALU 到 SRAM 到 DRAM 到 SSD，每一层的带宽都断崖式下降。传统 CPU 用 cache hierarchy + hardware prefetch 来掩盖这种悬崖，GPU 用 software-managed cache + 大 HBM 来应对，WSE 用"把所有东西放片上"的暴力美学直接消除悬崖。Luke 的 NPU 研究要选哪个策略？答案是：**根据工作负载的数据复用模式**，**精确设计存储 tier**——既不像 WSE 那么激进（成本太高），也不像传统 CPU 那么被动（性能不够）。这正是 dataflow architecture 的核心价值：把存储层次的"软件可控性"作为 first-class 设计目标。*

---

*Day 20 / 30. 第三阶段（存储篇）第四天。今天你掌握了"存储系统"的完整图景——从 SSD 的 FTL 到 RAID 的写放大，从 NVMe 的 PCIe 带宽到 I/O 路径的延迟分解。下一步是把视野从"片外存储"切换到"片内互连"——NoC 才是你 NoC 研究的真正主战场。*