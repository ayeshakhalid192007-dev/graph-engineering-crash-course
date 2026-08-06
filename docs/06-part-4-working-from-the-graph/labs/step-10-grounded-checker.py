#!/usr/bin/env python3
"""Step 10 live lab: the grounded checker.

No dependencies, no network, standard library only. Models the step-10
PR-5190 / PR-4821 scenario: a small repo graph of PR --modifies--> Module
edges (the kind extraction would produce from real diffs), plus two
"doesn't touch auth-module" claims -- one true, one fabricated -- made in
each PR's description.

The checker never reads either description. It decomposes each claim
into the single edge that would have to exist for the claim to be false
(<pr> --modifies--> auth-module), and looks that edge up directly in the
graph. This is the discriminating case a tone-reading checker would get
wrong: PR-5190's description reads as a harmless front-end refactor, but
the graph -- built from the actual diff -- has the falsifying edge
sitting in it anyway.

Exits 1 if the checker approves the fabricated claim (i.e. fails to
detect that PR-5190's falsifying edge is present), or if it wrongly
rejects the true claim for PR-4821. Exits 0 if it correctly confirms
PR-4821's claim and rejects PR-5190's.
"""

import sys

# Repo graph: (pr, "modifies", module) edges, as extraction over each
# diff would actually produce them -- nothing here reads like prose.
GRAPH_EDGES = [
    ("PR-4821", "modifies", "rate-limiter.py"),
    ("PR-4821", "modifies", "retry-config.py"),
    ("PR-5190", "modifies", "login-form.html"),
    ("PR-5190", "modifies", "login-form.css"),
    ("PR-5190", "modifies", "login_view.py"),
    ("PR-5190", "modifies", "auth-module"),
]

CLAIMS = [
    {
        "pr": "PR-4821",
        "text": "PR-4821 does not modify auth-module",
        "description": "Tightens the rate limiter's retry backoff. No auth changes.",
        "expected": True,  # true claim: no such edge exists
    },
    {
        "pr": "PR-5190",
        "text": "PR-5190 does not modify auth-module",
        "description": "Refactors the login form's client-side validation. "
                        "No backend changes, doesn't touch auth.",
        "expected": False,  # fabricated claim: the falsifying edge is present
    },
]


def decompose_claim(claim, forbidden_module="auth-module"):
    """Turn a "<pr> does not modify <module>" claim into the single edge
    that would have to exist for the claim to be false."""
    return (claim["pr"], "modifies", forbidden_module)


def check_claim(graph_edges, claim):
    """Grounded check: look the falsifying edge up in the graph. Never
    consult claim['description'] -- the check is mechanical, not a read
    of how confident the description sounds."""
    falsifying_edge = decompose_claim(claim)
    edge_present = falsifying_edge in graph_edges
    return not edge_present, falsifying_edge


def main():
    print("repo graph (modifies edges from extraction over each diff):")
    for edge in GRAPH_EDGES:
        print(f"  {edge[0]} --{edge[1]}--> {edge[2]}")

    results = []
    for claim in CLAIMS:
        holds, falsifying_edge = check_claim(GRAPH_EDGES, claim)
        results.append((claim, holds, falsifying_edge))
        print(f"\nclaim: \"{claim['text']}\"")
        print(f"  description says: \"{claim['description']}\"")
        print(f"  decomposed to falsifying edge: {falsifying_edge}")
        verdict = "CONFIRMED" if holds else "REJECTED"
        print(f"  edge present in graph: {falsifying_edge in GRAPH_EDGES} -> {verdict}")

    try:
        for claim, holds, falsifying_edge in results:
            assert holds == claim["expected"], (
                f"checker got '{claim['pr']}' wrong: expected "
                f"{'CONFIRMED' if claim['expected'] else 'REJECTED'}, got "
                f"{'CONFIRMED' if holds else 'REJECTED'} -- "
                f"a checker that approves a fabricated claim ({falsifying_edge} "
                "is actually present in the graph) is exactly the failure this "
                "checker exists to prevent"
            )
    except AssertionError as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        "\nPASS: PR-4821's true claim was confirmed and PR-5190's fabricated "
        "claim was rejected -- both decisions made from one looked-up edge "
        "each, never from reading either PR's description."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
