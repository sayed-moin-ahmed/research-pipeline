# research-pipeline — evidence standards, high-stakes handling, and known limitations

"Prefer primary sources" is too blunt to be a universal rule: a primary source can be biased, obsolete,
or self-serving, and in some domains a good secondary source (a systematic review, a court's summary)
outranks any single primary one. Pick the ladder that fits the topic **before** FAN-OUT and put it in the
shared research brief so every worker applies the same bar.

## Domain evidence ladders (strongest first)

| Domain | Evidence ladder (prefer higher) | Watch out for |
|---|---|---|
| **Medicine / health** | Systematic reviews & meta-analyses → large RCTs → small RCTs → cohort/observational → case reports → expert opinion. Regulatory assessments (EFSA/FDA) are strong. Discover papers with Elicit's systematic-review flow (`elicit.com/solutions/systematic-review`) / Consensus / PubMed, then read the primary source. | Single small studies overhyped in press; industry-funded trials; healthy-user bias; surrogate endpoints; citing an aggregator's summary instead of the paper. |
| **Science / engineering** | Peer-reviewed replications → peer-reviewed primary → preprints (arXiv) → reputable technical blogs → vendor docs. Use Elicit / Semantic Scholar / arXiv for discovery, then open the paper itself. | Preprints ≠ peer-reviewed; irreproducible single results; benchmarks run by the seller. |
| **Companies / markets** | Regulatory filings (10-K/S-1) → audited financials → reputable financial press → analyst notes → company blog/PR. | PR framing; TAM inflation; paid "research"; numbers with no defined methodology. |
| **Law / policy** | Statutes & the ruling text itself → official regulator guidance → law-firm analysis → news. Jurisdiction + currentness are decisive. | Outdated/overturned rulings; wrong jurisdiction; secondary summaries that drop nuance. Not legal advice. |
| **Software / tech choice** | Official docs & source code → neutral benchmarks (methodology published) → named production case studies → practitioner posts → vendor benchmarks. Reach docs via Context7 MCP, read source on GitHub, prefer published-methodology benchmarks (e.g. TechEmpower). | Vendor-vs-vendor benchmarks (label the affiliation); version drift; benchmark ≠ your workload. |
| **News / current events** | Primary documents & on-record statements → multiple independent outlets → single outlet → social media. | Single-source scoops; syndication counted as corroboration; anonymous claims. |

When a topic spans domains, apply each domain's ladder to its part.

## High-stakes handling (medical, legal, financial, safety, security)

For these, tighten everything and be explicit about limits:

- Hold to the **top of the evidence ladder**; a single blog is not acceptable support for a load-bearing
  medical/legal/financial claim.
- Add a plain disclaimer that the report is **research, not professional advice**, and recommend a
  qualified professional for decisions with real consequences.
- Prefer **official / regulatory** sources and note their jurisdiction and date.
- If asked to research something enabling clear harm (weapons, self-harm methods, targeting a private
  individual, circumventing security controls), decline that part and say why — the pipeline is for
  legitimate research.

## Known limitations (what this skill does NOT solve — say so, don't fake it)

Being honest about the boundary is part of trustworthiness. This skill is an LLM instruction set, not a
deterministic data pipeline, so it deliberately does **not**:

- **Cryptographically prove a citation was fetched.** `verify_citations.py` checks report ↔ ledger
  consistency (every citation maps to a ledger row with a real passage); it cannot see the original
  HTTP calls. The passage-in-ledger discipline is the mitigation, not a guarantee.
- **Guarantee search coverage.** Fan-out reduces but does not eliminate search-engine bias, English-
  language bias, and popularity bias. Disclose the source restrictions you applied as a limitation.
- **Extract non-web evidence robustly.** PDFs, datasets, court records, patents, images, and archived
  pages may need tools/skills this pipeline doesn't provide; note when a key source was inaccessible.
- **Verify heavy numerical/statistical work.** It sanity-checks obvious unit/denominator/percentage-point
  errors, but it is not a statistics engine — flag calculations a domain expert should re-derive.
- **Replace a domain expert** on specialist appraisal. Surface uncertainty; don't manufacture confidence.

Naming these in the report's caveats section is expected, not a weakness.
