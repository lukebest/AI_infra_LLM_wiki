---
type: Raw Source
title: "TileDRAM: Compiler-Controlled Tile-to-DRAM Layouts for 3D DRAM GPGPUs"
source_url: https://arxiv.org/abs/2610.23767
pdf: TileDRAM_Tile_to_DRAM_Layouts_3D_DRAM_GPGPU_2026.pdf
retrieved: 2026-10-20
org: ShanghaiTech University / MetaX Integrated Circuits (Shanghai)
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.23767)

Modern GPU compilers expose rich layout abstractions for mapping tensors to threads and on-chip resources, but compute-unit-local (CU-local) 3D DRAM architectures lack a corresponding abstraction for specifying how operand-tile data are
arranged within the DRAM address space. Without such an abstraction, conventional placement under the existing DRAM address mapping can subject structured tile accesses to severe row-buffer conflicts. We present TileDRAM, a compiler-runtime
toolchain that introduces tile-to-DRAM layouts as a compiler-visible abstraction for DRAM placement. TileDRAM extends the GPU Linear Layout abstraction from compute-side mapping targets to DRAM placement coordinates and selects layouts per
tile access signature, using recurring tile-local access behavior as the specialization unit. Since row-buffer locality depends on ordered request history, TileDRAM evaluates candidate layouts through their row-buffer behavior under fixed
DRAM address mappings. Accesses under the selected layouts are realized through ordinary address arithmetic, without new address-remapping hardware or ISA support. In full-trace replay on Accel-Sim/Ramulator2 across 108 mixture-of-experts
(MoE) feed-forward network (FFN) cases, TileDRAM reduces the request-weighted row-conflict rate from 75.7% to 15.2% and achieves a 1.77x geomean speedup. Retargeting six traces to six 3D DRAM organizations yields a 2.20x geomean speedup
under the same compiler abstraction. On an RTX 3090, address transformation adds 0.17% geomean overhead over identity.

# Excerpts (from arXiv PDF v1)

- "Stratum reports 19.01–30.34 TB/s of internal bandwidth across its memory tiers [38]. Exporting a stack through an HBM-style package interface instead offers roughly 0.8–1.2 TB/s per stack in HBM3/HBM3E [11, 46], making the package-level endpoint 16–38× narrower than the modeled internal path."
- "In the CU-local organization modeled here, the vertically integrated DRAM structure is connected to a separate logic die through face-to-face Cu–Cu hybrid bonding"
- "Stratum's reported 19.01–30.34 TB/s aggregate in-stack bandwidth [38] and the H100 whole-GPU peak [34] together give a local-memory ridge reference of 32.6–52.0 FLOP/B."
- "Retargeting to six 3D DRAM organizations, TileDRAM reduces row conflicts by 79.2% and achieves a 2.20× geomean speedup."
