---
type: Paper
title: "LizTail: Segment-Reconfigurable Systolic Arrays"
description: "UESTC — 128×128 切成 32 个 128×4 段，端点 180° 回折实现裁剪/拉长/分布式；LLM decode 几何均值 25.67× vs TPU-like，CNN 5.02×，EDP 最高降 38.23×"
tags:
- accelerator
- tpu
- dataflow
- inference
- decode
- llm
- architecture
- hardware
created: 2026-10-16
updated: 2026-10-16
timestamp: '2026-10-16T00:00:00Z'
paper_author: [Gang Liu, Chen Yang, Junyan Hu, Jianguo Chen, Lixin Duan]
year: 2026
arxiv: '2610.16159'
sources:
  - raw/papers/LizTail_Segment_Reconfigurable_Systolic_Arrays_2026.pdf
  - raw/papers/liztail-segment-reconfigurable-systolic-arrays.md
---

# LizTail：分段可重构脉动阵列

## 一句话结论
固定 128×128 脉动阵列在 skinny GEMM / 小批 LLM decode 上 PE 利用率极低。LizTail 把阵列切成 32 个 128×4 段，只在预定义端点加 180° 回折与入口缓冲，用裁剪（T）、拉长（E）、分布式并行（P，各子阵列还可本地裁剪/拉长）覆盖形状适配与空间并行，避免全 PE 级任意互连。

## 动机（论文数字）
- LLM 小批 decode 里 skinny GEMM/GEMV 占比远高于 CNN 与 prefill；固定阵列要么大量 PE 空闲，要么反复空间折叠。
- 等 PE 预算下，固定 / 拉长 / 多子阵列在不同 GEMM 形状上各有优势；例如 GPT-2 XL QKV (1,4800,1600) 沿 N 四分到四个 32×128，比单一 32×512 拉长阵列少 **17.9%** 周期。
- 任意 PE 级路由（如全双向交叉）面积与数据通路代价高；有用映射集中在：原生/裁剪、拉长路径、独立子阵列、子阵列内再适配。

## 方案
| 部件 | 做法 |
|---|---|
| 段 | 128×128 → 32×(128×4)；段内保持常规邻接脉动 |
| T-Mode | 激活连续 S 段形成 128×4S（可转置），关掉其余 |
| E-Mode | 端点 180° turn-back 串段，逻辑边长可超过物理边长 |
| P-Mode | 2–32 个子阵列；M/N 输出划分或 K 规约划分；子阵列可 P-Native / P-Trim / P-Extended |
| 数据 | CEB 边界投递 + SIB 段入口注入；区分 PE1–PE4 路由变体 |
| Mapper | 硬件约束先剪候选，再搜 dataflow / tile / 循环序；目标默认 EDP |

## 效果（仅论文数字；SCALE-Sim-v3 + 28 nm RTL）
- vs TPU-like：**LLM decode 几何均值 25.67×**（GPT-2 XL **27.39×**、LLaMA3 8B **27.04×**、Qwen3-30B-A3B **22.58×**）；**CNN 几何均值 5.02×**（ResNet-50 2.60×、MobileNetV3-L 8.74×、EfficientNet-B0 3.70×）。
- vs 已能拉长的 ReDas：三款 LLM 再快 **3.14× / 2.72× / 3.07×**。
- EDP vs TPU-like：CNN 降 **3.13–11.43×**；LLM 降 **38.23× / 37.50× / 31.37×**。
- ADP vs TPU-like（LLM）：**10.67–12.94×**。
- 面积：LizTail **31.7 mm²**（TPU-like 15.5、ReDas 20.8、SARA 77.3）。
- 默认：700 MHz、CEB/SIB 各 2 MB、片外 819 GB/s；bs=1→32 时加速比 **25.57×→7.86×**。

## 与 wiki 的关系
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 与 DynaCore/ReDas/SARA 同属可重构脉动；LizTail 强调「拉长 + 分布式」可组合
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — 收益集中在小批 decode 的 skinny 形状
- [DynaCore](/papers/dynacore-shape-adaptive-disaggregated-quantization.md) — 另一条形状自适应脉动路径（MEU 非对称重塑 + 量化分离）

## 局限
- 主评测是 decode（bs=1, ctx=1K）；大批与超长上下文加速比收窄，长上下文仍受 KV/带宽限制。
- 性能来自仿真 + 成本模型，面积/功耗来自 28 nm 综合。

# Citations
- Liu et al., "LizTail: Unifying Shape Adaptation and Spatial Parallelism with Segment-Reconfigurable Systolic Arrays", arXiv:2610.16159. [raw](/raw/papers/liztail-segment-reconfigurable-systolic-arrays.md) · [PDF](/raw/papers/LizTail_Segment_Reconfigurable_Systolic_Arrays_2026.pdf)
