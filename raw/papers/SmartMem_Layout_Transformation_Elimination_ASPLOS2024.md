---
type: Raw Source
title: 'SmartMem: Layout Transformation Elimination and Adaptation for Efficient DNN Execution on Mobile'
source_path: /home/luke/wiki/raw/papers/SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf
arxiv: '2404.13528'
ingested: 2026-07-22
---

# SmartMem (Source)

**Authors:** Wei Niu, Md Musfiqur Rahman Sanim, Zhihao Shu (U. Georgia), Jiexiong Guan, Xipeng Shen, Miao Yin, Gagan Agrawal, Bin Ren | **Venue:** ASPLOS 2024 | **PDF:** [raw/papers/SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf](SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf)

## Abstract (verbatim)

> "This paper presents SmartMem, a comprehensive framework for eliminating most layout transformations, with the idea that multiple operators can use the same tensor layout through careful choice of layout and implementation of operations."

## Opposite design philosophy from MAERI/SIGMA/FEATHER

- **MAERI/SIGMA/FEATHER**: build **flexible NoC** that **does** layout transformation in hardware
- **SmartMem**: build **smart compiler** that **avoids** layout transformation entirely

## Four operator groups classification

Each operator has a **performance sensitivity to input/output layout**:
- **ILD-Fixed** (Input-Layout-Dependent-Fixed): Transpose, Reshape → **can be eliminated** by static analysis
- **ILD-Variable**: layout affects performance → need careful co-search
- **Customizable**: output layout is flexible
- **ILD-Variable + Customizable**: highest freedom

## Procedure

1. **Classify** all operators into 4 groups
2. **Eliminate** ILD-Fixed operators (Transpose/Reshape disappear)
3. **Co-search** layouts for ILD-Variable + Customizable groups
4. **Map to 2.5D memory** (texture memory common on mobile GPUs)

## Results

- **2.8× average speedup** vs DNNFusion
- **6.9× speedup** vs TVM
- **7.9× speedup** vs MNN
- 18 networks (CNNs, Transformers, LLMs, Stable Diffusion)
- Mobile GPU: Snapdragon 8 Gen 2

## Significance

**Compelling counterpoint** — sometimes the best NoC is one that **never has to do layout conversion** because the compiler already eliminated it. **Direction 2 insight**: a compiler (MLIR) can combine MAERI-style flexible hardware + SmartMem-style smart layout choice.