#!/usr/bin/env python3
"""Step 11 live lab: the governance graph.

No dependencies, no network, standard library only. Builds the step-11
content-publishing pipeline as an actual structure: three loop nodes
(drafting, review, escalation) joined by labelled edges -- `feeds`,
`checks`, and `can-overrule`.

The point of the lab is that "escalation can overrule review" has to be
a real edge you can find by walking the graph, not a sentence in a
design doc. So the lab does three things:

  1. looks the authority edge up in the edge list;
  2. runs a topological sort over the `can-overrule` subgraph and
     reports the resulting authority ranking, which also proves the
     authority relation is acyclic (a ring of overrule edges cannot
     rank anyone, so it cannot resolve anything);
  3. replays article A-311, which carries two conflicting stamps, and
     resolves it from the ranking rather than from the timestamps --
     the timestamps deliberately favour the losing verdict.

Exits 1 if the authority edge is absent, if the overrule edges contain a
cycle, or if the resolver returns anything other than escalation's
`hold-for-editor` verdict. Exits 0 when all three hold.
"""

import sys

LOOPS = ["drafting", "review", "escalation"]

# (source, label, target). Only `can-overrule` carries authority; the
# other two labels describe data flow and judgement, which is exactly
# why neither of them can settle a conflict on its own.
EDGES = [
    ("drafting", "feeds", "review"),
    ("drafting", "feeds", "escalation"),
    ("review", "checks", "drafting"),
    ("escalation", "checks", "review"),
    ("escalation", "can-overrule", "review"),
]

# Two verdicts on one article node. Note the clock: the verdict that
# must win landed *first*, so resolving by recency gives the wrong
# answer here -- which is the point of using this article as the case.
A311_STAMPS = [
    {"loop": "escalation", "verdict": "hold-for-editor", "at": "09:14:22"},
    {"loop": "review", "verdict": "approved", "at": "09:14:41"},
]


def authority_edges(edges):
    return [(s, t) for (s, label, t) in edges if label == "can-overrule"]


def outranks(source, target, edges):
    """True if `source` can overrule `target`, directly or by following
    a chain of can-overrule edges."""
    pairs = authority_edges(edges)
    frontier = [source]
    seen = {source}
    while frontier:
        current = frontier.pop()
        for a, b in pairs:
            if a == current and b not in seen:
                if b == target:
                    return True
                seen.add(b)
                frontier.append(b)
    return False


def rank_authority(loops, edges):
    """Kahn's algorithm over the can-overrule subgraph. Returns a list
    ordered from most authority to least. Raises ValueError if the
    authority edges form a cycle, because a cyclic ranking cannot
    resolve a disagreement -- it just returns you to where you started.
    """
    pairs = authority_edges(edges)
    incoming = {loop: 0 for loop in loops}
    outgoing = {loop: [] for loop in loops}
    for source, target in pairs:
        outgoing[source].append(target)
        incoming[target] += 1

    ready = sorted(loop for loop in loops if incoming[loop] == 0)
    order = []
    while ready:
        loop = ready.pop(0)
        order.append(loop)
        for target in outgoing[loop]:
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
        ready.sort()

    if len(order) != len(loops):
        unranked = sorted(set(loops) - set(order))
        raise ValueError(
            "can-overrule edges form a cycle among " + ", ".join(unranked)
        )
    return order


def resolve(stamps, edges, ranking):
    """Pick the winning verdict by authority. Never looks at 'at'.

    Returns (None, reason) when the governance graph has no authority
    edge relating the two loops -- a gap to be filled deliberately, not
    a place to fall back on a timestamp."""
    if len({s["verdict"] for s in stamps}) == 1:
        return stamps[0]["verdict"], "no disagreement"

    ordered = sorted(stamps, key=lambda s: ranking.index(s["loop"]))
    winner, runner_up = ordered[0], ordered[1]
    if not outranks(winner["loop"], runner_up["loop"], edges):
        return None, (
            f"no authority edge relates {winner['loop']} and {runner_up['loop']}"
        )
    return winner["verdict"], f"{winner['loop']} outranks {runner_up['loop']}"


def main():
    print("governance graph edges:")
    for source, label, target in EDGES:
        print(f"  {source} --{label}--> {target}")

    authority = authority_edges(EDGES)
    print("\nauthority (can-overrule) edges found by walking the graph:")
    for source, target in authority:
        print(f"  {source} --can-overrule--> {target}")
    if not authority:
        print("  (none)")

    try:
        assert ("escalation", "review") in authority, (
            "no can-overrule edge from escalation to review -- the pipeline's "
            "authority relationship exists only in prose, so two stamps on one "
            "article cannot be resolved by looking anything up"
        )

        ranking = rank_authority(LOOPS, EDGES)
        print("\ntopological authority ranking (most authority first):")
        for position, loop in enumerate(ranking, start=1):
            print(f"  {position}. {loop}")

        assert ranking.index("escalation") < ranking.index("review"), (
            "escalation does not outrank review in the topological ordering"
        )

        print("\narticle A-311 carries two stamps:")
        for stamp in A311_STAMPS:
            print(f"  {stamp['loop']} -> {stamp['verdict']} (at {stamp['at']})")

        newest = max(A311_STAMPS, key=lambda s: s["at"])
        print(f"  a recency tiebreak would pick: {newest['verdict']}")

        verdict, reason = resolve(A311_STAMPS, EDGES, ranking)
        print(f"\nresolved verdict: {verdict}  ({reason})")

        assert verdict == "hold-for-editor", (
            f"resolver returned {verdict!r}; A-311 must be held because the "
            "graph says escalation outranks review, regardless of which stamp "
            "landed last"
        )
    except (AssertionError, ValueError) as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        "\nPASS: escalation's authority over review is a real edge with an "
        "acyclic ranking behind it, and A-311 resolves to hold-for-editor "
        "from that ranking rather than from either stamp's timestamp."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
