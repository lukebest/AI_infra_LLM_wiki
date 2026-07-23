---
type: Summary
title: 'SmartMem: Layout Transformation Elimination and Adaptation for Efficient DNN Execution on Mobile'
description: ASPLOS 2024 反向思路：编译期把 layout transformation 消除掉（不靠灵活 NoC）；4 类算子分类 + 2.5D 内存；2.8× vs DNNFusion、6.9× vs TVM、7.9× vs MNN
tags:
- compiler
- layout
- transformation
- mobile
- dnn
- asplos
- compiler-optimization
timestamp: '2026-07-22T00:00:00Z'
created: 2026-07-22
sources:
- raw/papers/SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf
---

# SmartMem

**Authors:** Wei Niu, Md Musfiqur Rahman Sanim, Zhihao Shu (U. Georgia), Jiexiong Guan, Xipeng Shen, Miao Yin, Gagan Agrawal, Bin Ren | **Venue:** ASPLOS 2024 | **PDF:** [raw/papers/SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf](SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf)

## 一句话总结

**SmartMem** 跟 MAERI / FEATHER 思路**完全相反**：与其让 NoC 能做 layout 转换，**不如让编译器把 layout 转换彻底消除掉**。把算子分成 4 类，**ILD-Fixed 的 Transpose / Reshape 直接消失**；其余 co-search 选 layout。vs DNNFusion 2.8×、vs TVM 6.9×、vs MNN 7.9×。

## 反向哲学

| | MAERI / FEATHER 路线 | SmartMem 路线 |
|---|---------------------|---------------|
| **应对 layout mismatch** | 让硬件 (NoC / reorder network) 兜底 | **让编译器把问题消灭在源头** |
| **layout 转换开销** | 显式 RAR 仍在（FEATHER 用 RIR 消除 critical path） | **零开销**（直接消除 Transpose / Reshape）|
| **硬件要求** | 柔性 interconnect、buffer 重排 | 标准 2.5D 内存即可 |
| **代价** | 硬件面积 + 编译期 mapping | **编译期 layout search** |

## 4 类算子

| 类别 | 含义 | 例子 |
|------|------|------|
| **ILD-Fixed (Input-Layout-Dependent-Fixed)** | 输出 layout 写死，无法调 | **Transpose / Reshape** |
| **ILD-Variable** | 输入 layout 影响性能 | 某些 conv 实现 |
| **Customizable** | 输出 layout 自由 | 普通 GEMM 输出 |
| **ILD-Variable + Customizable** | 最大自由 | 灵活 GEMM |

**关键洞察**：Transpose 和 Reshape 都是 ILD-Fixed → **它们的存在就是 layout mismatch 的表现** → **编译器可以直接消除它们**。

## 算法

1. **分类**：所有算子划入 4 类
2. **消除**：ILD-Fixed 的 Transpose / Reshape 节点直接从图中删除
3. **Co-search**：剩余算子搜索最优 layout
4. **映射到 2.5D 内存**：texture memory 友好 layout

## 数字

- **2.8× speedup** vs DNNFusion (SOTA mobile DNN compiler)
- **6.9× speedup** vs TVM
- **7.9× speedup** vs MNN
- 18 networks：CNN、Transformer（Swin, ViT）、LLM、Stable Diffusion
- Mobile GPU：**Snapdragon 8 Gen 2**

## 与 Direction 2 的关系

**绝妙的对照实验**：
- **MAERI 路线**：硬件 = 柔性 NoC，编译器 = 把 model 映射进 fabric
- **SmartMem 路线**：硬件 = 标准 GPU，编译器 = **消灭 layout 问题**
- **Direction 2 的统一视角**：MLIR 编译器**同时**做这两件事 —— **能消除的消除，必须转换的就交给硬件 RIR**

```
MLIR Pipeline:
  Op 1 (Conv) → Op 2 (Transpose) → Op 3 (Conv)
  ↓
  SmartMem: 删除 Op 2 → Op 1 → Op 3 with new layout
  或
  FEATHER 模式: Op 1 → Op 2 (RIR reorder in reduction) → Op 3
```

## 与 wiki 已有内容的关联

- [FEATHER Accelerator](/concepts/feather-accelerator.md) — 反向哲学对比
- [MAERI (paper summary)](/papers/maeri-flexible-dataflow-reconfigurable-interconnects.md) — 反向哲学对比
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — MLIR compiler 视角的现代 work
- [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md) — Direction 2 入口

# Citations

[1] [raw/papers/SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf](SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf) — Niu et al. ASPLOS 2024