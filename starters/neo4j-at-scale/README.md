# neo4j-at-scale Starter Kit

A single-tool (Claude Code) reference kit for the **neo4j-at-scale**
pattern: expressing a multi-hop traversal as a single variable-length
path match against native graph storage instead of a recursive
relational join that grows one level deeper for every extra hop. This is
an extended kit — see `starters/README.md` for how that differs from the
seven core kits.

Amberlynn Genomics Consortium and the derivation chain below are
invented for this course, not drawn from any real lab, consortium, or
contamination incident.

## Prerequisites

- Claude Code.
- No external services or API keys — the derivation chain below is
  everything the kit needs. This kit walks through the traversal
  reasoning a real graph database would execute; it doesn't require a
  running Neo4j instance to work through.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the relationship types and the derivation chain below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Allowed relationship types

- `USED_IN` — a reagent lot used directly in a sequencing run.
- `PRODUCES` — a run producing an experiment result.
- `DERIVED_FROM` — a new reagent lot repackaged from an existing result.

### The derivation chain (compromised lot: RL-2291, flagged 2026-06-03)

- **Hop 1 (`USED_IN`):** RL-2291 used directly in runs `R-88701`,
  `R-88702`, `R-88703`.
- **Hop 2 (`PRODUCES` then `DERIVED_FROM`):** `R-88701`'s output was
  repackaged into a new reagent lot, `RL-2340`, which was then used
  (`USED_IN`) in runs `R-88750` and `R-88761`.
- **Hop 3 (`PRODUCES` then a public reference dataset entry, itself
  reused):** `R-88761`'s output was published to a shared reference
  dataset entry six months later. An unrelated lab's analysis pipeline,
  run `R-88812`, consumed that dataset entry, making it three derivation
  steps removed from RL-2291 and outside the original lab entirely.
- **Not part of the chain:** run `R-91004`, in the same facility, on the
  same date as `R-88701`, using an unrelated reagent lot — shares a date
  and a facility with the contaminated chain but no derivation
  relationship to it.

### Claude Code

1. Load the skill: `.claude/skills/traverse-multi-hop/SKILL.md`.
2. Ask it to run: "Use the traverse-multi-hop skill starting from
   RL-2291 in README.md, following USED_IN, PRODUCES, and DERIVED_FROM,
   bounded to 10 hops."
3. It prints every node reached, tagged with its hop count and the exact
   relationship path that reached it.

## Expected Output

- **Hop 1:** `R-88701`, `R-88702`, `R-88703` — direct `USED_IN`.
- **Hop 2:** `RL-2340` (`PRODUCES` → `DERIVED_FROM`), then `R-88750`,
  `R-88761` (`USED_IN` off `RL-2340`).
- **Hop 3:** `R-88812` (`PRODUCES` off `R-88761` into the reference
  dataset entry, then consumed by an unrelated lab's pipeline).
- **`R-91004` does not appear** in the results — it shares a date and
  facility with `R-88701` but no relationship of any allowed type
  connects it to RL-2291's chain.
- **Deepest hop actually reached: 3** — well within the configured
  `*1..10` bound, and the report states this explicitly rather than
  leaving the reader to infer it from the result count.
- **No cycle detected.**

### Checking the result

- Confirm `R-88812` appears, tagged hop 3, with its full relationship
  path — this is the case a fixed one-hop or two-hop query would have
  missed entirely.
- Confirm `R-91004` is absent — a run that includes it has followed a
  same-date-and-facility coincidence instead of an actual typed
  relationship.
- Confirm every result carries its hop count and path, not a flat
  undifferentiated list that can't distinguish "used directly" from
  "three generations removed."

## Modifying the Example

1. Replace the relationship types and the derivation chain with your own
   traversal question.
2. Re-run the skill and confirm it still reports the deepest hop
   actually reached separately from the configured bound, and still
   excludes anything connected only by an unlisted relationship type or
   a coincidental shared property.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/traverse-multi-hop/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `R-88812` is missing from the results. | The hop bound was set too low to reach it, or `DERIVED_FROM`/`PRODUCES` was left out of the allowed relationship types the traversal follows. |
| `R-91004` appears in the results. | The traversal matched on a coincidental shared property (same date, same facility) instead of following only the allowed typed relationships. |
| The query never returns, or the skill reports it can't finish. | A cycle guard wasn't applied — a bookkeeping cycle in the derivation graph should be detected and reported, not walked forever. |
| Every result is tagged "hop 1" regardless of actual distance. | The traversal is returning a flat reachable-set instead of tagging each node with its real hop count and the specific relationship path that reached it. |

## Next Steps

- Review `patterns/neo4j-at-scale.md` in the course repo for the general
  (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
