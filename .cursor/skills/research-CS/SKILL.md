---
name: research-CS
description: RIPER-5 阶段1 — 信息收集与代码调查。读取文件、分析架构、识别约束。新对话默认模式。
disable-model-invocation: true
---

# Mode 1: RESEARCH

> **Prerequisite**: read `core-CS/SKILL.md` for shared protocol constraints.

```yaml
mode:
  name: RESEARCH
  purpose: information_gathering
  prefix: "[MODE: RESEARCH]"

allowed:
  - read_files
  - ask_clarifying_questions
  - analyze_code_structure
  - analyze_system_architecture
  - identify_tech_debt
  - create_task_file        # requires explicit user consent
  - create_feature_branch   # requires explicit user consent

forbidden:
  - propose_solutions
  - implement_changes
  - plan_details
  - hint_at_any_action

thinking:
  - decompose technical components systematically
  - map known / unknown elements
  - consider broader architecture impact
  - identify key constraints

output:
  format: markdown
  prefix: "[MODE: RESEARCH]"
  content: observations + questions only
  no_bullets: unless explicitly requested

entry_context:
  role: "entry path for projects with existing code"
  alternative: "use /init (dask-CS) for greenfield projects with no code to analyze"
```

## Protocol Steps

```yaml
steps:
  - id: create_branch
    action: "git checkout -b task/{TASK_IDENTIFIER}_{TASK_DATE_AND_NUMBER}"
    consent: required   # must ask user, no auto-create

  - id: create_task_file
    action: "mkdir -p .tasks && touch .tasks/{TASK_FILE_NAME}_{TASK_IDENTIFIER}.md"
    consent: required
    note: "call Get-Date for real timestamp — knowledge clock is frozen"

  - id: analyze_code
    substeps:
      - identify core files / functions
      - trace code flow
      - record findings for later phases
```

## Duration

```yaml
duration: until explicit "ENTER {NEXT} MODE" signal
```