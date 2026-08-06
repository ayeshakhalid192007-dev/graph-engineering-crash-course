---
name: file-graph-for-small-teams
category: G-storage
stage: storage
cost: low
tools: [Claude Code]
core: false
---

# file-graph-for-small-teams

## What it does

Stores the graph as plain JSON files inside a git repository, so every
change to it is diffable, reviewable in a normal pull request, and needs no
database of its own to stand up.

## Inputs

- Nodes and edges serialized as JSON — one file, or a small set of files,
  per graph.

## Outputs

- A version-controlled graph whose full history is the repository's own
  commit log.

## Failure mode if skipped

A database gets stood up and operated for a graph that a handful of
reviewable JSON files would have served just as well, at a fraction of the
setup and maintenance cost.

## Link to starter kit

**Kit:** `starters/file-graph-for-small-teams/README.md`
