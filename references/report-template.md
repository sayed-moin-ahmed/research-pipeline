# research-pipeline — report template

The report is the product. Its job: give the reader the answer, then the evidence, then the honest limits.
Use this structure. Adapt section depth to the tier, but keep the order — readers who stop early should
still get the truthful bottom line.

```markdown
# <Research question, as a title>

**Scope:** <what was and wasn't covered> · **Tier:** <quick/standard/deep> · **As of:** <date> ·
**Sources consulted:** <n>

## Executive summary
<3–6 sentences. The direct answer. If the honest answer is "it depends" or "the evidence is mixed", say
that here, not buried below. State overall confidence in one phrase.>

## Key findings
Each finding: the claim, the evidence, an inline citation, and a confidence/verification tag.

1. **<Finding as a claim>.** <Supporting evidence, one or two sentences.> [1][2] *(verified)*
2. **<Finding>.** <Evidence.> [3] *(single-source — treat with caution)*
3. **<Finding>.** <Evidence.> [4][5] *(contested — sources disagree; see below)*
...

## Where sources disagree / caveats
<Surface contradictions honestly. Which side has better/more recent evidence, and why. Note anything that
failed adversarial or cross-model checks. If a vendor cross-check flagged a claim, say so.>

## What the evidence does NOT support / inference vs. fact
<Separate what the sources actually show from what you inferred. Mark inference clearly. Call out claims
you could not verify.>

## Open questions
<What a deeper pass should chase next. Be specific — these are researchable follow-ups, not hand-waving.>

## Weakest link
<The single claim or gap you'd most want a second pass on. This is the honest "push here" pointer.>

## Sources
[1] <Title> — <publisher/author>, <date>. <URL>   *(what it supports)*
[2] ...
<Only URLs you actually fetched and read. Note each source's date. No citation theater.>
```

## Notes on citations

- Number sources and reference them inline `[n]` at the exact claim they support — not a bibliography
  dump at the end with no in-text anchors.
- Every source listed must have been fetched and read during the run. If a claim rests on something you
  couldn't open, it is `[unverified]`, not a citation.
- Prefer primary sources; when citing a secondary source, prefer ones that themselves cite primaries.
- For quantitative claims, cite the source that *originated* the number, not an aggregator that repeats it.

## Optional: visual

If the topic is quantitative or comparative and a visual genuinely helps (a comparison matrix, a trend
chart, a landscape map), offer to render it as an Artifact. Keep it faithful to the cited data — a chart
is a claim too, and it inherits the same sourcing bar. Don't add visuals for decoration.
