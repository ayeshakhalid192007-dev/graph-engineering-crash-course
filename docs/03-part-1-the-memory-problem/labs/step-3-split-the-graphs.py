#!/usr/bin/env python3
"""Step 3 live lab: split the graphs.

No dependencies, no network, standard library only. Builds a tiny
work-history list and a tiny fact list for the PR #391 / calculateDiscount
scenario from step-3, then naively merges them into one flat list the way a
team tempted to "save a step" might. Asserts -- and prints -- exactly what
that naive merge loses: once merged, the confirmed fact and the unverified
event it came from are indistinguishable strings, so there is no way left
to ask "was this ever independently checked, or did we only ever take one
agent's word for it."

Exits 0 once the demonstration has run and printed the corruption -- that
corruption is the lesson, not a bug in this script.
"""

import sys

CLAIM_TEXT = "calculateDiscount has no null check on customer.tier"

work_history = [
    {
        "agent": "Agent-Static",
        "event": "reviewed PR #391",
        "claim": CLAIM_TEXT,
    },
]

facts = [
    {
        "claim": CLAIM_TEXT,
        "verified_by": "Agent-Auditor",
    },
]


def naive_merge(history, checked_facts):
    """The shortcut: keep only the claim text, drop everything else."""
    return [entry["claim"] for entry in history] + [entry["claim"] for entry in checked_facts]


def main():
    print("work-history graph:")
    for entry in work_history:
        print(f"  {entry}")

    print("fact graph:")
    for entry in facts:
        print(f"  {entry}")

    merged = naive_merge(work_history, facts)
    print("naive merge of both lists:")
    for line in merged:
        print(f"  {line}")

    # The corruption: both entries are now the identical claim string, with
    # no field left to say which one was ever independently verified.
    assert len(merged) == 2, "expected exactly one work-history entry and one fact entry"
    assert merged[0] == merged[1] == CLAIM_TEXT, (
        "expected both merged entries to read identically once flattened to plain strings"
    )
    assert all(isinstance(entry, str) for entry in merged), (
        "expected the merge to have discarded the agent/verified_by structure, leaving plain text"
    )

    print(
        "PASS: naive merge loses the claim-vs-fact distinction -- "
        "the two merged lines are indistinguishable, so a later reader can no "
        "longer tell 'Agent-Static flagged this' apart from "
        "'Agent-Auditor independently confirmed this is true'."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
