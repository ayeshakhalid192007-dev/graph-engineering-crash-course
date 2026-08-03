# Observability

## Hook

A graph that's running doesn't announce when it's quietly going wrong — no exception fires when a fact graph grows too fast, or when a checker starts waving through claims it shouldn't. The signals below are the ones worth watching on purpose, because none of them shows up on a generic uptime dashboard.

## Explanation

### Growth rate of the fact graph

A work-history graph is supposed to grow with every attempt, so a high growth rate there is just a sign of a lot of work happening. A fact graph is a different instrument, and its growth rate should be slow and deliberate — every node in it earns its place by being checked, not just proposed. A fact graph whose growth rate starts tracking the work-history graph's growth rate is worth investigating on sight: it usually means something upstream stopped checking claims carefully and started admitting them the way a work-history graph does, on the strength of an attempt having been made rather than a claim having been verified.

### How often the grounded checker rejects a claim

The grounded checker's rejection rate is worth a standing chart of its own, not just a pass/fail read on any single claim. A rejection rate that's rising over time is a signal before it's a crisis — it can mean upstream extraction has started producing claims that don't hold up, or that whatever's generating claims for the checker to verify has drifted away from what the graph actually contains. Either way, the rejection itself already did its job; the rate over time is what tells a team something changed, days or weeks before any individual rejected claim would have been notable enough to investigate on its own.

### Supersession rate versus silent correction

A healthy fact graph supersedes claims regularly — that's what routine re-verification looks like once it's added up across a graph's whole history, and a supersession rate of zero over a long stretch is itself a little suspicious, since it usually means nothing is being re-checked rather than that everything is already correct. What should never happen, at any rate above zero, is a silent correction — a claim's fields changing without a new claim, a new provenance record, and a `supersedes` edge to show for it. A supersession is visible in the graph's own structure; a silent correction, by definition, isn't, which means it can only be caught by comparing what a claim used to say against what it says now and noticing the record itself changed shape with no trail behind it. Any confirmed instance of that is worth treating as a provenance failure, not a data-quality nitpick, because it means the one property the rest of this course's write path depends on — that the graph never quietly rewrites its own past — has already been broken once.

## Related

- [`safety.md`](safety.md) — the append-only discipline that makes a supersession-vs-silent-correction check possible to run in the first place.
- [`anti-patterns.md`](anti-patterns.md) — design anti-patterns that these signals tend to catch early, before they harden into a structural problem.
