# Step 16 · Recognizing the Skip-It Cases

## Hook

The Fernbank Tool Library lends drills, ladders, and garden equipment out of a converted garage, run entirely by five rotating volunteers and whoever shows up for a Saturday shift. A new volunteer coordinator spends her first week sitting in on every job the library does, and comes back convinced the whole operation should run on a knowledge graph. Four things end up written on the sign-out clipboard as candidates. This month's twelve open Saturday shifts, each claimed first-come-first-served by whichever volunteer signs their name next to it, with no shift's coverage depending on any other shift getting filled. The single donated liability-waiver template every first-time borrower signs, where the only live question this week is whether clause four covers a borrowed table saw. The pairing between the library's four tool categories — power, hand, garden, ladder — and the two short orientation sessions a volunteer has to sit through before they're allowed to hand that category out, a pairing that has changed exactly once since the library opened three years ago. And the scrap of paper at the desk tracking which borrower currently has which tool out, so that whoever's on shift can tell a caller whether the tape measure is free, reset and rewritten fresh most weekends.

She's right that none of these four is currently "structured," in the sense of living anywhere more durable than a clipboard or somebody's memory. She's not right that the fix is the same for all four — and working out which fix fits which candidate is exactly the judgment this page exists to sharpen.

## Explanation

Four situations come up often enough, across wildly different domains, that it's worth being able to recognize each one on sight rather than working through a long checklist every single time. Each has a lighter-weight answer than a graph, and reaching past that lighter answer straight for a schema and an extraction pipeline doesn't buy anything — it just adds a maintenance obligation nobody asked for.

**Work items with no real connection between them are a queue's job, not a graph's.** The twelve open shifts fail the dependency test outright: nothing about who takes Saturday's ten-to-two slot has any bearing on who takes Sunday's. A queue — something that lists what's open and marks an item claimed the moment someone takes it — covers this completely, and it does that without anyone having to design a schema for "shift" and "volunteer" first. The tell is simple: if you could hand every item to a different person working in total isolation and lose nothing, you're looking at a queue problem, not a memory problem.

