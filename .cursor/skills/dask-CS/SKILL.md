---
name: dask-CS
description: 逐问题深问直到意图完全清晰。用户说"拷问我"、"帮我审视"或想压力测试计划时使用。
disable-model-invocation: false  # 允许自然语言触发，与阶段 skill 区分
---

# Dask-CS — Deep Ask Skill

> **Principle**: implementation quality ceiling = intent clarity. This skill exists to make intent explicit before any code is written.

```yaml
skill:
  name: dask-CS
  method: one_question_per_turn
  loop: walk every branch of decision tree → resolve dependencies sequentially
  language: user's language (default: zh-CN)

core_rule:
  - for each unresolved decision:
      - check_local_codebase_first
      - calibrate_against_external_evidence
      - provide_recommendation_with_explicit_tradeoffs
      - ask_exactly_one_question
      - wait_for_answer
```

## Response Format

```yaml
response_format:
  prefix: "[PHASE: {phase_name}]"
  rule: "exactly one PHASE label per response, at the very top"
  phases:
    - Initialize
    - Interrogate
    - Domain
    - Scenario
    - PreMortem
    - Conclude
  constraint: "never switch PHASE unless truly entering next stage"
```

## Session Lifecycle

```yaml
lifecycle:
  - phase: Initialize
    on_start:
      - read CONTEXT.md if exists
      - read all existing ADRs
      - read user's initial plan
      - compute rough decision tree outline
      - state scope + estimated depth (light: 3-7, medium: 8-15, deep: 16+)

  - phase: Interrogate
    loop: |
      for each unresolved decision in dependency order:
        Decision: {what we're deciding}
        Local findings: {code/config/patterns, or "unanswered locally"}
        External calibration: {engineering precedents + sources, or "no strong precedent"}
        Recommendation: {adopt/adapt/reject + reason}
        Acceptable trade-off: {cost/risk/future constraint}
        Question: {one precise question}
    rules:
      - one question at a time — batch breaks interrogation rhythm
      - every question ships with a recommendation — neutral is not interrogation
      - dependency order — upstream before downstream
      - prefer codebase exploration (rg, targeted reads) over broad exploration
      - reject "TBD" or vague answers — drill to specifics
      - use user's written language throughout

  - phase: Domain
    maintain: live glossary
    rules:
      - flag term conflicts with CONTEXT.md immediately
      - force precision on ambiguous terms
      - update CONTEXT.md in real-time when terms resolve
      - propose ADR when: hard_to_reverse + surprising_without_context + real_tradeoff

  - phase: Scenario
    construct: concrete scenarios probing edge cases
    targets:
      - partial failure + retry
      - migration + rollback
      - concurrent updates
      - deleted/archived/expired entities
      - permission + ownership boundaries
      - dependency degradation
      - unexpected scale changes
      - future feature pressure
    rule: "each scenario links to a specific decision"

  - phase: PreMortem
    assume: "plan is implemented and failed catastrophically"
    ask:
      - "most likely production failure mode?"
      - "if only one decision is wrong, which causes worst cascade?"
      - "what early warning signal reveals the wrong decision?"
    output: "record risks in decision log"

  - phase: Conclude
    when: decision tree fully resolved (all branches [RESOLVED])
    outputs:
      - decision_summary: all resolved decisions + accepted trade-offs
      - open_risks + mitigation strategies
      - glossary additions/updates
      - ADRs created or suggested
      - artifact: decision-log.md (format: references/decision-log.md)
    handoff_options:
      - to-brainstorm: "prompt user: ENTER BRAINSTORM MODE (default path after /init)"
      - to-prd: convert decisions to PRD (planned)
      - to-issues: split decisions to issues (planned)
      - dask-CS --light: lighter follow-up session
```

## Decision Tracking

```yaml
decision_states:
  - OPEN:      "identified but unresolved"
  - RESOLVED:  "agreed with explicit trade-off"
  - DEFERRED:  "intentionally postponed with trigger condition"
  - RISKY:     "accepted with known risk requiring monitoring"

progress_snapshot:
  available: on_user_request
  shows: "current decision tree with state markers + open boundaries"
```

## Evidence Hierarchy

```yaml
evidence_priority:
  1: production-grade open-source codebases with similar constraints
  2: official framework/language/database/cloud vendor docs
  3: research papers, RFCs, standards, formal design notes
  4: engineering blogs, conference talks, post-mortems from trusted teams
  5: community consensus signals (forums, GitHub issues, HN, Reddit)

calibration_rule: "state whether external example is truly comparable; never equate popularity with evidence"
```

## Documentation Capture

```yaml
capture_rules:
  when:
    - user explicitly requests
    - decision is crystallized with obvious persistence location
  convention: "follow project existing conventions; ask before creating new files"
  adr_creation:
    requires_all_three:
      - hard_to_reverse
      - surprising_without_context
      - real_tradeoff
```

## References

```yaml
references:
  - references/decision-log.md    # decision log format
  - references/pre-mortem.md      # pre-mortem method
  - references/downstream-skills.md  # downstream skill contracts (planned)
  - references/triggers.md        # trigger keywords per agent platform
```