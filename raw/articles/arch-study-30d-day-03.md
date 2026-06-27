---
type: Raw Source
title: 📰 体系结构晨报 — Day 3
source_path: /home/luke/openclawdata/workspace-research/notes/projects/arch-study-30d/day-03.md
textbook: "Computer Architecture: A Quantitative Approach (6th ed.) / RISC-V Edition"
ingested: 2026-06-24
---

# 📰 体系结构晨报 — Day 3

📅 2026-06-16（Day 3 / 30）
🎯 阶段：基础篇（Day 1-7）
📖 教材：《计算机组成与设计：RISC-V版》Ch.2

---

## 今日主题：指令集原理 + RISC-V 基础

### 🧭 为什么今天学这个？

指令集架构 (ISA) 是软硬件之间唯一的接口。理解 ISA，你才能真正理解处理器在"做什么"。RISC-V 是当今最简洁、最干净的 ISA 设计——用它来学习 ISA 原理再合适不过。对于你的 WSE 研究来说，理解通用 RISC 核与 WSE 的专用 SLA 核的区别，必须先掌握 ISA 的基本概念。

---

## 📖 阅读任务（约 60-90 分钟）

**《计算机组成与设计：RISC-V版》第 2 章：Instructions: Language of the Computer**

### 核心阅读内容：
1. **RISC 设计哲学** — 精简指令集的设计动机和原则
2. **RISC-V 基本指令集 (RV32I)** — 47 条基础整数指令
3. **寄存器组** — x0-x31，32 个通用寄存器
4. **指令编码格式** — R/I/S/B/U/J 五种格式
5. **寻址模式** — 立即数、寄存器、基址+偏移、PC 相对
6. **函数调用约定** — jal/jalr 与调用栈

---

## 🔑 核心概念（必须掌握）

### 1. Load/Store 架构

RISC-V 是 **Load/Store 架构**（又称 Register-Register 架构）：

```
# 内存中的数据不能直接参与运算，必须先加载到寄存器
lw  x5, 0(x10)      # Load: memory[0+x10] → x5
lw  x6, 4(x10)      # Load: memory[4+x10] → x6
add x7, x5, x6      # 运算在寄存器间进行
sw  x7, 8(x10)      # Store: x7 → memory[8+x10]
```

**设计理由**：简化指令编码，所有运算指令只操作寄存器，内存访问只通过专门的 load/store 指令。这使硬件设计大大简化——ALU 不需要关心内存地址计算。

### 2. 寄存器组 (Register File)

| 寄存器 | ABI 名 | 用途 |
|--------|--------|------|
| x0 | zero | 硬连线 0（读出永远为 0，写入无效） |
| x1 | ra | 返回地址 (Return Address) |
| x2 | sp | 栈指针 (Stack Pointer) |
| x5-x7 | t0-t2 | 临时寄存器 |
| x8-x9 | s0/fp, s1 | 保存寄存器 |
| x10-x17 | a0-a7 | 参数/返回值寄存器 |
| x18-x27 | s2-s11 | 保存寄存器 |
| x28-x31 | t3-t6 | 临时寄存器 |

**x0 = 0 是 RISC-V 的天才设计**：很多操作（move、clear、compare with zero）不需要专用指令，只需用 `add x1, x0, x0` 就能清零。

### 3. 指令编码格式

RISC-V 所有指令固定 **32 位**，5 种格式：

```
R-type: [funct7(7)][rs2(5)][rs1(5)][funct3(3)][rd(5)][opcode(7)]
        寄存器-寄存器运算：add, sub, sll, slt, xor, or, and, srl...

I-type: [imm(12)][rs1(5)][funct3(3)][rd(5)][opcode(7)]
        立即数运算 + Load：addi, andi, lw, jalr...

S-type: [imm[11:5](7)][rs2(5)][rs1(5)][funct3(3)][imm[4:0](5)][opcode(7)]
        Store 操作：sw, sh, sb

B-type: [imm[12][10:5](7)][rs2(5)][rs1(5)][funct3(3)][imm[4:1][11](5)][opcode(7)]
        条件分支：beq, bne, blt, bge...

U-type: [imm[31:12](20)][rd(5)][opcode(7)]
        长立即数 + 地址上界：lui, auipc

J-type: [imm[20][10:1][11][19:12](20)][rd(5)][opcode(7)]
        无条件跳转：jal
```

**关键观察**：
- opcode 固定在最低 7 位 [6:0] — 译码器第一时间知道指令类型
- rd 固定在 [11:7]（R/I/U/J 类型中）— 目标寄存器位置一致，简化译码
- rs1 固定在 [19:15]，rs2 固定在 [24:20]（R/S/B 类型中）— 源操作数位置一致

**这种编码一致性不是偶然的**——它是 RISC 设计哲学的体现：降低译码复杂度，提高流水线效率。

### 4. 寻址模式

RISC-V 只有 **5 种寻址模式**（极致精简）：

| 模式 | 语法 | 等价 | 使用场景 |
|------|------|------|----------|
| 立即数 | `addi x1, x2, 10` | x1 = x2 + 10 | 常量运算 |
| 寄存器 | `add x1, x2, x3` | x1 = x2 + x3 | 通用运算 |
| 基址+偏移 | `lw x1, 8(x2)` | x1 = mem[x2+8] | 结构体/数组访问 |
| PC 相对 | `beq x1, x2, label` | if (x1==x2) PC += offset | 分支跳转 |
| 绝对地址（伪） | `la x1, symbol` | lui+addi 组合 | 全局变量 |

