# LLM Wiki

本仓库是一个基于 [**Hermes Agent 的 `llm-wiki` skill**](https://github.com/NousResearch/hermes-agent/blob/main/skills/research/llm-wiki/SKILL.md) 搭建的 **LLM Wiki**：用互相链接的 Markdown 页面持续沉淀知识，而不是把结论留在单次对话里。

入门思路与整体叙事可参考 [**Karpathy Wiki（中文导读）**](https://karpathy-wiki.lol/zh)，它与 Andrej Karpathy 提出的「LLM Wiki」工作方式一脉相承；原始gist见 [LLM Wiki by Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

---

## Karpathy 知识库的核心理念

传统 **RAG** 往往在每次提问时从切片语料里临时检索并拼装答案；**Karpathy Wiki 模式**则强调 **先把跨资料的综合写进可维护的产物**，让之后的问答站在上一次整理过的结果上继续演进。

可以概括为几点：

- **沉淀而非反复从零推导**：高质量摘要、对比与结论写入页面；新资料进入时在已有页面上修订，而不是每次都从头拼一遍。
- **人机分工**：人负责选题、筛选资料与判断优先级；模型负责摘要、交叉引用、归档与一致性维护（具体目录与约定见仓库内的 `SCHEMA.md`）。
- **资料层与工作层分离**：原始材料放在不可随意改写的资料区（如 `raw/`），Wiki 页作为工作层吸收、评议与链接；Schema（如 `SCHEMA.md`）约束结构与标签，避免笔记发散成噪声。
- **矛盾与演进可追溯**：冲突信息记在相关页面或 frontmatter 中，配合日志（`log.md`），便于复核而不是被静默覆盖。
- **答案可复用**：有价值的问答可以回填为 `queries/`、`comparisons/` 等页面，避免优质推理只存在于聊天记录里。

一句话：**RAG 偏重「检索时的召回」，Karpathy Wiki 偏重「长期编译后的知识状态」。**

---

## 本仓库的目的：团体知识协作与共享

本 Wiki 面向 **团队共同维护与使用**：

- **共享同一套结构与术语**（见 `SCHEMA.md`、`index.md`），减少各人笔记孤岛与重复劳动。
- **协作增量**：新成员可通过索引与图谱快速定位主题； ingest / 更新 / lint 式的维护可由人或 Agent 按约定执行，变更记录在 `log.md`。
- **知识归属清晰**：资料来源与页面引用可追溯，便于评审、对齐与后续迭代。

仓库内的领域范围与标签体系以 `SCHEMA.md` 为准；若你希望扩展领域或协作流程（分支策略、评审门槛），建议在 Schema 或团队约定中显式写明，以便人机协作一致。

---

## 快速开始：克隆本仓库并用 `llm-wiki` 增量扩展

下面是一条完整路径：**先把本 Wiki 仓库拉到本地 → 让 Hermes 的 `WIKI_PATH` 指向该目录 → 用 `llm-wiki` skill 在已有页面与结构上持续 ingest（增量）。**

### 1. 克隆本 Wiki 仓库

在你希望存放知识库的目录执行（将 URL 换成你 fork 后的地址亦可）：

```bash
git clone https://github.com/lukebest/llm_wiki.git
cd llm_wiki
```

若使用 SSH：

```bash
git clone git@github.com:lukebest/llm_wiki.git
cd llm_wiki
```

确认仓库根目录下已有 `SCHEMA.md`、`index.md`、`log.md` 以及 `raw/`、`entities/`、`concepts/` 等结构——说明这是一份**已有内容**的 Wiki，后续只做增量。

### 2. 把 `WIKI_PATH` 固定到该克隆目录

`llm-wiki` skill 只认 **`WIKI_PATH`** 指向的目录（未设置时默认为 `~/wiki`）。必须指向**当前克隆的根目录**（包含 `SCHEMA.md` 的那一层），例如：

```bash
# 临时（当前终端会话）
export WIKI_PATH="$(pwd)"          # 在 llm_wiki 根目录下执行时

# 或写绝对路径（推荐给 Hermes / 定时任务）
export WIKI_PATH=/home/you/projects/llm_wiki
```

把同一行写入 **`~/.hermes/.env`**（或你运行 Hermes 的环境配置文件），避免每次手动 export。

### 3. 安装并启用 `llm-wiki` skill

见下文 **「使用 `llm-wiki` skill 生成与维护知识库」**：从 Hub 安装或将上游 skill 放入 `~/.hermes/skills/`，确保会话加载该 skill。

### 4. 增量扩展的典型流程（每次有新资料）

1. **同步团队最新内容（可选但推荐）**  
   ```bash
   cd "$WIKI_PATH"   # 即你的克隆目录
   git pull
   ```

2. **定向（每次开干前）**  
   让 Agent 先读 `SCHEMA.md`、`index.md`、`log.md` 末尾若干条，避免重复建页、遵守标签与命名。

3. **摄取（增量核心）**  
   向 Agent 提供 URL、文件或粘贴正文，并说明按 llm-wiki **在本仓库现有结构下 ingest**，遵守 `SCHEMA.md`。Agent 会把原文落入 `raw/`（含 frontmatter），按阈值 **新增或更新** `entities/`、`concepts/` 等页面，并更新 `index.md`、`log.md`。

4. **自检（可选）**  
   请求「对 wiki 做 lint」，修复断链、孤儿页等问题后再提交。

5. **提交并推送（团体协作）**  
   ```bash
   cd "$WIKI_PATH"
   git status
   git add -A
   git commit -m "wiki: ingest <简短说明>"
   git push
   ```

这样，**下载（克隆）的是完整知识库快照**，**增量**体现在：新资料进入 `raw/`、Wiki 页与索引在原有基础上追加与修订，并通过 Git 与他人合并。

---

## 使用 `llm-wiki` skill 生成与维护知识库

**前提：** 请先完成上一节 **「快速开始」**（克隆本仓库并设置 `WIKI_PATH`）。

以下说明聚焦在本仓库上的 **摄取与维护**；上游 [**`llm-wiki` SKILL**](https://github.com/NousResearch/hermes-agent/blob/main/skills/research/llm-wiki/SKILL.md) 文档另有完整操作列表，可自行查阅。

### 1. 安装与启用 skill（Hermes Agent）

- **获取 skill**：从 [Hermes Skills Hub](https://hermes-agent.nousresearch.com/docs/skills/) 用 `hermes skills` CLI 浏览/安装对应条目，或将上游仓库中的 [`skills/research/llm-wiki/`](https://github.com/NousResearch/hermes-agent/tree/main/skills/research/llm-wiki) 放入本机的 `~/.hermes/skills/`，并在 `~/.hermes/config.yaml` 里通过 `external_dirs` 指向团队共享的 skill 目录（见 [Hermes Agent Skills 指南](https://openclawlaunch.com/guides/hermes-agent-skills)）。
- **生效方式**：确保会话会加载该 skill（Hub 安装或本地路径注册后，按 Hermes 文档执行 `hermes skills configure` 等步骤）。

### 2. 把 Wiki 路径指向本仓库

Skill 通过 **`WIKI_PATH`** 定位知识库目录（未设置时默认为 `~/wiki`）。本仓库若clone在其它路径，请在 **`~/.hermes/.env`** 或运行环境中设置，例如：

```bash
export WIKI_PATH=/path/to/this/wiki/repo   # 指向包含 SCHEMA.md 的目录
```

团队共用同一克隆路径或 NFS/Git 工作副本时，全员使用相同的 `WIKI_PATH`，避免 Agent 写到错误目录。

### 3. 核心操作：摄取与审计（由你在对话里发起）

| 操作 | 你对 Agent 说什么（示例） | Agent 按 SKILL 做的事 |
|------|---------------------------|------------------------|
| **摄取 ingest** | 「把这篇 URL/文件收进 wiki」「处理附件里的原文」 | 原文写入 `raw/`（带 `source_url` / `ingested` / `sha256`），按阈值新建或更新 `entities/`、`concepts/` 等，更新 `index.md` 与 `log.md` |
| **审计 lint** | 「对 wiki 做 lint / 健康检查」 | 检查断链、孤儿页、索引完整性、frontmatter、陈旧页等，并记入 `log.md` |

**注意：** `raw/` 内正文摄取后视为不可原地改写；修订结论应在 Wiki 页完成。

### 4. 每次会话开始前的「定向」（避免重复建页）

在已有 wiki 上继续工作时，应先让 Agent **阅读** `SCHEMA.md`、`index.md` 和 `log.md` 近期条目（SKILL 要求如此），再执行 ingest 或大规模更新。你可直接提示：「先按 llm-wiki 定向：读 SCHEMA、index、最近 30 条 log。」

---

## 使用 OpenClaw、Hermes 与其它 Agent 查询知识库

查询的本质是：**先从已编译的 Markdown 页面作答**，必要时再补充外部检索；高价值回答可回填到 `queries/` 或 `comparisons/`（见 SKILL 的 Query 流程）。

### Hermes Agent（含通过 OpenClaw Launch 托管的 Hermes）

- **同一套 skill**：查询前同样应加载 `llm-wiki`，且 `WIKI_PATH` 指向本仓库根目录。
- **自然语言即可**：例如「根据 wiki 总结 [[某概念]] 与 [[另一实体]] 的关系」「wiki 里对某某硬件的结论是什么？请引用页面」。
- Agent 侧应按 SKILL 执行：**读 `index.md` →（页面多时）在 wiki 目录内搜索关键词 → `read_file` 相关页 → 综合回答并标注依据的 `[[wikilink]]`**；值得保留的深度对比可新建页面并写 `log.md`。
- 若在 **[OpenClaw Launch](https://openclawlaunch.com/)** 上部署 Hermes，工具与技能仍属 Hermes 体系；配置 wiki 路径与环境变量的方式以实例 Dashboard / 文档为准（参见 [OpenClaw 上的 Hermes Skills 说明](https://openclawlaunch.com/guides/hermes-agent-skills)）。OpenClaw 与 Hermes 的「skill」来自不同生态（ClawHub vs Hermes Hub），**自带 OpenClaw skill 不等于自带 `llm-wiki`**；要以 LLM Wiki 工作流查询本仓库，仍需 Hermes + `llm-wiki` 或下文「通用 Agent」做法。

### OpenClaw 或其它未内置 llm-wiki 的 Agent

将 **本仓库作为工作区挂载**（克隆到本地、容器卷、或通过 MCP/文件工具可读），然后在系统提示或首轮对话中固定下列约束：

1. 知识库根目录即 `WIKI_PATH`，必须先读 `SCHEMA.md`、`index.md`、近期 `log.md`。
2. 用仓库内搜索或文件名定位相关 `.md`，只读 `entities/`、`concepts/`、`comparisons/`、`queries/`（以及团队约定的 `analyses/`、`summaries/` 等），**勿改写 `raw/` 原文**。
3. 回答须引用实际读到的页面标题或路径；需要持久保存的结论写入 Wiki 层并更新 `index.md` / `log.md`。

### Cursor、Claude Code、CLI Agent 等开发类 Agent

- **打开本仓库为当前项目**，在对话里说明：「遵循 Karpathy LLM Wiki / llm-wiki：先定向再问答。」
- 可选：在 `.cursor/rules` 或项目 `AGENTS.md` 中摘录 SKILL 的「Resuming」「Query」「Lint」要点，减少每次手动复述。

### 人工快速查阅（不经过 Agent）

直接用编辑器或 Obsidian 打开本目录，从 `index.md` 跳转；复杂主题可用全文搜索 `*.md`。这与 Agent 查询互补，适合抽查与审稿。

---

## 仓库导航（简要）

| 路径 | 作用 |
|------|------|
| `SCHEMA.md` | 领域、命名、标签与更新策略 |
| `index.md` | 内容目录与一页摘要 |
| `log.md` | 按时间记录的操作日志 |
| `raw/` | 原始资料（摄取后原则上不改写正文） |
| `entities/`、`concepts/` 等 | Wiki 工作层页面 |

本地可与 Obsidian 等 Markdown 工具配合使用；`WIKI_PATH` 与 Agent 查询方式见上文「把 Wiki 路径指向本仓库」及「使用 OpenClaw、Hermes 与其它 Agent 查询知识库」。

---

## 许可证与致谢

- Wiki **工作方法**来自 Karpathy 的 LLM Wiki 理念及 Hermes **`llm-wiki`** skill 的实践整理。
- 本 README 仅描述仓库用途与哲学背景；具体页面的版权声明与引用请以各 `raw/` 文件及页面 `sources` 为准。
