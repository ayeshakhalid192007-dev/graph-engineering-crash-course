# Step 14 · Six Honest Questions Before You Build

## Hook

Bramble & Co. is three people — a designer, a developer, and a part-time bookkeeper — and a new operations hire has just come back from a conference talking about knowledge graphs. She pitches putting one in front of everything the studio touches. Four candidates get written on the whiteboard. Five client onboarding checklists, each running for a different client with nobody's steps depending on anybody else's. One forty-page vendor contract legal needs a yes-or-no read on before Friday. A short list of which of the studio's three subcontractors is certified for which of two specialties, a list that has changed exactly once in the fourteen months since it was written. And a genuinely tangled one: which of this year's paid invoices trace back to which signed statement of work, needed because an audit is coming and "we're pretty sure it's fine" will not be an acceptable answer to the auditor.

The pitch treats all four as the same kind of problem — four things the studio doesn't currently have structured, so four things a graph would fix. Before anyone opens a schema file, the honest move is to ask the same six questions of all four, expecting them to land in different places, because they aren't the same kind of problem at all.

## Explanation

Every one of these six questions is a version of the same underlying check: does the thing you're about to build cost less than the thing it's replacing, once you count the parts that don't show up until later. A schema has to be designed. Extraction has to be run and rerun as new material shows up. Whatever gets merged as "the same thing" has to stay reversible. Every claim needs a record of where it came from. None of that is free, and none of it is optional once you've committed to it — a graph half-built and then abandoned is worse than no graph, because it leaves behind claims nobody is maintaining and nobody has agreed to trust.

**Do the pieces actually depend on each other, or are they just running next to each other?** The five onboarding checklists fail this one outright — nothing about Client A's step 3 has any bearing on Client B's step 3. Independent work with no cross-references doesn't need shared memory; it needs a queue, something that hands out the next item and tracks what's done, and a queue is a far cheaper thing to build and reason about than a graph.

**Is the honest answer already sitting inside one document?** The vendor contract is single-source: everything legal needs is in that one PDF, and the job is reading it well, not connecting it to anything else. A good prompt against that one document beats a schema and an extraction pipeline built to serve exactly one source.

**Is the real relationship set small, fixed, and basically done changing?** Three subcontractors, two specialties, one change in over a year — that's a spreadsheet tab, not a graph. A **[schema](../02-foundations/glossary.md#schema)** earns its cost on a relationship set that grows or shifts; it's pure overhead on one that doesn't.

