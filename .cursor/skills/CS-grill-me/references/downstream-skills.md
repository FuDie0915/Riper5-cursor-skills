# Downstream Skills — Concept Spec

> Consumes `grill-me` output. **Not yet implemented** — contracts for future development.

## Overview

```yaml
pipeline:
  flow: "grill-me → decision-log.md → [to-prd | to-issues | grill-me --light]"
  principle: "decision log is the single source of truth"
  communication: "no skill talks directly to another — all via decision log"

interface:
  +------------+------------------+------------------+
  | Skill      | Reads            | Produces         |
  +------------+------------------+------------------+
  | grill-me   | user input, code | decision-log.md  |
  | to-prd     | decision-log.md  | prd.md           |
  | to-issues  | decision-log.md  | issues/          |
  | grill-me   | decision-log.md  | updated          |
  |  --light   |                  | decision-log.md  |
  +------------+------------------+------------------+
```

## to-prd (planned)

```yaml
purpose: "convert resolved decision log to PRD"
input: decision-log.md (key decisions [RESOLVED] or [RISKY])
output: prd.md (standard template)
flow:
  - read decision-log.md, extract all decisions
  - group by functional domain (auth, data model, API, ...)
  - per group write:
      overview: what + why
      requirements: functional requirements derived from decisions
      decisions: specific choices + trade-offs
      open_questions: any [DEFERRED] decisions affecting this area
      risks: relevant risk register entries
  - include glossary from decision log
  - add "Out of Scope" section for explicitly deferred items
trigger: 'user says "convert this to PRD" or handoff recommends to-prd'
```

## to-issues (planned)

```yaml
purpose: "split resolved decision log into executable GitHub/GitLab issues"
input: decision-log.md (key decisions [RESOLVED] or [RISKY])
output: issue files or API-created issues
flow:
  - read decision-log.md, build decision tree
  - identify leaf decisions (no downstream deps) → become implementation tasks
  - group related leaf decisions into epics
  - per issue:
      title: action-oriented ("Implement idempotency keys for PaymentIntent")
      description: link to parent decision + trade-off context
      labels: derived from decision domain + risk level
      dependencies: reference upstream decisions that must resolve first
  - create "Implementation Order" section by dependency
trigger: 'user says "break this into issues" or handoff recommends to-issues'
```

## grill-me --light

```yaml
purpose: "shorter follow-up session on decision subset"
input: existing decision-log.md with [OPEN] or [DEFERRED] decisions
flow:
  - read existing decision log
  - identify open boundaries ([OPEN] decisions + dependencies)
  - run compressed interrogation (light depth: 3-7 questions)
  - update same decision-log.md in place
trigger: 'user says "follow up on deferred decisions" or "grill me on remaining open questions"'
```

## Design Principle

```yaml
principle: "decision log is the universal interface between skills"
benefits:
  - each skill independently testable
  - each skill replaceable
  - no direct skill-to-skill coupling
```