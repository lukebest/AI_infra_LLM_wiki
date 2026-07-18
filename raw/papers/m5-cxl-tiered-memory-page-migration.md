---
type: Raw Source
title: 'M5: Mastering Page Migration and Memory Management for CXL-based Tiered Memory Systems'
source_path: /home/luke/wiki/raw/papers/M5_CXL_Tiered_Memory_Page_Migration_2025.pdf
doi: '10.1145/3676641.3711999'
zotero: 2NAEEBA8
ingested: 2026-07-17
sha256: cc17c5fdbe69bbb6539acf798423579265cc752f21a65848d68470720e911cd7
---

# M5: Mastering Page Migration and Memory Management for CXL-based Tiered Memory Systems

Authors: Yan Sun, Jongyul Kim, Zeduo Yu, Jiyuan Zhang, et al. (UIUC, SNU, Intel Labs)
Venue: ASPLOS 2025 | DOI: 10.1145/3676641.3711999

Structured notes / key excerpts:

- **Context**: CXL DRAM 2–3× 慢于 DDR，形成 tiered memory；需高效 page migration。CXL 控制器第三方集成带来 near-memory profiling 机会。
- **Contribution 1 — PAC/WAC**: FPGA CXL 设备上 Page/Word Access Counter，透明统计每 4KB page / 64B word 访问次数。
- **Contribution 2 — CPU-driven 有害**: ANB/DAMON 等把 warm page 当 hot（访问次数仅为 PAC 真 hot 的 21%/29%）；86% Redis 页仅 16/64 words 被访问（sparse page）；错误迁移导致 cache pollution 和性能下降。
- **Contribution 3 — M5 platform**: Hot-Page Tracker (HPT) + Hot-Word Tracker (HWT) + M5-manager 软件接口；CXL 控制器内硬件追踪，CPU 侧只做策略。
- **Results**: 平均识别 **47%** 更热页面；比最佳 CPU 方案 **+14%** 性能；比 ANB **+20%**、比 DAMON **+14%**（内存密集型应用，简单策略）。
- **Background**: CXL 5.0 带宽可比 DDR5 但 pin 数 3× 少；访问延迟 +140–170 ns vs DDR。
