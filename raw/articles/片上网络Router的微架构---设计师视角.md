---
title: "片上网络Router的微架构---设计师视角"
source: "https://zhuanlan.zhihu.com/p/1998888912119174831?utm_psn=1999771185517446570"
author:
  - "[[ppo丶nAI芯片设计]]"
published:
created: 2026-05-14
description: "Router是现代NoC设计中的核心组件，直接影响了NoC的性能和带宽利用率，如何设计高性能低成本的Router一直是NoC设计的重要部分。本书是为数不多的真正从设计者视角详细介绍Router设计方法的书籍，由浅入深，且全面…"
tags:
  - "clippings"
---
[收录于 · 互连网络](https://www.zhihu.com/column/c_1998891634851606642)

150 人赞同了该文章

目录

收起

1\. NoC设计介绍

1.1 物理媒介

1.2 流控

1.3 读写事务

1.4 网络上的传输：传输层

1.5 合在一起

2\. 链路级流控和buffer

2.1 Elastic buffer

2.2 通用的FIFO队列

2.3 抽象流控模型

2.4 Credit-based流控

2.5 流水线数据传输

2.6 req-ack握手和bufferless流控

2.7 宽消息传输

3\. 基准Switch模块和Router

3.1 多输入连接到一个输出

3.2 反向连接：拆分一个源到多个接收侧

3.3 使用简化的逻辑将交换路径将多个输入连接到多个输出

3.4 使用unroll交换datapath将多个输入连接到多个输出

3.5 头阻

3.6 网络中的Router：路由计算

3.7 层次化Switch

4\. 仲裁逻辑

4.1 固定优先级仲裁

4.2 Round-Robin仲裁

4.3 具有2D优先级状态的仲裁器

5\. 流水线的Wormhole Router

5.1 单周期Router组织概述

5.2 流水线阶段的RC

5.2.1 RC流水线截断的无空闲cycle操作

5.3 流水线阶段的Switch Allocation

5.4 具有RC和SA流水线阶段的流水线Router

6\. VC流控和缓冲

6.1 虚拟通道流控的操作

6.2 VC buffer

6.3 buffer 共享

6.4 流水线链路中的VC流控

7\. 基本的携带VC的switch模块和router

7.1 带VC的多to一连接

7.2 使用unroll datapath的多to多连接：一个完整的VC-based Router

7.3 使用中心化分配器构建的VA和SA

8\. VC-based router中的高速分配器

8.1 虚拟网络：降低VA的复杂度

8.2 超前VA1

8.3 没有VA2的VA：组合分配器

8.4 预测SA

8.5 具有input-speedup的VC-based router

9\. 流水线VC-based router

9.1 单周期VC-based router组织的review

9.2 流水线阶段的RC

9.3 流水线阶段的VA

9.4 流水线阶段的SA

9.5 VC-based多级流水线router

Router是现代 [NoC](https://zhida.zhihu.com/search?content_id=269555697&content_type=Article&match_order=1&q=NoC&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Nzg5MjAxMDEsInEiOiJOb0MiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNjk1NTU2OTcsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.cloLEWg-22wPJSrInnzP0eky2X-virdhKcMbN1xmDgI&zhida_source=entity) 设计中的核心组件，直接影响了NoC的性能和带宽利用率，如何设计高性能低成本的Router一直是NoC设计的重要部分。本书是为数不多的真正从设计者视角详细介绍Router设计方法的书籍，由浅入深，且全面的介绍了Router的基本概念：路由、 [流控](https://zhida.zhihu.com/search?content_id=269555697&content_type=Article&match_order=1&q=%E6%B5%81%E6%8E%A7&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Nzg5MjAxMDEsInEiOiLmtYHmjqciLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNjk1NTU2OTcsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.yg9a_bnSutdNzsBFmVbIrmhIIwG_YkpGG_XhbV7njwg&zhida_source=entity) 、仲裁，并给出了Router设计的电路级、cycle级结构描述，特别的，这本书花费大量篇幅介对流控/VC进行了详尽的介绍。

## 1\. NoC设计介绍

将通信网络技术应用在片上以解决晶体管密度增加带来的节点数增多、异构程度复杂的问题已经被证明是一个可行办法，但研究如何适应新的架构，并以最小的功耗和面积开销来提供最大性能、QoS和动态的自适应性仍是一个需要持续探索的课题。

### 1.1 物理媒介

设计者在物理层面可以直接使用的是晶体管和wire，适当的使用它们就可以构造出复杂电路。片上导线如下图1.1所示，被组织在多个金属层中实现用于连接两个点。

![](https://pica.zhimg.com/v2-88bd71da49f2fc0d41809953e3f101fe_1440w.jpg)

第一层金属主要为local连接量身定做，并针对数百um的片上连接进行了优化，可以提供高密度的连接。高层金属具有更大的横截面，可以提供更低的电阻，并允许以更低延时传输更长距离，同样的其密度也比较低。

技术演进也为设计者提供了更多的可能性，如下图1.2所示，2.5D/3D封装提供了额外的跨chip且具有良好特性的tsv导线。

![](https://pica.zhimg.com/v2-9ed3ea399171b4793af9592ccee70dfe_1440w.jpg)

目前主流还是基于wire的电路信号传输，但是目前也有一些研究基于片上光互联的技术。

### 1.2 流控

系统层面，发送方和接收方只使用数据传输是不够的，还需要一些sideband信号表示数据的是否有效和接收方的接收能力，这些sideband信号分为forward和backward传输，共同构成了流控机制。具体如下图1.3所示。

![](https://pic2.zhimg.com/v2-03761400bd8d3a6e3ea17d0c3ba0fc3d_1440w.jpg)

单根wire范围的流控机制通常称为链路级流控，进一步将其拓展到任意源和目的之间的流控可以称之为端到端流控。链路级流控很好实现，而端到端流控实现较难，需要一些显式或隐式的机制：

- 显式实现需要不同目的地通过wire来显式反馈其状态
- 隐式实现可以在任意源和目的节点间通过传输的正常或特殊message来传递得知另一方的状态

流控策略的本质是要知道另一端的buffer占用情况，因此不同流控协议的不同语义会对buffer方案的实现有不同约束。

任意点对点连线传输什么样的message是取决于应用程序的，而跟wire无关，因此通常message的粒度和实际物理wire的实现粒度是不同的，所以具体channel的位宽选择需要综合考虑应用级到物理实现级的限制。

因为message和wire的粒度不匹配，所以可能需要串行成多个word的形式在wire上传输，所以流控机制也需要考虑channel上分配buffer的粒度：

- 粗粒度流控可能将每个message/packet当做一个整体
- 细粒度流控可能将sub-message当做一个整体

### 1.3 读写事务

除了点对点通信外，chip上还会有多个IP核之间还需要相互通信，其通常使用广泛接受的标准协议来实现读写事务，如AMBA AXI或OCP-IP，下图1.4展示了AXI协议示意。

![](https://pic1.zhimg.com/v2-41ea74024c9e8c65e79bb327211b5e3c_1440w.jpg)

Transaction层通信只定义端到端的操作，不应该对如何实现做约束

### 1.4 网络上的传输：传输层

直接在接口链路上支持事务层读写事务是容易过设计的，会造成大量布线资源。所以通常是用封装的原则，将事务层信息封装到传输层的接口发送到网络，每个packet中就会包含header和payload字段。

1.4.1 网络接口

在NoC外围通常会有NI(network interfaces)来执行事务层和传输层的转换，其上游连接特定IP，需要呈现给IP特定的传输层语义要求，同时负责向网络中收发数据。

下图1.5展示了一个NI的例子，通常使用request和response分离的做法来避免依赖并避免死锁。具体的，这种分离还可以体现在时间/空间上：

- 时间上的体现即VC，可以分时复用同一物理线
- 物理上的体现就是直接使用不同的不同物理线
![](https://pic3.zhimg.com/v2-a06b30333ecb822b9b9c6fc15d84f610_1440w.jpg)

1.4.2 网络：物理层

网络中的两个关键问题是连接性和竞争：

- 连接性意味着两个连接到网络的IP core可以交换信息
- 竞争意味着存在连接性的多条链路具有共享channel
- 处理竞争需要物理层特定的仲裁、mux和buffer
	- 如下图1.6所示，即使有多个NI接口都可以到达RAM，但是因为共享链路原因，每个cycle只有一个packet被服务
![](https://pic1.zhimg.com/v2-546d5e01613deb1bdaeb8e77cb7c8cca_1440w.jpg)

### 1.5 合在一起

下图1.7展示了一个例子，CPU期望与chip上另一侧的memory共享数据：

1. NI将读事务打包，包括地址和控制信息
2. 每一级router解析packet以识别需要去下一条哪个通路
3. slave侧NI解析收到的包，转成对memory的读事务
4. 之后slave NI发起响应包
![](https://pic2.zhimg.com/v2-946cd58f0b4ce5c8e3c67eaf1f2b1ec5_1440w.jpg)

对应的完整的协议层转换如下图1.8，这种分层设计最大的好处是可以允许每一层不同的实现之间可以共存，每一层的独立更新并不影响其他层。

![](https://pic1.zhimg.com/v2-4bfe95f7ef4c4395ed90b9e539acc38a_1440w.jpg)

## 2\. 链路级流控和buffer

下图2.1展示了一个基于valid/ready握手协议的流控机制及对应的时序图，valid/ready信号的不同组合对应了链路的不同状态：

- Transfer: when valid = 1 and ready = 1
- Idle: when valid = 0
- Wait: when valid = 1 and ready = 0
![](https://pic1.zhimg.com/v2-bf7a3f0cb3ebcce6e90776989b46e90a_1440w.jpg)

### 2.1 Elastic buffer

valid/ready握手机制允许接收方和发送方都可以随时停止数据传输，所以两侧也都需要使用buffer来保持处于stall状态的数据。

Elastic buffer是实现valid/ready握手buffer的最直接方式，如下图2.2所示。

![](https://pic2.zhimg.com/v2-34614eccfcc81993f9f2c85967261297_1440w.jpg)

抽象层次看，EB可以使用FIFO来构建，其结构图如下图2.3。

![](https://pic3.zhimg.com/v2-57e75bb104037fa07d80b4877ac01e74_1440w.jpg)

2.1.1 半带宽Elastic Buffer

基于上边的抽象表示，可以实现任意大小的EB，最简单的是只是用一个寄存器，并使用一个RS触发器来表示空满状态。其对应的VHDL描述和电路结构如下图2.4所示。

![](https://pic4.zhimg.com/v2-e681bad9c7997b31a11625ce74fb852d_1440w.jpg)

这样的设计允许每一拍执行push或者pop操作，所以对应的连续传输也会引入气泡，所以称其为半带宽EB(HBEB)，具体一个运行的示例如下图2.5所示。

![](https://picx.zhimg.com/v2-768089341494fe2e84fd0127ba3b99b7_1440w.jpg)

2.1.2 半带宽2-slot EB

上边HBEB对带宽的限制可以通过在时分复用的方式实现，如下图2.6所示。

![](https://picx.zhimg.com/v2-0488a7e453df74d3ad91c94f4d5fb399_1440w.jpg)

这样即可提供全带宽无气泡传输，并且隔离了上下游valid/ready握手时序，对应的传输描述如下图2.7。

![](https://pic3.zhimg.com/v2-a1f9c9a470e3f8295edf65af102f5546_1440w.jpg)

2.1.3 另一种全带宽EB

除了使用上边2-slot来实现全带宽外，还可以通过通过扩展1-slot设计来达到类似效果（同时需要吞吐量-时序的trade-off）：

- 当buffer为空时可以写入（和HBEB一样）
- 或者同cycle会变成empty时也可以写入（full状态同时当拍也会出数时）

上述设计也称之为PEB(pipelined EB)（在写端口提供更多并行性），结构如下图2.8所示，但是这引入了直接的ready\_in到ready\_out的组合环路。

![](https://pic4.zhimg.com/v2-4d9ef2871510086212999f485ff597e7_1440w.jpg)

还有另一种方法，称之为BEB(bypass EB)，其在读端口提供更多并行性。此时，在buffer中没有数据的时候也可以向外传递数据（假设同拍又enqueue操作），其电路结构如下图2.9。对应的这会引入data的bypass组合逻辑。

![](https://picx.zhimg.com/v2-bec1d5e761097ba3cd59932f7794b36b_1440w.jpg)

### 2.2 通用的FIFO队列

除了上述流控外，还有一个需要考虑的关键问题是在接收方stall前如何保持尽可能的让发送方保持busy状态，一个显然的方案是使用更深的FIFO，其可以在接收方stall之后让发送方额外工作一段时间。

实际上，这样FIFO的作用就是可以吸收bursty类型的输入流量并有效的增加整体带宽。类似的，也可以使用如下图2.10所示的多级并行HBEB来实现，并使用tail/head指针来索引对应内容。

![](https://picx.zhimg.com/v2-bc1e54223c4c561f268d35f48d08591f_1440w.jpg)

然而，这样的结构在读通路上需要一个很大的mux，会引入不可忽略的开销。其也可以通过在输出接口增加一个2-slot EB来解决，如下图2.11所示：

- 当FIFO为空时，直接写入最后的EB
- 只有当最后的EB为满时才开始往FIFO写数据
- 读取时，只从EB中读取
![](https://pic2.zhimg.com/v2-73f6445d5fe64b937695afe884b88bc7_1440w.jpg)

对于特别大型的FIFO，则可以使用双端口SRAM来实现。

### 2.3 抽象流控模型

任意实现valid/ready握手的FIFO或简单EB都可以抽象为包含一个保存数据的buffer加一个counter（如下图2.12a）：

- counter记录还有多少空闲的slot（可能通过链表接口隐式的实现）
- buffer用来存储数据
![](https://pic4.zhimg.com/v2-028f9f94a01b73af2aaef0eb32feae73_1440w.jpg)

follow这样的思路，可以观察到不一定需要将这个counter与接收方互联，而是可以放在任意位置，如图2.12b。继续的可以把控制逻辑全部放在发送端，如图c（即credit协议）。

### 2.4 Credit-based流控

在把counter放在发送方时，完全由发送方进行start/stop控制，这称为credit-based流控。发送方显式的追踪接收方的有效slot，其称为credit。其控制示意图如下图2.13所示。

![](https://pic3.zhimg.com/v2-993add9029bd005721ae6df48518a722_1440w.jpg)

同样条件下的valid/ready握手协议时序情况则如下图2.14所示。

![](https://pic2.zhimg.com/v2-3aaacc65cc996e1691fe1a42cd72b999_1440w.jpg)

### 2.5 流水线数据传输

2.5.1 Valid/Ready流控下的流水线链路

使用和分别表示前向和后向寄存器数量，那么其等效流控模型可表示为下图2.15。

![](https://pic3.zhimg.com/v2-b55e18b90d786402b6436d271f0dcfbe_1440w.jpg)

其中接收方的slot counter以及发送放的ready起作用都为0 cycle，在图中以虚线表示。那么从ready信号触发，到真正接收方看到起作用需要个周期，这就意味着最差的情况接收方需要在buffer内剩余这么多slot的时候就开始通知发送方。

虽然上边这样的做法比较保险，但是很大程度限制了吞吐率并且浪费资源，因为ready控制信号起作用速度太慢，使得吞吐量最多只能达到50%。

一种解决办法是增加接收方的buffer，增加到，那么就可以使断流时间更短，在最差情况下，每个cycle都传输数据时，其吞吐量的比例可以达到

进一步考虑细节，在发送方ready拉低后可以当拍起作用，所以会有一拍数据缓存在发送方出口寄存器，使得整体情况有好转，所需buffer深度可以优化为。这样的理论也可以应用于上边的EB设计，对应的，其需要才能保证带宽不损失。

2.5.2 使用EB的流水线链路

上边直接Valid/Ready握手对buffer资源深度开销较大，所以在NoC实现中，流量控制可以通过插入EB来实现，从而切断每一级的流控路径。

下图2.16展示了不同方案：

- 图a只使用了pipeline寄存器，在接收方需要10深度buffer来保证带宽
- 图b将第一级pipeline寄存器替换为EB，则RTT减少，接收方只需要6深度buffer即可
- 图c使用EB替换所有pipeline寄存器，可以以最少的资源实现同样功能
- 总的，将个打拍寄存器替换为EB，buffer资源可以从降低为
	- 所以这种方式总是首选
![](https://pic2.zhimg.com/v2-5e89dd9726f8eb7c6514b1cff722cabb_1440w.jpg)

2.5.3 Credit-based流控和打拍链路

基于Credit-based流控的打拍链路描述如下图2.17所示，与valid/ready握手不同，此时credit消耗和数据传输所经历的Latency不同。

![](https://pic4.zhimg.com/v2-4e783f72e6416d067e400590343aa055_1440w.jpg)

此时，基于Credit流控传输的吞吐量和初始credit数量和RTT，有很大关系，不同配置下的情况如下图2.18所示，在valid/crdit都插入一拍的情况下，需要credit=3才能打满带宽。

![](https://pic1.zhimg.com/v2-86c71cfc48af652b6ac276085eeb438a_1440w.jpg)

通常情况下，在Credit-based流控下，为保证无损传输和100%吞吐量，接收方所需要的buffer深度需要时。

### 2.6 req-ack握手和bufferless流控

使用req-ack握手，发送方不再像valid/ready和credit-based一样感知接收方的buffer状态。每次发送请求都乐观的认为其已经发送，发送后有两个选择：

- 要么在发送下一个有效数据前等待一个ack
- 此时吞吐量被限制在50%，因为req/ack各需要一个cycle
- 要么继续发送新数据并且需要有能力处理可能到达的nack
- cycle收到ack就在cycle继续发送数据
	- 下一cycle继续发送数据，因为上一笔还没有ack，所以不能擦除，需要保存在辅助buffer中
	- 如果后边收到ack则擦除并将新的数据放入
	- 否则发送方停止发送数据
- 被拒绝的话，下一cycle则继续发送辅助buffer内的数据

典型的req-ck协议可以被证明其所需的buffer数量是等于valid/ready握手的。

另一种追求最少化buffer的bufferless流控（每一拍压缩buffer数量到一个寄存器）是rea-ack流控的缩减版：

- 接收方不能被接收的数据不在发送方keep，而是会直接丢弃
- 下一cycle继续传输新的数据，而由更上层的协议来重传丢失的数据

但是这种做法对上层的设计复杂度要求很高，也不一定就有优势。

### 2.7 宽消息传输

片上网络通常需要传输不同size大小的消息，如果按照宽消息来实现物理wire宽度则浪费太大，通常的做法事保持练度宽度接近系统中最常用的消息宽度，并将较大消息传输拆分为顺序传输，其格式通常如下图2.19所示。第一个携带地址和控制信息的flit为head，最后一个为tail。

![](https://picx.zhimg.com/v2-23daf44b938c3892f3576ff0be5b9549_1440w.jpg)

下图2.20展示了典型4-flit包的传输。

![](https://pic3.zhimg.com/v2-4494b5b65a7a842c0aab0d3642d92174_1440w.jpg)

那么在把Packet往下传输前应该需要下游有多少buffer呢？这就引入了两种做法：

- Virtual Cut Through (VCT)
- 需要下游可以容纳整个packet
- [wormhole](https://zhida.zhihu.com/search?content_id=269555697&content_type=Article&match_order=1&q=wormhole&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Nzg5MjAxMDEsInEiOiJ3b3JtaG9sZSIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjI2OTU1NTY5NywiY29udGVudF90eXBlIjoiQXJ0aWNsZSIsIm1hdGNoX29yZGVyIjoxLCJ6ZF90b2tlbiI6bnVsbH0.C80GkZURaq8UjlEsM6UoBE-FZ4lLTwF3PRtlnzieb7I&zhida_source=entity) (WH)
- 只需下游可以容纳一个flit即可
	- 相对对buffer深度的要求较低
![](https://pic1.zhimg.com/v2-d3a828a4870add05f234e81e7bfd7286_1440w.jpg)

## 3\. 基准Switch模块和Router

片上系统中经常会出现需要多个对等点共享一条链路访问其他节点的例子，如下图3.1共享一个MC的例子所示。

![](https://picx.zhimg.com/v2-98345162bcb097059d4e2377e12353d5_1440w.jpg)

该结构需要增加一个mux，并由仲裁器决定如何选择哪个IP可以访问共享链路。仲裁器可以在每个cycle选择，也可以在传输一个packet中间keep住（通常是后者，也是VCT/wormhole的需求；前者通常在使能VC的条件下可以支持）。

### 3.1 多输入连接到一个输出

除仲裁外，多to一情况下还需要考虑输出的流控机制，假设输入输出均为valid/ready协议，则其组织结构可以表述为下图3.2。

![](https://pic2.zhimg.com/v2-1b9238a5498d415a950a4fd8416b5a05_1440w.jpg)

为了保证一packet为粒度传输，所以只有head flit会发起仲裁请求，一旦授权则会一直锁定直到tail：

- `outAvailable` 表示仲裁器输出状态，表示连接到哪个输入
- 用于连接到mux
- `outLock` 表示第几个请求被连接到输出
- 对于head flit，需要参与仲裁，所以其被 `outAvailable` 所qualified
- 在将请求发送到仲裁器前，还需要保证数据可以被接收（与ready做与）
- 经过这两级mask，之后所有送到arbiter的请求都是有效的，由arbiter选择其中一个授权，一旦完成仲裁后产生grant信号用于：
- 驱动输出mux的sel信号选择对应input
	- 设置 `outLock` 信号，之后的body和tail信号就可以直接由 `outLock` 信号驱动
	- 驱动ready\_in信号
- tail flit发送完成后释放 `outAvailable` 和 `outLock`

在很多实际场景下，需要将link和仲裁器/mux的时序路径隔离，可以如下图3.3一样插入EB实现。

![](https://picx.zhimg.com/v2-e25aaaa39c3293d5ba72368a7f4263f9_1440w.jpg)

3.1.1 输出链路上Credit-based流控

基于第二章中的抽象流控模型，可以重构switch模型如下图3.4a。

![](https://pic1.zhimg.com/v2-0383bbbb6066e7200f80d4023c000240_1440w.jpg)

将slot counter位置挪动到图b的位置即变成credit-based流控，此时再增加拍就可以通过简单的增加pipeline寄存器即可，如tuc所示。

3.1.2 buffer分配的粒度

片上网络通常使用VCT或wormhole基于flit为单位进行资源分配。

3.1.3 层次化switch

一个层次化仲裁和mux的电路如下图3.5a，其可以保证每一个仲裁器的规模都为2to1，为此需要对应的修改其电路，因为没有全局仲裁器来检查所有输入的请求，可以可以将每个merge point都当做一个部分输出节点，其都拥有自己的 `outAvailiable` 标志。

![](https://picx.zhimg.com/v2-b9751014422f943907c90b7f3d132f63_1440w.jpg)

这样的设计使得每个小的branch都独立工作，其数据传输flow如图3.5b所示，同样可以抱着满带宽速率运行。

### 3.2 反向连接：拆分一个源到多个接收侧

1to多的反向连接相对简单，其split结构可以表示为下图3.6，此时也不需要保证packet为粒度的授权。

![](https://pic1.zhimg.com/v2-56502063be219544b2a5b39cb788dca8_1440w.jpg)

### 3.3 使用简化的逻辑将交换路径将多个输入连接到多个输出

扩展到多对多的switch设计结构如下图3.7所示，此时每个packet的head flit都需要知道其要去哪个目的地。

![](https://pic1.zhimg.com/v2-b4e78f1c4c0799096d4206c6d5380ca6_1440w.jpg)

其中：

- `outAvailable[j] = 1` 表示第j个输出为空闲状态
- 每个源根据目的地和对应目的地的ready状态产生仲裁请求信号
- 当第i个请求赢得grant时，需要并行执行：
- 设置 `outLock[i]` 信号为1
	- 为每个输入的状态变量 `outPort[i]` 赋值，存储其对应的目的地
	- 为每个输入根据grant信号产生ready\_in

3.3.1 输出链路上credit-based流控

在基于credit的流控下，输入在发送flit前需要保证输出可以接收，其结构如下图3.8，需要在每个输出端口增加一个credit counter，

![](https://pic3.zhimg.com/v2-9335c29f6190807a06883b6859b6f21e_1440w.jpg)

3.3.2 增加更多的switch元素

上边只使用一个仲裁器和mux将数据包路由到多个输出很大程度限制了吞吐量，可以如图9所示增加更多的datapath路径来增加吞吐量。但是图中的做法只有两个mux但是有3个输出，这会在内部mux和输出之间引入额外的控制逻辑，所以典型的做法是展平，即为每个输出端口分配一个仲裁器和mux。

![](https://pic3.zhimg.com/v2-89cefeeec8050f8a5fa95a202556f578_1440w.jpg)

### 3.4 使用unroll交换datapath将多个输入连接到多个输出

为了打满带宽需要使用如下图3.10a所示的unroll数据路径，即为每个输出分配一个仲裁器和mux。

![](https://pic1.zhimg.com/v2-f540675a04c66fe20a132cb0babfe1a2_1440w.jpg)

具体每个输入/输出侧的实现细节如下图3.11所示：

- 每个输入侧接收N-bit `outAvailable` 和 `ready` 信号
- head flit则根据目的地产生请求信号，否则直接使用 `outPort` 值
- 输入侧的ready\_in信号则根据对应的所有输出侧仲裁器按位或产生
![](https://pic1.zhimg.com/v2-5df91d2066f905733b498e5ad0c4eb9a_1440w.jpg)

进一步的，credit-based流控结果如下图3.12，

![](https://pica.zhimg.com/v2-3a6d7288c5ef7be5e4b5bc7e39856782_1440w.jpg)

### 3.5 头阻

以下图3.13中3to3为例，当两个输入端口请求同一输出端口时，当一个port赢得仲裁后会一直占用直到其tail flit被发送完成。然而port2中除了同样去端口2的请求外还有需要去输出1的请求，但是会同样被阻塞，这称为头阻并且是switch性能限制的主要瓶颈，而这只能通过在input buffer中增加灵活性来同时并发多个flit来缓解。

![](https://pica.zhimg.com/v2-0cb83fc718618a833b5e8324df2e3f68_1440w.jpg)

那么，如果已经知道traffic的分布特性，那么就可以从理论计算角度来评估出每个输出的期望吞吐率。

假设每个输入端口希望每个cycle都传输一个新的flit，并且每个flit到达每个输出端口的概率是。当多个输入指向同一输出时，只有一个能通过。且只有当所有输入都不指向输出时，输出才会空闲。

输入选择输出的概率，即不选择输出的概率是。每个输入端口间相互独立，那么所有个输入都不往发送请求的概率是。

因此一个输出j接收新的flit的概率是，对应2\*2 switch为0.75， 3\*3 switch为0.703，并随着N增大逐渐趋近于0.63。

如果进一步考虑到调度策略的影响，实际最终的每个输出最大吞吐量还会下降，在N较大时会降低到58%左右。

### 3.6 网络中的Router：路由计算

Router放在网络拓扑的汇聚点钟，如下图3.14，负责处理竞争和flit的路由转发。

![](https://pic3.zhimg.com/v2-e7045930fbe55105c9fba2557a41e5d2_1440w.jpg)

除了根据已知信息路由外，在一个大的网络中Router还需要负责计算输出端口，判断Flit应该沿着哪个路径传播，其结构可以是一个简单的查找表，根据head信息计算应该发往哪个输出端口，结构如下图3.15所示。

![](https://pic1.zhimg.com/v2-b76beb40646829be951e26090eeb24a6_1440w.jpg)

对应的，路由计算模块在整个Router中的位置如下图3.16所示。

![](https://picx.zhimg.com/v2-e7d52a296564a9d671b5193c70336497_1440w.jpg)

3.6.1 前瞻路由计算

路由计算根据head flit中的地址来决定发往哪个输出端口进而产生请求，所以正常来说需要等待RC计算完成才能产生请求和仲裁，而如果flit在到达当前Router的时候就已经携带当前router的RC结果就可以避免该串行依赖，这需要引入Lookahead routing computation (LRC)模块，其结构如下图3.17所示。

- 图a为典型串行设计
- 图b将RC与链路传输并行执行
- 图c将RC模块继续往前推进异步，放在输入侧，在仲裁的同时并行执行下一级的RC
![](https://pic1.zhimg.com/v2-080f288d428d31e3b5ab8a4bf8fba6a2_1440w.jpg)

具体的，依赖于LRC的Router架构如下图3.18所示，当前Router收到的Head flit中已经携带了所需RC字段，同时并行的执行LRC来执行下一跳的RC。

![](https://pic4.zhimg.com/v2-a5dae17154066d946be726be518bc3df_1440w.jpg)

### 3.7 层次化Switch

上边3.1.3节提到的层次化switch的结构也可以应用在Router的设计中，结构如下图3.19所示。

![](https://pic3.zhimg.com/v2-b864025061be8aeaa516108b5b92ac32_1440w.jpg)

这样子的设计，在一些特定路由规则的网络中还可以选择性打开/关闭一些资源，比如X-Y路由规则下可以把Y->X的路径连接关系及buffer资源省略。

## 4\. 仲裁逻辑

Router的核心switch模块包括仲裁器和mux，需要小心的协同优化来高效实现。mux选择较少，而仲裁器可能性很多。通用的Dynamic Priority Arbiter (DPA)如下图4.1所示，主要包括：

- 仲裁逻辑
- 基于当前优先级状态决定授权哪个请求
- 优先级更新逻辑
- 根据当前grant结果，决定输入的优先级
	- 其weight根据不同的仲裁策略可能是1-bit或多bit
![](https://pic4.zhimg.com/v2-5ab7074bdfa629da4165a588ee5c20f1_1440w.jpg)

### 4.1 固定优先级仲裁

最简单的仲裁器即Fixed Priority Arbiters (FPAs)，端口的优先级被静态分配，因而不需要优先级状态，通常端口号更低的输入的优先级更高。有不同的实现策略：

1. 其grant结果可以直接通过优先级编码实现
2. 另一种实现是取反加一取补码后再与原始请求按位与实现；
3. 将所有请求视为0/1数字，那么也可以利用排序的方法实现，比如基于二叉树的方式，如下图4.2a所示。
![](https://pic3.zhimg.com/v2-4aeaa02fdac74408d7c4b81f940cca3a_1440w.jpg)

4.1.1 Grant信号的产生

图4.2a中的电路可以增强为图4.2b中的样子，以并行的产生grant信号。

进一步优化成并行执行的方式，如下图4.3。

![](https://picx.zhimg.com/v2-fdc064b366043ef1ea00077ef0b2d5b7_1440w.jpg)

### 4.2 Round-Robin仲裁

轮询仲裁器从最高优先级请求开始，每一次仲裁周期结束，将相邻请求的端口赋值为最高优先级，下图4.4展示了一个4输入仲裁的例子。

![](https://pic2.zhimg.com/v2-99a317f99467ff0d02c03ff2ff23e5a5_1440w.jpg)

有很多不同的实现方法，本文的策略如下图4.5，将所有请求分为HP/LP两部分，每个部分内都是FPA，同时只有在HP中完全没有有效请求时才会使用LP内的请求。

![](https://pic1.zhimg.com/v2-fafc4e693bc751dde7350ac1770a2d74_1440w.jpg)

通过这样的思路，可以将roub-robin仲裁转换为如下图4.6样找最大值的逻辑电路。

![](https://pic4.zhimg.com/v2-ddb22591954395f6086486231fb4f509_1440w.jpg)

4.2.1 将Round-robin仲裁器和mux合并

将数据和代表优先级的一同经过mux电路可以不再需要同时产生grant信号。

### 4.3 具有2D优先级状态的仲裁器

将优先级保存在一个2D矩阵中，当时则代表输入i的优先级要高于输入j(也代表着请求i如果有效则可以mask掉请求j)，对角线元素固定为0。一个优先级矩阵的例子如下图4.8所示。

![](https://pic4.zhimg.com/v2-a1754689c511b17d7c1fd9882102bc53_1440w.jpg)

在该优先级表示的定义下，可以按列生成mask信号来屏蔽优先级低的请求并产生grant信号，电路如下图4.9所示。

![](https://pic3.zhimg.com/v2-e9e312cc034f7319b13dc56d6d73f302_1440w.jpg)

4.3.1 优先级更新策略

基于以上2D的优先级状态表示，可以推导出多个不同的仲裁策略，它们之间的区别只是更新weight矩阵的方式不同：

- Least recently granted
- 一旦第i个请求被授权，则将其优先级置为最低（第i行全部置0，第i列置1）
- Most recently granted
- 一旦第i个请求被授权，则将其优先级置为最高（第i行全部置1，第i列置0）
- Incremental Round robin
- 在2D网络中实现类似RR的策略，通过降低最高优先级的位置来实现而不关心其是否被授权
	- 每一次仲裁周期，都将优先级最高的请求降低为最低（第i行全部置0，第i列置1）
- Hybrid First-Come First Served and Least Recently Used
- 当新的请求到达输入i，输入j上没有新请求，则设置
	- 当请求信号从0变成1时则认为有一个新的请求，如果输入i的新请求当拍没有被授权，则不再认为其是新请求
	- 当输入i/j同时收到新请求时，则keep原始值
	- 当请求i被授权时，其优先级置位最低（第i行全部置0，第i列置1）

## 5\. 流水线的Wormhole Router

单周期Router结构如下图5.1所示，其顺序的执行所有计算，并且在输出侧可以有两种实现选择：

1. 只是用打拍寄存器，其反应下游router的credit
1. 本文都使用该策略
3. 使用一个真正的credit counter
![](https://pic4.zhimg.com/v2-8cb623799e4f6713e1f2feeb64030ed3_1440w.jpg)

另一方面，为了提供运行速率和吞吐量，通常也需要采用流水线设计，本节会逐一介绍。

### 5.1 单周期Router组织概述

单周期Router的微架构如下图5.2，主要包括3个主要任务：

- RC
- 执行完RC之后才能根据当前状态计算出请求需要前去的目的地
- SA
- 当一个flit赢得SA，那么就会存储到输出buffer中，则需要CC模块更新当前credit数量
- ST
- 如果授权的是head/tail，则需要使用SU模块更新寄存器 `outAvailable`
![](https://pic3.zhimg.com/v2-5919923a42490fb75593243800aa1318_1440w.jpg)

上边的结构核心包括两个关键路径：

- control path
- 从RC开始生成req，经过SA之后，终止到ST的选择信号以及去往每个输入buffer的grant信号
- data path
- 只涉及input buffer中的mux操作以及ST中的mux

5.1.1 Credit消耗和状态更新

Credit更新和 `outAvailable` 状态更新并不必须要等待SA结构，从而可以并行的与SA执行。

5.1.2 单周期Router的Packet Flow示意

示意如下图5.3所示：

- 第一周期是(Link Traversal – LT)-(Buffer Write – BW)
- 第二周期是Router内计算
- Route Compute (RC)/Credit consume (CC)/State Update (SU)/Switch Allocate(SA)/DeQueue(DQ)/Switch Transfer(ST)
- 之后body和tail就不再需要执行RC和SA
![](https://pic4.zhimg.com/v2-41b7dc12873aeff0264a6209b34586cb_1440w.jpg)

### 5.2 流水线阶段的RC

将RC隔离为一条单独的流水线是最简单的方式，只需要包含一个额外的流水线寄存器，结果如下图5.4所示。

- 可以直接使用outPort寄存器来当做打拍寄存器，唯一的变动就是将该bypass逻辑去掉
- 此时寄存器的en信号，当检测到head时keep，检测到tail时reset即可
![](https://pic2.zhimg.com/v2-d3d23aa1e0406b8ed439fc6d70335491_1440w.jpg)

此时的流水线传输时序如下图5.5所示。

![](https://picx.zhimg.com/v2-7494a57bcf3f7ed002a2ab8ab9b75d31_1440w.jpg)

如果因为此时其他input获得授权导致本输入无法正常传输，则会导致阻塞，此时的时序结构如下图5.6所示（其被图5.5中flit传输所阻塞）。

![](https://pic4.zhimg.com/v2-0c73a3b311db4b52d3b28002eb49d167_1440w.jpg)

### 5.2.1 RC流水线截断的无空闲cycle操作

为了消除上边的气泡，可以通过并行的添加一个data pipeline寄存器来满足（使用1-slot EB），其对应的结构如下图5.7所示。

![](https://pic1.zhimg.com/v2-1187628ac9dcfb7806dab33229a1ae5c_1440w.jpg)

此时可以无气泡传输，其时序如下图所示，RC只在控制路径发生，cycle 2可以同时将head往下发送的同时接收下一个body。

![](https://pica.zhimg.com/v2-4e5e2eaabab33857f6b0bb7eb33b1ff4_1440w.jpg)

### 5.3 流水线阶段的Switch Allocation

第二种有趣的形式是将SA与ST分离，

5.3.1 基本组织形式

如下图5.9所示，如果想要将SA与ST分离，那么就需要对SA输出的grant结果进行打拍，在此结构下，会使得每两拍才能授权一个请求出去（因为只对控制路径做了打拍）。

![](https://pic3.zhimg.com/v2-d0da6b8bd8b81e0f9c0aca20643d79ea_1440w.jpg)

为了实现这个行为，在第二拍grant之前就需要第一拍的重复请求，对应其中的mask部分。从而这样的电路结构会引入气泡，其对应的时序图如下图5.10所示（该例子中的RC也是非流水线的，所以存在两个气泡）。

![](https://pic4.zhimg.com/v2-71b559bd9e6884100ca422e52fde6e83_1440w.jpg)

5.3.2 SA流水线阶段的另一种组织形式

观察到，body/tail flit其实并不需要产生任何SA，所以可以让其继承之前的grant，从而删除非head flit的空闲周期。此时对应的电路结构如下图5.11，其使用一个寄存器缓存grant结果并直接给非head flit使用。

![](https://pic3.zhimg.com/v2-b9b042f7428706e1fb3a1b8ffcece330_1440w.jpg)

此时对应的时序图如下图5.12所示，body/tail flit可以减少一拍。

![](https://pica.zhimg.com/v2-0211cd69c441522e4c3e510e4d2b0bf6_1440w.jpg)

5.3.3 SA流水线阶段的无空闲周期操作

通过额外增加以及输入侧流水线寄存器可以解决该气泡问题，如下图5.13所示，其可以不使用流控，因为不会有flit被门控，其作用只是将grant结果和数据对齐。 同时为了保证对齐，还需将传递回上游的grant信号放在寄存器打拍前。

![](https://pic2.zhimg.com/v2-d3fd52de84fc2514bdd26b06d0170e2b_1440w.jpg)

具体的，其对应的flow时序图如下图5.14所示。

![](https://pica.zhimg.com/v2-7c5c81d77142255404ca193aea29f7a8_1440w.jpg)

### 5.4 具有RC和SA流水线阶段的流水线Router

同时融合RC和SA阶段，即可派生出3-stage流水线实现。

5.4.1 只在控制路径的Router

此时对应的完整电路结构如下图5.15所示，对应的会引入诸多气泡问题，如下图5.16所示。

![](https://pic3.zhimg.com/v2-2bb731eda7dd784636905d1b1fc34ad8_1440w.jpg)

![](https://pic1.zhimg.com/v2-c4fbfe53d27d596ed5e2bd1ef59f3fae_1440w.jpg)

5.4.2 同时在控制和数据路径流水

此时对应的完整router结构如下图5.17所示。

![](https://pic2.zhimg.com/v2-bf73cf74a8651da365befacdd18ce02f_1440w.jpg)

对应的flow时序图如下图5.18所示。

![](https://pica.zhimg.com/v2-4f98cdee912f03ea4f94525a042218fe_1440w.jpg)

## 6\. VC流控和缓冲

上边描述的所有包传输行为，在tail flit被完整传输之前需要一直占据整个link，其行为就类似于一条链路上有两个不同方向的汽车，如下图6.1所示，右转的车也必须要等待直行的车走完之后才能进行。

![](https://picx.zhimg.com/v2-e6a8e75a45f223c6b53e1f8fa38b8097_1440w.jpg)

为了实现流量隔离，需要在空间/时间上增加更多的资源，本章介绍虚拟通道，如下图6.1b，其涉及到同一物理通道的时分复用，类似于存在多个并行的Wormhole通道。

VC最早提出用来解决死锁问题，以避免资源的循环依赖，特别是在一致性协议中，对VC有着特别的要求，比如MOESI基于Directory的一致性协议至少需要3个虚拟网络来避免协议级死锁。此外，VC还可以用于：

- 传输不同类型的流量比如req/reply
- 节省wire并提高链路利用率

### 6.1 虚拟通道流控的操作

为了将一个物理通道切分为 `V` 个虚拟通道，接收方就需要有 `V` 个队列。为了支持特性，需要同步增强链路级流控，特别是为每个VC分配一些独立的信息。

valid/ready握手没办法区分不同的flow，所以如果需要支持则需要使用如下图6.2所示的多组握手信号。其中，虽然有多组握手信号，但是同一时刻只能传递一个数据。

![](https://picx.zhimg.com/v2-e7ea5fff024e7dd0438e658913b01abd_1440w.jpg)

在VC流控中，buffer资源和流控握手线都会随着VC数量翻倍。因此需要对之前第二章的流控模型，如下图6.3a，需要为每个VC分配一个slot counter

![](https://pic3.zhimg.com/v2-2910df21f7c50fc79e954a73df75416a_1440w.jpg)

图6.3b进一步的将流控机制counter放在发送放，即扩展的credit-based流控，好处是中间不需要那么多的valid/ready信号。此时，在链路上还需要增加sideband信号来标识返回的credit/发送的数据属于哪个VC，所以需要一个vc id字段。具体的下图6.4给出了所有完整的信号线。

![](https://pic2.zhimg.com/v2-862a5c1d878163a658961f2dfb2263e9_1440w.jpg)

### 6.2 VC buffer

在没有VC的通道中，2-slot EB即可提供无损带宽，基于此扩展，一个简单的3-VC buffer结构可以包括3个EB以及一个arbiter，结构如下图6.5所示，其中当前VC中的数据可以传输到下一级的任意一个VC中。

![](https://pic3.zhimg.com/v2-6d204c43a1102d0a7681db2c6710373a_1440w.jpg)

下图6.6给出了两个这样结构的VC buffer互联时的时序图。此时两个VC各使用了50%的带宽，同时每个VC也只使用了其一半的有效buffer，第二个buffer只有在VC stall的时候才会使用。随着VC数量的增多，这种buffer浪费会变得更加严重。

![](https://pic3.zhimg.com/v2-2b4f940b7e608ec2e760f7673ea08258_1440w.jpg)

### 6.3 buffer 共享

自然地，解决上述冗余buffer的办法是共享buffer，其可以为每个VC管理一个长度可变的queue。

共享buffer的基本结构原理如下图6.7所示，每个VC有自己私有的buffer，同时它们还有一个共享buffer，当私有buffer被用完时可以使用该共享buffer：

- 需要为每个私有buffer和一个共享buffer分配一个counter
- 接收方需要反向传递update和vc id
![](https://picx.zhimg.com/v2-1d49ea16830321fe9c3cc7ea329d5347_1440w.jpg)

具体下图6.8展示了该共享buffer结构工作的时序图：

- 如果私有VC为空，则直接进入该buffer
- 否则进入共享buffer先缓存，之后等私有buffer空闲后再进入
![](https://pic1.zhimg.com/v2-63fad8ae370df0fe92b0ef59e5240eb4_1440w.jpg)

6.3.1 一个通用共享buffer的组织和操作

共享buffer设计的关键是需要维护不同VC间flit的到达顺序，其可以通过每次数据移位或者链表实现，链表结构的例子如下图6.9所示。对应的enqueue和dequeue所需要执行的操作如下图6.10所示。

![](https://pica.zhimg.com/v2-efc72322d02907c44f4dc4e7d25a9f06_1440w.jpg)

![](https://pica.zhimg.com/v2-efc72322d02907c44f4dc4e7d25a9f06_1440w.jpg)

6.3.2 针对VC的原始共享buffer: ElastiStore

ElastiStore在V个VC中只是用V+1个buffer，下图6.11展示了具有两个VC的ElastiStores结构：

- 好处是节省了buffer数量
- 劣势是在网络比较拥塞的时候会限制网络带宽
![](https://pic1.zhimg.com/v2-f475659805bf1b4d53e040f4a1e86a8a_1440w.jpg)

对应的，ElastiStore电路微架构如下图6.12所示。

![](https://pic1.zhimg.com/v2-8df99c6e8bd5fbd39b83dac013233e22_1440w.jpg)

### 6.4 流水线链路中的VC流控

长距离数据传输是需要使用reg slice打断时序路径，两种单lane/多lane的结构对应的其时序电路如下图6.13所示。但是后者在复杂的soc实现中很难处理，可能会有物理实现问题。

![](https://pic1.zhimg.com/v2-9f5b96b7fba64418454bb691018ec5da_1440w.jpg)

6.4.1 使用valid/ready流控的流水线链路VC

可以如下图6.14一样利用简单的valid/ready流控寄存器，但是因为中间简单的使用寄存器，所以flit不能在link中间停止，因为内部没有流控机制：

- 此时每个VC需要保留的buffer深度为
- 为保证可以满吞吐量运行，需要的buffer深度为
![](https://pic2.zhimg.com/v2-531b07ef6f444c0302342565218ab331_1440w.jpg)

同样的，该结构也可以使用共享buffer来降低资源开销，比如将作为共享buffer，则所有VC私有buffer维持在深度即可保持满带宽运行。

6.4.2 使用基于Credit流控的流水线链路VC

基于credit，即使每个VC的私有buffer深度只有1也可以保证安全运行，不需要担心链路间的相互依赖，所以其可以非常灵活的组织私有buffer和共享buffer间的资源分配。

这也是为什么现代VC设计都是基于credit流控。

## 7\. 基本的携带VC的switch模块和router

### 7.1 带VC的多to一连接

输入/输出均携带VC多to一抽象连接结构如下图7.1所示。

![](https://pic1.zhimg.com/v2-85ab09c9b6d32cd2f53c72989d2cd998_1440w.jpg)

7.1.1 每个输入/输出VC所需的状态变量

为了支持Vc，需要增强每个输入/输出的状态信息以允许VC级和port级的调度，具体包括：

- 输出端口需要每个VC一个credit counter
- 用于为每个VC产生ready信号
- 每个switch的输出需要维护 `outAvailable` 来标识当前输出是否被分配到特定输入
- 基于VC的设计中，属于不同VC的flit可以相互交织发送
- VC allocator (VA)负责将输入VC匹配到输出VC
- 所以需要有V个 `outAvailable` 分别标记输出的不同VC
	- VC可以根据路由需求改变其VC的分配或者施加一些特殊约束
- 每个输入侧需要为每个VC维护 `outVCLock` 和 `outVC` 变量
- outVCLock表示对应VC被分配到一个输出VC
	- 具体对应到哪个输出VC由outVC指定

7.1.2 VA的请求生成

每个输入侧都需要有一个controller，负责生成发往VA的请求，并收集对应的grant信号，其结构如下图7.2所示。

![](https://picx.zhimg.com/v2-c6c6d2503499d956a2f7e56506a7406f_1440w.jpg)

每个VC还会向VA发送一系列的候选output VC，如果其网络传输中不允许改变VC的话，，如果允许的话则会有多个候选值。

VA则在请求VC和有效VC间选择，将所有输入的reqVC向量合并可以得到行，V列的矩阵，当时意味着第i个输入VC正在请求输出VC j。

下图7.3展示了一个例子，有两个输入，每个输入对应3个VC。

![](https://pic4.zhimg.com/v2-23f09864595f3297902dab1fbfd986a9_1440w.jpg)

VA完成仲裁需要选择被授权的VC，同时输出 `selOutVC` 和 `candidateOutVC` 给每个输入。另外 `VCgranted` 信号用于表示对应输出VC被成功授权。一旦某个VC被成功授权，则应该停止继续发送请求到VC，直到其tail flit传输完成。

7.1.3 SA的请求生成

VA之后需要通过SA来竞争对输出端口的访问，相比于VA每个packet执行一次，SA需要每个flit执行一次。当满足以下条件时，输入VC可以申请发往SA的请求：

- Valid flit
- 即存在有效flit
- Output VC already allocated
- 即VA已经为其分配所属的VC
- The output VC has enough credits
- 只有在其对应的VC存在有效credit的前提下才能竞争SA

完整的，负责生成VA/SA请求的输入侧controller结构如下图7.4所示。

![](https://pic4.zhimg.com/v2-1220531ec6b216afb44c94e0bcba4d5d_1440w.jpg)

7.1.4 汇总grant并且向输出移动

SA、VA向input侧传递一系列控制信号：

- inputGrantSA
- 当其为1时意味着第个VC被授权往输出端口移动
- 在允许切换VC的设计中，发送flit时需要使用outVC来替换原有flit中的VCid字段

7.1.5 多to一连接的VA内部组织

VA中，每个request会申请多个输出侧VA，其中有些位置还可能是已经被分配了，所以需要：

- 首选使用已经分配的VC mask掉一些没有意义的请求
- 第一阶段仲裁为VA1，针对每个input VC进行，限制为只对每一个输出的一个VC发起请求。
- 因为每个输入端口独立进行，所以可能选同一输出VC
- 第二个阶段为VA2，在每个output VC进行，只为其选择一个input VC

完整的电路结构如下图7.5所示，每个input VC包括一个V:1仲裁器，以及每个output VC包含一个N\*V:1的仲裁器。

![](https://pic1.zhimg.com/v2-08ed0734a0ef8df623cc155eecd7b0fc_1440w.jpg)

下图7.6则展示了上述电路微架的具体授权过程中的一个例子。

![](https://pic3.zhimg.com/v2-cff536f21ebf4e72590be9aaac2824fc_1440w.jpg)

7.1.6 多to一连接的SA内部组织

SA为所有已经分配到一个output VC的input VC提供服务，其仲裁包括：

- 第一步称为SA1
- 每个input的一个local仲裁，选择将哪个VC仲裁出去
- 第二步称为SA2
- 进行input port到output port的映射

具体SA的组织形式如下图7.7所示，这种分离式的方式相比于之前没有VC的设计需要等待SA2授权完成才能更新SA1的优先级信息。

![](https://pic4.zhimg.com/v2-53a7567bd1a180e315bc220cdcc56fb5_1440w.jpg)

7.1.7 输出优先分配

VA/SA仲裁器的分配顺序可以为input first或output first。

- output first下，所有input VC首先将其请求转发到输出侧的arbiter
- 此时，VA阶段一个input VC可能获得多个output VC的grant
	- 只有再使用input侧仲裁器从中选择一个

output first仲裁器已经被证明比input first仲裁器有更强的公平性，但是input first的延时更低。

### 7.2 使用unroll datapath的多to多连接：一个完整的VC-based Router

VC-based router的基准电路结构设计如下图7.8所示。

![](https://pic4.zhimg.com/v2-6fdb491b08c956b70b040341df0331fb_1440w.jpg)

7.2.1 路由计算

最简单的实现RC的电路结构示意如下图7.9所示，如果RC计算逻辑复杂，则可以使用一个mux逻辑来共用一个，因为每个cycle每个input port只会有一个flit输入/输出。

![](https://pic4.zhimg.com/v2-e50cdab57835e371ee10b534a0aa1f91_1440w.jpg)

7.2.2 VC分配器

如下图7.10所示，展示了input侧产生请求信号的逻辑，主要包括请求的VC号 `reqVC` 以及请求的输出端口号 `reqPort` 。

![](https://picx.zhimg.com/v2-2cec6135fce26625fb85983258de93d5_1440w.jpg)

7.2.3 Switch分配器

将SA的请求产生逻辑也包含进来的完整input控制器的电路结构如下图7.11所示，将 `outPort` 驱动给SA需要满足的条件包括：

- The request corresponds to a valid flit
- The packet has allocated an output VC
- The output VC has enough credits
![](https://picx.zhimg.com/v2-4e7f719fd77e36371e4d5c086352f819_1440w.jpg)

SA的仲裁授权逻辑也可以使用矩阵表示，结构如下图7.12，对应一个3\*3的router。

![](https://pic4.zhimg.com/v2-0fc2a3f2d583fd2a60dc0218ea928185_1440w.jpg)

7.2.4 汇总grant并移动到输出

此步骤由ST阶段完成，根据SA产生的grant信号，将对应的数据发送至下游即可。

7.2.5 VC-based router的内部VA组织

VA需要有能力并行的将输入VC分配到输出VC中。input需要提供的信息包括其请求的输出端口reqPort以及reqVC。具体VA对应的硬件电路结构如下图7.13所示，包括：

1. VA1：每个输入VC选择其中一个有效的输出VC
2. VA2：每个输出VC选择最多一个输入VC
![](https://pica.zhimg.com/v2-8f393582777823a2fdebca5d16fd8b4a_1440w.jpg)

**VA1阶段更快的组织**

一种更快的，可以避免mux逻辑的组织形式如下图7.14所示。其使用了多个并行的逻辑替代了mux组件。

![](https://pica.zhimg.com/v2-74f430b6488654e27c4e9e094e584b5c_1440w.jpg)

7.2.6 VC-based router中SA的内部组织

同样的包含了两级仲裁，结构如下图7.15所示：

- VA1：从input端口的多个VC中选择一个
- VA2：从多个input端口中选择一个发往输出
![](https://pica.zhimg.com/v2-0db8162f8426ba85b4084042b11a4956_1440w.jpg)

下图7.16展示了一个3\*3 Router的一个具体仲裁例子。

![](https://pic2.zhimg.com/v2-df4c7f7426cb8f3e951da1d562541eab_1440w.jpg)

**自适应路由下的SA**

自适应路由条件下，可能会允许一个input同时申请多个output，这就需要在链路中再增加一个select unit，可以根据网络状态和拥塞控制算法实现。

### 7.3 使用中心化分配器构建的VA和SA

除了使用分离的输入/输出仲裁外，还可以使用中心化方式实现。N个请求和N个资源的集中式分配以矩阵方式进行：

- 矩阵每一行对应一个请求，可以申请多个资源
- 每一列对应一个资源，可以接收多个请求
- 调度时，每行每列都只有能有一个1
- 一旦某一行请求或者某一列资源被grant，则对应行/列则不能再被grant

中心化allocator通过集中式的分配来提供分配率，这种基于对角线的调度方式和策略如下图7.17所示。

![](https://pica.zhimg.com/v2-2a18567e1bf0127958f32d051dda2232_1440w.jpg)

基于上边的中心化分配器，也称为wavefront分配器，可以构建VA/SA。具体的，VA需要构建分配器，如下图7.18所示：

- 行为input VC，列为output VC
![](https://pic2.zhimg.com/v2-a1bdafe8c2722224965304dcef79ac93_1440w.jpg)

类似的，SA则可以使用N\*N大小的allocator实现，结构如下图7.19所示。

![](https://pic4.zhimg.com/v2-ddc1b24af14928e49daac2baa0ea20ed_1440w.jpg)

## 8\. VC-based router中的高速分配器

VC-based router中有两种资源需要分配：

- output VC，这需要VC allocator
- output port，这需要VA allocator

### 8.1 虚拟网络：降低VA的复杂度

典型的VA中，VA1需要V:1仲裁器；VA2需要N\*V:1仲裁器，以及一些信号的gather/mask/distribute。而如果禁止packet在不同虚拟网络间的变换，则可以将VA切分为并行的更小的VA，如下图8.1所示。

![](https://pic1.zhimg.com/v2-b625baeec20dd15fed08bbed38b407d6_1440w.jpg)

如果每个VC对应一个VA，则可以完全将VA1阶段移除，因为第i的input VC总是请求第i个输出VC。

### 8.2 超前VA1

另一种优化时序的办法是超前VA1，允许超前为每个input VC计算出其目的output VC，对应的电路结构如下图8.2所示。

![](https://pic1.zhimg.com/v2-2e8ab2b8c56a0bd5e009501a2c3ec322_1440w.jpg)

但是这样的做法一个缺点是没有办法看到output VC的状态，所以可能提前导致请求无效行，而降低整体吞吐带宽。

### 8.3 没有VA2的VA：组合分配器

因为每个输入同一时刻只能传输一个flit，也只能对应一个VC。利用该特性，可以使用SA阶段来等效实现VA2。

8.3.1 VA1与SA串行执行的组合分配器

具体的结构如下图8.3a所示：

- VA1为每个input VC查找至少有一个credit的output VC
- SA1接收来自VC的请求，从中仲裁处胜利的input VC
- SA2顺带实现了之前VA2的功能
![](https://pica.zhimg.com/v2-5b71b93cb6044c4682eb0f1088823968_1440w.jpg)

8.3.2 VA1与SA并行执行的组合分配器

VA1的结果在SA2结束之前并不会被使用，所以可以将VA1和SA1并行执行。其结构如上图8.3b所示。

8.3.3 具有超前VA1的组合分配器

对应的结构如上图8.3c所示。

### 8.4 预测SA

其在没有预先获得一个output VC的情况下允许访问一个output port，此时SA和VA并行执行，根据仲裁输出的不同，会发生4种情况：

- packet在VA和SA都失败
- 其将在下一个cycle继续尝试
- VA授权，但是SA失败
- 下一个cycle继续尝试SA
- VA失败，但是SA成功
- 这是预测失败的场景，是可能发生的最差情况，此时即使仲裁成功也不能发生会存在一个气泡
- VA和SA都成功
- 可以成功发射，是最好的场景

为了降低预测失败的可能，引入了两个独立的SA：

- 第一个执行预测功能
- 第二个使用VA的输出，非预测性的执行SA功能

具体的，该电路结构如下图8.4所示。

![](https://pica.zhimg.com/v2-1791390943f23c36e84d9bdd7a85fd34_1440w.jpg)

8.4.1 处理预测和非预测grant

只有当预测SA中没有有效的grant时才会考虑预测性SA，下图8.5描述了在这两种类型SA中进行选择的组件。

![](https://pic2.zhimg.com/v2-98743a79e3a6e8c52264e655eaca315f_1440w.jpg)

### 8.5 具有input-speedup的VC-based router

通过允许多个VC直接连接到crossbar来提供分配效率，其结构如下图8.6所示。

![](https://pic3.zhimg.com/v2-12e472cb1f16247216add51cc59b6d50_1440w.jpg)

Input-Speedup 是处理分离式SA低效的一个有用技术，主要缺点是增加了crossbar的规模。

一旦不允许跨VC传输，并且最大化input speedup，则不再需要VA，属于同一VC但是不同端口可以使用私有的router，其结构如下图8.7所示。

![](https://pic2.zhimg.com/v2-5be9be5eae59d5769f91468cbbf5551f_1440w.jpg)

## 9\. 流水线VC-based router

### 9.1 单周期VC-based router组织的review

其完整的组织结构如下图9.1所示，包括：

- control path
- 其中包含了RC/VA/SA阶段
- data path
- 其中包括了input multiplexer选择传输哪个VC以及crossbar
![](https://pic4.zhimg.com/v2-3622193b68b6625f76fc0b89ab60ad25_1440w.jpg)

9.1.1 示例1：两个packet到达同一input VC

其对应的时序图如下图9.2。

![](https://pic4.zhimg.com/v2-6c46fc3d4e78765775ca9c4774beba2b_1440w.jpg)

9.1.2 示例2：两个到达不同input VC的packet

两个到达同一input但是不同VC的packet传递时序如下图9.3，其中，在cycle 2的时候第二个packet执行了RC和VA但是竞争失败没有传递。

![](https://pic1.zhimg.com/v2-36aaa8ae7124679eee8af77bf6796810_1440w.jpg)

### 9.2 流水线阶段的RC

9.2.1 只在控制路径打拍

将RC在控制路径单独打拍的结构如下图9.4所示，和第5章结构基本一致。

![](https://picx.zhimg.com/v2-9e294cd154b16ffd57cd847e9a4a29bf_1440w.jpg)

其对应的传递时序图如下图9.5，可以看到，因为只在控制路径打拍，所以引入了气泡。

![](https://pic1.zhimg.com/v2-c864b270940d0b17f50041b69395c3d0_1440w.jpg)

9.2.2 控制路径和数据路径同时打拍的Router

和第5章一样，在控制路径添加EB即可解决气泡问题，对应的电路结构和时序图分别如下图9.6和9.7所示。

![](https://pic1.zhimg.com/v2-e5d7236d5c3feb6c2e13a7748eb2df48_1440w.jpg)

![](https://pic4.zhimg.com/v2-ea5d64a4d38ca4b0e7c6cff44b92aa1d_1440w.jpg)

### 9.3 流水线阶段的VA

和RC类似的方案可以将VA从控制路径中单独隔离一拍，其结构如下图9.8所示。

![](https://pic2.zhimg.com/v2-940ec4efa2d9e9f563ff789e6113b917_1440w.jpg)

9.3.1 示例1：两个packet到达同一input VC

时序结构如下图9.9所示，同样因为只在控制路径插拍，导致引入气泡。

![](https://pic2.zhimg.com/v2-46a12d7c1e7ab56a4cf03024b5160781_1440w.jpg)

9.3.2 示例2：两个packet到达不同的input VC

如下图9.10所示，灰色部分表示对应的flit仲裁失败。

![](https://pic3.zhimg.com/v2-f1f6f932b27af049d71e7ea35e4e7f08_1440w.jpg)

9.3.3消除VA流水线引入的气泡

可以和RC使用一样的方法来消除气泡，但是这有可能会引入死锁风险，比如：

- 一个tail flit在EB中执行SA
- 另一个packet中的head flit正在请求一个输出VC
- 假设tail flit赢得了输出VC#1
- 而后续相邻的head flit正在请求VC#0
- 此时如果EB中的tail授权失败了，则会出现相同输入VC同时获得了两个输出VC的授权
- 这会创建一个循环依赖：VC#0在VC#1被release之前都不能被访问
	- 同时因为这两个VC可能属于不同的输出端口进而会影响不同的router

为了解决这个依赖，需要保证前一个tail发出去之前都不能继续发送head flit，而此时这个EB也就没用了，所以在VA的流水线设计中通常不在datapath打拍，而容忍该气泡。具体的，会出现该气泡的场景包括：

- 两个packet连续到达同一input VC
- 两个packet要前往同一输出VC

### 9.4 流水线阶段的SA

和第5章类似，在SA阶段打拍需要针对grant信号，结构如下图9.11所示。

![](https://pic2.zhimg.com/v2-94fabfd8e1285bda57dafdc78fcefb45_1440w.jpg)

对应的传输时序图如下图9.12，因为在switch datapath前同时插了一拍，所以不会引入气泡问题。

![](https://pic1.zhimg.com/v2-00af4a45780ebcf66095c4398273e7cc_1440w.jpg)

### 9.5 VC-based多级流水线router

9.5.1 3级流水线组织：RC/VA/SA-ST

此时Router的实际组织结构如下图9.13所示。

![](https://pic3.zhimg.com/v2-463ef6bc8f38f98dd7b594a4b4d6566c_1440w.jpg)

对应的时序图如下图9.14，因为VA只在控制路径打拍，所以连续传输会引入气泡问题。

![](https://pic2.zhimg.com/v2-fe1197f87744be6771a5a095fa7fb713_1440w.jpg)

9.5.2 3级流水线组织：RC-VA/SA/ST

对应结构如下图9.15所示，时序图如下图9.16，同样因为VA的问题会引入气泡。

![](https://pic3.zhimg.com/v2-ecac7978d7113400e23044eecac4bfa4_1440w.jpg)

![](https://pica.zhimg.com/v2-2ae2297cd94e92ca89b0c1debc4ebd14_1440w.jpg)

9.5.3 4级流水线组织

对应的结构如下图9.17所示，时序图如下图9.18，同样因为VA的问题导致连续访问存在气泡。

![](https://pic4.zhimg.com/v2-290772a3849148d23fd10a9b4d5cf723_1440w.jpg)

![](https://pic4.zhimg.com/v2-f3141060e7b5701ce34bf6d01fe8f703_1440w.jpg)

编辑于 2026-01-25 23:01・北京