# Pre-Mortem Method

> Assume plan is implemented and failed catastrophically. Work backwards to discover risks that forward planning misses.

```yaml
when: after core decisions resolved, before session concludes
skip: never (medium/deep sessions)
```

## Flow

```yaml
step_1_set_scene:
  prompt: "It's six months later. The system is live and failing badly. What happened?"

step_2_generate_failures:
  target: 3-5 failure modes
  format:
    columns: [failure_mode, probable_cause, early_warning_signal, prevention]
  priority:
    - cascade_failure: "one bad decision breaks multiple subsystems"
    - silent_failure: "system appears normal but produces wrong results"
    - scale_failure: "works small, collapses at scale"

step_3_identify_weakest:
  question: "If only one decision from this session is wrong, which causes the most damage?"
  action: "mark that decision [RISKY] in decision log + add monitoring/mitigation"

step_4_extract_risks:
  output: risk register entries
  fields:
    severity: high (system down) | medium (degraded) | low (inconvenience)
    trigger: "when monitoring escalates to action"
    owner: "who watches this risk"
```

## Example

```yaml
example:
  failure_mode: "duplicate charges under high load"
  probable_cause: "chose optimistic concurrency for payment gateway (D3) without idempotency keys"
  early_warning: "duplicate charge rate > 0.01%"
  prevention: "add idempotency keys before launch; monitor charge uniqueness"
```

## Rules

```yaml
rules:
  - reject vague risks like "performance issues" — demand specifics
  - every risk links to a specific decision in this session
  - if a risk has no mitigation → decision stays [OPEN] not [RESOLVED]
  - pre-mortem is not pessimism — it makes the plan resilient enough for reality
```