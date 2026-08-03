---
name: brainstorm-CS
description: RIPER-5 阶段2 — 方案头脑风暴、权衡评估、架构替代探索。不写代码，不做承诺。
disable-model-invocation: true
---

# Mode 2: BRAINSTORM

> **Prerequisite**: read `core-CS/SKILL.md` for shared protocol constraints.

```yaml
mode:
  name: BRAINSTORM
  purpose: brainstorm_approaches
  prefix: "[MODE: BRAINSTORM]"

allowed:
  - discuss_multiple_solutions
  - evaluate_pros_and_cons
  - seek_method_feedback
  - explore_architecture_alternatives
  - record_findings_in_task_file   # "proposed solution" section

forbidden:
  - concrete_planning
  - implementation_details
  - write_code
  - commit_to_specific_solution

thinking:
  - dialectical: explore multiple solution paths
  - creative: break conventional patterns
  - balance: theoretical elegance ↔ practical feasibility
  - evaluate: feasibility, maintainability, scalability
```

## Protocol Steps

```yaml
steps:
  - id: build_plan_from_research
    substeps:
      - study research dependencies
      - consider multiple implementation approaches
      - evaluate pros / cons per approach
      - write to task_file.proposed_solution

  - id: no_code_changes
    rule: "do not modify any code in this phase"
```

## Output

```yaml
output:
  format: markdown
  prefix: "[MODE: BRAINSTORM]"
  style: natural flowing paragraphs
  content: possibilities + considerations only
  preserve: organic links between solution elements
```

## Duration

```yaml
duration: until explicit "ENTER {NEXT} MODE" signal
```