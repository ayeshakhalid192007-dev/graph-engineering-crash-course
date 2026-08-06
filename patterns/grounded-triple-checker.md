---
name: grounded-triple-checker
category: E-checker
stage: read
cost: medium
tools: [Claude Code, OpenCode]
core: true
---

# grounded-triple-checker

## What it does

Breaks a claim down into the specific edges that would need to exist for
it to be true, then checks the graph for each one individually, rather than
judging the claim on how confident it reads (the checking move from Step
10).

## Inputs

- A claim to verify.
- The graph it should be grounded in.

## Outputs

- A verdict per required edge: present, missing, or contradicted.
- An overall pass/fail for the claim as a whole.

## Failure mode if skipped

A checker that only judges how confident a claim sounds ends up approving
claims that were never actually grounded in anything the graph can produce
evidence for.

## Link to starter kit

**Kit:** `starters/grounded-triple-checker/README.md`
