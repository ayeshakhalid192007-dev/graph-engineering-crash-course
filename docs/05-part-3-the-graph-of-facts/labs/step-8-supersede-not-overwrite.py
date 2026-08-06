#!/usr/bin/env python3
"""Step 8 live lab: supersede, don't overwrite.

No dependencies, no network, standard library only. Models the step-8
PM-2117 scenario: a claim extracted under schema v1, later re-extracted
under schema v2 once v2 adds a required confidence field the v1 claim
never had. Builds the v2 claim as a brand-new node linked back to the v1
claim by a supersedes edge, and marks the v1 claim's status superseded --
it never edits the v1 claim's own fields or removes it from the store.

Exits 1 if the v1 record is missing afterward, or if it was mutated in
place instead of left as it was originally recorded. Exits 0 if the v1
record still exists, unedited, marked superseded, and reachable via the
v2 claim's supersedes edge.
"""

import sys
import copy

claims = {}

V1_ID = "claim-pm2117-cause-v1"
V2_ID = "claim-pm2117-cause-v2"

claims[V1_ID] = {
    "id": V1_ID,
    "subject": "checkout-api",
    "relation": "caused-by",
    "object": "expired internal CA cert",
    "provenance": {"source": "PM-2117", "run": "extraction-014", "schema_version": "v1"},
    "status": "active",
}

# Snapshot of the v1 claim exactly as it looked before any v2 work, used
# later to prove it was never mutated in place.
v1_before_supersession = copy.deepcopy(claims[V1_ID])


def supersede(store, old_id, new_claim):
    """Create a new claim and mark the old one superseded -- never touch
    the old claim's own fields."""
    store[new_claim["id"]] = new_claim
    store[old_id]["status"] = "superseded"
    store[old_id]["superseded_by"] = new_claim["id"]
    return store


def main():
    print("v1 claim, before re-extraction:")
    print(f"  {claims[V1_ID]}")

    v2_claim = {
        "id": V2_ID,
        "subject": "checkout-api",
        "relation": "caused-by",
        "object": "expired internal CA cert",
        "confidence": 0.9,
        "provenance": {"source": "PM-2117", "run": "extraction-029", "schema_version": "v2"},
        "status": "active",
        "supersedes": V1_ID,
    }

    supersede(claims, V1_ID, v2_claim)

    print("\nafter re-extraction under schema v2:")
    print(f"  v1: {claims[V1_ID]}")
    print(f"  v2: {claims[V2_ID]}")

    try:
        assert V1_ID in claims, "v1 claim was deleted instead of superseded"
        assert claims[V1_ID]["status"] == "superseded", "v1 claim's status was not updated"
        assert claims[V1_ID]["superseded_by"] == V2_ID, "v1 claim does not point at its replacement"
        assert claims[V2_ID]["supersedes"] == V1_ID, "v2 claim does not point back at v1"
        assert claims[V2_ID]["provenance"]["schema_version"] == "v2", (
            "v2 claim's provenance must record schema v2"
        )

        # The only fields allowed to differ between the pre- and
        # post-supersession v1 record are status and superseded_by --
        # everything else, provenance included, must be untouched.
        untouched = {
            k: v for k, v in claims[V1_ID].items() if k not in ("status", "superseded_by")
        }
        original = {
            k: v for k, v in v1_before_supersession.items() if k not in ("status", "superseded_by")
        }
        assert untouched == original, (
            "v1 claim's own fields were edited in place -- provenance no longer "
            "matches what schema v1 actually produced"
        )
    except AssertionError as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        "\nPASS: v1 claim still exists, unedited, marked superseded, and linked "
        "forward to v2 -- nothing was deleted or rewritten in place."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
