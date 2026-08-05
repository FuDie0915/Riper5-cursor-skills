# Cursor Skills — RIPER-5 AI Coding Behavior Protocol

> 本项目基于 **RIPER-5: AI 编码行为协议** 开发，为 Cursor 提供一套结构化的 AI 编码行为约束框架。

## 什么是 RIPER-5

RIPER-5 是一个五阶段 AI 编码行为协议，通过严格的模式隔离防止 AI 在未经授权的情况下修改代码。每个阶段有明确的允许/禁止边界，阶段间只能通过显式信号转换。

```
/init 或 /research → BRAINSTORM → PLAN → EXECUTE → REVIEW
  需求澄清/代码分析    方案探索    技术规范    忠实实施    无情验证
```

## 双入口

```yaml
init_entry:
  trigger: "/init"
  适用: "从零开始的项目，无代码可分析"
  流程: "dask-CS 完整生命周期 → decision-log.md → BRAINSTORM"

research_entry:
  trigger: "/research"
  适用: "已有代码的项目"
  流程: "research-CS 代码分析 → BRAINSTORM"
```

## Skills 清单

```yaml
skills:
  - name: core-CS
    path: .cursor/skills/core-CS/
    role: 协议骨架，被以下 5 个阶段 skill 引用

  - name: research-CS
    path: .cursor/skills/research-CS/
    role: 阶段1 — 信息收集、代码调查、架构分析

  - name: brainstorm-CS
    path: .cursor/skills/brainstorm-CS/
    role: 阶段2 — 方案头脑风暴、权衡评估

  - name: plan-CS
    path: .cursor/skills/plan-CS/
    role: 阶段3 — 精确技术规范、编号实施清单

  - name: execute-CS
    path: .cursor/skills/execute-CS/
    role: 阶段4 — 严格按清单实施、更新进度

  - name: review-CS
    path: .cursor/skills/review-CS/
    role: 阶段5 — 逐行验证实施与计划偏差

  - name: dask-CS
    path: .cursor/skills/dask-CS/
    role: 独立深问 skill — 逐问题拷问计划直到意图清晰
```

## Commands 清单

```yaml
commands:
  - name: init
    path: .cursor/commands/init.md
    trigger: /init
    action: 触发 dask-CS 跑需求澄清与架构决策（从零开始项目入口）

  - name: dask
    path: .cursor/commands/dask.md
    trigger: /dask
    action: 触发 dask-CS 独立深问（已有项目方案审视）

  - name: research
    path: .cursor/commands/research.md
    trigger: /research
    action: 调用 research-CS 信息收集与代码分析

  - name: plan
    path: .cursor/commands/plan.md
    trigger: /plan
    action: 调用 plan-CS 生成技术规范

  - name: execute
    path: .cursor/commands/execute.md
    trigger: /execute
    action: 调用 execute-CS 按清单实施

  - name: review
    path: .cursor/commands/review.md
    trigger: /review
    action: 调用 review-CS 逐行验证

  - name: git-commit
    path: .cursor/commands/git-commit.md
    trigger: /git-commit
    action: 根据 git diff 生成提交消息
```

## 用法

### 启动 RIPER-5 流程

从零开始的项目：

```
用户: /init
AI:   [PHASE: Initialize] 读取项目上下文，构建决策树
AI:   [PHASE: Interrogate] 一次只问一个问题，附带推荐答案
      ...
AI:   [PHASE: Conclude] 输出 decision-log.md → 进入 BRAINSTORM

用户: ENTER BRAINSTORM MODE
AI:   [MODE: BRAINSTORM] 探索多种方案、评估优劣

用户: ENTER PLAN MODE
AI:   [MODE: PLAN] 输出编号实施清单，等待批准

用户: ENTER EXECUTE MODE
AI:   [MODE: EXECUTE] 逐项实施，每步请求确认

用户: ENTER REVIEW MODE
AI:   [MODE: REVIEW] 逐行比对计划与实施，输出结论
```

已有代码的项目：

```
用户: /research
AI:   [MODE: RESEARCH] 读取文件、分析架构、提出澄清问题

用户: ENTER BRAINSTORM MODE
AI:   [MODE: BRAINSTORM] 探索多种方案、评估优劣
...（后续相同）
```

### 使用 /dask 独立深问

