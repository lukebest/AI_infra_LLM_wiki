---
type: Concept
title: In-Core Nonlinear Operator Acceleration
description: 核内非线性运算加速：softmax、GELU/SiLU、LayerNorm/RMSNorm 与 exp/除法/rsqrt 单元在 GPU/NPU/FPGA 上的实现路线（融合在线算法、专用归约单元、快速内建指令、量化后多阈值比较）与 wiki 内已有案例索引
tags:
- nonlinear
- activation
- accelerator
- gpu
- fpga
- kernel
- quantization
- attention
- hardware
created: 2026-10-19
updated: 2026-10-29
timestamp: '2026-10-19T00:00:00Z'
sources:
  - raw/papers/multi-threshold-non-monotonic-activations-finn.md
  - raw/papers/meta-amd-mi350x-training-codesign.md
  - raw/papers/fuselse-intlse-logsumexp-neurips2026.md
---

# 核内非线性运算加速

## 定义与范围
GEMM 之外、按元素或按行执行的非线性算子：softmax（exp + 行归约 + 除法）、GELU/SiLU（含 tanh/sigmoid）、LayerNorm/RMSNorm（均值/方差归约 + rsqrt），以及支撑它们的 exp、倒数/除法、rsqrt 运算单元。矩阵单元越来越快、格式越来越低比特时，这些算子的占比和延迟会被放大。

## 实现路线

| 路线 | 思路 | wiki 案例 |
|---|---|---|
| 融合 + 在线算法 | 把 softmax 留在片上 SRAM，与 GEMM 流水重叠（running max / exp sum 重标定） | [FlashAttention](/concepts/flashattention.md)、[FlashAttention-3](/concepts/flashattention-3.md)（GEMM–softmax 2-stage 流水）、[WMHA](/papers/world-model-hardware-accelerator-wmha.md)（单遍 online-softmax） |
| 专用行归约单元 | 在加速器 PE 旁加水平归约，服务 LayerNorm/SoftMax/RMSNorm | [HC2026 Meta MTIA 400](/papers/hc2026-meta-mtia-400.md) |
| 稀疏化下游 | 注意力分数稀疏后加快 softmax 与第二个 BMM | [HC2026 NVIDIA Rubin](/papers/hc2026-nvidia-rubin.md)（「2x faster downstream SoftMax and BMM2」） |
| 快速内建指令 | 选能映射单条硬件指令的近似公式 | [Meta × AMD MI350X](/papers/meta-amd-mi350x-training-codesign.md)：GeLU 改走 sigmoid 形式 + `fast_expf`/`fast_dividef`，`tl.rsqrt()` 替代库调用 |
| 量化后多阈值比较 | 低比特下把激活+scale+bias 折成阈值表，硬件只做比较/二分搜索 | [Multi-Threshold 非单调激活](/papers/multi-threshold-non-monotonic-activations-finn.md)（SiLU 用 Lambert W 求阈值；非单调只多几百 LUT） |
| 跨 CTA 归约 | 行归约跨 CTA 借 DSMEM 完成 | [Credit DSMEM](/papers/credit-dsmem-inter-cta-tiling.md)（LayerNorm、softmax-logits backward 等） |
| 绕开 softmax | 线性注意力族改写 attention，减少 exp/归一化 | [Linear Attention Evolution](/concepts/linear-attention-evolution.md) |
| 独立 LSE 原语融合 / 整数近似 | 不绑在 attention 内的 `logsumexp`：单遍融合降 HBM；无 SFU 平台改整数近似 | [FuseLSE / IntLSE](/papers/fuselse-intlse-logsumexp-neurips2026.md)（GPU ~6–11×，CPU IntLSE 再 3–6×） |

