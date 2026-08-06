#!/usr/bin/env python3
"""Step 4 live lab: the ratchet.

No dependencies, no network, standard library only. Runs a fixed list of
five candidate prompt-variant scores from the step-4 scenario through the
ratchet rule -- each candidate is compared against the current best kept
attempt, and only strictly-improving candidates get appended to durable
history. Everything else is logged to a discard list instead, never
deleted and never promoted to the new reference point. Prints the final
kept chain and the discarded list side by side.

Exits 0 once the demonstration has run and both lists have been printed --
there is no failure condition here, only the shape of the split itself.
"""

import sys

# Five candidate prompt variants tried overnight, in the order they were
# generated, each with the score it got against the held-out ticket set.
CANDIDATES = [
    {"id": "variant-1", "score": 0.52},
    {"id": "variant-2", "score": 0.49},
    {"id": "variant-3", "score": 0.61},
    {"id": "variant-4", "score": 0.58},
    {"id": "variant-5", "score": 0.68},
]


def run_ratchet(candidates):
    durable_history = []
    discarded = []
    current_best = None

    for candidate in candidates:
        if current_best is None or candidate["score"] > current_best["score"]:
            durable_history.append(candidate)
            current_best = candidate
        else:
            discarded.append({**candidate, "lost_to": current_best["id"]})

    return durable_history, discarded


def main():
    durable_history, discarded = run_ratchet(CANDIDATES)

    print("candidates tried, in order:")
    for c in CANDIDATES:
        print(f"  {c['id']}: score {c['score']}")

    print("\ndurable history (kept -- each strictly beats the one before it):")
    for entry in durable_history:
        print(f"  {entry['id']}: score {entry['score']}")

    print("\ndiscarded (logged, not kept):")
    for entry in discarded:
        print(f"  {entry['id']}: score {entry['score']} (lost to {entry['lost_to']})")

    # The ratchet invariant: durable history must be strictly increasing,
    # and every candidate must land in exactly one of the two lists.
    scores = [entry["score"] for entry in durable_history]
    assert scores == sorted(scores) and len(set(scores)) == len(scores), (
        "durable history must be strictly increasing"
    )
    assert len(durable_history) + len(discarded) == len(CANDIDATES), (
        "every candidate must land in exactly one of durable history or discarded"
    )

    print(
        f"\nPASS: {len(durable_history)} of {len(CANDIDATES)} candidates kept as durable "
        f"history, {len(discarded)} logged as discarded -- none deleted, none lost."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