```
用户: /dask 帮我审视这个架构
AI:   [PHASE: Initialize] 读取项目上下文，构建决策树
AI:   [PHASE: Interrogate] 一次只问一个问题，附带推荐答案
      ...
AI:   [PHASE: Conclude] 输出 decision-log.md
```

### 使用 Commands

在 Cursor 中输入 `/` 触发命令面板，选择对应命令即可。

## 模式转换规则

```yaml
transitions:
  trigger: "ENTER {MODE} MODE"   # 唯一合法的转换信号
  auto_fallback:
    - EXECUTE 发现偏离 → 回退 PLAN
    - EXECUTE 全部完成且用户确认 → 进入 REVIEW
  rollback_paths:
    - PLAN → RESEARCH（约束不清晰）
    - PLAN → BRAINSTORM（方案选错）
    - BRAINSTORM → RESEARCH（暴露未知约束）
    - EXECUTE → PLAN（偏离需设计变更）
    - REVIEW → EXECUTE（实现层偏差，可修复）
    - REVIEW → PLAN（设计层偏差，需重新规划）
  rollback_rule: "不允许跳跃式回退，每次回退携带原因 + 目标问题"
  forbidden: "任何未经显式信号的模式切换"
```

## 偏离分级

```yaml
deviation_classification:
  level_1_inline_fix:
    范围: "不影响接口签名、数据结构、模块边界"
    处理: "EXECUTE 内修正，记录 task_progress 并附判断依据，继续"

  level_2_design_deviation:
    范围: "涉及接口、数据结构、模块关系或新依赖"
    处理: "立即回退 PLAN"

  review_check: "REVIEW 校验 level_1 判断；误判 level_2 为 level_1 = 偏差"
```

## 跨平台适配

```yaml
claude_code:
  适配方式: "将 SKILL.md 正文合并进 CLAUDE.md 或用 @include 拆分"
  不需要: "frontmatter、command 机制、目录结构"
  代价: "失去斜杠命令便利性，全靠手打 ENTER {MODE} MODE"

codex:
  适配方式: "走 system prompt 注入或 rules 文件"
  不需要: "frontmatter、command 机制"
  代价: "同上"

generic_system_prompt:
  适配方式: "所有 SKILL.md 内容拼接进 system prompt"
  代价: "token 占用，所有阶段全量注入"
```

适配原则：协议内容（SKILL.md 正文 YAML 块）零修改，只动载体层（目录结构、激活机制、命令系统）。

## Known Limitations

```yaml
limitations:
  - id: skill_dependency
    issue: "无机制确保 core-CS 在阶段 skill 之前加载"
    impact: "如果 AI 跳过 core-CS，协议不变量不会被约束"
    workaround: "完全依赖 AI 自觉性；平台级强制需 Cursor 支持 skill 依赖声明"

  - id: lite_mode_no_persistence
    issue: "未创建 task file 时协议仍可运行，但不支持跨会话"
    impact: "复杂任务在新会话中必须从 RESEARCH 重新进入"
    workaround: "用户可在任意阶段中途创建 task file，从当前阶段开始写入"
```

## 项目结构

```
.cursor/
├── rules/
│   └── system.mdc              # 全局规则
├── commands/
│   ├── init.md                 # /init — 从零开始入口
│   ├── dask.md                 # /dask — 独立深问
│   ├── research.md             # /research — 代码分析
│   ├── plan.md                 # /plan — 技术规范
│   ├── execute.md              # /execute — 实施
│   ├── review.md               # /review — 验证
│   └── git-commit.md           # /git-commit — 提交消息
└── skills/
    ├── core-CS/               # 协议骨架
    │   └── SKILL.md
    ├── research-CS/           # 阶段1
    │   └── SKILL.md
    ├── brainstorm-CS/         # 阶段2
    │   └── SKILL.md
    ├── plan-CS/               # 阶段3
    │   └── SKILL.md
    ├── execute-CS/            # 阶段4
    │   └── SKILL.md
    ├── review-CS/             # 阶段5
    │   └── SKILL.md
    └── dask-CS/               # 独立深问
        ├── SKILL.md
        ├── assets/
        │   ├── example-decision-log.md
        │   └── test-shuffled-fields.md
        ├── references/
        │   ├── decision-log.md
        │   ├── pre-mortem.md
        │   ├── downstream-skills.md
        │   └── triggers.md
        └── scripts/
            └── decision_tree_visualizer.py
```