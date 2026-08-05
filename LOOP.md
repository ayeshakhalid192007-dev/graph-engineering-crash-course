# LOOP.md

This repository is not just a pile of files — it is maintained by a small
number of loops, in the sense this course itself teaches: a heartbeat that
fires on some trigger, a spine — the durable state each loop picks up at the
start of a turn and writes back at the end — that carries it from one run to
the next, and a maker/checker split so the loop doesn't get to grade its own
homework. This document names the loops that actually keep this repo
correct, what each one touches, and the two structural guarantees — an
anchor and a set of frozen nodes — that stop those loops from drifting into
a shared, self-consistent delusion about the state of the course.

## The content loop

This is the loop that produces new material. A writer (human or agent) drafts
or revises a page under `docs/`. The checker step is mechanical and runs
before anything merges: `scripts/originality-check.mjs` confirms the new
prose doesn't share an eight-word run with cached source text or with another
page in this repo, and `markdown-lint` confirms the page is well-formed. Only
after both come back clean does a human reviewer read the page and merge it.
The maker (the writer) and the checker (the two automated gates plus the
human reviewer) are deliberately different parties — a writer cannot merge
their own page on the strength of their own judgment that it's fine.

The content loop's scope is narrow on purpose: it looks at the page in front
of it, and the sources that page might be echoing. That narrowness is what
makes it fast and cheap to run on every single change. It is also exactly why
it can't be the only loop watching this repo.

## The audit loop

Some problems are invisible from inside a single page's diff. A link that
pointed somewhere valid last month can rot silently once a target page is
renamed three commits later, in a PR that never touched the page holding the
link. A pattern kit can drift out of sync with the Graph Ready checklist one
small edit at a time, with no single commit looking suspicious. The content
loop, reviewing one page at a time, structurally cannot catch either of
these — it never has the whole repo in view at once.

The audit loop exists to look from a wider vantage point than any single
content-loop run does. It's a periodic pass — run on a schedule and on
every push, not triggered by any one writer's PR — that runs `link-check`
across every page in the repo and `graph-ready-audit` across every pattern
kit, regardless of which change might have caused a given problem. This
follows the same governance-graph fix this course teaches for a loop that's
structurally blind to a whole category of failure from where it sits: rather
than trying to make the narrow loop smarter, add a second loop built to take
in more of the repo at once.

The audit loop is read-only. It never edits a page, never rewrites a link,
and never touches a pattern kit itself — it opens an issue describing what it
found and stops there. Fixing what it flags is still a content-loop change,
reviewed the normal way.

## The anchor

Both loops answer, ultimately, to something outside themselves: the CI
workflows in `.github/workflows/` (`originality-check`, `link-check`,
`markdown-lint`, `graph-ready-audit`, `registry-validate`, `web-build`),
running as real automated checks against the actual repository state on a
real server, not a loop's own self-report of how it thinks it did. A loop
claiming its output is clean is not the same thing as CI actually passing,
and only the latter counts as done. This is the anchor: a signal neither
loop can quietly satisfy by agreeing with itself.

## The frozen nodes

Two things in this repository no loop — content or audit — may ever rewrite,
no matter how convenient it would be in the moment:

- `graph-plan.md`, the master spec (see `AGENTS.md` §1).
- The ten source entries in `resources/sources.md`, this course's
  attribution record.

Both stay fixed points that every loop's output can be checked against, but
that no loop's output can feed back into changing.
