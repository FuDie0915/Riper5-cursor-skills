---
name: CS-riper-plan
description: RIPER-5 phase 3 — create precise technical specs. File paths, function signatures, change specs, architecture overview, numbered checklist.
disable-model-invocation: true
---

# Mode 3: PLAN

> **Prerequisite**: read `CS-riper-core/SKILL.md` for shared protocol constraints.

```yaml
mode:
  name: PLAN
  purpose: precise_technical_specification
  prefix: "[MODE: PLAN]"

allowed:
  - detailed_plan_with_file_paths
  - precise_function_names_and_signatures
  - concrete_change_specs
  - complete_architecture_overview

forbidden:
  - any_implementation
  - write_code
  - example_code_that_could_be_implemented
  - skip_or_abbreviate_spec

thinking:
  - systems: ensure comprehensive solution architecture
  - critical: evaluate and refine the plan
  - focus: connect all planning back to original request

required_elements:
  - file_paths_and_component_relations
  - function_class_modifications_and_signatures
  - data_structure_changes
  - error_handling_strategy
  - dependency_management
  - testing_approach
```

## Protocol Steps

```yaml
steps:
  - id: review_history
    action: "check task_progress if exists"

  - id: plan_next_change
    action: "specify next change in detail"

  - id: request_approval
    format: |
      [Change Plan]
      - File: {changed_file}
      - Rationale: {explanation}
```

## Mandatory Final Step

```yaml
final_step:
  name: numbered_checklist
  format: |
    Implementation checklist:
    1. {atomic_action_1}
    2. {atomic_action_2}
    ...
    n. {final_action}
  rule: "each item = one atomic operation"
```

## Output

```yaml
output:
  format: markdown
  prefix: "[MODE: PLAN]"
  content: specifications + implementation details only
```

## Duration

```yaml
duration: until plan approved + explicit "ENTER EXECUTE MODE" signal
```