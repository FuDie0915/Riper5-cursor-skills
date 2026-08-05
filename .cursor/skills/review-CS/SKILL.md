---
name: review-CS
description: RIPER-5 阶段5 — 无情验证实施与计划。逐行比对、标记偏差、最终提交准备。
disable-model-invocation: true
---

# Mode 5: REVIEW

> **Prerequisite**: read `core-CS/SKILL.md` for shared protocol constraints.

```yaml
mode:
  name: REVIEW
  purpose: brutal_verification
  prefix: "[MODE: REVIEW]"

allowed:
  - line_by_line_compare_plan_vs_implementation
  - technical_validation_of_implemented_code
  - check_for_errors_defects_unexpected_behavior
  - validate_against_original_request
  - final_commit_preparation

required:
  - flag_any_deviation_no_matter_how_small
  - verify_all_checklist_items_completed
  - check_security_implications
  - confirm_maintainability

thinking:
  - critical: verify implementation accuracy
  - systems: evaluate total system impact
  - check: unexpected consequences
  - validate: technical correctness + completeness
```

## Protocol Steps

```yaml
steps:
  - id: validate_all
    action: "compare all implementation against plan"

  - id: on_success
    substeps:
      - stage_changes: "git add --all :!.tasks/*"
      - commit: 'git commit -m "{COMMIT_MESSAGE}"'

  - id: complete_task_file
    action: "fill final_review section"
```

## Deviation Format

```yaml
deviation_report: "Detected deviation: {exact_description}"
```

## Mismatch Routing

```yaml
mismatch_routing:
  judgment_criteria: "whether deviation touches interface signatures, data structures, or module boundaries"

  implementation_level:
    action: "rollback to EXECUTE with deviation checklist"

  design_level:
    action: "rollback to PLAN with deviation analysis"
```

## Deviation Review

```yaml
deviation_review:
  additional_check: "verify EXECUTE's level_1 deviation classifications"
  rule: "if EXECUTE classified a level_2 deviation as level_1, flag as deviation"
```

## Report

```yaml
report:
  required: "must state whether implementation matches plan exactly"
  conclusion:
    match: "Implementation matches plan exactly"
    mismatch: "Implementation deviates from plan"
```

## Output

```yaml
output:
  prefix: "[MODE: REVIEW]"
  content: systematic comparison + explicit verdict
  format: markdown
```