# Trigger Keywords & Activation

> Structured trigger definitions for keyword/pattern-based skill activation on agent platforms.

## Primary Triggers (high confidence)

```yaml
primary_triggers:
  - pattern: "interrogate me"
    example: "interrogate me on this plan"
  - pattern: "dask-CS"
    example: "run dask-CS on this design"
  - pattern: "interrogate me pro"
    example: "use dask-CS"
  - pattern: "interrogate + plan|design|architecture"
    example: "interrogate this architecture"
  - pattern: "challenge my + design|plan|approach"
    example: "challenge my design"
  - pattern: "stress test + plan|design|architecture"
    example: "stress test this plan"
  - pattern: "帮我审视"
    example: "帮我审视一下这个架构"
  - pattern: "先别写代码 + 厘清|明确|讨论"
    example: "先别写代码，先帮我把需求厘清"
  - pattern: "拷问我"
    example: "拷问我这个方案"
```

## Secondary Triggers (context-dependent)

```yaml
secondary_triggers:
  - pattern: "设计 + 方案|架构|数据库|API"
    context: "design discussion"
  - pattern: "plan + architecture|design|refactor"
    context: "planning discussion"
  - pattern: "decide + technology|framework|database"
    context: "technology selection"
  - pattern: "compare + options|approaches|solutions"
    context: "comparison discussion"
  - pattern: "trade-off / tradeoff"
    context: "evaluating trade-offs"
  - pattern: "assumptions"
    context: "examining assumptions"
```

## Negative Triggers (should NOT activate)

```yaml
negative_triggers:
  - pattern: "interrogate (data context)"
    reason: "data analysis, not design review — e.g. 'interrogate this dataset'"
  - pattern: "plan (scheduling)"
    reason: "personal schedule, not technical design — e.g. 'plan my day'"
  - pattern: "design (visual)"
    reason: "visual/graphic design, not architecture — e.g. 'design a logo'"
  - pattern: "review code"
    reason: "code review ≠ plan review"
  - pattern: "debug / fix"
    reason: "troubleshooting, not planning"
```

## Confidence Scoring

```yaml
confidence:
  certain: 1.0   # exact skill name match (dask-CS)
  high: 0.9      # primary trigger + design/plan context
  medium: 0.7    # secondary trigger + clear planning context
  low: 0.4      # single keyword match, no context
  none: 0.0     # matches negative trigger
```

## Platform Notes

```yaml
platforms:
  claude_code:
    activation: "via CLAUDE.md or @include; no frontmatter/command mechanism"
    note: "inject SKILL.md body into CLAUDE.md or separate file"

  cursor_windsurf_codex:
    activation: "via .cursorrules or skill directory"
    note: "copy SKILL.md content to agent rules/skills directory"

  generic_system_prompt:
    activation: "inject SKILL.md body into system prompt"
    note: "skill always active — triggers become irrelevant"
```