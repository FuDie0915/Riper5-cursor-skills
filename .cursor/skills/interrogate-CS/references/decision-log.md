# Decision Log Format

> `grill-me` session artifact. Consumed by downstream skills (`to-prd`, `to-issues`).

```yaml
artifact:
  file: decision-log.md
  location: docs/ (fallback: project root)
  captures: resolved decisions + context + downstream impact

template:
  header:
    title: "Decision Log — {session title}"
    date: YYYY-MM-DD
    topic: "{brief description}"
    depth: light | medium | deep
    status: complete | partial  # note which branches remain open

  decisions:
    - id: "D{n}"
      title: "{decision title}"
      status: "[RESOLVED]" | "[DEFERRED]" | "[RISKY]"
      question: "{exact question asked}"
      answer: "{agreed answer}"
      trade_off_accepted: "{cost/risk/constraint accepted}"
      local_evidence: "{codebase findings, or 'none'}"
      external_evidence: "{engineering precedents consulted, or 'none'}"
      terms_defined: "{glossary terms resolved by this decision}"
      downstream_impact: "{which later decisions depend on this}"

  risk_register:
    columns: [id, risk, severity, mitigation, owner]
    severity_levels: [high, medium, low]

  terminology:
    columns: [term, definition, alias_or_avoid]

  adrs_created:
    - "docs/adr/XXXX-{slug}.md — {title}"

  open_questions_deferred:
    - "{question} — deferred until {trigger_condition}"

  handoff:
    recommended_next: to-prd | to-issues | grill-me --light | none
    key_context: "{critical info for downstream implementer}"
```

## Rules

```yaml
rules:
  - assign stable IDs (D1, D2, ...) for downstream reference
  - preserve exact question + answer, not summaries — summaries lose nuance
  - record trade-offs explicitly — most important field
  - mark decisions with downstream dependencies — forms tree structure
  - separate risks from decisions — a decision can be correct yet risky
  - deferred decisions must have trigger conditions, not "later"
```