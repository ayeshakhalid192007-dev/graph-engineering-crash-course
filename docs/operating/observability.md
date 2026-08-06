# Observability

## Hook

A graph that's running doesn't announce when it's quietly going wrong — no exception fires when a fact graph grows too fast, or when a checker starts waving through claims it shouldn't. The signals below are the ones worth watching on purpose, because none of them shows up on a generic uptime dashboard.

## Explanation

### Growth rate of the fact graph

A work-history graph is supposed to grow with every attempt — a high growth rate there just means a lot of work is happening. A fact graph is a different instrument. Its growth rate should be slow and deliberate: every node earns its place by being checked, not just proposed.

A fact graph whose growth rate starts tracking the work-history graph's is worth investigating on sight. It usually means something upstream stopped checking claims carefully, and started admitting them the way a work-history graph does — on the strength of an attempt having been made, not a claim having been verified.

### How often the grounded checker rejects a claim

The grounded checker's rejection rate is worth a standing chart of its own, not just a pass/fail read on any single claim. A rejection rate that's rising over time is a signal before it's a crisis — it can mean upstream extraction has started producing claims that don't hold up, or that whatever generates claims for the checker has drifted from what the graph actually contains.

Either way, the rejection itself already did its job. The rate over time is what tells a team something changed — days or weeks before any single rejected claim would have been notable enough to investigate on its own.

### Supersession rate versus silent correction

A healthy fact graph supersedes claims regularly — that's what routine re-verification looks like, added up across a graph's history. A supersession rate of zero over a long stretch is itself a little suspicious: it usually means nothing is being re-checked, not that everything is already correct.

What should never happen, at any rate above zero, is a **silent correction** — a claim's fields changing with no new claim, no new provenance record, and no `supersedes` edge to show for it. A supersession is visible in the graph's own structure; a silent correction, by definition, isn't. It can only be caught by comparing what a claim used to say against what it says now, and noticing the record itself changed shape with no trail behind it.

Any confirmed instance of that is a provenance failure, not a data-quality nitpick — it means the one property the rest of this course's write path depends on, that the graph never quietly rewrites its own past, has already been broken once.

## Related

- [`safety.md`](safety.md) — the append-only discipline that makes a supersession-vs-silent-correction check possible to run in the first place.
- [`anti-patterns.md`](anti-patterns.md) — design anti-patterns that these signals tend to catch early, before they harden into a structural problem.
