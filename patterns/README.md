# Pattern Library

An index of the 23 graph patterns in this course. Every entry here has a
matching spec at `patterns/<name>.md` and a `patterns/registry.yaml` entry;
the 7 marked **core** below ship (or will ship, once Tasks 3–10 land) as
full starter kits with runnable examples in both Claude Code and OpenCode.
The remaining 16 **extended** patterns ship as specs plus a single-tool
reference implementation and a porting note, per the tool-coverage policy in
`graph-plan.md` §18.

Each pattern belongs to one of seven categories, matching the write path
(extraction → resolution → provenance), the read path (subgraph
construction → checking), and the governance and storage concerns that sit
alongside both. See `graph-plan.md` §17 for the full catalog this table
mirrors, and §14 for how each write- and read-path category maps back onto
the 17-step course.

## Catalog

**A. Extraction**

| Pattern | Stage | Cost | Core |
| --- | --- | --- | --- |
| [document-to-facts](document-to-facts.md) | write | medium | yes |
| [code-change-to-graph](code-change-to-graph.md) | write | medium | no |
| [conversation-to-claims](conversation-to-claims.md) | write | medium | no |

**B. Resolution**

| Pattern | Stage | Cost | Core |
| --- | --- | --- | --- |
| [alias-merge-with-trail](alias-merge-with-trail.md) | write | low | yes |
| [confidence-scored-dedup](confidence-scored-dedup.md) | write | medium | no |
| [reversible-merge-audit](reversible-merge-audit.md) | write | low | no |

**C. Provenance**

| Pattern | Stage | Cost | Core |
| --- | --- | --- | --- |
| [receipt-per-edge](receipt-per-edge.md) | write | low | yes |
| [supersession-chain](supersession-chain.md) | write | low | no |
| [versioned-schema-log](versioned-schema-log.md) | write | low | no |

**D. Subgraph / context construction**

| Pattern | Stage | Cost | Core |
| --- | --- | --- | --- |
| [task-scoped-retrieval](task-scoped-retrieval.md) | read | low | yes |
| [budget-capped-subgraph](budget-capped-subgraph.md) | read | low | no |
| [conflict-aware-bundle](conflict-aware-bundle.md) | read | medium | no |

**E. Checker**

| Pattern | Stage | Cost | Core |
| --- | --- | --- | --- |
| [grounded-triple-checker](grounded-triple-checker.md) | read | medium | yes |
| [contradiction-detector](contradiction-detector.md) | read | medium | no |
| [early-victory-guard](early-victory-guard.md) | read | low | no |

**F. Governance wiring**

| Pattern | Stage | Cost | Core |
| --- | --- | --- | --- |
| [counter-metric-loop](counter-metric-loop.md) | governance | low | yes |
| [arbitration-edge](arbitration-edge.md) | governance | low | no |
| [audit-loop](audit-loop.md) | governance | medium | no |
| [anchor-and-freeze](anchor-and-freeze.md) | governance | low | no |

**G. Storage & scale**

| Pattern | Stage | Cost | Core |
| --- | --- | --- | --- |
| [sqlite-backed-graph](sqlite-backed-graph.md) | storage | low | yes |
| [file-graph-for-small-teams](file-graph-for-small-teams.md) | storage | low | no |
| [postgres-backed-graph](postgres-backed-graph.md) | storage | medium | no |
| [neo4j-at-scale](neo4j-at-scale.md) | storage | high | no |

## Core vs. extended

**Core (7, one per category, full kits):** `document-to-facts`,
`alias-merge-with-trail`, `receipt-per-edge`, `task-scoped-retrieval`,
`grounded-triple-checker`, `counter-metric-loop`, `sqlite-backed-graph`.

**Extended (16, specs + single-tool reference):** everything else in the
table above. Promoting an extended pattern to a full multi-tool kit is
welcome contribution work — see below.

## Adding a pattern

New patterns follow `pattern-template.md`'s shape and join
`patterns/registry.yaml` alongside a starter kit under `starters/<name>/`.
For the full walkthrough — branching, writing the spec, the originality
rules that apply to it, and the review checks a pattern PR runs — see
[`CONTRIBUTING.md`](../CONTRIBUTING.md)'s "How to Add a Pattern" section.