**对比 x86**：x86 有超过 20 种寻址模式，如 `[base + index*scale + disp]`（SIB 寻址）。复杂寻址模式增加了硬件译码难度和 CPI。

---

## 🧪 练习题（约 30-60 分钟）

### 基础题

**Q1**：以下 RISC-V 汇编实现什么功能？

```asm
    addi x5, x0, 0      # x5 = 0
    addi x6, x0, 10     # x6 = 10
    addi x7, x0, 1      # x7 = 1
loop:
    beq  x7, x6, done   # if x7 == 10, exit
    add  x5, x5, x7     # x5 += x7
    addi x7, x7, 1      # x7++
    jal  x0, loop       # jump to loop
done:
```
> 答：计算 1+2+3+...+9 = 45。x5 最终 = 45。

**Q2**：以下代码将 C 语句 `a = b + c[4] - d;` 翻译为 RISC-V 汇编，补全缺失部分。假设 a→x10, b→x11, d→x13, c 的基地址→x14。

```asm
    lw   ____, ____(____)    # 加载 c[4]
    add  x10, ____  , ____   # b + c[4]
    sub  x10, ____  , ____   # (b+c[4]) - d
```
> 答：
> ```asm
>     lw   x5, 16(x14)      # c[4]，int 是 4 字节，offset = 4×4 = 16
>     add  x10, x11, x5     # b + c[4]
>     sub  x10, x10, x13    # (b+c[4]) - d
> ```

### 进阶题

**Q3**：手动统计以下程序的指令数 (IC)：

```c
int sum = 0;
for (int i = 0; i < 100; i++) {
    sum += i;
}
```

对应的 RISC-V 汇编（每次循环执行的指令）：
```asm
# 初始化（执行 1 次）
    addi x5, x0, 0      # sum = 0       → IC: 1
    addi x6, x0, 0      # i = 0          → IC: 1
    addi x7, x0, 100    # limit = 100    → IC: 1

# 循环体（执行 100 次）
loop:
    add  x5, x5, x6     # sum += i       → IC: 100
    addi x6, x6, 1      # i++            → IC: 100
    blt  x6, x7, loop   # if i < 100     → IC: 100
```

> 答：总 IC = 3 + 100×3 = **303 条指令**
> 
> 思考：编译器优化能否减少指令数？例如循环展开（unroll）？

### 思考题（与 WSE 研究关联）

**Q4**：WSE 的 SLA (Sparse Linear Algebra) 核心不使用通用 RISC 指令集。从以下角度分析为什么：

1. **面积效率**：一个 64 位 RISC-V 核（含乘法器）约 0.1-0.5 mm²，而 WSE 的 PE 仅约 0.05 mm²。如果用通用 RISC 核，每 wafer 能放多少 PE？
   > 提示：WSE-3 晶圆面积约 46,225 mm²。用 RISC-V 核：~92,000-462,000 PE。用 SLA PE：~900,000 PE。

2. **指令译码开销**：通用 ISA 需要完整的译码器、寄存器堆、流水线控制逻辑。这些在数据流模型中完全是浪费——因为 WSE 的 PE 只做固定的 MAC 运算。

3. **编程模型差异**：RISC-V 面向控制流编程（if/else/loop），WSE 面向数据流编程（CSL/SpaDA）。不同的编程模型需要不同的 ISA。

**核心洞察**：**ISA 的复杂度与微架构的灵活性成正比，与 PE 密度成反比**。通用性是有代价的——在 wafer-scale 场景下，这个代价就是 PE 数量减少一个数量级。

---

## 📝 笔记任务

在 `day-03.md` 中补充：
1. 画出 RISC-V 5 种指令编码格式的位域图
2. 列出 RV32I 47 条指令的分类（算术/访存/分支/系统）
3. 记录你对 Load/Store 架构 vs CISC 内存操作的理解
4. 标注不理解的概念 ❓

---

## 🔗 与 WSE/NoC 研究的关联

| 概念 | 传统处理器 | WSE 的 SLA 核心 | 为什么不同 |
|------|-----------|-----------------|-----------|
| ISA | RV32I / x86 / ARM | 无通用 ISA，数据流驱动 | 面积效率优先 |
| 寄存器堆 | 32×64-bit (~1KB) | 极少寄存器，主要靠本地 SRAM | 减少面积 |
| 指令译码 | 硬件译码器 (复杂) | 无传统译码器，指令通过 NoC 流入 | 简化控制 |
| 寻址模式 | 5-20+ 种 | 线性地址访问本地 SRAM | 去掉不灵活的地址计算 |
| 分支/循环 | 分支指令 + 硬件预测 | 无分支（数据流条件控制） | 消除控制冒险 |

**今天学完 RISC-V 之后**，你应该理解为什么 WSE **故意不用**通用 ISA：面积预算全部给了算术单元和片上 SRAM。这是领域专用架构 (DSA) 的核心权衡——**放弃通用性换取极端的计算密度**。

---

## 🔗 明日预告

**Day 4：指令集进阶 + ISA 对比**
- CISC vs RISC 之争的历史教训
- x86、ARM、RISC-V、MIPS 四大 ISA 横向对比
- 指令格式设计的深层权衡
- 为 WSE 设计专用 ISA 应该长什么样？

---

## 💡 今日感悟位

> 留给你写一句话总结今天的收获。

---

*Day 3 / 30 — 理解 ISA 是理解一切处理器设计的钥匙。*
