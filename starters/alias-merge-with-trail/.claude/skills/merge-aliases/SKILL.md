---
name: merge-aliases
description: Folds two surface names for the same backend system into one canonical entity, keeping every original mention individually retrievable, and refuses to merge pairs that only share spelling
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# merge-aliases

Takes two or more surface names pulled from different source documents and
decides whether they name the same underlying system. When they do, it
produces one canonical entity, but every surface string that fed into that
decision stays in the output as its own retrievable record — nothing gets
overwritten or thrown away to make room for the canonical name.

## Instructions

You are a Claude Code skill implementing the `alias-merge-with-trail`
pattern. A merge is a claim, and a claim needs standing evidence — not a
resemblance between two strings. Follow these steps in order:

1. **Read the schema first.** Open `schema.example.json` and note the two
   shapes it defines: a `Service` entity with a `canonical_name` and a
   `merge_reason`, and an alias record whose `mentions` array holds one
   entry per surface string, each carrying its own `source` and a
   `retrievable` flag. Treat this shape as fixed for the run.
2. **Read the source material.** Default to `sample-input.md` in this kit
   unless the user names a different file or pair of files. Pull out
   every surface string used for a system, along with which source
   section it came from and any timestamp or reference number attached to
   it.
3. **Group candidate surface strings into pairs (or larger clusters) that
   might name the same system.** For each candidate group, look for a
   concrete, checkable link between the sources involved — a shared
   timestamp window, an explicit cross-reference from one document to the
   other, a shared ticket or deployment identifier. A pair that shares
   nothing but a plausible-sounding name is not a candidate for merging;
   set it aside.
4. **For a group with real evidence:** create one canonical `Service`
   entity, write the concrete evidence into `merge_reason` in plain
   language (name the shared timestamp or cross-reference, don't just say
   "these seem related"), and add one `mentions` entry per original
   surface string — each with its own `source` and `retrievable: true`.
   Do not delete, rename, or collapse the original surface strings into
   the canonical one; they stay as separate entries pointing at it.
5. **For a group with no real evidence** (including the decoy pair in
   `sample-input.md`): do not merge. Report the pair by name and state
   plainly why it was left alone — e.g., no shared timestamp, no
   cross-reference between the two mentions.
6. **Write the result to `output.json`** (or the path the user requested)
   in this kit's root, following `schema.example.json`'s `entities` and
   `aliases` shape. Print the same structure alongside a short list of any
   groups you considered and chose not to merge, with the reason for
   each.
7. **Confirm reversibility before finishing:** for every canonical entity
   you produced, check that a lookup keyed on each of its original surface
   strings independently — not just a lookup on the canonical name — would
   still return that entity and both of its mentions. State this check
   explicitly in your output rather than assuming it.

## Input

- `schema.example.json` — the fixed shape for a canonical entity and for a
  retained mention record.
- `sample-input.md` — the two source excerpts to pull surface names from
  (or another file/pair the user names).

## Output

- `output.json` (or user-specified path) — canonical entities and their
  alias groups, matching `schema.example.json`'s shape, with every
  original mention still present and marked `retrievable: true`.
- A printed list of any candidate groups that were deliberately left
  unmerged, with the reason.

## Example Usage

```
Run the merge-aliases skill on sample-input.md using schema.example.json.
Expected merge:
  canonical: billing-svc
  merge_reason: Source A's checkout complaint (14:03-14:24 UTC, 2026-03-03)
    and Source B's billing-svc rollback/redeploy entries for the same
    window are explicitly cross-referenced by ticket #5821.
  mentions:
    - surface: "the payments service", source: Support Ticket #5821, retrievable: true
    - surface: "billing-svc", source: Infrastructure Change Log, retrievable: true
Expected skip:
  "the notifications thing" / "notify-svc" — no shared timestamp, no
  cross-reference between the two mentions; left as separate, unmerged
  entities.
```

## Validation

The companion agent (`.claude/agents/graph-verifier.md`) independently
re-checks `output.json` against `schema.example.json` and flags any merge
that dropped a mention, weakened a stated reason to bare name similarity,
or folded in a pair that never had a concrete link between its sources.
