# research-pipeline — verification protocol

Verification is what makes this a *research* pipeline and not a summarizer. Spend the effort on the
**load-bearing claims** — the ones the conclusion rests on. A decorative background fact doesn't need a
skeptic; the number your recommendation hinges on does. All verification runs against the **claim ledger**
(see `playbook.md`): `claim | quoted passage | URL | date(s) | independence | status`.

Order of trust, strongest first: **(1) source-grounded** → **(2) adversarial** → **(3) cross-model**.
The first is primary and non-negotiable; the third is a cheap adjunct, not proof.

## Check 1 — Source-grounded (always; this is the real gate)

For each load-bearing claim:

1. **Did you actually fetch the page?** If the passage came from a search-result snippet and you never
   opened the page, that is not a citation — open it or mark the claim `unverified`. This is the single
   most common failure and the reason the ledger stores a *quoted passage*, not a paraphrase.
2. **Does the passage actually support the claim?** Re-read it. "Real URL but irrelevant passage" is a
   citation that lies. The quote in the ledger must contain the fact the claim asserts.
3. **Is the source *metadata* right?** Take the author, venue, and year from the **page itself**, not from
   memory — a correct URL with correct numbers but a wrong author name is a real, common defect (e.g.
   crediting a study to the wrong first author). Confirm the byline on the page.
4. **Is the support independent?** See below.

Set the ledger `status`: `verified` (≥2 independent sources, passages check out), `single-source`,
`contested`, or `unverified`. A claim that can't reach at least `single-source` with a real passage does
not appear as a sourced statement in the report.

### What "independent" means (not just "two URLs")

Two links are **not** independent if they trace to the same origin — same wire story, same press
release, same underlying paper or dataset, same author, same funder. Modern web content syndicates
heavily, so three blogs repeating one press release is **one** source, not three. Dedupe by **canonical
origin**: trace each claim to where the information was first produced and count origins, not URLs. When
a whole cluster of sources cites one study, treat the study as the source and read *it*. Flag when key
sources share funding or authorship (especially vendor benchmarks — the vendor's own numbers are
evidence about the vendor, not a neutral finding).

### Temporal check — which date?

"Source date" is ambiguous and the ambiguity causes errors. For each source record what's relevant:
**publication date**, the **event/data-period** it describes, and **last-updated**. A 2021 article and a
2025 article can silently "corroborate" a claim about 2026 that neither actually supports. For
fast-moving topics, anchor claims to an explicit **"as of <date>"** and flag stale sources rather than
blending them.

## Check 2 — Adversarial (Standard tier and up, on top claims)

For the top 3–5 load-bearing claims, dispatch a **skeptic subagent** whose job is to *refute with
evidence*, not argue rhetorically. A skeptic that only reasons in the abstract is performative; require
it to go find things:

```
Try to REFUTE this claim: "<claim>" (currently supported by: <quoted passage + source>).
Search for and FETCH disconfirming evidence: contrary primary sources, methodological flaws in the
support, missing baselines/controls, more recent data that overturns it, or context that changes its
meaning. Do not argue from reasoning alone — cite what you found (with URLs and quoted passages).
Return: verdict (holds | weakened | refuted), the strongest counter-evidence (source + passage), and
what would have to be true for the original claim to stand.
```

- **holds** → keep it. **weakened** → soften wording, note the caveat *on the claim* (not buried later).
- **refuted** → remove it, or invert it if the counter-evidence is well-sourced.

Deep tier, high stakes: run several skeptics on the same top claim and take the majority.

## Check 3 — Cross-model (Deep tier, or when the user asks to "revalidate across vendors")

Different vendors' models fail differently, so a non-Claude model can catch a Claude-specific
hallucination. Useful — but **be honest about what it is**: the other model re-reads your *claims
digest*, it does **not** re-scrape the live web. So agreement means "this reads as internally
consistent / not obviously hallucinated to another model", **not** "this is independently confirmed
true". If your Stage-3 digest carried a syndicated error in, cross-model will happily rubber-stamp it.
It is a cheap hallucination-smell check layered on top of real source-grounded verification — never a
substitute for it.

Prefer the `triangulate` skill if available (it wraps this and reconciles via `advisor()`). Otherwise
run the two most reliable CLIs **in parallel**, with a timeout, stdin closed, and graceful fallback:

```bash
# Build a compact numbered claims digest (claim + its source + the quoted passage), then:
timeout 420 codex exec --skip-git-repo-check "Fact-check this research digest. For each numbered claim say
SUPPORTED / DUBIOUS / WRONG and why; flag anything that smells hallucinated or lacks a credible source.
Be blunt.\n\n<digest>" </dev/null

timeout 420 agy -p "Fact-check this research digest. For each numbered claim say SUPPORTED / DUBIOUS /
WRONG and why; flag anything hallucinated or weakly sourced. Be blunt.\n\n<digest>" </dev/null
```

- **Environment reality:** these CLIs may be missing, unauthenticated, sandboxed-off, or slow. Cross-model
  is **optional** — if a CLI errors or times out, note it and proceed on Checks 1–2; never let it stall
  the run. `gemini` is a nice-to-have third opinion but its free tier has failed with quota errors — do
  not depend on it. Two vendors (codex + agy) is plenty.
- **Privacy:** the digest leaves the session for another provider. Don't send private/sensitive material
  through cross-model without the user's ok.
- **Reconcile:** flagged DUBIOUS/WRONG by **both** vendors → high priority, re-verify against sources or
  drop. Flagged by **one** → low-confidence, sanity-check yourself. If a vendor contradicts your fetched
  primary source, **the source wins** — the model may be running on stale training data. Surface the
  conflict; don't silently flip.

## Output of verification

The ledger, with every load-bearing row's `status` set and cross-model verdicts noted where Check 3 ran.
This tagged ledger — not the raw search hits — is the input to SYNTHESIZE.
