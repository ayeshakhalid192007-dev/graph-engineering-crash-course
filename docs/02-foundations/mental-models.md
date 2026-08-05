# Mental Models

## Hook

Before any of the formal vocabulary — before "node," before "edge," before "provenance" — it helps to have a picture in your head of what a graph is actually *for*. Two everyday scenes do most of that work, and neither one requires knowing anything about graph theory to follow.

## Explanation

### A recipe notebook versus an expo rail

A home cook keeps a personal notebook: recipes, notes in the margin, a scribbled reminder that the oven runs five degrees hot. It works beautifully because exactly one person ever writes in it and exactly one person ever reads it, and those two people are the same person. Nothing about the notebook has to handle two hands reaching for the pen at once.

Now picture the expo rail in a busy restaurant kitchen — the strip of paper tickets where every station clips its order, and every cook, working a different station, glances at the same rail to know what's cooking, what's ready, and what's been sent back. Six people are reading and writing against the same shared surface at the same time, and the rail only works because it isn't just a notebook stretched across six people — it has structure. Each ticket is pinned in a specific place, marked with a specific status, tied to a specific table. That structure is what a graph gives a team of agents that a single shared file cannot: a place several writers can update without silently overwriting each other, because what each of them is allowed to touch is scoped and labeled, not a free-for-all blank page.

### A search team's incident board versus a hiker's trail journal

A solo hiker keeping a trail journal writes whatever she wants, in whatever order it occurs to her — "saw a fox," "trail forked, went left," "low on water." It's a personal record, and nobody but her ever has to make sense of it.

A search-and-rescue team coordinating a missing-person search cannot work that way. Someone maintains a board where each searched area is a distinct, labeled entry, connected to who searched it, when, and what they found — not a diary entry, but a specific claim: *this exact section, cleared, by this team, at this time.* That's the difference a graph's structure buys you over a shared pile of notes: not just that many people can write to it, but that what each contribution means is precise enough for someone else to act on without re-asking the person who wrote it.

Hold both pictures loosely as you go — the expo rail for why structure lets several writers share one surface safely, the incident board for why a labeled claim is worth more than a loose note. The formal vocabulary in the rest of this course is mostly just names for pieces you've already met in these two scenes.
