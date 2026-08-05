# loop-budget.md

`graph-plan.md` §11 makes the point that graph infrastructure has a real
cost — schemas, resolution, provenance, subgraph construction — and that the
honest first question is always whether that cost is justified at all, not
just how to pay it. The same question applies one level down, to the loops
that maintain this repository itself: a loop with no limit on how much it
can touch in a single run can rack up a review burden, or a blast radius,
that costs more than the drift it was built to catch. This document sets
that limit for each loop named in `LOOP.md`.

## Content loop budget

One page, or one tightly related small group of pages, per pull request. A
PR that touches an entire part of the course at once is too large for a
human reviewer to check carefully in one sitting, and it makes the
originality checker's output harder to read — a single failing PR with
twenty pages in it forces the reviewer to hunt for which page actually
tripped the check. Splitting work into small, single-topic PRs keeps each
review cheap and keeps `git blame` pointing at a specific, understandable
change rather than a bundle of unrelated ones.

If a change genuinely can't be split — renaming a term that appears across
many pages, for instance — that's no longer an ordinary content-loop run; it
needs a human decision to treat it as a one-off, reviewed with extra care,
not a routine PR.

## Audit loop budget

Unlimited in what it may *look at* — it is expected to sweep the whole repo
every run, that's the point of its wider vantage point — but strictly
read-only in what it may *do*. It produces a report and, if something is
wrong, opens a single issue describing what it found. It never opens a PR,
never pushes a fix, and never auto-merges anything, even a change that looks
trivial like a single corrected link. The moment an audit loop starts
patching what it finds, it stops being a check on the content loop and
becomes a second, unsupervised writer with none of the content loop's
review discipline — which recreates exactly the kind of ungoverned loop
this course exists to warn against.

## Why the budget stays this small

A tighter budget costs more human review hours up front, in the sense that
more, smaller PRs get looked at instead of fewer, larger ones. That cost is
worth paying here because the failure mode on the other side — a large,
hard-to-review change slipping a subtle originality violation or a broken
link into the course — is expensive to catch after the fact and expensive to
a learner who trusts the material. If maintaining this repo ever stopped
needing that level of care — say, if the content froze entirely and updates
became rare, small corrections — shrinking or retiring one of these loops
would be the right call, per the same not-every-problem-needs-this-much-
machinery reasoning §11 applies to the course's own subject matter.
