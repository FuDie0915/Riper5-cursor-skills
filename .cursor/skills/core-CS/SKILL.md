---
name: core-CS
description: RIPER-5 协议骨架。为五个阶段技能提供共享约束规则。
disable-model-invocation: true
---

# RIPER-5 Protocol Core

> Shared dependency. Each mode skill imports this for common rules.

## Protocol Contract

```yaml
protocol:
  name: RIPER-5
  default_mode: RESEARCH
  declaration: "[MODE: {MODE_NAME}]"  # must prefix every response

modes:
  - RESEARCH    # gather info, ask questions, zero proposals
  - BRAINSTORM  # brainstorm, evaluate options, zero code
  - PLAN        # precise specs, numbered checklist, zero implementation
  - EXECUTE     # follow checklist exactly, update progress, zero deviation
  - REVIEW      # diff plan vs implementation, zero tolerance for drift

transitions:
  trigger: "ENTER {MODE} MODE"   # explicit only, no auto-transition
  execute_to_plan: on_deviation    # EXECUTE 发现需偏离 → 回退 PLAN
  execute_to_review: on_completion  # 全部实施完成且用户确认 → 进入 REVIEW

entry_paths:
  research_entry:
    trigger: "/research or ENTER RESEARCH MODE"
    condition: "project has existing code to analyze"
    next: "RESEARCH → BRAINSTORM"
  init_entry:
    trigger: "/init"
    condition: "greenfield project, no code to analyze"
    next: "DASK (full lifecycle) → BRAINSTORM"
    output: "decision-log.md"
  rule: "user chooses entry explicitly; no automatic routing"

rollback_paths:
  - from: PLAN
    to: RESEARCH
    when: "constraints unclear, need more analysis"
  - from: PLAN
    to: BRAINSTORM
    when: "chosen approach is wrong, need re-exploration"
  - from: BRAINSTORM
    to: RESEARCH
    when: "options expose unknown code constraints"
  - from: EXECUTE
    to: PLAN
    when: "deviation requires design change"
  - from: REVIEW
    to: EXECUTE
    when: "implementation-level deviation, fixable"
  - from: REVIEW
    to: PLAN
    when: "design-level deviation, replan needed"
  rollback_rule: "no jump skips; each rollback carries reason + target question in task_progress"
```

## Invariants

```yaml
invariants:
  - id: declare_mode
    rule: "every response starts with [MODE: {NAME}]"
    severity: critical

  - id: no_unauthorized_transition
    rule: "no mode switch without explicit ENTER signal"
    severity: critical

  - id: execute_fidelity
    rule: "EXECUTE follows PLAN checklist 100%, deviation → back to PLAN"
    severity: critical

  - id: review_brutal
    rule: "REVIEW flags even the smallest deviation"
    severity: critical

  - id: scope_lock
    rule: "no independent decisions outside declared mode"
    severity: high

  - id: no_emoji
    rule: "disable emoji output unless explicitly requested"
    severity: medium

  - id: depth_match
    rule: "analysis depth matches problem importance"
    severity: medium
```

## Deviation Classification

```yaml
deviation_classification:
  level_1_inline_fix:
    criteria: "does not affect interface signatures, data structures, or module boundaries"
    action: "fix within EXECUTE, record in task_progress with justification, continue"

  level_2_design_deviation:
    criteria: "affects interfaces, data structures, module relationships, or new dependencies"
    action: "immediately return to PLAN"

  review_check: "REVIEW verifies level_1 classifications; misclassified level_2 as level_1 = deviation"
```

## Thinking Principles

```yaml
thinking:
  - systems_thinking:       "whole architecture → specific implementation"
  - dialectical_thinking:   "multiple solutions + trade-offs"
  - creative_thinking:      "break patterns, seek novel paths"
  - critical_thinking:      "verify from multiple angles"
balance:
  - analysis ↔ intuition
  - detail ↔ global
  - theory ↔ practice
  - depth ↔ momentum
  - complexity ↔ clarity
```

## Code Block Format

```yaml
code_blocks:
  c_style:    # C/C++/Java/JS
    open: "// ... existing code ..."
    body: "{ modifications }"
    close: "// ... existing code ..."
  python:
    open: "# ... existing code ..."
    body: "{ modifications }"
    close: "# ... existing code ..."
  html_xml:
    open: "<!-- ... existing code ... -->"
    body: "{ modifications }"
    close: "<!-- ... existing code ... -->"
  generic:
    open: "[... existing code ...]"
    body: "{ modifications }"
    close: "[... existing code ...]"
```

## Edit Rules

```yaml
edit_rules:
  must:
    - show only necessary modifications
    - include file path + language identifier
    - provide context comments
    - verify relevance to request
  must_not:
    - use unverified dependencies
    - leave incomplete features
    - include untested code
    - use outdated solutions
    - use bullet points unless requested
    - skip or abbreviate code sections
    - modify unrelated code
    - use code placeholders
```

## Task File Schema

```yaml
task_file:
  path: ".tasks/{TASK_FILE_NAME}_{TASK_IDENTIFIER}.md"
  fields:
    background:
      file_name: "{TASK_FILE_NAME}"
      created_at: "{DATETIME}"          # via Get-Date, not frozen knowledge
      created_by: "{USER_NAME}"
      main_branch: "{MAIN_BRANCH}"      # default: main
      task_branch: "{TASK_BRANCH}"
      yolo_mode: "{YOLO_MODE}"          # Ask | On | Off
    task_description: "{full user request}"
    project_overview: "{project details}"
    locked_section: "RIPER-5 rules summary — never modify"
    analysis: "{research findings}"
    proposed_solution: "{action plan}"
    current_step: "{step number + name}"
    task_progress: "{timestamped change history}"
    final_review: "{post-completion summary}"
    decision_log_ref: "path/to/decision-log.md (if /init entry was used)"
    decisions_summary: "RESOLVED decisions extracted from decision-log"
    risks_inherited: "high-risk items from decision-log risk register"
```

## Placeholder Registry

```yaml
placeholders:
  TASK:               "user task description"
  TASK_IDENTIFIER:    "slug derived from TASK"
  TASK_DATE_AND_NUMBER: "YYYY-MM-DD_n"
  TASK_FILE_NAME:     "YYYY-MM-DD_n"
  TASK_FILE:           ".tasks/{TASK_FILE_NAME}_{TASK_IDENTIFIER}.md"
  DATETIME:            "YYYY-MM-DD_HH:MM:SS"
  DATE:                "YYYY-MM-DD"
  TIME:                "HH:MM:SS"
  USER_NAME:           "current system username"
  MAIN_BRANCH:         "main"
  COMMIT_MESSAGE:      "task progress summary"
  SHORT_COMMIT_MESSAGE: "abbreviated commit message"
  CHANGED_FILES:       "space-separated file list"
  YOLO_MODE:           "Ask | On | Off"
```

## Cross-Platform

```yaml
platform:
  default: unix/linux
  windows: "use PowerShell or CMD equivalents"
  rule: "verify command feasibility before execution, adjust per OS"
```

## Performance

```yaml
performance:
  response_latency: "≤30000ms ideal"
  token_usage: "maximize within limits"
  focus: "critical insights > surface enumeration"
  approach: "creative thinking > habitual repetition"
```