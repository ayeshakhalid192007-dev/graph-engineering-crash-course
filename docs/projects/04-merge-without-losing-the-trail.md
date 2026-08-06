# Project 4 · Merge Without Losing the Trail

**Difficulty:** Intermediate–Advanced
**Time:** 45–60 minutes
**Concepts:** resolution, reversible merge, canonical node, stated-reason requirement
**Maps to:** Step 7 (Part 3 of the course) — the page on collapsing two mentions into one canonical node without deleting either. The [top-level docs guide](../README.md) has the direct link.

> **Throwaway repo, small data first.** Five support-ticket mentions of a name, none of them long — the whole point is deciding, carefully, whether they're one customer or two.

## The scenario

A small plant shop's support inbox has five tickets that each sign off with some variant of the same-looking name. Different agents typed what they heard or read differently — a full name here, a nickname there, an abbreviation somewhere else. Your job is to work out which of these five mentions actually refer to the same person, using something more solid than "the names look alike," and to do it in a way that could be undone later if you turn out to be wrong.

## Starting material

| Mention | Raw name | Source ticket | Email | Order # | Phone (last 4) |
| --- | --- | --- | --- | --- | --- |
| m1 | Jonathan Ferreira | #401 | `jonathan.ferreira88@gmail.com` | 10432 | — |
| m2 | Jon Ferreira | #405 | `jonathan.ferreira88@gmail.com` | 10432 | — |
| m3 | J. Ferreira | #412 | `j.ferreira@ferreiradesigns.com` | 10890 | — |
| m4 | Jonny F | #418 | `jonathan.ferreira88@gmail.com` | 11002 | — |
| m5 | Ferreira, J | #420 | — | 10432 | 4471 |

## Your task

1. In a throwaway repo, create `customers.json` and record all five mentions above as their own nodes — raw name, source ticket, and whatever contact fields that ticket recorded. Do not delete or overwrite any of them at any point in this project.
2. For each pair of mentions, decide whether you have a concrete, checkable reason to believe they name the same customer — a shared email address, a shared order number, a shared phone number. Spelling or nickname similarity alone does not count as a reason.
3. Group the mentions that share real evidence into one canonical `Customer` node each, and attach a `mentioned_as` edge from every original mention to its canonical node. Write the specific evidence for each grouping directly on the canonical node — not "names matched," but which field matched and across which tickets.
4. At least one mention in this set looks like it belongs with the others by name, but has no matching email, order, or phone with any of them. Leave it as its own unmerged canonical node, and write one sentence explaining what would need to show up in a future ticket before you'd merge it.
5. Check your work by picking one canonical node with more than one mention and asking: if someone deleted this node right now, could they reconstruct exactly which original mentions it contained and why, using only the merge reason you wrote? If not, the reason isn't specific enough yet.

## Done when

- All five original mentions still exist as their own nodes in `customers.json` — none were deleted, renamed, or overwritten during merging.
- Every canonical `Customer` node with more than one mention states the specific field (email, order number, or phone) that justified the merge, naming the tickets it came from.
- The one mention with no matching evidence is left unmerged, with a written reason for why — not silently folded in because the name looked close enough.
- Nothing in `customers.json` was merged on name similarity alone.

## Reference solution

[`solutions/04-merge-without-losing-the-trail.md`](solutions/04-merge-without-losing-the-trail.md) — the full resolved graph for the five mentions above, including which merge to make, which mention to leave alone, and why.