**Will anything downstream ever need to ask where a claim came from?** This is where the audit trail candidate starts looking different from the other three. "We checked, it's fine" is not a sentence an auditor accepts — the studio needs to point at a specific invoice and a specific statement of work and show the connection, which means every claim needs a **[provenance](../02-foundations/glossary.md#provenance)** record from the moment it's created, not bolted on afterward once someone asks.

**Is there a team here large enough, and sticking around long enough, to carry this as upkeep?** A graph built once and never touched again decays the moment the underlying material changes and nobody updates it. Three people is a real answer here, not an automatic disqualifier — but it means whoever owns the invoice-to-SOW tracking has to actually keep owning it, not build it as a one-week project and move on.

**How fast does the underlying relationship set turn over?** Invoices and statements of work accumulate all year, steadily, in a way that makes a static list stale within a month of finishing it. That's different from "changes once every fourteen months," and it's the difference between a table that can just be edited by hand and a system that needs an ongoing extraction step to stay current.

Run all four candidates through all six questions and only the invoice-to-SOW tracking passes cleanly: real dependencies, material spread across many documents rather than one, a relationship set that keeps growing, a real downstream need to trace a claim to its source, a team willing to maintain it, and a pace of change too fast for a table someone edits by hand once a quarter. The other three each fail on a different question, which is the point — this isn't a checklist that always says no, and it isn't one that always says yes. It's honest in both directions.

## Diagram

```mermaid
flowchart TD
    Q1{"Real dependencies,<br/>or independent work?"}
    Q2{"One document,<br/>or many sources?"}
    Q3{"Small & fixed,<br/>or growing?"}
    Q4{"Ever need to trace<br/>a claim to its source?"}
    Q5{"Team can carry<br/>the upkeep?"}
    Q6{"Domain changes<br/>faster than a table?"}
    BUILD["Build the graph"]
    SKIP["Skip it -- queue,<br/>prompt, or table instead"]

    Q1 -- "independent" --> SKIP
    Q1 -- "real deps" --> Q2
    Q2 -- "one doc" --> SKIP
    Q2 -- "many sources" --> Q3
    Q3 -- "small & fixed" --> SKIP
    Q3 -- "growing" --> Q4
    Q4 -- "no downstream need" --> SKIP
    Q4 -- "yes" --> Q5
    Q5 -- "no team to own it" --> SKIP
    Q5 -- "yes" --> Q6
    Q6 -- "slow, table keeps up" --> SKIP
    Q6 -- "fast, table goes stale" --> BUILD
```

Any single "skip it" answer ends the checklist for that candidate — a graph isn't the tiebreaker for five yeses and one no, because the one no is telling you exactly where the cost stops being worth paying.

## Claude Code vs OpenCode

Both configurations run the same six questions against a described situation, in the same order, and stop at the first question whose answer already settles it rather than working through all six once a verdict is clear.

### Claude Code

```markdown
---
name: pre-build-checklist
description: Runs a described situation through six honest questions and reports build-a-graph or skip-it, naming the question that decided it.
---

1. Read the situation description. Identify what's actually being asked
   for: tracking, answering, or synthesizing something.
2. Ask, in order, stopping at the first "skip it" answer:
   - Do the pieces genuinely depend on each other, or are they
     independent work items?
   - Does the answer live inside one document, or does it require many
     sources?
   - Is the relationship set small and essentially fixed, or does it
     grow?
   - Will anything downstream need to trace a claim back to where it
     came from?
   - Is there a team able to maintain this as ongoing upkeep, not a
     one-time build?
   - Does the underlying domain change faster than a manually-edited
     table could track?
3. Report "build a graph" only if every question points that way.
   Otherwise report "skip it" and name the specific question that ended
   the check -- never just "no" without saying which one.
```

### OpenCode

```markdown
---
description: Check a described situation against six honest pre-build questions and report which one settled it
---

Take the situation as given and work through six questions in order,
stopping the moment one of them settles the case: real dependencies
between the pieces, one document versus many sources, a small fixed
relationship set versus a growing one, a genuine downstream need to
trace a claim to its origin, a team able to maintain this over time
rather than just build it once, and a domain that changes faster than
someone could keep a table current by hand. Only recommend building a
graph if all six point that direction -- and whenever the answer is
"skip it," name the exact question that decided it instead of returning
a bare no.
```

## Going Deeper

Notice that none of the six questions asks whether a graph *could* model the situation. Almost anything can be modeled as nodes and edges — that's close to the definition of a graph, not a reason to reach for one. The six questions are deliberately not about capability; they're about cost, ongoing cost specifically, because the expensive part of graph engineering was never drawing the first diagram. It's the extraction pass that has to keep running as new material shows up, the resolution decisions that have to stay reversible, and the provenance records that have to be written honestly every time, forever, or the whole structure quietly turns into decoration nobody trusts. A team that answers all six questions "yes" and builds the graph anyway without budgeting for that ongoing cost hasn't avoided the mistake this checklist exists to catch — they've just delayed it past the point where the checklist could still help.

## Check Yourself

<details>
<summary>The subcontractor-certification list has changed once in fourteen months, but the ops hire points out that the studio is about to double its subcontractor roster this quarter. Does that change the verdict, and which question moves? Reveal the answer.</summary>

It's worth re-asking, yes — and the question that moves is the last one, how fast the domain changes, not the third one about whether the relationship set is small and fixed. A roster about to double is signaling a coming shift in turnover rate, not proof that the *current* set is already large or already growing; three subcontractors and two specialties is still small today. The honest move isn't to jump straight to "build a graph" on an anticipated future — it's to notice that question six is trending toward "yes" and revisit the checklist once the roster has actually grown, rather than build ahead of a change that hasn't happened yet. A **[pre-build checklist](../02-foundations/glossary.md#pre-build-checklist)** is meant to be asked again when the situation changes, not answered once and filed away.

</details>

## Try With AI

Pick something at work or in a personal project that you've been tempted to build "real" tracking for — a spreadsheet, a notes file, a shared doc. Describe the situation honestly to Claude Code or OpenCode in a sentence or two, including who else touches it and how often it changes, and ask it to run your six-question checklist against it. See whether it stops early with a clear "skip it, and here's the question that decided it," or works all the way through to a "build a graph" verdict — then decide for yourself whether you agree with where it stopped, especially on the team-size and change-speed questions, which are the two most likely to need judgment the tool doesn't have access to.

## When It Goes Wrong

**Symptom:** a team builds a graph, uses it for a month, and then it silently stops being updated while everyone quietly goes back to asking each other in chat.

**Cause:** the checklist either never ran, or ran and got overridden by enthusiasm for the idea rather than an honest answer to the team-size and maintenance-cost question — the graph was buildable, but nobody had actually committed to keeping it current.

**Fix:** run all six questions before any schema work starts, and treat a "no" on the team-size or change-speed question as disqualifying on its own, not as one vote among six. `labs/step-14-six-questions-checklist.py` runs three planted situations — an independent task queue, a single-document question, and a genuinely graph-shaped tracking problem — through the checklist and asserts each one gets the verdict it should.

---

Back to [Part 6 overview](README.md) · Step 15 takes the one candidate that passed and actually builds it, twice, once per tool.
