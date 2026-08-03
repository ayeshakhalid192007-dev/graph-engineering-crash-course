# Safety

## Hook

The four failure modes on this page's sibling are all about loops that behave exactly as designed and still go wrong. Safety is the layer underneath that: what happens when something with write access to the shared graph does not behave as designed at all — a bug, a bad prompt, a compromised credential, or a loop given more access than the job in front of it needed.

## Explanation

### A bad actor or buggy loop with write access

Any process with write access to a shared graph can, in principle, write something false, delete something true, or overwrite a claim other work already depends on. This isn't a hypothetical reserved for malicious actors — a loop with a bug in its extraction logic, or one pointed at the wrong graph entirely, does the same damage by accident, and does it faster than a person would, because nothing about running on a schedule slows it down to notice something looks wrong. The graph itself can't tell a deliberate attack from an honest mistake; both look the same from the inside, which is a write nobody meant to make.

### Append-only history and the supersession discipline

The safety net for that isn't trying to make every writer trustworthy — that's a losing bet against a system meant to run unattended. It's making the graph itself resistant to a bad write by never allowing an outright overwrite in the first place. Every claim that enters the graph stays in the graph; a correction doesn't erase the old version, it adds a new claim and marks the old one superseded, exactly as Step 8 (Part 3) describes for the ordinary case of a claim getting more accurate over time. The same discipline that keeps a graph's history honest as it improves also keeps it recoverable after damage: if a bad write lands, nothing about append-only storage prevented it, but everything the bad write would have destroyed is still sitting there under its old, unaltered status, waiting for someone to walk the record back and see exactly what changed and when. A graph that allows in-place overwrites has no such trail — a bad write and a clean history look identical the moment the overwrite lands, and there is no way to ask what used to be there.

### Access scoping

Append-only history limits the damage a bad write can do after the fact; scoping who can write at all limits how often the chance for one comes up in the first place. Not every worker touching the graph needs write access to the whole thing, and most don't — a loop whose entire job is checking claims against evidence has no legitimate reason to hold write access to the schema, and a worker fixing one function has no legitimate reason to be able to edit claims about a module it never opened. This is the same principle Step 9 (Part 4) applies to reading — handing a worker only the slice it needs rather than the whole graph — extended to writing: the smaller the set of things a given process can touch, the smaller the blast radius when that process turns out to be the one that goes wrong.

## Related

- [`observability.md`](observability.md) — what to actually watch once these safeguards are in place, including the signal that tells you provenance broke down somewhere.
- [`failure-modes.md`](failure-modes.md) — the four ways a loop fails while behaving exactly as intended, distinct from the operational risks on this page.
