---
name: your-pattern-name
category: A-extraction   # one of: A-extraction | B-resolution | C-provenance | D-subgraph | E-checker | F-governance | G-storage
stage: write              # one of: write | read | governance | storage
cost: low                 # one of: low | medium | high
tools: []                 # e.g. [Claude Code, OpenCode] once a starter kit exists for this pattern
core: false                # true only for the 7 patterns with a full multi-tool kit; see patterns/README.md
---

# Your Pattern Name

<!--
This is the blank template every new pattern spec is copied from. Fill in
each section before adding the pattern to `patterns/registry.yaml`. See
`CONTRIBUTING.md`'s "How to Add a Pattern" section for the full contribution
walkthrough, and `patterns/README.md` for the catalog this file joins.
-->

## What it does

One to two sentences describing the mechanism: what the pattern actually
does to the graph, step by step, not just the problem category it belongs
to.

## Inputs

What this pattern expects to be handed before it can run — e.g. a candidate
set of facts, an existing schema, a task description, a budget ceiling.

## Outputs

What the pattern produces or changes in the graph once it runs — new nodes,
new edges, a modified merge state, a bounded subgraph, a verdict.

## Failure mode if skipped

One to two sentences on what concretely breaks, silently or otherwise, if a
team omits this pattern.

## Link to starter kit

**Kit:** `starters/your-pattern-name/README.md`
