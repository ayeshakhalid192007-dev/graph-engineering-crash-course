# AGENTS.md

Operating rules for any agent — human-directed or autonomous, Claude Code,
OpenCode, or anything else — that touches this repository. These rules apply
regardless of which tool is doing the work. If you are looking for tool-specific
notes, see `CLAUDE.md`; the rules below sit underneath it and take priority
whenever the two seem to disagree.

## 1. `graph-plan.md` is the master spec, and it is human-only

`graph-plan.md` is the single source of truth for what this course is and how
it is built. No agent, loop, or automated process may edit it. It changes only
by direct action of the human owner of this repository. If a plan, a page, or
a piece of tooling seems to conflict with `graph-plan.md`, the plan wins and
the conflict gets flagged for the human to resolve — the fix is never to
quietly bring the spec in line with whatever the agent already did.

The same protection covers the source table in `resources/sources.md`: the
ten entries there (see below) are load-bearing attribution records, not
editorial copy, and no automated process may add to, remove from, or reword
that table.

## 2. The originality policy is not optional

Every `docs/` page in this course is written from a contributor's own
understanding of an idea, never with a source page open next to the editor
and never as a light rewording of someone else's sentences. This isn't a
style preference — it's mechanically enforced. Before any `docs/` change is
committed, `scripts/originality-check.mjs` must run clean. The full policy,
including the quoting exception for the one attributed statement in this
course, lives in `graph-plan.md` §2.1; the record of exactly which idea came
from which of the ten sources, and why it earned a place here, lives in
`resources/sources.md`. An agent that cannot make a page pass the originality
check should stop and rewrite from a blank page, not fight the checker with
synonym substitution — synonym-swapped plagiarism is still plagiarism, and the
checker is not the only line of defense; a human reviewer reads for it too.

## 3. Every concept page follows the same shape

`graph-plan.md` §12 defines one repeatable structure that every concept page
in this course uses, so a learner's reading habits transfer from page to page
instead of resetting each time. In short: open with a scenario built for this
course, explain the idea in plain language, illustrate it with a diagram
drawn fresh for this material, show it worked in more than one agent tool,
offer an optional deeper aside that still credits ideas rather than quoting
them, check understanding with one short question, hand the reader a real
exercise to run, and close with a troubleshooting box mapping a symptom to
its cause and its fix. An agent authoring or reviewing a page should check it
against the full template in §12 before treating it as done — a page missing
one of these pieces is an unfinished page, not a stylistic variant.

## 4. Commit small, one concern per commit

Every commit should do one identifiable thing. Adding a page, fixing a
broken link, updating tooling, and revising `STATE.md` are four different
concerns and belong in four different commits, even when they happen back to
back in the same session. This keeps `git blame` useful, keeps a bad change
easy to isolate and revert, and keeps `loop-run-log.md` entries meaningful —
a log entry that points at a commit doing five unrelated things tells a
future reader almost nothing. Write commit messages that describe what
changed and, briefly, why; a reviewer or a future agent should be able to
understand the change from the message alone, without opening the diff.

## 5. Where the other rules live

- `CLAUDE.md` — operating notes specific to working in this repo with Claude
  Code.
- `LOOP.md` — the loops that keep this repo's own content correct over time,
  and what each one is and isn't allowed to touch.
- `loop-budget.md` — how much each loop may change per run, and why.
- `loop-constraints.md` — hard limits no loop may cross, regardless of
  budget.
- `STATE.md` — which day and phase this repo's own build is currently in.
- `loop-run-log.md` — the append-only record of what each loop run actually
  did.
