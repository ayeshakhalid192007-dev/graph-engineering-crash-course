# Sources

This page is the canonical attribution record for the Graph Engineering Course. Every idea this course borrows is credited here to where it came from. Nothing on this page, or anywhere else in this repository, is copied from the sources below — each entry states the idea we took and, in our own words, why it earned a place in the curriculum. Where a page elsewhere in this course credits a concept, it links back to the matching entry here rather than re-explaining who the person or project is.

Ten sources shaped this course. Nine were read in full for their mechanisms and then set aside before any of our material was drafted. The tenth is a short, named, direct quotation, handled as a quotation on purpose — everywhere else, credit goes to the idea, never to the sentence that first expressed it.

---

## 1. Panaversity — Graph Engineering: A Crash Course

agentfactory.panaversity.org

This is the course whose scope this project measures itself against: it walks through roughly a dozen and a half concepts spread over seven parts, and that shape told us how much ground a graph-engineering curriculum needs to cover to be complete rather than a sampler. We treated it strictly as a map of *what to teach*, never as a script for *how to say it* — every explanation, example, and diagram in this repository was built independently from the concept list, not adapted from its prose.

## 2. Panaversity — Loop Engineering: A Crash Course

agentfactory.panaversity.org

Before a reader gets here, this material assumes they already know how a single automated loop behaves — its heartbeat, its spine, and the maker/checker split that keeps one loop honest. We lean on that shared vocabulary instead of re-teaching it, which is what lets this course start from "now put more than one loop in the room" rather than from first principles.

## 3. Panaversity — Harness Engineering: A Crash Course

agentfactory.panaversity.org

The second prerequisite hands us a vocabulary for keeping a single agent inside its lane — constrain, inform, verify, correct, escalate. Graph Engineering doesn't replace that vocabulary; it gives those same five moves somewhere durable to write their results, so a fact one agent verifies can be trusted by another agent that never ran the check itself.

## 4. Andrej Karpathy — `autoresearch`

github.com/karpathy/autoresearch (MIT)

The idea we took from this project is a discipline more than a design: log every attempt a system makes, discard nothing, but only let the runs that actually improved on their predecessor become the record future attempts build on. That ratchet — history that only moves forward — is what keeps a long-running graph from either losing hard-won progress or accumulating every false start as if it mattered equally.

## 5. Andrej Karpathy — `AgentHub` (sketch)

referenced via companion coverage; original repo no longer public

Even known only through secondhand description now, the mechanism worth keeping is clear: a branch of exploration that fails doesn't have to disappear. Turned into a node that later work can still query, a dead end stops being wasted effort and becomes evidence — proof that a particular path was tried and what it produced, available to anything that asks.

## 6. Anthropic — Knowledge Graph Construction Cookbook

platform.claude.com/cookbook

What this source demonstrates is that turning unstructured text into graph-shaped facts doesn't require a dedicated natural-language-processing pipeline — asking a capable model for structured output, against a schema you define up front, does the same job with far less machinery. That schema-first move is the extraction mechanism this course teaches as the default, rather than the classical NLP techniques it displaces.

## 7. Anthropic — Dynamic Workflows in Claude Code

code.claude.com/docs

This source names the exact scale problem this entire course exists to answer: a session that fans out into many sub-agents running in parallel, each one starting with no memory of what the others have already found or decided. That gap between "many workers" and "one shared understanding" is the problem a graph is built to close, and it's the reason this course treats memory as infrastructure rather than an afterthought.

## 8. Carlos E. Perez — "From Loop Engineering to Graph Engineering?"

essay

The contribution we credit here is a diagnostic frame: a single loop, however well built, tends to fail in a small number of recognizable ways once it's asked to coordinate with others or hold state across time. Naming those failure modes is what makes the case that the fix isn't a smarter loop — it's governance structure sitting around the loop, which is exactly what a graph of nodes and edges provides.

## 9. Peter Steinberger — public statement, mid-2026

attributed quote

The practice this course teaches didn't start as an abstract design exercise — it started as someone naming, plainly, why a habit they'd already adopted mattered. That statement is quoted directly below, in the person's own words, because paraphrasing it would blur the one thing worth preserving exactly: the motivation in the voice that first stated it.

<!-- attributed-quote:steinberger -->
<!-- BLOCKED: awaiting real quote -->
> "the exact quoted words go here" — Peter Steinberger

**BLOCKED: need the real Peter Steinberger quote text and its exact source URL/date from the user before this file can be finalized.** No quote has been fabricated; the marker above is a placeholder only, flagged for resolution at the Day 1 checkpoint.

## 10. Panaversity — `agentfactory-labs` companion repo

github.com/panaversity/agentfactory-labs/tree/main/crash-course/graph-eng

What we took from this repository is structural, not literal: proof that a companion set of small, runnable, dependency-free demos belongs alongside a course like this one, so a learner can execute an idea instead of only reading about it. Every live lab in this course is written from scratch against our own scenarios — none of this repository's code is reused — but the decision to ship labs at all, and to keep them minimal enough to run without a heavy setup, follows the precedent this companion repo set.

---

Placeholder attribution identity for this repository: **Graph Engineering Course Contributors**, pending confirmation of a real identity before publishing (see `CITATION.cff`).
