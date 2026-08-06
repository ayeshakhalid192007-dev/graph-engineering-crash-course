# Starter Kits

This directory contains runnable starter kits for all 23 patterns in the library. Each kit includes a quickstart, schema examples, and reference implementations in Claude Code and/or OpenCode.

## Install one without cloning

```bash
npx @graph-engineering/graph-kit list        # browse all 23
npx @graph-engineering/graph-kit <kit-name>  # install into the current directory
```

The [`@graph-engineering/graph-kit`](../packages/graph-kit/README.md) CLI carries the kits and their specs and nothing else — no course, no clone, no API keys. Copying a directory out of this folder by hand does the same job and stays supported.

## Core Kits (Full Multi-Tool)

These 7 patterns have complete implementations in both Claude Code and OpenCode, with full `.claude/` and `opencode/` subdirectories:

1. **[document-to-facts](document-to-facts/)** — Schema-first extraction from documents, transforming unstructured text into typed entities and relationships.
2. **[alias-merge-with-trail](alias-merge-with-trail/)** — Merging duplicate identifiers (e.g., "payments-svc" and "payment-service") while maintaining an audit trail of all canonical decisions.
3. **[receipt-per-edge](receipt-per-edge/)** — Recording the provenance of every graph edge: which source document, extraction run, and schema version produced it.
4. **[task-scoped-retrieval](task-scoped-retrieval/)** — Returning a bounded subgraph for a given task (e.g., direct dependencies of a function, plus conflicting claims about it).
5. **[grounded-triple-checker](grounded-triple-checker/)** — Verifying that a claim (e.g., "this PR doesn't touch auth") is grounded in the actual graph, rejecting fabricated assertions.
6. **[counter-metric-loop](counter-metric-loop/)** — Running a parallel optimization loop to catch metric gaming in the main loop.
7. **[sqlite-backed-graph](sqlite-backed-graph/)** — Persisting the entire graph in SQLite with foreign-key constraints and provenance fields.

## Extended Kits (Single-Tool Reference + Porting Notes)

These 16 patterns each have a single-tool Claude Code reference implementation plus documented guidance for porting to other tools. Start with one of these to understand the pattern in a simpler setting before scaling to the full multi-tool anatomy:

1. **[code-change-to-graph](code-change-to-graph/)** (Claude Code) — Recording every function or module touched by a change as queryable edges in the graph.
2. **[conversation-to-claims](conversation-to-claims/)** (Claude Code) — Extracting facts asserted in an agent conversation into provisional claim nodes, rather than losing them in the transcript.
3. **[confidence-scored-dedup](confidence-scored-dedup/)** (Claude Code) — Merging probable duplicates while assigning confidence scores, leaving low-confidence merges as "unresolved" for human review.
4. **[reversible-merge-audit](reversible-merge-audit/)** (Claude Code) — Merging nodes and edges while recording enough information to reverse the merge if new evidence emerges.
5. **[supersession-chain](supersession-chain/)** (Claude Code) — Tracking the lineage of successive versions of a node or edge (e.g., schema v1 → v2 → v3).
6. **[versioned-schema-log](versioned-schema-log/)** (Claude Code) — Recording schema changes over time so you can replay and audit which facts fit which schema versions.
7. **[budget-capped-subgraph](budget-capped-subgraph/)** (Claude Code) — Returning the "most important" subset of a subgraph when a full retrieval would exceed a cost or token budget.
8. **[conflict-aware-bundle](conflict-aware-bundle/)** (Claude Code) — Bundling related claims together, marking any internal contradictions, so a reader sees the full debate around a fact.
9. **[contradiction-detector](contradiction-detector/)** (Claude Code) — Finding edges or claims that directly contradict each other (e.g., "auth-svc is critical" vs. "auth-svc can be removed").
10. **[early-victory-guard](early-victory-guard/)** (Claude Code) — Detecting when a governance loop has arrived at a stable state, so it can shut down rather than spinning endlessly.
11. **[arbitration-edge](arbitration-edge/)** (Claude Code) — Recording disputes: marking edges that are contested and noting which parties disagree on the claim.
12. **[audit-loop](audit-loop/)** (Claude Code) — Continuously checking that the graph remains consistent against a set of invariants (e.g., "every node must have a type").
13. **[anchor-and-freeze](anchor-and-freeze/)** (Claude Code) — Pinning a stable snapshot of the graph at a known point in time, preventing accidental retroactive rewrites.
14. **[file-graph-for-small-teams](file-graph-for-small-teams/)** (Claude Code) — Storing the entire graph as JSON files in a Git repo, suitable for small teams and version control.
15. **[postgres-backed-graph](postgres-backed-graph/)** (Claude Code) — Persisting the graph in PostgreSQL with advanced querying and full-text search.
16. **[neo4j-at-scale](neo4j-at-scale/)** (Claude Code) — Using Neo4j for large-scale graph storage and traversal, with native graph algorithms.

## Build Scope

This build window covers all 23 pattern specifications and starter kits. The 7 core kits have full multi-tool implementations (both Claude Code and OpenCode). The 16 extended kits each provide a single-tool reference implementation (Claude Code only) plus clear porting notes for adopting the pattern in other tools and environments. This is the deliberate, disclosed scope for this phase of the project — not a placeholder or incomplete work, but a pragmatic choice to ship patterns with depth in one tool while documenting the path to scale across many.

## How to Use a Kit

Each kit contains:

- **`PATTERN.md`** — What the pattern does, its inputs, outputs, and the failure mode if you skip it.
- **`README.md`** — Quickstart instructions: prerequisites, how to run the example, what to expect.
- **`schema.example.json`** (write-path patterns) or **`sample-graph.example.json`** (read-path patterns) — A concrete example to work with.
- **`.claude/skills/`** — Claude Code skill(s) implementing the pattern.
- **`.claude/agents/graph-verifier.md`** — Agent definition that validates outputs.
- **`opencode/`** — OpenCode equivalents (core kits only).
- **`PORTING.md`** (extended kits only) — Guidance for adapting the pattern to other tools or environments.

Pick a kit, follow its `README.md`, and try the example. If you want to adapt it to your own scenario, start with the `PATTERN.md` to understand what it does, then modify the schema or sample data and re-run the skill.

## Contributing

To add a new pattern to this library, see the [Contributing](../CONTRIBUTING.md) guide in the repo root.
