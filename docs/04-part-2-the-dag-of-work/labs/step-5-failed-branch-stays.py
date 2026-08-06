#!/usr/bin/env python3
"""Step 5 live lab: failed branch stays queryable.

No dependencies, no network, standard library only. Models the step-5
webhook-double-fulfillment scenario as three fix-attempt nodes connected to
one bug node by a tried_for edge -- two attempts marked failed, one marked
abandoned. Runs the same query a fourth agent would run before proposing a
new fix ("what's already been tried for this bug") and checks that both
failed attempts are still present in the result, exactly as if nothing had
ever been deleted.

Exits 1 if either failed attempt is missing from the query result (the
node was deleted or the query silently filtered it out). Exits 0 if both
failed attempts -- and the abandoned one -- all come back intact.
"""

import sys

BUG_ID = "bug-double-fulfillment"

# Every attempt node carries a status: failed, abandoned, or (not modeled
# here) succeeded. None of that status information causes a node to be
# excluded from the graph -- it's just a field on the node.
attempts = [
    {
        "id": "attempt-a",
        "agent": "Agent-A",
        "approach": "in-memory dedupe cache keyed by event ID",
        "status": "failed",
        "reason": "no shared state across load-balanced replicas",
        "tried_for": BUG_ID,
    },
    {
        "id": "attempt-b",
        "agent": "Agent-B",
        "approach": "database uniqueness constraint on event ID",
        "status": "failed",
        "reason": "constraint checked after fulfillment side effects already ran",
        "tried_for": BUG_ID,
    },
    {
        "id": "attempt-c",
        "agent": "Agent-C",
        "approach": "reorder side effects to run after the constraint check",
        "status": "abandoned",
        "reason": "session ended before the fix was tested",
        "tried_for": BUG_ID,
    },
]


def query_tried_for(nodes, bug_id):
    """What Agent-D runs before proposing a new fix.

    Deliberately does not filter on status -- a query that excluded failed
    or abandoned attempts would recreate the exact problem this Step
    exists to prevent.
    """
    return [node for node in nodes if node["tried_for"] == bug_id]


def main():
    print(f"querying tried_for({BUG_ID}):")
    result = query_tried_for(attempts, BUG_ID)
    for entry in result:
        print(
            f"  {entry['id']} ({entry['agent']}): {entry['approach']} "
            f"-- status: {entry['status']} ({entry['reason']})"
        )

    result_ids = {entry["id"] for entry in result}
    failed_ids = {a["id"] for a in attempts if a["status"] == "failed"}

    try:
        missing = failed_ids - result_ids
        assert not missing, f"failed attempt(s) missing from query result: {sorted(missing)}"
        assert len(result) == len(attempts), (
            "expected the query to return every attempt tried for this bug, "
            "abandoned attempts included, not just the failed ones"
        )
    except AssertionError as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        f"\nPASS: all {len(failed_ids)} failed attempt(s) and the abandoned attempt "
        "are still present in the query result -- nothing was deleted, so Agent-D "
        "can see the full trail before proposing a fourth fix."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
