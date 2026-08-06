---
name: file-graph-for-small-teams
category: G-storage
stage: storage
cost: low
tools: [Claude Code]
core: false
---

# file-graph-for-small-teams

This kit is the runnable companion to the `file-graph-for-small-teams`
pattern specification (`patterns/file-graph-for-small-teams.md`). It is
an extended kit — a single Claude Code reference implementation, lighter
than the full multi-tool anatomy the seven core kits carry. See
`starters/README.md` for that distinction.

## What it does

Keeps the graph's nodes and edges as plain JSON inside a git repository,
so a change to the graph is a change a normal pull request already knows
how to show: a diff, a reviewer, and a merge, with no database to stand
up or operate on the team's behalf.

## Inputs

- Nodes and edges serialized as JSON, in one file or a small set of
  files per graph.

## Outputs

- A version-controlled graph whose full history is nothing more than the
  repository's own commit log.

## Failure mode if skipped

A team stands up and maintains a database for a graph a handful of
reviewable JSON files, checked in like any other source file, would have
served just as well — paying setup and operational cost for
concurrency guarantees a three-person team touching the graph a few
times a week never actually needed.

## Worked scenario

Larkspur Tape Archive, a fictional three-volunteer community radio
archive project, keeps its whole catalog — recovered tape reels, the
programs recorded on them, and the hosts who ran those programs — as
nodes and edges in a single `graph.json` file committed to a shared git
repository. When a volunteer catalogs a newly recovered reel, they open a
pull request adding the new node and its edges, exactly the way anyone
on the project would propose a change to any other file. Reviewing one
such PR, a second volunteer notices the proposed edge attributes a reel
to the wrong host — a handwriting misread on the reel's box label — and
catches it in the diff before it ever reaches the shared history. See
`README.md` for the reel in question and the correction the review
caught.

## Link to starter kit

**Kit:** `starters/file-graph-for-small-teams/README.md`
