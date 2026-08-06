#!/usr/bin/env python3
"""Step 13 live lab: the anchor and the frozen node.

No dependencies, no network, standard library only. Reconstructs the
step-13 runbook library as a sealed governance graph, scaled down to
seven files so the whole state fits on one screen.

Three loops -- link, owner, freshness -- each read `catalogue.yaml` and
each check a different property of everything the catalogue lists. They
also cross-check one another: none of them reports green unless all
three examined the same number of runbooks. In this planted scenario
every one of those reports is truthful and every cross-check passes.

The catalogue is nonetheless missing one entry. `payments-failover` sits
on disk and has for a year; a cleanup commit dropped it from the list.
No loop reads the directory, so no loop, and no fourth loop watching the
first three, can possibly notice.

The anchor is the directory listing itself: a value no loop in this
system wrote and none of them can arrange to agree with. The frozen node
is the ninety-day review window -- the rule the freshness loop is judged
against, which the freshness loop is not permitted to widen in order to
report green.

Exits 1 if the anchor comparison fails to surface the planted omission,
if the inter-loop cross-check does not pass (which would mean the sealed
scenario was never actually set up), or if a loop is allowed to write to
the frozen review window. Exits 0 when all three hold.
"""

import sys

# The anchor. Stands in for a real directory listing: produced outside
# the loop system, not authored by any loop, not reachable by any of
# them. This is the only input here that nothing in the system shaped.
RUNBOOKS_ON_DISK = (
    "cache-eviction-storm",
    "cert-rotation",
    "db-failover",
    "dns-propagation-stall",
    "payments-failover",
    "queue-backpressure",
    "region-evacuation",
)

# What the catalogue claims. One real file is missing from it.
CATALOGUE = (
    "cache-eviction-storm",
    "cert-rotation",
    "db-failover",
    "dns-propagation-stall",
    "queue-backpressure",
    "region-evacuation",
)

# Rules the loops are judged against. Frozen keys may not be rewritten
# by any loop, at any budget, for any reason -- including the reason
# that rewriting one would turn a failing check green.
RULES = {"review_window_days": 90}
FROZEN_RULE_KEYS = frozenset({"review_window_days"})


def loop_report(loop_name, catalogue):
    """Each loop examines exactly what the catalogue lists, and each is
    entirely truthful about what it examined."""
    return {
        "loop": loop_name,
        "examined": len(catalogue),
        "failures": 0,
    }


def cross_check(reports):
    """The check the three loops run on each other: do all three agree
    on how many runbooks exist, and does anyone report a failure?"""
    counts = {report["examined"] for report in reports}
    failures = sum(report["failures"] for report in reports)
    return len(counts) == 1 and failures == 0


def anchor_check(catalogue, on_disk):
    """Compare the catalogue against the anchor. Returns the runbooks
    present in unmanipulated reality but absent from every loop's view."""
    return sorted(set(on_disk) - set(catalogue))


def request_rule_write(loop_name, key, new_value, rules, frozen_keys):
    """A loop asking to change a rule it is judged by. Refused outright
    when the key is frozen; the rules dict is never touched."""
    if key in frozen_keys:
        return False, (
            f"{loop_name} may not write '{key}' -- frozen node, current value "
            f"{rules[key]}, requested {new_value}"
        )
    rules[key] = new_value
    return True, f"{loop_name} set '{key}' to {new_value}"


def main():
    reports = [loop_report(name, CATALOGUE) for name in ("link", "owner", "freshness")]

    print("what each loop reported (all three read catalogue.yaml):")
    for report in reports:
        print(
            f"  {report['loop']:<9} examined {report['examined']} runbooks, "
            f"{report['failures']} failures"
        )

    internally_consistent = cross_check(reports)
    print(f"\ninter-loop cross-check passes: {internally_consistent}")
    print("  (every report agrees with every other report, and all are truthful)")

    missing = anchor_check(CATALOGUE, RUNBOOKS_ON_DISK)
    print(f"\nanchor: {len(RUNBOOKS_ON_DISK)} runbook files present outside the loop system")
    print(f"catalogue claims: {len(CATALOGUE)}")
    if missing:
        print("anchor comparison found, in no loop's field of view:")
        for name in missing:
            print(f"  {name}")
    else:
        print("anchor comparison found nothing")

    allowed, message = request_rule_write(
        "freshness", "review_window_days", 365, RULES, FROZEN_RULE_KEYS
    )
    print(f"\nfrozen-node test: {message}")
    print(f"review window after the request: {RULES['review_window_days']} days")

    try:
        assert internally_consistent, (
            "the three loops did not agree, so this run never demonstrated the "
            "thing it exists to demonstrate -- a system that is wrong while "
            "every internal check passes"
        )
        assert missing == ["payments-failover"], (
            f"the anchor comparison returned {missing!r}; it must surface "
            "payments-failover, the runbook that is real on disk and invisible "
            "to every loop, because nothing inside the loop system ever can"
        )
        assert not allowed, (
            "a loop was permitted to widen the review window it is judged "
            "against -- with that write allowed, a stale runbook can be made "
            "compliant by moving the standard instead of reviewing the runbook"
        )
        assert RULES["review_window_days"] == 90, (
            "the frozen review window changed value despite the write being "
            "refused"
        )
    except AssertionError as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        "\nPASS: all three loops agreed and all three were wrong; the anchor "
        "named payments-failover from outside the system, and the frozen "
        "review window survived a loop's attempt to widen it."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
