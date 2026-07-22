#!/usr/bin/env python3
"""checkpoint.py — self-describing research-pipeline state for resume-on-failure.

WHY THIS EXISTS
    Research runs are long and get interrupted (a subagent dies, the user pauses, the
    session ends). Without state, a resumed run redoes finished work — wasting tokens and
    time. This stores one JSON file per run so any future agent, with NO prior context, can
    read what's done and continue.

STATE SCHEMA (workspace/.research-pipeline/<slug>/state.json)
    {
      "slug": "ev-battery-suppliers",
      "question": "Who supplies EV batteries to European OEMs?",
      "tier": "standard",                  # quick | standard | deep
      "status": "in_progress",             # in_progress | complete
      "threads": {                         # one entry per PLAN sub-question
        "pricing":  {"status": "done",    "file": "findings/pricing.md"},
        "suppliers":{"status": "pending", "file": null}
      },
      "report": null                        # path to final report when complete
    }
    A thread status is one of: pending | in_progress | done.

USAGE
    checkpoint.py init   <slug> --question "..." [--tier standard] [--root <dir>]
    checkpoint.py plan   <slug> --thread pricing --thread suppliers      # register threads
    checkpoint.py save   <slug> --thread pricing --status done [--file findings/pricing.md]
    checkpoint.py status <slug>                                          # human-readable summary (read before fan-out)
    checkpoint.py get    <slug>                                          # raw JSON
    checkpoint.py done   <slug> --report report.md                      # mark run complete

    --root defaults to ./.research-pipeline ; state lives at <root>/<slug>/state.json
    Exit code 0 on success, 1 on error. `status` exits 0 even mid-run.

If Python is unavailable, maintain the same JSON by hand — the schema above is the contract.
"""
import argparse
import json
import os
import sys


def state_path(root: str, slug: str) -> str:
    return os.path.join(root, slug, "state.json")


def load(root: str, slug: str) -> dict:
    p = state_path(root, slug)
    if not os.path.exists(p):
        sys.stderr.write(f"no state for slug '{slug}' at {p}\n")
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def store(root: str, slug: str, data: dict) -> None:
    d = os.path.join(root, slug)
    os.makedirs(d, exist_ok=True)
    with open(state_path(root, slug), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def cmd_init(a):
    data = {
        "slug": a.slug,
        "question": a.question,
        "tier": a.tier,
        "status": "in_progress",
        "threads": {},
        "report": None,
    }
    store(a.root, a.slug, data)
    print(f"initialized run '{a.slug}' (tier={a.tier}) at {state_path(a.root, a.slug)}")


def cmd_plan(a):
    data = load(a.root, a.slug)
    for t in a.thread:
        data["threads"].setdefault(t, {"status": "pending", "file": None})
    store(a.root, a.slug, data)
    print(f"threads: {', '.join(data['threads'])}")


def cmd_save(a):
    data = load(a.root, a.slug)
    entry = data["threads"].setdefault(a.thread, {"status": "pending", "file": None})
    entry["status"] = a.status
    if a.file:
        entry["file"] = a.file
    store(a.root, a.slug, data)
    print(f"thread '{a.thread}' -> {a.status}" + (f" ({a.file})" if a.file else ""))


def cmd_status(a):
    data = load(a.root, a.slug)
    threads = data.get("threads", {})
    done = [t for t, v in threads.items() if v["status"] == "done"]
    pending = [t for t, v in threads.items() if v["status"] != "done"]
    print(f"run '{data['slug']}' | tier={data['tier']} | status={data['status']}")
    print(f"question: {data['question']}")
    print(f"done ({len(done)}): {', '.join(done) or '-'}")
    print(f"pending ({len(pending)}): {', '.join(pending) or '-'}")
    if data.get("report"):
        print(f"report: {data['report']}")


def cmd_get(a):
    print(json.dumps(load(a.root, a.slug), indent=2, ensure_ascii=False))


def cmd_done(a):
    data = load(a.root, a.slug)
    data["status"] = "complete"
    if a.report:
        data["report"] = a.report
    store(a.root, a.slug, data)
    print(f"run '{a.slug}' complete" + (f" -> {a.report}" if a.report else ""))


def main():
    p = argparse.ArgumentParser(description="research-pipeline checkpoint state")
    p.add_argument("--root", default=".research-pipeline", help="state root dir")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init"); pi.add_argument("slug"); pi.add_argument("--question", required=True); pi.add_argument("--tier", default="standard", choices=["quick", "standard", "deep"]); pi.set_defaults(func=cmd_init)
    pp = sub.add_parser("plan"); pp.add_argument("slug"); pp.add_argument("--thread", action="append", required=True); pp.set_defaults(func=cmd_plan)
    ps = sub.add_parser("save"); ps.add_argument("slug"); ps.add_argument("--thread", required=True); ps.add_argument("--status", default="done", choices=["pending", "in_progress", "done"]); ps.add_argument("--file"); ps.set_defaults(func=cmd_save)
    pst = sub.add_parser("status"); pst.add_argument("slug"); pst.set_defaults(func=cmd_status)
    pg = sub.add_parser("get"); pg.add_argument("slug"); pg.set_defaults(func=cmd_get)
    pd = sub.add_parser("done"); pd.add_argument("slug"); pd.add_argument("--report"); pd.set_defaults(func=cmd_done)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
