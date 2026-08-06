---
name: code-change-to-graph
category: A-extraction
stage: write
cost: medium
tools: [Claude Code]
core: false
---

# code-change-to-graph

## What it does

Reads a diff and records every function or module it touches as a node,
connected back to the entity it changed by a `modifies` edge. The graph
ends up with a queryable trace of what a change actually affected, separate
from the diff text itself.

## Inputs

- A diff or commit.
- The existing graph of code entities (functions, modules, files) it may
  touch.

## Outputs

- New or updated nodes for each touched function or module.
- A `modifies` edge from the change to each entity it altered.

## Failure mode if skipped

The only record of what a change touched is the diff text — useful in the
moment, unqueryable later, and gone from working memory the instant the
branch is merged and the context window that reviewed it closes.

## Link to starter kit

**Kit:** `starters/code-change-to-graph/README.md`