**One source with one honest answer inside it calls for a careful prompt, not a pipeline.** The waiver question is single-source: everything relevant to "does clause four cover the table saw" sits inside one PDF, and the job is reading that PDF carefully, not connecting it to anything else the library holds. Building a **[schema](../02-foundations/glossary.md#schema)** and an extraction step to serve exactly one document, asked one question at a time, is infrastructure built for a scale this job will never reach.

**A relationship set that's small and holding still belongs on a plain table.** Four tool categories, two orientation sessions, one change in three years — that's a four-row, two-column grid a volunteer can read in ten seconds, not a graph. A schema earns its keep on a set of relationships that keeps taking new shapes; on one that's settled and small, it's overhead with nothing to show for it.

**And when no later reader will ever need to point back at where a claim originated, none of this gets built at all — not even a stripped-down provenance layer.** The who-has-what scrap of paper looks the most graph-shaped of the four, since it's genuinely about relationships between borrowers and tools. But nobody at Fernbank has ever needed to prove, three weeks later, exactly which loan record shows the tape measure left the building on a specific date — the only question anyone asks is "is it out right now," and the answer gets rewritten fresh most weekends anyway. Building **[provenance](../02-foundations/glossary.md#provenance)** — a record of source, run, and version on every claim — is pure cost when nobody later will ever ask the question that record exists to answer. Where the waiver and the orientation pairing get replaced by something lighter, this fourth candidate doesn't get replaced by anything at all; the scrap of paper is already the right amount of infrastructure.

None of this is a checklist that always lands on "don't build one." A fifth candidate — say, tracing a damaged power tool back through every borrower who's had it, because the library's insurer now requires proof of a maintenance chain before covering a replacement — would fail none of these four tests: real dependencies between borrowings, material spread across many loan records rather than one document, a relationship set that keeps growing every week, and a downstream party that will genuinely ask for the trail. That candidate is what a **[decision aid](../02-foundations/glossary.md#decision-aid)** like this one is for: not talking a team out of every graph, but sorting the four situations that don't need one from the rest, quickly, before a schema gets designed for a job a queue or a table already does.

## Diagram

```mermaid
flowchart TD
    START{"What shape<br/>is the job?"}
    A["Tasks with no<br/>real dependencies"]
    B["One document,<br/>one question"]
    C["Small, fixed<br/>relationship set"]
    D["Nothing downstream<br/>needs the source"]
    E["None of the above"]
    QUEUE["Use a queue"]
    PROMPT["Use a good prompt"]
    TABLE["Use a relational table"]
    SKIP["Skip the graph entirely"]
    BUILD["Build the graph"]

    START --> A --> QUEUE
    START --> B --> PROMPT
    START --> C --> TABLE
    START --> D --> SKIP
    START --> E --> BUILD
```

Landing in any of the first four boxes ends the question for that candidate. Only a job that clears all four does the fifth box — building the graph — become the right next move.

## Claude Code vs OpenCode

Both configurations take a described situation and sort it into one of the four skip-it patterns or, failing all four, a build recommendation — naming which pattern matched rather than returning a bare verdict.

### Claude Code

```markdown
---
name: skip-or-build
description: Sorts a described situation into one of four lighter-weight patterns, or recommends building a graph if none of the four fit.
---

1. Read the situation. Identify what's actually needed: getting work
   done, answering a question, tracking a relationship, or proving
   where a claim came from.
2. Check, in order, and stop at the first match:
   - Are the pieces independent of each other, with no piece's outcome
     depending on another's? -> recommend a queue.
   - Does the answer live inside exactly one document or source? ->
     recommend a good prompt against that source.
   - Does the set of relationships stay small and hold roughly still
     over time? -> recommend a plain table.
   - Would no later reader ever need to point back at the source a
     claim originated from? -> recommend skipping structured tracking
     entirely.
3. If none of the four match, recommend building a graph, and name
   which of the four conditions is the one that pushed it past every
   lighter option.
```

### OpenCode

```markdown
---
description: Match a described situation against four lighter-weight patterns before recommending a graph
---

Take the situation as given and check it against four patterns in
order, stopping at the first one that fits: independent tasks with no
real dependencies (a queue handles it), a single document holding the
whole answer (a good prompt handles it), a relationship set that stays
small and holds still (a table handles it), and a case where no later
reader will ever need to point back at where a claim originated (skip
structured tracking altogether). Only recommend a graph when the
situation clears all four -- and say explicitly which condition was
the one that ruled out every lighter option.
```

## Going Deeper

This four-pattern sort and the six-question checklist from Step 14 aren't doing the same job, even though they overlap. The six questions are built for the case that's already made it past an obvious "no" — a candidate worth taking seriously, where the honest answer might genuinely be to build. This page's four patterns are built for recognizing the obvious "no" faster, before spending time on a six-question pass at all: most independent task sets, single-document questions, small fixed tables, and no-provenance-needed logs are recognizable on sight once you know to look for the shape. Use this page's patterns as the fast first look, and reach for Step 14's longer checklist on whatever's left once the obvious skips are out of the way — running the full six questions against all twelve of Fernbank's open shifts would have gotten to the same "use a queue" verdict eventually, just with far more effort spent to get there.

## Check Yourself

<details>
<summary>Suppose the library's insurer starts requiring proof of who last had a damaged tool before approving a replacement claim. Which of the four patterns stops applying to the who-has-what scrap of paper, and what changes about the underlying job, not just the paperwork? Reveal the answer.</summary>

The fourth pattern — nothing downstream needs the source — is the one that stops applying, because now something downstream genuinely does: the insurer wants a specific loan traced back to a specific borrower and a specific date. What changes isn't just that a form now exists to fill out; it's that the scrap of paper, rewritten fresh every weekend, is actively hostile to the new job, since last month's entries are already gone by the time a claim comes in. This is also a case worth running through Step 14's full six questions rather than assuming the insurer's requirement alone settles it — a library filing one claim a year might still be better served by keeping dated paper logs in a folder than by building extraction and a schema for an event that happens once annually. The insurer's requirement removes one lighter-weight option; it doesn't automatically hand the graph the job by default.

</details>

## Try With AI

Pick something you or your team currently tracks informally — a spreadsheet, a shared doc, a channel everyone scrolls back through when they need an answer — and describe it honestly to Claude Code or OpenCode: what it's for, who touches it, and how often it changes. Ask it to sort your situation into one of this page's four patterns, or say plainly that none of the four fit. If it lands on a pattern, push back once by describing a small change to your situation — more contributors, a growing relationship set, a new party who'd want to trace a claim — and see whether the tool notices the verdict should move, or keeps defending its first answer past the point where the facts changed.

## When It Goes Wrong

**Symptom:** a team spends a week designing a schema and an extraction pipeline for something that turns out to be four rows in a spreadsheet, or a dozen independent tickets nobody needed connected in the first place.

**Cause:** nobody checked the shape of the job against the four common lighter-weight patterns before reaching for a graph, so the graph got built because it was capable of holding the data, not because it was the cheapest thing that could.

**Fix:** run the four patterns first, before any schema work starts, and only move to the longer six-question checklist for whatever's left once the obvious skips are ruled out. `labs/step-16-skip-decision.py` runs four planted situations — an independent shift roster, a single-document waiver question, a fixed orientation table, and a log nothing downstream will ever trace — through a small decision function and asserts each one resolves to the matching lighter-weight alternative rather than a graph.

---

Back to [Part 7 overview](README.md) · Step 17 turns to the graphs that do get built, and how much of one is actually worth building.
