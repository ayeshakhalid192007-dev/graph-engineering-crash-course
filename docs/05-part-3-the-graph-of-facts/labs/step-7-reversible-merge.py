#!/usr/bin/env python3
"""Step 7 live lab: reversible merge.

No dependencies, no network, standard library only. Models the step-7
"the payments service" / "billing-svc" scenario: two mention nodes from
two different sources, merged into one canonical Service node with a
recorded reason. Checks the merge is reversible in the one sense that
actually matters here -- both original mention strings, and their
sources, are still individually retrievable by querying the merged node,
not silently replaced by whichever name won.

Exits 1 if either original mention is missing from the merged node's
attached mentions. Exits 0 if both are still present and independently
readable.
"""

import sys

MENTIONS = [
    {"text": "the payments service", "source": "incident retro"},
    {"text": "billing-svc", "source": "deploy log"},
]

MERGE_REASON = "same deployment target, same on-call rotation"


def resolve(mentions, canonical_name, reason):
    """Reversible merge: build one canonical node that keeps every
    original mention attached, rather than picking a winning name and
    discarding the rest."""
    return {
        "canonical_name": canonical_name,
        "mentions": list(mentions),  # copy, not a reference to the input
        "merge_reason": reason,
    }


def mentions_of(node, text):
    return [m for m in node["mentions"] if m["text"] == text]


def main():
    print("original mentions:")
    for m in MENTIONS:
        print(f"  '{m['text']}' (source: {m['source']})")

    merged = resolve(MENTIONS, canonical_name="billing-svc", reason=MERGE_REASON)

    print(f"\nmerged into canonical node: {merged['canonical_name']}")
    print(f"merge reason: {merged['merge_reason']}")
    print("mentions still attached to the merged node:")
    for m in merged["mentions"]:
        print(f"  '{m['text']}' (source: {m['source']})")

    try:
        for original in MENTIONS:
            found = mentions_of(merged, original["text"])
            assert found, f"original mention '{original['text']}' is missing from the merged node"
            assert found[0]["source"] == original["source"], (
                f"mention '{original['text']}' lost its original source"
            )
        assert merged["merge_reason"], "a merge without a recorded reason cannot be reviewed later"
    except AssertionError as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        "\nPASS: both original mentions -- 'the payments service' and 'billing-svc' -- "
        "are still individually retrievable from the merged node, sources intact."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
