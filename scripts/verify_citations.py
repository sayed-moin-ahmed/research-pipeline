#!/usr/bin/env python3
"""verify_citations.py — mechanical report <-> claim-ledger consistency check.

WHAT IT HONESTLY DOES (and does not)
    A skill cannot see the WebFetch calls a subagent made, so this does NOT prove a URL was fetched.
    What it CAN do — and what stops most "citation theater" — is check that the finished report is
    internally consistent with the claim ledger the run built:

      1. Every URL cited in the report appears in the ledger.       (no invented sources)
      2. Every ledger row backing a citation has a non-empty passage. (no empty-evidence rows)
      3. Report URLs are well-formed http(s).                        (no obvious junk)
      4. (Optional, --check-http) each cited URL is reachable now.   (catches typos/dead links;
                                                                       NOT proof it was read)

    Exit 0 = consistent. Exit 2 = problems found (printed). Exit 1 = usage/IO error.
    This is a guardrail, not a guarantee — see references/evidence-standards.md "Known limitations".

LEDGER FORMAT (ledger.json): a JSON list of rows, each with at least {"url": "...", "passage": "..."}.
USAGE
    verify_citations.py --report report.md --ledger ledger.json [--check-http] [--timeout 15]
"""
import argparse
import json
import re
import sys
import urllib.request

URL_RE = re.compile(r'https?://[^\s)\]<>"]+')


def report_urls(text):
    # strip trailing punctuation that markdown commonly appends
    return sorted({u.rstrip('.,;') for u in URL_RE.findall(text)})


def load_ledger(path):
    data = json.load(open(path, encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("ledger.json must be a JSON list of rows")
    return data


def http_ok(url, timeout):
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "Mozilla/5.0 (research-pipeline verifier)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return 200 <= r.status < 400
    except Exception:
        # some servers reject HEAD; try a light GET
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return 200 <= r.status < 400
        except Exception:
            return False


def main():
    ap = argparse.ArgumentParser(description="report <-> ledger citation consistency check")
    ap.add_argument("--report", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--check-http", action="store_true", help="also check each cited URL is reachable")
    ap.add_argument("--timeout", type=int, default=15)
    a = ap.parse_args()

    try:
        text = open(a.report, encoding="utf-8").read()
        ledger = load_ledger(a.ledger)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    ledger_by_url = {}
    for row in ledger:
        u = (row.get("url") or "").rstrip('.,;')
        if u:
            ledger_by_url.setdefault(u, row)

    problems = []
    rurls = report_urls(text)
    if not rurls:
        problems.append("report contains no cited URLs at all")

    for u in rurls:
        if not re.match(r'https?://\S+\.\S+', u):
            problems.append(f"malformed URL cited: {u}")
            continue
        row = ledger_by_url.get(u)
        if row is None:
            problems.append(f"cited URL not in ledger (possible fabrication): {u}")
        elif not (row.get("passage") or "").strip():
            problems.append(f"cited URL has empty ledger passage (no real evidence): {u}")

    if a.check_http:
        for u in rurls:
            if re.match(r'https?://\S+\.\S+', u) and not http_ok(u, a.timeout):
                problems.append(f"cited URL not reachable (dead/typo/blocked): {u}")

    print(f"report URLs: {len(rurls)} | ledger URLs: {len(ledger_by_url)} | "
          f"http-checked: {a.check_http}")
    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        sys.exit(2)
    print("\nPASS — every cited URL maps to a ledger row with a real passage.")
    sys.exit(0)


if __name__ == "__main__":
    main()
