# Loop Run Log

Append-only. Never edit or delete a prior entry — if a past entry turns out
to be wrong, add a new entry that supersedes it and says so.

## 2026-07-31 — Day 1 kicked off

Repo initialized locally (no remote yet). Day 1 plan (`day-1-plan.md`)
approved and execution started: root project files, dogfooding files,
prerequisites, foundations, originality-check tooling.

## 2026-08-01 — Day 1 complete

All Day 1 tasks done: root project files, resources/sources.md (blocked on
real Steinberger quote text), .github scaffold, originality-check.mjs,
dogfooding files, 00-start-here/01-prerequisites/02-foundations docs.
originality-check: 24 files checked, 0 violations. Manual link check: 0
unexpected broken links (17 expected 404s are Day 2 step pages, out of
scope per plan). Awaiting user approval before day-2-plan.md.

## 2026-08-03 — Day 2 complete

All 17 step pages, 7 quizzes, and 6 flashcard sets (Part 6 has quiz only,
per §23) written across Parts 1–7, plus `docs/methods/` (build-a-graph
method, pattern picker, decision framework), `docs/operating/`
(anti-patterns, failure modes, safety, observability), and 17 live-lab
scripts under `docs/0N-part-*/labs/`. `scripts/verify-labs.sh` added and
run: 17/17 PASS. originality-check: 61 files checked, 0 violations.
Manual link check: 165 relative links resolve, 0 broken, including
`docs/README.md`'s 17-step table of contents (written Day 1) now hitting
real files for the first time. Also batch-fixed the stale Day 1 placeholder
text in all seven Part `README.md` files plus `docs/operating/README.md`
and `docs/methods/README.md`, none of which had been updated since Day 1.
One open item carried forward: "contradiction-aware bundle" (this repo,
introduced in Part 4) vs. "conflict-aware-bundle" (graph-plan.md §17) is a
naming mismatch that needs reconciling before Day 3's pattern library task
references either name. Awaiting user approval before day-3-plan.md.

## 2026-08-03 — Day 2 content restyled for readability

User feedback: the 17 step pages read as dense, uniform paragraphs and
needed a more scannable, professional style, modeled on the maintainer's
companion Loop Engineering course repo. Restyled all 17 Steps
(`docs/03-part-1-…` through `docs/09-part-7-…`), plus `docs/methods/` and
`docs/operating/` — 27 files total, one commit per Part/group (9 commits).
Changes are presentational only, applied uniformly: subheadings and
numbered/bulleted lists inside Explanation, an added "Edge cases worth
naming" list per Step, "When It Goes Wrong" converted from one bolded
Symptom/Cause/Fix paragraph to a multi-row table, and a short glossary
(and, where relevant, source-attribution) line before each Step's closing
navigation. `docs/methods/build-a-graph-method.md`'s six lettered stages
and `pattern-picker.md`'s seven categories were converted to tables.
`docs/operating/` pages got shorter paragraphs and bulleted intros;
`failure-modes.md`'s existing table was left as-is. No technical content,
example, diagram, or code sample changed — every edit was re-verified
against the §12 template shape and the originality checker after each
group. originality-check: 61 files checked, 0 violations (iterated
several times per group to resolve self-duplication in repeated
boilerplate — e.g. footer phrasing and "When It Goes Wrong" table headers
— before each commit). markdownlint: 0 issues across all 27 touched
files. Quizzes, flashcards, and labs were read and left unchanged; they
were already short and structured. The Part 4 naming-mismatch item above
is still open and untouched by this pass.

## 2026-08-04 — Naming mismatch reconciled, Day 2 approval gate cleared

Resolved the one open item from Day 2: Part 4 used "contradiction-aware
bundle" while graph-plan.md §17 (and day-3-plan.md's `registry.yaml`,
Task 1 Step 3) name the same pattern `conflict-aware-bundle`. Renamed all
four occurrences in `docs/06-part-4-working-from-the-graph/step-9-…md`
and `flashcards.md` to "conflict-aware bundle", matching the canonical
pattern name. No other content changed. originality-check: 61 files
checked, 0 violations. `STATE.md`'s Day 2 row now shows no open items.
User has reviewed and approved proceeding to `day-3-plan.md`; Day 3's own
independent `/loop` starts next.

## 2026-08-06 — Day 3 complete

Pattern library complete: 23 specs, 7 full multi-tool core kits, 16
single-tool + porting-note extended kits. 8 projects with reference
solutions, three cheatsheets, the Ultra-Pro advanced tier, and the
assessments (final exam, capstone rubric, Graph Ready certification) all
written. The three remaining gate scripts — `link-check.mjs`,
`validate-registry.mjs`, `graph-ready-audit.mjs` — now exist, and the Day
1 existence guards that let their workflows pass by skipping have been
removed. All four CI gates green: originality-check 86 files / 0
violations, link-check 270 files / 0 broken links, validate-registry 23
patterns / 0 errors, graph-ready-audit 23 kits / 0 violations.
markdownlint clean across all 86 linted files. Deliverable 1 is
feature-complete.

Verified at close-out: registry holds 23 entries, exactly 7 marked `core:
true`, and those 7 are precisely the kits carrying an `opencode/`
directory; the other 16 each carry a `PORTING.md`. (An eighth `opencode/`
directory exists under `starters/_template/`, which is the scaffold and
correctly ships both tool directories.)

Three judgment calls from this day need sign-off at the approval gate.
Two were anticipated in `day-3-plan.md`: all 16 extended kits use Claude
Code as their single reference tool rather than a mix, and
`patterns/registry.yaml` is validated by a hand-rolled parser scoped to
that file's flat shape rather than by a YAML library dependency.

The third was not anticipated and was approved by the user mid-run.
`scripts/originality-check.mjs` — a Day 1 deliverable and a live CI gate
— now scans prose only: fenced code blocks, inline code spans, and the
URL half of Markdown links are removed before the 8-word-run scan. The
trigger was Task 11: a project page's starting material and its reference
solution's worked result legitimately show the same JSON record, and the
checker was reporting all 55 such runs as duplication, plus 8 more where
two pages linked to the same document or shared a long page title. The
change matches the policy `day-3-plan.md`'s Global Constraints already
stated — code and config are not prose and were never subject to the
8-word rule. Genuine prose duplication was fixed by rewriting, not by the
tool change: 25 real overlaps were reworded before the checker was
touched. Each removal now leaves a barrier that a word run may not span,
so dropping a code sample cannot splice the sentences on either side of
it into a run no page wrote. Verified by canary: a page duplicating an
existing paragraph is still caught (12 runs flagged, exit 1). The three
new scripts were canary-tested the same way before commit — a dangling
link, a core kit with its `opencode/` removed, and a `PATTERN.md` with a
renamed section each produced exit 1 naming the specific cause.

One smaller fix worth recording: seven markdownlint errors shipped with
projects 1–4 in the previous session's commit (two unlabelled code
fences, four bare email addresses in a table, one list missing a leading
blank line), which left the markdown-lint workflow red. Cleared as part
of Task 11.

Day 3's loop stops here, permanently. Awaiting user approval before
`day-4-plan.md`; Day 4 starts as its own fresh, independent `/loop`, not
a continuation of this one.
