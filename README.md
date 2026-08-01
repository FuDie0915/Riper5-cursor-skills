# Cursor Skills — RIPER-5 AI Coding Behavior Protocol

> 本项目基于 **RIPER-5: AI 编码行为协议** 开发，为 Cursor 提供一套结构化的 AI 编码行为约束框架。

## 什么是 RIPER-5

RIPER-5 是一个五阶段 AI 编码行为协议，通过严格的模式隔离防止 AI 在未经授权的情况下修改代码。每个阶段有明确的允许/禁止边界，阶段间只能通过显式信号转换。

```
RESEARCH → INNOVATE → PLAN → EXECUTE → REVIEW
 收集信息    方案探索    技术规范    忠实实施    无情验证
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

  - name: interrogate-CS
    path: .cursor/skills/interrogate-CS/
    role: 独立质询 skill — 逐问题拷问计划直到意图清晰
```

## Commands 清单

```yaml
commands:
  - name: git-commit
    path: .cursor/commands/git-commit.md
    trigger: /git-commit
    action: 根据 git diff 生成提交消息

  - name: riper-plan
    path: .cursor/commands/riper-plan.md
    trigger: /riper-plan
    action: 调用 plan-CS skill 生成技术规范

  - name: riper-execute
    path: .cursor/commands/riper-execute.md
    trigger: /riper-execute
    action: 调用 execute-CS skill 按清单实施

  - name: riper-grill
    path: .cursor/commands/riper-grill.md
    trigger: /riper-grill
    action: 先研究代码，再用 grill-me 方式逐层拷问用户意图
```

## 用法

### 启动 RIPER-5 流程

```
用户: ENTER RESEARCH MODE
AI:   [MODE: RESEARCH] 读取文件、分析架构、提出澄清问题

用户: ENTER INNOVATE MODE
AI:   [MODE: INNOVATE] 探索多种方案、评估优劣

用户: ENTER PLAN MODE
AI:   [MODE: PLAN] 输出编号实施清单，等待批准

用户: ENTER EXECUTE MODE
AI:   [MODE: EXECUTE] 逐项实施，每步请求确认

用户: ENTER REVIEW MODE
AI:   [MODE: REVIEW] 逐行比对计划与实施，输出结论
```

### 使用 grill-me 质询

```
用户: 帮我审视一下这个架构
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
    - EXECUTE 发现偏离 → 自动回退 PLAN
    - EXECUTE 全部完成且用户确认 → 进入 REVIEW
  forbidden: "任何未经显式信号的模式切换"
```

## 项目结构

```
.cursor/
├── rules/
│   └── system.mdc              # 全局规则
├── commands/
│   ├── git-commit.md           # git 提交命令
│   ├── riper-execute.md        # 执行命令
│   ├── riper-plan.md           # 规划命令
│   └── riper-grill.md          # 研究+质询命令
└── skills/
    ├── core-CS/              # 协议骨架
    │   └── SKILL.md
    ├── research-CS/          # 阶段1
    │   └── SKILL.md
    ├── brainstorm-CS/        # 阶段2
    │   └── SKILL.md
    ├── plan-CS/              # 阶段3
    │   └── SKILL.md
    ├── execute-CS/           # 阶段4
    │   └── SKILL.md
    ├── review-CS/            # 阶段5
    │   └── SKILL.md
    └── interrogate-CS/       # 质询 skill
        ├── SKILL.md
        ├── assets/
        ├── references/
        └── scripts/
```