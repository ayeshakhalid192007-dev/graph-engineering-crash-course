---
name: task-scoped-retrieval
category: D-subgraph
stage: read
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# task-scoped-retrieval

## What it does

Builds a subgraph containing only the nodes and edges relevant to one
worker's specific task, rather than handing that worker the entire graph
and trusting it to find what matters (the read-path move from Step 9).

## Inputs

- A description of the task a worker is about to run.
- The full graph the subgraph is drawn from.

## Outputs

- A bounded subgraph scoped to that one task.

## Failure mode if skipped

A worker either drowns in context that has nothing to do with its task, or
— just as likely — never sees the single edge its task actually depended
on, buried somewhere in everything else it wasn't given a reason to read.

## Link to starter kit

**Kit:** `starters/task-scoped-retrieval/README.md`
