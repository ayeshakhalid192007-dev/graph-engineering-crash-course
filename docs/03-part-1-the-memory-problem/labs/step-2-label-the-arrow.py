#!/usr/bin/env python3
"""Step 2 live lab: label the arrow.

No dependencies, no network, standard library only. Builds the
auth-middleware / session-store example from step-2 as a plain dict
adjacency structure, prints the one directed edge it contains, and asserts
that the two directions of that edge -- A->B and B->A -- are treated as
distinct claims, never as interchangeable statements of the same fact.

Exit code 0 on success, 1 if any assertion fails.
"""

import sys


# Plain dict adjacency structure: each node maps to a list of outgoing
# edges, and each edge is {"label": ..., "to": ...}. RateLimiter is present
# in the graph -- it's part of the same service -- but has no outgoing edge
# yet, which is a legitimate state, not a mistake.
graph = {
    "AuthMiddleware": [{"label": "depends_on", "to": "SessionStore"}],
    "SessionStore": [],
    "RateLimiter": [],
}


def has_edge(g, source, label, target):
    return any(
        edge["label"] == label and edge["to"] == target
        for edge in g.get(source, [])
    )


def main():
    print("graph contents:")
    for source, edges in graph.items():
        if not edges:
            print(f"  {source} (no outgoing edges)")
        for edge in edges:
            print(f"  {source} --{edge['label']}--> {edge['to']}")

    forward = has_edge(graph, "AuthMiddleware", "depends_on", "SessionStore")
    backward = has_edge(graph, "SessionStore", "depends_on", "AuthMiddleware")

    try:
        assert forward, "expected AuthMiddleware --depends_on--> SessionStore in the graph"
        assert not backward, "no reverse edge was ever asserted -- it must not appear as true"
        assert forward != backward, "A->B and B->A must be treated as distinct claims, not the same one"
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)

    print(
        "PASS: edge direction is meaningful -- "
        "AuthMiddleware->SessionStore and SessionStore->AuthMiddleware are distinct claims"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
