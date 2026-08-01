# CLAUDE.md

Operating notes for Claude Code sessions working in this repository. The
rules that apply to every agent regardless of tool — the originality policy,
the page template, commit conventions, and the human-only status of
`graph-plan.md` — live in `AGENTS.md`. Read that file first; this one only
adds the details specific to running Claude Code here.

## Before committing any `docs/` change

Run the originality checker and make sure it exits clean:

```bash
node scripts/originality-check.mjs
```

This walks every file under `docs/`, compares it against the cached source
text (or, if no cache is present yet, checks each page against every other
page for accidental self-duplication), and fails on any run of eight or more
consecutive words that matches. Treat a red run as a hard stop, not a
warning: rewrite the flagged passage from your own understanding of the idea
rather than rewording around the exact phrase it caught. This same check
runs in CI on every push and pull request, so catching it locally first
saves a review cycle.

## Where the day-by-day plan lives

The actual task breakdown for this build is not in this file — it's in four
sibling documents at the repo root:

- `day-1-plan.md` — repo foundation, prerequisites, and foundations.
- `day-2-plan.md` — the full 17-step course and its assessments.
- `day-3-plan.md` — the pattern library, practice projects, and the advanced
  tier.
- `day-4-plan.md` — the website build and final polish.

These four files are the authoritative source for what gets built and in
what order. If a task here in this repo seems to disagree with what one of
those plans says, the plan wins; open a question for the human owner rather
than improvising a different task list. `STATE.md` tracks which of the four
days this repo is currently on, and `loop-run-log.md` records what actually
happened during each day's work.

## Everything else

Rules that hold regardless of which agent tool is doing the work — the
originality policy, the concept-page template, commit conventions, and the
rule that only a human edits `graph-plan.md` — are in `AGENTS.md`, not
duplicated here. If something in this file and something in `AGENTS.md`
appear to conflict, treat `AGENTS.md` as authoritative and flag the
conflict for a human to resolve.
