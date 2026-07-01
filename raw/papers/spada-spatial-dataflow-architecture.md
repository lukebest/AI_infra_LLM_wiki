---
type: Raw Source
title: SpaDA Spatial Dataflow Architecture Programming Language
source_path: /home/luke/snap/zotero-snap/common/Zotero/storage/RV4TLWPR/Gianinazzi 等 - 2026 - SpaDA a spatial dataflow architecture programming language.pdf
arxiv: '2511.09447'
ingested: 2026-06-24
sha256: 8331414fb74f81f85b5b84ed6e586cf236db49a181cc95e44ccfef2a228e858e
---

# SpaDA: A Spatial Dataflow Architecture Programming Language

**Authors:** Lukas Gianinazzi, Tal Ben-Nun, Torsten Hoefler  
**Affiliations:** Noeda Research; Lawrence Livermore National Laboratory; ETH Zurich  
**PDF:** [SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf](SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf)  
**arXiv:** 2511.09447v2 (Apr 2026) | **Code:** https://github.com/spcl/spada/

## 问题

WSE 等 SDA：无 cache hierarchy、无共享内存；电路交换 NoC + 有限 color/task ID + DSD 向量化 → CSL 学习曲线陡、代码膨胀严重。

## 语言

- **place**：PE 子网格数据布局
- **dataflow**：`relative_stream(dx,dy)` 通信管道
- **compute**：async/await、`foreach` over streams、`map` 向量化作用域
- **phase** + meta-for：结构化多 stage 异步（tree reduce 等）

## 编译管线

GT4Py Stencil IR → SpaDA → Canonicalization → Checkerboard routing → Task DAG (fusion/recycling) → DSD codegen → CSL + layout

关键 pass：checkerboard color 分配、task fusion/recycling、copy elimination、自动 DSD 向量化。

## 结果（WSE-2, SDK 1.4.0）

- 代码：SpaDA vs CSL **4.68–13.13×** 更少；harmonic mean **14.09×**；GT4Py Laplacian **616×**
- Collectives vs HPDC'24 CSL：**1.04×**（harmonic mean）
- Stencil UVBKE：**>260 TFlop/s**（~730K PE）
- GEMV vs CUBLAS A100：**82.9×**
