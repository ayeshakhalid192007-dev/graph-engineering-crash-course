#!/usr/bin/env python3
"""Step 16 live lab: the four skip-it patterns as a decision function.

No dependencies, no network, standard library only. Encodes Step 16's four
recognizable situations -- independent tasks, a single-document question, a
small fixed relationship set, and no downstream need for provenance -- as a
small decision function, runs it against four planted Fernbank-style
situations plus one control situation that should actually build a graph,
and asserts each one gets the verdict the step page says it should get.

Each situation is described by four booleans, each one True when that
property points *toward* needing a graph:

  depends_on_others   -- the pieces have real dependencies, not just
                          proximity (False -> use a queue)
  spans_many_sources  -- the honest answer isn't sitting inside one document
                          (False -> use a good prompt)
  relationships_grow  -- the relationship set isn't small and essentially
                          fixed (False -> use a relational table)
  needs_provenance    -- something downstream will actually need to trace a
                          claim back to where it came from (False -> skip
                          structured tracking entirely)

The decision function checks these in the same order Step 16 presents them
and stops at the first one that says "skip it," naming both the verdict and
the matching lighter-weight alternative. A situation only reaches "build a
graph" if all four point that direction.

Exits 1 if any of the five planted situations produces the wrong verdict or
the wrong alternative. Exits 0 when all five match what Step 16 claims.
"""

import sys

SITUATIONS = {
    "independent-shift-roster": {
        "description": (
            "Twelve open Saturday shifts at a tool library, each claimed "
            "first-come-first-served, with no shift's coverage depending "
            "on any other shift being filled."
        ),
        "flags": {
            "depends_on_others": False,
            "spans_many_sources": False,
            "relationships_grow": False,
            "needs_provenance": False,
        },
        "expected_verdict": "skip",
        "expected_alternative": "queue",
    },
    "single-document-waiver": {
        "description": (
            "Whether clause four of one donated liability-waiver PDF "
            "covers a borrowed table saw -- a single yes/no read of one "
            "document."
        ),
        "flags": {
            "depends_on_others": True,
            "spans_many_sources": False,
            "relationships_grow": False,
            "needs_provenance": False,
        },
        "expected_verdict": "skip",
        "expected_alternative": "prompt",
    },
    "fixed-orientation-pairing": {
        "description": (
            "Which of four tool categories requires which of two "
            "orientation sessions -- a pairing that has changed once in "
            "three years."
        ),
        "flags": {
            "depends_on_others": True,
            "spans_many_sources": True,
            "relationships_grow": False,
            "needs_provenance": False,
        },
        "expected_verdict": "skip",
        "expected_alternative": "table",
    },
    "who-has-what-scrap-log": {
        "description": (
            "A desk log of which borrower currently has which tool, reset "
            "fresh most weekends, where nobody has ever needed to trace a "
            "loan back to a specific date."
        ),
        "flags": {
            "depends_on_others": True,
            "spans_many_sources": True,
            "relationships_grow": True,
            "needs_provenance": False,
        },
        "expected_verdict": "skip",
        "expected_alternative": "no provenance needed",
    },
    "insurer-required-maintenance-chain": {
        "description": (
            "Control situation: tracing a damaged tool back through every "
            "borrower who has had it, because the library's insurer now "
            "requires a proof-of-chain before covering a replacement."
        ),
        "flags": {
            "depends_on_others": True,
            "spans_many_sources": True,
            "relationships_grow": True,
            "needs_provenance": True,
        },
        "expected_verdict": "build",
        "expected_alternative": None,
    },
}


def decide(flags):
    """Return (verdict, alternative, deciding_condition).

    Checks the four conditions in Step 16's order and stops at the first
    one that says "skip it." Only recommends building a graph if every
    condition points that way.
    """
    if not flags["depends_on_others"]:
        return "skip", "queue", "depends_on_others"
    if not flags["spans_many_sources"]:
        return "skip", "prompt", "spans_many_sources"
    if not flags["relationships_grow"]:
        return "skip", "table", "relationships_grow"
    if not flags["needs_provenance"]:
        return "skip", "no provenance needed", "needs_provenance"
    return "build", None, None


def main():
    print("Step 16 decision aid -- four skip-it patterns, five situations\n")

    failures = []
    for name, situation in SITUATIONS.items():
        verdict, alternative, deciding = decide(situation["flags"])
        print(f"{name}:")
        print(f"  {situation['description']}")
        if verdict == "skip":
            if alternative == "no provenance needed":
                print(f"  verdict: skip it -- {alternative}  (decided by: {deciding})")
            else:
                print(f"  verdict: skip it -- use a {alternative}  (decided by: {deciding})")
        else:
            print("  verdict: build a graph  (all four conditions pointed this way)")
        print()

        if verdict != situation["expected_verdict"]:
            failures.append(
                f"{name}: expected verdict {situation['expected_verdict']!r}, got {verdict!r}"
            )
        if alternative != situation["expected_alternative"]:
            failures.append(
                f"{name}: expected alternative {situation['expected_alternative']!r}, "
                f"got {alternative!r}"
            )

    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    print(
        "PASS: all four skip-it situations resolved to the correct lighter-weight "
        "alternative, and the control situation correctly resolved to build a graph."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
