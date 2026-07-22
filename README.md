# research-pipeline

A Claude Code **agent skill** that produces rigorous, verified, fully-cited research reports on **any topic** by running a disciplined five-stage pipeline:

```
CLARIFY → PLAN (editable) → FAN-OUT (parallel subagents)
        → VERIFY (source-grounded · adversarial · cross-model)
        → SYNTHESIZE (cited report)      [checkpoint/resume throughout]
```

## Why it exists

Every serious research system (Anthropic's multi-agent Research, Google Deep Research, OpenAI Deep Research, GPT Researcher) is the same loop. This skill makes that loop explicit and adds a **layered verification discipline** so the product is a report you can *defend*, not a fast guess.

## What's inside

| File | Purpose |
|---|---|
| `SKILL.md` | The five-stage loop, the **claim-ledger backbone**, effort tiers, stop conditions, anti-patterns |
| `references/playbook.md` | Per-stage procedure, subagent brief, shared research brief, ledger format |
| `references/verification.md` | Source-grounded → adversarial → cross-model protocol (honest about what cross-model buys) |
| `references/evidence-standards.md` | Per-domain evidence ladders, high-stakes handling, known limitations |
| `references/report-template.md` | The cited-report structure |
| `scripts/checkpoint.py` | Self-describing resume state (`state.json`) |
| `scripts/verify_citations.py` | Mechanical report ↔ ledger consistency gate (anti "citation theater") |

## Key ideas

- **Claim ledger** — every load-bearing claim is a row (`claim → quoted passage → URL → date → status`). The report is generated *from* the ledger, and `verify_citations.py` checks they stay consistent.
- **Cross-model verification is an adjunct, not ground truth** — a different vendor re-reads your *digest*, not the live web, so it's a cheap hallucination-smell check layered on top of source-grounded verification.
- **Effort tiers** (quick / standard / deep) scale subagent count and verification depth to the stakes.
- **Graceful degradation** — cross-model CLIs are optional; a missing/blocked vendor never stalls a run.

## Install

Copy the `research-pipeline/` directory into `~/.claude/skills/`, or install the packaged `.skill` file.

## Provenance

Designed and hardened with cross-vendor review (codex + agy) on both the design and actual output reports.
