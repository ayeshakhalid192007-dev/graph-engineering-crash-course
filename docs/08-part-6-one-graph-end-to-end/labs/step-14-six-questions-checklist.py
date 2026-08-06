#!/usr/bin/env python3
"""Step 14 live lab: the six-question pre-build checklist.

No dependencies, no network, standard library only. Encodes Step 14's
six honest questions as a small CLI-style checklist, runs it against
three planted situations, and asserts each one gets the verdict the
step page says it should get.

Each question is answered True when it points *toward* needing a graph
(real dependencies exist / material spans many sources / the
relationship set grows or varies / something downstream needs to trace
a claim to its source / the team can carry the upkeep / the domain
changes faster than a hand-edited table could track). The verdict is
"build a graph" only when every question points that way -- a single
"skip it" answer is disqualifying on its own, matching the step page's
point that this checklist is meant to say no more often than it says
yes.

Exits 1 if any of the three planted situations produces the wrong
verdict. Exits 0 when all three match what Step 14 claims about them.
"""

import sys

QUESTIONS = (
    "real_dependencies",     # pieces depend on each other, not independent
    "spans_many_sources",    # answer isn't sitting in one document
    "relationships_grow",    # relationship set isn't small & fixed
    "needs_provenance",      # something downstream must trace a claim to its source
    "team_can_maintain",     # a team exists to carry this as ongoing upkeep
    "domain_changes_fast",   # faster than a manually-edited table could track
)

SITUATIONS = {
    "independent-task-queue": {
        "description": (
            "Five independent customer-support tickets, each closed by a "
            "different agent, with no ticket depending on any other."
        ),
        "answers": {
            "real_dependencies": False,
            "spans_many_sources": False,
            "relationships_grow": False,
            "needs_provenance": False,
            "team_can_maintain": True,
            "domain_changes_fast": False,
        },
        "expected": False,
    },
    "single-document-question": {
        "description": (
            "Answering yes/no questions about the contents of one signed "
            "contract PDF."
        ),
        "answers": {
            "real_dependencies": False,
            "spans_many_sources": False,
            "relationships_grow": False,
            "needs_provenance": False,
            "team_can_maintain": True,
            "domain_changes_fast": False,
        },
        "expected": False,
    },
    "supplier-production-line-tracking": {
        "description": (
            "Tracking which of a factory's twelve suppliers feed parts into "
            "which of its six production lines, so a defective-batch "
            "complaint can be traced back to the supplying vendor; the "
            "supplier list turns over monthly as contracts change."
        ),
        "answers": {
            "real_dependencies": True,
            "spans_many_sources": True,
            "relationships_grow": True,
            "needs_provenance": True,
            "team_can_maintain": True,
            "domain_changes_fast": True,
        },
        "expected": True,
    },
}


def verdict(answers):
    """Build a graph only if every question points that direction. Return
    the verdict plus the first question (in fixed order) that says no,
    so a "skip it" result always names what decided it."""
    for question in QUESTIONS:
        if not answers[question]:
            return False, question
    return True, None


def main():
    print("Step 14 checklist -- six questions, three planted situations\n")

    results = {}
    for name, situation in SITUATIONS.items():
        build, deciding_question = verdict(situation["answers"])
        results[name] = build
        label = "build a graph" if build else "skip it"
        print(f"{name}:")
        print(f"  {situation['description']}")
        print(f"  verdict: {label}", end="")
        if deciding_question:
            print(f"  (decided by: {deciding_question})")
        else:
            print("  (all six questions pointed this way)")
        print()

    try:
        for name, situation in SITUATIONS.items():
            assert results[name] == situation["expected"], (
                f"{name}: expected verdict {situation['expected']!r}, "
                f"got {results[name]!r}"
            )
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)

    print(
        "PASS: independent tasks and a single document both correctly "
        "skip it, and the growing multi-source tracking problem correctly "
        "builds a graph."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