## 当前认知
- GPU 上的主要手段在 kernel 层：融合、减少 HBM 往返、挑选硬件友好的近似式；同一近似在不同厂商上展开方式不同（tanh 在 AMD 上展开成 2σ(2x)−1）。
- 专用 ASIC/NPU 倾向在矩阵阵列旁加归约/特殊函数单元；FPGA 数据流架构在低比特下可把整条激活数据通路做成比较器（几百 LUT 量级）。
- 精度契约要跟着格式走：MX/NVFP4 等块缩放格式让「scale 折叠进阈值/归约」成为可行的融合点（参见 [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md)）。

## 案例补充（2026-10-22）
- [M3D-FLOW](/papers/m3d-flow-monolithic-3d-pnm-normalizing-flow.md)：近存 PE 内独立 Non-Linear Engine，exp/GeLU/ln/倒数做单周期 LUT，softmax 由 exp LUT → 归约树 → 倒数 LUT → 缩放串起来在 NLE 内完成，中间值不回流乘法阵列[6]。

## 开放问题
- 高比特（≥8 bit）激活下，多阈值、分段多项式、查表三种实现的面积/精度交叉点。
- LLM decode 小 batch 下 RMSNorm/softmax 的行归约延迟如何与 GEMV 重叠；专用归约单元与 SIMT 软件路径的分界。
- 训练反向中的非线性（softmax backward、norm backward）对专用单元的需求尚少有硬件论文量化。

## 相关页面
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — SFU/特殊函数与 occupancy
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 阵列外的后处理单元
- [FP4 QAT](/concepts/fp4-qat.md) — 低比特训练对激活路径的影响

## 案例补充（2026-10-26）
- [FlashAttention 长向量重排](/papers/flashattention-long-vector-riscv.md)：EPAC RISC-V 长向量核没有硬件 exp，softmax 占 FlashAttention **38%** cycle；软件多项式系数挤占向量寄存器导致溢出，挪到标量寄存器后 softmax 向量访存指令 **−78.7%**；转置分数块后行最大值/行和两处归约消失，整核 cycle 降 **1.84–2.08×**[7]。


## 案例补充（2026-10-29）
- [FuseLSE / IntLSE](/papers/fuselse-intlse-logsumexp-neurips2026.md)：针对独立 `torch.logsumexp`（九子 kernel、~**6×** HBM 往返）。GPU 上融合把流量压到约 **1×**，相对 PyTorch 小/大负载约 **10–11× / 6×**；CPU 上 IntLSE 整数近似再比 FuseLSE **3–6×**（粒子滤波 vs torch **2.8–5.2×**）[8]。

# Citations
[1] [raw/papers/multi-threshold-non-monotonic-activations-finn.md](/raw/papers/multi-threshold-non-monotonic-activations-finn.md) — Berganski et al., arXiv:2610.21825
[2] [raw/papers/meta-amd-mi350x-training-codesign.md](/raw/papers/meta-amd-mi350x-training-codesign.md) — Zhang et al., MICRO'26, arXiv:2610.22230
[3] [papers/hc2026-meta-mtia-400.md](/papers/hc2026-meta-mtia-400.md) — MTIA 400 水平归约
[4] [papers/hc2026-nvidia-rubin.md](/papers/hc2026-nvidia-rubin.md) — Rubin 稀疏注意力下游 SoftMax
[5] [concepts/flashattention.md](/concepts/flashattention.md) — online softmax
[6] [raw/papers/m3d-flow-monolithic-3d-pnm-normalizing-flow.md](/raw/papers/m3d-flow-monolithic-3d-pnm-normalizing-flow.md) — Magar et al., arXiv:2610.27371
[7] [raw/papers/flashattention-long-vector-riscv.md](/raw/papers/flashattention-long-vector-riscv.md) — Irabor & Casas, arXiv:2610.29489
[8] [raw/papers/fuselse-intlse-logsumexp-neurips2026.md](/raw/papers/fuselse-intlse-logsumexp-neurips2026.md) — Yao et al., NeurIPS 2026, arXiv:2610.33647
