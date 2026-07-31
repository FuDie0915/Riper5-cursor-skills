---
name: CS-riper-execute
description: RIPER-5 phase 4 — implement planned changes exactly. Follow numbered checklist, update progress, request confirmation. Only enters on explicit "ENTER EXECUTE MODE".
disable-model-invocation: true
---

# Mode 4: EXECUTE

> **Prerequisite**: read `CS-riper-core/SKILL.md` for shared protocol constraints.

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
    action: "move to REVIEW"
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
  rule: "if any issue requires deviation → immediately return to PLAN"
```

## Output

```yaml
output:
  prefix: "[MODE: EXECUTE]"
  content: implementation matching plan + current checklist item
```