#!/usr/bin/env python3
"""Step 6 live lab: schema-first extraction.

No dependencies, no network, standard library only. Defines the PM-2117
schema from step-6 as a plain dict (allowed entity types, allowed
relationship types), then runs a fake "extraction" over a hardcoded set of
items that stand in for what an extraction pass pulled from the postmortem
-- no LLM call, no parsing, fully deterministic. Two items match the
schema; one is deliberately malformed (an entity type and a relationship
type the schema never defined) to prove the schema gate actually rejects
what it's supposed to reject, rather than letting everything through.

Exits 1 if the schema gate accepts the malformed item, or rejects either
of the two valid items. Exits 0 if the gate's accept/reject split matches
the schema exactly.
"""

import sys

SCHEMA = {
    "entity_types": {"Service", "Incident", "Cause"},
    "relationship_types": {"caused-by", "affected"},
}

# Stand-in for what an extraction pass produced from PM-2117's prose.
# Each item is {subject_type, subject, relation, object_type, object}.
EXTRACTED_ITEMS = [
    {
        "subject_type": "Incident",
        "subject": "PM-2117",
        "relation": "caused-by",
        "object_type": "Cause",
        "object": "expired internal CA cert",
    },
    {
        "subject_type": "Incident",
        "subject": "PM-2117",
        "relation": "affected",
        "object_type": "Service",
        "object": "checkout-api",
    },
    {
        # Deliberately malformed: "escalated-to" and "Team" are not on the
        # schema's allowed lists. A working schema gate must reject this.
        "subject_type": "Incident",
        "subject": "PM-2117",
        "relation": "escalated-to",
        "object_type": "Team",
        "object": "on-call rotation",
    },
]


def matches_schema(item, schema):
    return (
        item["subject_type"] in schema["entity_types"]
        and item["relation"] in schema["relationship_types"]
        and item["object_type"] in schema["entity_types"]
    )


def apply_schema_gate(items, schema):
    accepted, rejected = [], []
    for item in items:
        (accepted if matches_schema(item, schema) else rejected).append(item)
    return accepted, rejected


def describe(item):
    return f"{item['subject']} --{item['relation']}--> {item['object']}"


def main():
    print("schema:")
    print(f"  entity types: {sorted(SCHEMA['entity_types'])}")
    print(f"  relationship types: {sorted(SCHEMA['relationship_types'])}")

    print("\nitems offered to the schema gate:")
    for item in EXTRACTED_ITEMS:
        print(f"  {describe(item)}")

    accepted, rejected = apply_schema_gate(EXTRACTED_ITEMS, SCHEMA)

    print("\naccepted (enters the fact graph):")
    for item in accepted:
        print(f"  {describe(item)}")

    print("\nrejected (schema does not define this type):")
    for item in rejected:
        print(f"  {describe(item)}")

    try:
        assert len(accepted) == 2, f"expected 2 accepted items, got {len(accepted)}"
        assert len(rejected) == 1, f"expected 1 rejected item, got {len(rejected)}"
        assert rejected[0]["relation"] == "escalated-to", (
            "expected the escalated-to item to be the one rejected"
        )
        assert all(matches_schema(item, SCHEMA) for item in accepted), (
            "every accepted item must actually match the schema"
        )
        assert not matches_schema(rejected[0], SCHEMA), (
            "the rejected item must not match the schema"
        )
    except AssertionError as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        "\nPASS: 2 schema-valid items accepted, 1 malformed item rejected -- "
        "the schema gate is enforced, not decorative."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
