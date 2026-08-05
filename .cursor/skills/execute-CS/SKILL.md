---
name: execute-CS
description: RIPER-5 阶段4 — 严格按编号清单实施变更。更新进度、请求确认。仅在显式 "ENTER EXECUTE MODE" 后进入。
disable-model-invocation: true
---

# Mode 4: EXECUTE

> **Prerequisite**: read `core-CS/SKILL.md` for shared protocol constraints.

```yaml
mode:
  name: EXECUTE
  purpose: faithful_implementation
  prefix: "[MODE: EXECUTE]"
  entry: 'only on explicit "ENTER EXECUTE MODE" command'

allowed:
  - implement_only_what_plan_specifies
  - follow_numbered_checklist_exactly
  - mark_completed_checklist_items
  - update_task_progress_after_each_step   # standard built-in step

forbidden:
  - any_deviation_from_plan
  - improvements_not_in_plan
  - creative_additions_or_better_ideas
  - skip_or_abbreviate_code

thinking:
  - focus: accurate implementation of spec
  - verification: apply system checks during implementation
  - fidelity: follow plan precisely
  - completeness: proper error handling
```

## Protocol Steps

```yaml
steps:
  - id: implement
    rule: "follow plan exactly"

  - id: update_progress
    after_each: true
    format: |
      [{real_timestamp via Get-Date}]
      - Modified: {files and code changes}
      - Change: {summary}
      - Reason: {rationale}
      - Blockers: {list}
      - Status: unconfirmed | success | failure

  - id: request_confirmation
    prompt: "Status: success / failure?"

  - id: on_failure
    action: "return to PLAN"

  - id: on_success_more
    action: "continue to next checklist item"

  - id: on_all_complete
    action: "prompt user: ENTER REVIEW MODE"
```

## Code Quality

```yaml
quality:
  - always show full code context
  - specify language + file path in code blocks
  - proper error handling
  - standardized naming
  - concise meaningful comments
  - format: "```language:file_path"
```

## Deviation Handling

```yaml
deviation:
  level_1_inline_fix:
    criteria: "does not affect interface signatures, data structures, or module boundaries"
    examples: ["function name correction", "local logic adjustment", "missing error handling"]
    action: "fix within EXECUTE, record in task_progress with justification, continue"
    required: "must write judgment basis (why it doesn't touch interfaces/structures/boundaries)"

  level_2_design_deviation:
    criteria: "affects interfaces, data structures, module relationships, or new dependencies"
    action: "immediately return to PLAN"

  review_check: "REVIEW verifies level_1 judgments — misclassification = deviation"
```

## Output

```yaml
output:
  prefix: "[MODE: EXECUTE]"
  content: implementation matching plan + current checklist item
```

## Duration

```yaml
duration: until all checklist items complete + explicit "ENTER REVIEW MODE" signal
next_prompt: "when all items complete, prompt user: ENTER REVIEW MODE"
```