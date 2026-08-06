#!/usr/bin/env python3
"""Step 9 live lab: task-scoped subgraph.

No dependencies, no network, standard library only. Models the step-9
resolve_shipping_zone scenario: a small "codebase graph" of function nodes
connected by calls/called_by edges, with two claim nodes attached to the
target function that flatly contradict each other about its behavior (one
from a docstring, one from a test file), linked by a contradicts edge.

Builds a depth-1 task-scoped subgraph around the target function -- the
target itself, its direct call-graph neighbors, and every claim node
attached to it, contradiction included -- and checks two things a
subgraph builder could get wrong in opposite directions: that the slice
is actually smaller than the full graph (it isn't just returning
everything), and that the deliberately-inserted contradicting claim pair
still survives inside the slice (it isn't being filtered out along with
everything else that got left behind).

Exits 1 if the subgraph is not strictly smaller than the full graph, or
if either claim node or the contradicts edge between them is missing
from the subgraph. Exits 0 if both properties hold.
"""

import sys

TARGET = "resolve_shipping_zone"

# Full "codebase graph": 12 function nodes + 2 claim nodes = 14 nodes.
FULL_NODES = {
    "generate_manifest", "resolve_shipping_zone", "lookup_postal_code",
    "nearest_warehouse", "validate_address", "calculate_rate",
    "apply_discount_code", "format_label", "log_shipment",
    "notify_customer", "retry_queue", "audit_trail",
    "claim_docstring", "claim_test",
}

# Each edge is (subject, relation, object). Only the edges touching
# resolve_shipping_zone directly should end up inside its depth-1 subgraph;
# everything reachable only through validate_address, format_label, or
# retry_queue is two-or-more hops away and must be left out.
FULL_EDGES = [
    ("generate_manifest", "calls", "resolve_shipping_zone"),
    ("resolve_shipping_zone", "calls", "lookup_postal_code"),
    ("resolve_shipping_zone", "calls", "nearest_warehouse"),
    ("resolve_shipping_zone", "claims", "claim_docstring"),
    ("resolve_shipping_zone", "claims", "claim_test"),
    ("claim_docstring", "contradicts", "claim_test"),
    ("validate_address", "calls", "calculate_rate"),
    ("calculate_rate", "calls", "apply_discount_code"),
    ("format_label", "calls", "log_shipment"),
    ("log_shipment", "calls", "notify_customer"),
    ("retry_queue", "calls", "audit_trail"),
]

CLAIM_TEXT = {
    "claim_docstring": "defaults unmatched postal codes to the nearest warehouse",
    "claim_test": "raises an error on unmatched postal codes",
}


def build_task_scoped_subgraph(nodes, edges, target):
    """Depth-1 subgraph: the target, every node one calls/called_by hop
    away, and every claim node attached to the target -- contradictions
    kept, never filtered down to a single "winning" claim."""
    neighbor_nodes = {target}
    kept_edges = []
    for subj, rel, obj in edges:
        if subj == target or obj == target:
            neighbor_nodes.add(subj)
            neighbor_nodes.add(obj)
            kept_edges.append((subj, rel, obj))
    # A contradicts edge between two claims already pulled in must also
    # travel with the slice -- both endpoints are already inside it.
    for subj, rel, obj in edges:
        if rel == "contradicts" and subj in neighbor_nodes and obj in neighbor_nodes:
            if (subj, rel, obj) not in kept_edges:
                kept_edges.append((subj, rel, obj))
    return neighbor_nodes, kept_edges


def main():
    print(f"full graph: {len(FULL_NODES)} nodes, {len(FULL_EDGES)} edges")

    sub_nodes, sub_edges = build_task_scoped_subgraph(FULL_NODES, FULL_EDGES, TARGET)

    print(f"\ntask-scoped subgraph around '{TARGET}': "
          f"{len(sub_nodes)} nodes, {len(sub_edges)} edges")
    print("nodes:", ", ".join(sorted(sub_nodes)))
    print("claims carried into the subgraph:")
    for claim_id in ("claim_docstring", "claim_test"):
        tag = "in subgraph" if claim_id in sub_nodes else "MISSING"
        print(f"  {claim_id} ({tag}): {CLAIM_TEXT[claim_id]}")

    try:
        assert len(sub_nodes) < len(FULL_NODES), (
            "subgraph is not smaller than the full graph -- "
            "it isn't scoping anything, it's just returning everything"
        )
        assert "claim_docstring" in sub_nodes and "claim_test" in sub_nodes, (
            "the contradicting claim pair did not survive into the subgraph"
        )
        assert ("claim_docstring", "contradicts", "claim_test") in sub_edges, (
            "the contradicts edge between the two claims was filtered out -- "
            "the subgraph is hiding a disagreement instead of carrying it"
        )
        # Nodes reachable only through the unrelated branches must not
        # leak into a depth-1 slice around resolve_shipping_zone.
        excluded = {"validate_address", "calculate_rate", "apply_discount_code",
                    "format_label", "log_shipment", "notify_customer",
                    "retry_queue", "audit_trail"}
        leaked = excluded & sub_nodes
        assert not leaked, f"unrelated nodes leaked into the subgraph: {leaked}"
    except AssertionError as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        f"\nPASS: subgraph ({len(sub_nodes)} nodes) is strictly smaller than "
        f"the full graph ({len(FULL_NODES)} nodes), and both contradicting "
        "claims -- plus the contradicts edge between them -- survived the slice."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
