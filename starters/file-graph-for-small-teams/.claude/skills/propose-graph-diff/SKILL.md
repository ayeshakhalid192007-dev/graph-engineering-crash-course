---
name: propose-graph-diff
description: Turns a proposed addition to a JSON-file graph into a minimal, reviewable diff, flagging any proposed edge that conflicts with a cross-reference already on file, and never writing directly to the shared graph file itself
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# propose-graph-diff

Reads the graph's current JSON state and a proposed node/edge addition,
produces the minimal diff a pull request would show, cross-checks the
proposal against facts already on file, and flags anything that doesn't
line up — without ever merging the change itself.

## Instructions

You are a Claude Code skill implementing the `file-graph-for-small-teams`
pattern. Follow these steps in order:

1. **Read the current graph file's state** — the existing nodes and
   edges — as the base to diff against. Default to `graph.json` as
   given in this kit's `README.md` unless told otherwise.
2. **Read the proposed addition exactly as given** — the new node and
   its edges. Do not invent, infer, or add any node or edge beyond what
   was actually proposed, even if you think the graph is "obviously"
   missing something related.
3. **Produce a minimal diff**: only the new or changed lines, in the
   same shape the existing file uses, not a full rewrite of the file.
   A reviewer looking at a pull request needs to see exactly what
   changed, not re-verify the entire graph from scratch.
4. **Before finalizing the diff, cross-check every claimed attribution
   in the proposed edges** against any other fact already on file about
   the same subject or object — for example, an announcer ID logged on
   an existing host node, or another edge already asserting something
   about the same reel. If a proposed edge conflicts with an existing
   cross-reference, do not silently include it as if uncontested.
5. **Flag conflicts explicitly, but still include the diff.** Do not
   drop the proposed line and do not silently correct it to what you
   think is right — this skill's job is to produce the diff and name the
   conflict, not to decide which fact wins. That decision belongs to
   whoever reviews the pull request.
6. **Never write directly to the shared graph file.** This skill's
   output is a diff and a flag list for a human to review and merge
   through a normal pull request — merging into the shared file is a
   human git action this skill does not perform.
7. **Report the diff for every proposal**, plus a separate flagged list
   naming the specific conflicting fact for anything flagged, so a
   reviewer can tell "clean addition" apart from "needs a second look"
   at a glance.

## Input

- The current graph file's state (defaults to `graph.json` in this
  kit's `README.md`).
- One or more proposed additions (defaults to the two reels in
  `README.md`).

## Output

- A minimal diff per proposed addition.
- A separate flagged-for-review list naming the specific on-file
  cross-reference each flagged proposal conflicts with.

## Example Usage

```
Use the propose-graph-diff skill on both proposed additions against the
current graph.json in README.md.

Expected:
  DIFF (reel:LT-0447) -- no flag:
    + { "id": "reel:LT-0447", "type": "reel", "found": "estimated spring 1987" }
    + { "subject": "reel:LT-0447", "predicate": "recorded-during", "object": "program:nightline-request-hour" }
    + { "subject": "reel:LT-0447", "predicate": "hosted-by", "object": "host:dana-voss" }

  DIFF (reel:LT-0452) -- FLAGGED:
    + { "id": "reel:LT-0452", "type": "reel", "found": "estimated spring 1987" }
    + { "subject": "reel:LT-0452", "predicate": "recorded-during", "object": "program:nightline-request-hour" }
    + { "subject": "reel:LT-0452", "predicate": "hosted-by", "object": "host:renata-kwan" }
    Flag: on-tape announcer ID for this reel reads "D.V.", matching
      host:dana-voss's announcer_id ("D.V."), not host:renata-kwan's
      ("R.K."). Proposed attribution conflicts with an existing
      cross-reference -- needs reviewer resolution before merge.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check two things: that every
proposed diff is minimal (no unrelated existing lines pulled in), and
that a flag only fires when a proposal genuinely conflicts with a fact
already on file, not merely because the touched node already has more
than one fact recorded about it.
