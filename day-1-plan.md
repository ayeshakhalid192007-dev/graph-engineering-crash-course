# Day 1 Implementation Plan — Repo Foundation, Dogfooding, Prerequisites & Foundations

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Execution mode:** This plan runs under a single `/loop` (dynamic, self-paced). The loop dispatches Tasks 1–6 below to parallel subagents where marked, then runs Task 7 (verification) itself before self-stopping. It does **not** advance to `day-2-plan.md` on its own — it stops and waits for the user's explicit approval, per the "Plans first, approve each day" execution mode agreed with the user.

**Goal:** Stand up `graph-engineering-course/` as a real, browsable GitHub repo — project scaffolding, the repo's own dogfooded Loop Engineering discipline, and the entry-layer docs (`00-start-here/`, `01-prerequisites/`, `02-foundations/`) — all passing the originality gate.

**Architecture:** One flat repo root. `docs/` is the single source of truth (per graph-plan.md §3); Day 1 only populates its entry layer (`00-start-here/`, `01-prerequisites/`, `02-foundations/`) and creates empty scaffolding for the parts Day 2–3 will fill. A local Node.js script (`scripts/originality-check.mjs`) enforces graph-plan.md §2.1 mechanically from Day 1 onward, run manually now and wired into CI so it applies to every later day too.

**Tech Stack:** Markdown, Node.js (ESM, no dependencies) for `scripts/`, GitHub Actions YAML, git.

## Global Constraints

- **Originality policy (graph-plan.md §2.1):** every sentence in `docs/` is written fresh, from understanding, never with a source open. No run of 8+ consecutive words in any `docs/` page may match cited source text. The one exception is the single attributed Peter Steinberger quote (source #9) — see Task 6.
- **Page template (graph-plan.md §12):** concept pages (not pure reference pages like a glossary) should carry: hook → explanation → diagram → dual-tool code → going-deeper → check-yourself → try-with-AI → when-it-goes-wrong → glossary popovers. Day 1's prerequisite/foundation pages are primers and reference material, so only hook + explanation + check-yourself are required this early (dual-tool code and live-lab exercises start in earnest at Step 1, which is Day 2) — call out per-task below which template elements apply.
- **License / attribution placeholders:** copyright holder and citation author = `Graph Engineering Course Contributors` (placeholder, confirmed with user; swap for real identity before publishing). No GitHub remote exists yet — everything is local commits only.
- **No verbatim source reproduction anywhere**, including in this plan document itself — outlines below are *our own* structural summaries of graph-plan.md (which is already original), not excerpts from the ten external sources.
- **Definition of Done for Day 1** (graph-plan.md §27 Day 1 + relevant slice of §29): repo browsable on GitHub with no broken relative links; all `01-prerequisites/` and `02-foundations/` pages complete, readable, and pass `scripts/originality-check.mjs`; dogfooding files (`AGENTS.md`, `CLAUDE.md`, `LOOP.md`, `STATE.md`, `loop-budget.md`, `loop-constraints.md`, `loop-run-log.md`) contain real, specific content — not templates with blanks.

---

## Task 1: Root project files

**Files:**
- Create: `LICENSE`
- Create: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `CODEOWNERS`
- Create: `CITATION.cff`
- Create: `.gitignore`

**Interfaces:**
- Consumes: nothing (first task, no dependencies).
- Produces: `README.md` must link to `docs/00-start-here/`, `docs/README.md` (created in Task 6), `patterns/README.md` and `starters/README.md` (stub links — real content lands Day 3; link-check in Task 7 must not fail on these because Task 5 creates stub `README.md` placeholders in every scaffolded empty directory).

- [ ] **Step 1: Write `LICENSE`**

Standard MIT license text, copyright line:
```
Copyright (c) 2026 Graph Engineering Course Contributors
```

- [ ] **Step 2: Write `README.md`**

Sections required: hero (one-paragraph pitch drawn from graph-plan.md §1, in fresh wording — do not reuse §1's sentences verbatim, since §1 is this project's own planning prose but the README is a different document with a different audience), badges row (placeholder shields.io badges for license/CI, real URLs added once a remote exists — mark with an HTML comment `<!-- TODO: replace with real CI badge once a GitHub remote exists -->`, which is an infra note, not a content placeholder, so it does not violate the "no placeholders" rule for prose), navigation table linking to `docs/00-start-here/`, `patterns/`, `starters/`, `resources/sources.md`, quickstart (clone, read `docs/00-start-here/`, no build step required for the GitHub course), and a one-line pointer to the prerequisites (Loop Engineering, Harness Engineering) per graph-plan.md §4.

- [ ] **Step 3: Write `CONTRIBUTING.md`**

Contribution ladder (good-first-issue → pattern author → track maintainer), and a concrete "how to add a pattern" walkthrough referencing the kit shape in graph-plan.md §18 (`PATTERN.md`, `README.md`, `schema.example.json`, `.claude/`, `opencode/`) and the registry file `patterns/registry.yaml` (created Day 3) that a new pattern must be added to.

- [ ] **Step 4: Write `SECURITY.md`**

Standard responsible-disclosure text: how to report a vulnerability (email placeholder, since no real security contact exists yet — use `security@graph-engineering-course.example` clearly marked as a placeholder to replace before publishing), expected response time, scope (this is a docs/starter-kit repo — most "vulnerabilities" would be in `starters/` example code, not the docs themselves).

- [ ] **Step 5: Write `CODEOWNERS`**

One line: `* @graph-engineering-course-contributors` (placeholder team handle — note inline as a placeholder to update once real maintainers exist).

- [ ] **Step 6: Write `CITATION.cff`**

Valid Citation File Format v1.2.0 YAML, `title: Graph Engineering — A Crash Course`, `authors: - name: "Graph Engineering Course Contributors"`, `date-released: 2026-07-31`, `license: MIT`.

- [ ] **Step 7: Write `.gitignore`**

```
node_modules/
.next/
.env
.env.local
.originality-cache/
.DS_Store
*.log
```
(The `.originality-cache/` entry matters — see Task 4; it holds locally-fetched reference snapshots of the ten external sources for the originality checker and must never be committed, since redistributing that text would defeat graph-plan.md §2.1.)

- [ ] **Step 8: Commit**

```bash
git add LICENSE README.md CONTRIBUTING.md SECURITY.md CODEOWNERS CITATION.cff .gitignore
git commit -m "Add root project files (license, readme, contributing, security)"
```

---

## Task 2: `resources/sources.md` — full attribution

**Files:**
- Create: `resources/sources.md`

**Interfaces:**
- Consumes: the source table in graph-plan.md §5 (ten rows: name, provenance, role).
- Produces: the canonical attribution page every other page and the website Sources page link to — later tasks (Task 6 primers, Day 2 step pages) must link here by relative path `../../resources/sources.md` (adjust depth per file location) whenever they credit an idea, not restate the source's identity.

- [ ] **Step 1: Write `resources/sources.md`**

One entry per source (all ten from graph-plan.md §5), each with: name, link/provenance, one original sentence (not copied from graph-plan.md §5's own wording) explaining what idea this course took from it and why, and — for source #9 (Peter Steinberger) only — the single attributed direct quote in quotation marks with the person named inline, wrapped in the HTML marker the originality checker looks for:

```markdown
<!-- attributed-quote:steinberger -->
> "the exact quoted words go here" — Peter Steinberger
```

(The real quote text is not available in this offline environment — flag this explicitly as **BLOCKED: need the real Peter Steinberger quote text and its exact source URL/date from the user before this file can be finalized.** Do not fabricate a quote. Leave the marker and a `<!-- BLOCKED: awaiting real quote -->` comment in its place and surface this to the user at the Day 1 checkpoint.)

- [ ] **Step 2: Commit**

```bash
git add resources/sources.md
git commit -m "Add resources/sources.md with attribution for all ten sources"
```

---

## Task 3: `.github/` scaffold

**Files:**
- Create: `.github/workflows/link-check.yml`
- Create: `.github/workflows/registry-validate.yml`
- Create: `.github/workflows/originality-check.yml`
- Create: `.github/workflows/graph-ready-audit.yml`
- Create: `.github/workflows/web-build.yml`
- Create: `.github/workflows/markdown-lint.yml`
- Create: `.github/ISSUE_TEMPLATE/bug_report.md`
- Create: `.github/ISSUE_TEMPLATE/pattern_proposal.md`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/dependabot.yml`

**Interfaces:**
- Consumes: nothing directly, but four of these six workflows reference scripts that do not exist until later days (`link-check.mjs`, `validate-registry.mjs`, `graph-ready-audit.mjs` all ship Day 3; `web-build.yml` needs `web/` which ships Day 4).
- Produces: `originality-check.yml` is the only workflow that must be fully live on Day 1 (it calls `node scripts/originality-check.mjs`, created in Task 4).

- [ ] **Step 1: Write the four not-yet-runnable workflows as real, valid YAML that no-ops safely today**

For `link-check.yml`, `registry-validate.yml`, `graph-ready-audit.yml`, and `web-build.yml`: write the trigger (`on: [push, pull_request]`) and job steps exactly as they will run once their target script/directory exists, but guard the `run:` step with an existence check so Day 1 CI runs are green rather than red on a script that legitimately doesn't exist yet, e.g.:

```yaml
name: link-check
on: [push, pull_request]
jobs:
  link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Run link check
        run: |
          if [ -f scripts/link-check.mjs ]; then
            node scripts/link-check.mjs
          else
            echo "scripts/link-check.mjs not created yet (ships Day 3) — skipping."
          fi
```
Apply the same guarded pattern to the other three, each pointing at its own future script/dir (`scripts/validate-registry.mjs`, `scripts/graph-ready-audit.mjs`, and `web/package.json` respectively for `web-build.yml`, whose guard checks `[ -f web/package.json ]` before running `npm ci && npm run build`).

- [ ] **Step 2: Write `originality-check.yml` (fully live today)**

```yaml
name: originality-check
on: [push, pull_request]
jobs:
  originality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Run originality check
        run: node scripts/originality-check.mjs
```

- [ ] **Step 3: Write `markdown-lint.yml`**

```yaml
name: markdown-lint
on: [push, pull_request]
jobs:
  markdown-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DavidAnson/markdownlint-cli2-action@v16
        with:
          globs: '**/*.md'
```

- [ ] **Step 4: Write `.github/ISSUE_TEMPLATE/bug_report.md` and `pattern_proposal.md`**

`bug_report.md`: standard front matter (`name: Bug report`, `about: Something in the docs or a starter kit is wrong`) plus sections: What's wrong, Where (file/link), Expected, Repro if it's a starter kit.
`pattern_proposal.md`: front matter (`name: New pattern proposal`) plus sections: Pattern name, Which category (A–G per graph-plan.md §17), Which write/read/governance stage, Why it's not already covered by an existing pattern.

- [ ] **Step 5: Write `.github/PULL_REQUEST_TEMPLATE.md`**

Checklist: originality-check passes locally, link-check passes locally (once it exists), page follows the §12 template if it's a concept page, new pattern is registered in `patterns/registry.yaml` if applicable.

- [ ] **Step 6: Write `.github/dependabot.yml`**

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/web"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

- [ ] **Step 7: Commit**

```bash
git add .github
git commit -m "Scaffold GitHub Actions workflows, issue/PR templates, dependabot"
```

---

## Task 4: `scripts/originality-check.mjs`

**Files:**
- Create: `scripts/originality-check.mjs`
- Create: `scripts/README.md`

**Interfaces:**
- Consumes: every `.md` file under `docs/`; optionally `.originality-cache/**/*` if present (gitignored — see Task 1 Step 7).
- Produces: exit code 0 (pass) / 1 (fail) with violation lines printed to stderr; this is the "test suite" every later day's content tasks run against before committing.

- [ ] **Step 1: Write `scripts/originality-check.mjs`**

```javascript
#!/usr/bin/env node
// Enforces graph-plan.md §2.1 rule 2: no run of 8+ consecutive words in any
// docs/ page may match an 8+ word run in a cached source text.

import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, extname } from "node:path";

const DOCS_DIR = "docs";
const CACHE_DIR = ".originality-cache";
const MIN_RUN = 8;
const ALLOWED_QUOTE_MARKER = "<!-- attributed-quote:steinberger -->";

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    const s = statSync(p);
    if (s.isDirectory()) out.push(...walk(p));
    else if (extname(p) === ".md") out.push(p);
  }
  return out;
}

function tokenize(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean);
}

function ngrams(tokens, n) {
  const set = new Set();
  for (let i = 0; i + n <= tokens.length; i++) set.add(tokens.slice(i, i + n).join(" "));
  return set;
}

function stripAttributedQuoteBlocks(text) {
  const lines = text.split("\n");
  const kept = [];
  let skipping = false;
  for (const line of lines) {
    if (line.includes(ALLOWED_QUOTE_MARKER)) { skipping = true; continue; }
    if (skipping && line.trim() === "") { skipping = false; continue; }
    if (!skipping) kept.push(line);
  }
  return kept.join("\n");
}

function main() {
  if (!existsSync(DOCS_DIR)) {
    console.error(`originality-check: ${DOCS_DIR}/ not found`);
    process.exit(1);
  }

  const docFiles = walk(DOCS_DIR);
  let sourceNgrams = null;

  if (existsSync(CACHE_DIR)) {
    sourceNgrams = new Set();
    for (const f of walk(CACHE_DIR)) {
      for (const g of ngrams(tokenize(readFileSync(f, "utf8")), MIN_RUN)) sourceNgrams.add(g);
    }
  } else {
    console.warn(
      `originality-check: ${CACHE_DIR}/ not present — skipping cross-source check, ` +
      `running self-duplication check only. See scripts/README.md.`
    );
  }

  let violations = 0;
  const seenBySelf = new Map();

  for (const file of docFiles) {
    const cleaned = stripAttributedQuoteBlocks(readFileSync(file, "utf8"));
    const grams = ngrams(tokenize(cleaned), MIN_RUN);

    for (const g of grams) {
      if (sourceNgrams && sourceNgrams.has(g)) {
        console.error(`originality violation in ${file}: matches cached source text: "${g}"`);
        violations++;
      }
      if (seenBySelf.has(g) && seenBySelf.get(g) !== file) {
        console.error(`self-duplication in ${file}: matches ${seenBySelf.get(g)}: "${g}"`);
        violations++;
      } else if (!seenBySelf.has(g)) {
        seenBySelf.set(g, file);
      }
    }
  }

  if (violations > 0) {
    console.error(`\noriginality-check: ${violations} violation(s) found.`);
    process.exit(1);
  }
  console.log(`originality-check: ${docFiles.length} files checked, 0 violations.`);
}

main();
```

- [ ] **Step 2: Write `scripts/README.md`**

Explain: what each script in this directory does (this one now, `link-check.mjs`/`validate-registry.mjs`/`graph-ready-audit.mjs` arriving Day 3), and specifically for `originality-check.mjs`: that `.originality-cache/` is a gitignored, locally-populated directory of reference-text snapshots of the ten sources (populated once by whoever runs CI with source access — not shipped in the repo), that the self-duplication check runs even without it, and the known limitation that repeated template boilerplate (e.g. a recurring section header phrase) across pages can produce false positives — to be refined with an allowlist file if that becomes a real problem once Day 2 content exists.

- [ ] **Step 3: Run it against the current (nearly empty) `docs/` tree to confirm it works**

```bash
mkdir -p docs && node scripts/originality-check.mjs
```
Expected: `originality-check: 0 files checked, 0 violations.` (or a small nonzero count once Tasks 5/6 land — rerun after those tasks, not just once).

- [ ] **Step 4: Commit**

```bash
git add scripts/originality-check.mjs scripts/README.md
git commit -m "Add originality-check script and wire its docs"
```

---

## Task 5: Dogfooding files

**Files:**
- Create: `AGENTS.md`
- Create: `CLAUDE.md`
- Create: `LOOP.md`
- Create: `STATE.md`
- Create: `loop-budget.md`
- Create: `loop-constraints.md`
- Create: `loop-run-log.md`

**Interfaces:**
- Consumes: the Loop Engineering vocabulary this course assumes as prerequisite (heartbeat, spine, maker/checker — graph-plan.md §5 source #2) and this course's own governance-graph concepts (graph-plan.md §10).
- Produces: `STATE.md` becomes the living record of which day/phase this repo build is in — every later day's plan approval gate should update it (noted in Task 7 and mirrored in day-2/3/4 plans).

- [ ] **Step 1: Write `AGENTS.md`**

This repo's own rules file for any agent (human-directed or autonomous) contributing to it. Cover, in original prose: the originality policy is non-negotiable and mechanically enforced (link to `resources/sources.md` and `scripts/originality-check.mjs`); the page template a concept page must follow (§12); commit conventions (small, one concern per commit); the rule that `graph-plan.md` is the master spec and is never edited by an automated process, only by the human owner.

- [ ] **Step 2: Write `CLAUDE.md`**

Claude-Code-specific operating notes for this repo: how to run `scripts/originality-check.mjs` before committing any `docs/` change, where the day-plans live (`day-1-plan.md` … `day-4-plan.md`) and that they are the authoritative task breakdown, a pointer back to `AGENTS.md` for the rules that apply to every agent regardless of tool.

- [ ] **Step 3: Write `LOOP.md`**

Describe, in original prose, the actual loops that maintain this repo, using this course's own vocabulary from graph-plan.md §10: a **content loop** (a writer drafts a page → `originality-check` + `markdown-lint` run as the checker → a human reviewer merges), and an **audit loop** (a periodic run of `link-check` + `graph-ready-audit` across the whole repo, catching drift the content loop's narrower scope can't see — this is a direct instance of the "audit loop with a wider vantage point" fix from §10). Name the anchor (real CI, not a loop grading itself) and the frozen node (`graph-plan.md` itself, and the ten entries in `resources/sources.md` — no loop may rewrite either).

- [ ] **Step 4: Write `STATE.md`**

The spine of this repo's own build. A simple living table:

```markdown
| Day | Status | Plan | Notes |
| --- | ------ | ---- | ----- |
| 1 | in progress | day-1-plan.md | repo foundation + prerequisites + foundations |
| 2 | not started | day-2-plan.md | full 17-step course + assessments |
| 3 | not started | day-3-plan.md | pattern library + projects + advanced tier |
| 4 | not started | day-4-plan.md | website build + polish + ship |
```
Update the Day 1 row to `done` as the last step of Task 7 below, once verification passes.

- [ ] **Step 5: Write `loop-budget.md`**

Original policy doc: how much the content loop and audit loop are each allowed to touch per run (e.g., content loop: one page or one tightly-related group of pages per PR; audit loop: read-only, never auto-merges a fix, only opens an issue). Ties to graph-plan.md §11's "know when the cost isn't justified" framing — applied here to this repo's own maintenance cost.

- [ ] **Step 6: Write `loop-constraints.md`**

Hard rules the loops must never violate, as a bullet list: never merge a `docs/` change with a red `originality-check`; never edit `graph-plan.md` or `resources/sources.md`'s source table automatically; never delete an entry from `loop-run-log.md` (append-only, per graph-plan.md §8's provenance discipline — supersede, don't overwrite).

- [ ] **Step 7: Write `loop-run-log.md`**

Seed with one real entry documenting this actual Day 1 kickoff:

```markdown
# Loop Run Log

Append-only. Never edit or delete a prior entry — if a past entry turns out
to be wrong, add a new entry that supersedes it and says so.

## 2026-07-31 — Day 1 kicked off

Repo initialized locally (no remote yet). Day 1 plan (`day-1-plan.md`)
approved and execution started: root project files, dogfooding files,
prerequisites, foundations, originality-check tooling.
```

- [ ] **Step 8: Commit**

```bash
git add AGENTS.md CLAUDE.md LOOP.md STATE.md loop-budget.md loop-constraints.md loop-run-log.md
git commit -m "Add dogfooding files: AGENTS, CLAUDE, LOOP, STATE, loop-budget/constraints/run-log"
```

---

## Task 6: Entry-layer docs — `00-start-here/`, `01-prerequisites/`, `02-foundations/`

**Files:**
- Create: `docs/README.md`
- Create: `docs/00-start-here/README.md`
- Create: `docs/01-prerequisites/README.md`
- Create: `docs/01-prerequisites/loop-engineering-primer.md`
- Create: `docs/01-prerequisites/harness-engineering-primer.md`
- Create: `docs/01-prerequisites/environment-setup.md`
- Create: `docs/02-foundations/glossary.md`
- Create: `docs/02-foundations/mental-models.md`
- Create: `docs/02-foundations/concepts.md`
- Create: `docs/02-foundations/the-two-graphs.md`

**Interfaces:**
- Consumes: graph-plan.md §4 (audience/outcomes), §5 (sources #2, #3 for the primers), §6–§7 (body of knowledge for foundations), §12.1 (skill tracks table, for the start-here router), §22 (glossary term list).
- Produces: `docs/README.md` is the course index every later day's parts (`03-…` through `09-…`) link back to; `docs/02-foundations/the-two-graphs.md` is an **intro-level** treatment only — the deeper Step 3 page (`docs/03-part-1-the-memory-problem/step-3-*.md`, Day 2) covers the same split in full and must not duplicate this page's specific examples or wording (Day 2's plan calls this out).

- [ ] **Step 1: Write `docs/README.md`**

Course index: the four skill tracks (G1–G4) table (reproduce the *structure* of graph-plan.md §12.1's table with fresh column text, not copy its cell wording verbatim), the 17-step roadmap as a linked table of contents (links will 404 until Day 2 creates those files — acceptable for Day 1, Task 7's link-check must treat `docs/03-…` through `09-…` as out of scope until Day 2, since Task 5 in this same task list only scaffolds empty stub directories for them, not linked pages yet — see Step 9 below), and the two reading paths (core path vs. second read) from §12.

- [ ] **Step 2: Write `docs/00-start-here/README.md`**

A short router: 2–3 self-assessment questions ("Have you completed Loop Engineering? Harness Engineering? Are you here to build one graph, or to decide whether you need one at all?") each branching to a suggested starting point (`01-prerequisites/` if either prerequisite is shaky, `docs/03-part-1-the-memory-problem/` if both are solid, `docs/09-part-7-staying-grounded/` if the reader mainly wants the "do we even need this" checklist). Original scenario-driven framing, not a copy of any source's onboarding flow.

- [ ] **Step 3: Write `docs/01-prerequisites/README.md`**

Index page: states plainly that this course assumes Loop Engineering and Harness Engineering (graph-plan.md §4), links the two primers and the environment-setup page, and sets expectation that the primers are recaps for readers who want a refresher — not a substitute for the full prerequisite courses.

- [ ] **Step 4: Write `docs/01-prerequisites/loop-engineering-primer.md`**

Template elements required: hook + explanation + check-yourself (diagram/code/exercise not required at this recap depth). Original-prose recap of the loop vocabulary this course assumes: heartbeat (what triggers a loop iteration), spine (the durable backlog/state a loop works from), maker/checker (the separation between the thing doing work and the thing checking it). Close with one sentence bridging forward: a single loop's spine is one file it alone reads and writes — that's exactly the assumption Graph Engineering starts by breaking (ties to graph-plan.md §6, in fresh wording).

- [ ] **Step 5: Write `docs/01-prerequisites/harness-engineering-primer.md`**

Same template depth as Step 4. Original-prose recap of constrain / inform / verify / correct / escalate. Close with a bridge sentence: the graph this course builds is one of the things a harness's "verify" stage can check against (fresh wording, no reuse of Step 4's or this file's own phrasing between the two primers).

- [ ] **Step 6: Write `docs/01-prerequisites/environment-setup.md`**

Practical setup page: what a learner needs installed — git, Node.js and Python 3 (for the dependency-free live labs in §21, which need no API key and no network), and at least one of Claude Code / OpenCode for the dual-tool code tabs starting Day 2. Note the tool-coverage policy (§18): core patterns get both tools, extended patterns get one plus a porting note.

- [ ] **Step 7: Write `docs/02-foundations/glossary.md`**

Reference-format page (no §12 template required — it's a glossary, not a concept page). Define, each in this course's own words, one paragraph max per term: Graph, Node, Edge, Work-history graph, Fact graph, Extraction, Resolution, Provenance, Subgraph, Grounding, Governance graph, Anchor, Frozen node, Counter-metric (the exact term list from graph-plan.md §22).

- [ ] **Step 8: Write `docs/02-foundations/mental-models.md`**

Hook + explanation depth. One or two original analogies (not from any of the ten sources) that make the "graph as shared memory" idea concrete before the formal vocabulary lands — e.g., contrasting a single shared notebook one person updates versus a filing system built for several people to read and write at once. Must be a scenario invented for this course.

- [ ] **Step 9: Write `docs/02-foundations/concepts.md`**

Hook + explanation + check-yourself. Introduces "comprehension debt" for shared memory (per graph-plan.md §23's description of this file) — the idea that a memory structure only a subset of the team fully understands accrues risk the same way undocumented code does. Original framing and example.

- [ ] **Step 10: Write `docs/02-foundations/the-two-graphs.md`**

Hook + explanation only, deliberately shorter than the Day 2 Step 3 treatment. Introduces the work-history-graph-vs-fact-graph split at a vocabulary level (drawing on the ideas in graph-plan.md §7, in fresh original wording and with its own small example distinct from whatever example Day 2's Step 3 page will later use — pick a different concrete scenario here, e.g. a support-ticket system, so the two pages don't read as the same page twice).

- [ ] **Step 11: Create stub `README.md` placeholders so Task 1's README links don't 404 yet**

For each of `patterns/`, `starters/`, `skills/`, `templates/`, `examples/`, `assets/`, `resources/` (beyond `sources.md`), and `docs/03-part-1-the-memory-problem/` through `docs/09-part-7-staying-grounded/`, `docs/methods/`, `docs/operating/`, `docs/advanced/`, `docs/projects/`, `docs/appendix/cheatsheets/`, `docs/assessments/`: create the directory with a one-line `README.md` stub: `# <Directory Name>\n\nContent for this section ships on Day <N> — see \`day-<N>-plan.md\`.` This keeps every relative link resolvable today per the Day 1 Definition of Done ("no broken relative links"), while being honest that the content isn't written yet (an infra placeholder for scaffolding, not a content placeholder in prose — allowed).

- [ ] **Step 12: Run the originality check on everything written so far**

```bash
node scripts/originality-check.mjs
```
Expected: `0 violations`. If any 8+-word run collides between the two primers (Step 4 vs Step 5) or between `concepts.md`/`the-two-graphs.md`/`mental-models.md`, rewrite the offending page's phrasing — do not weaken the checker to allow it.

- [ ] **Step 13: Commit**

```bash
git add docs
git commit -m "Add docs/00-start-here, 01-prerequisites, 02-foundations, and directory scaffolding"
```

---

## Task 7: Verification & Day 1 close-out

**Files:**
- Modify: `STATE.md` (mark Day 1 row `done`)
- Modify: `loop-run-log.md` (append close-out entry)

**Interfaces:**
- Consumes: everything from Tasks 1–6.
- Produces: the go/no-go signal for the Day 1 approval gate below.

- [ ] **Step 1: Run the originality check**

```bash
node scripts/originality-check.mjs
```
Expected: exit 0, `0 violations`.

- [ ] **Step 2: Manually verify no broken relative links**

Since `link-check.mjs` doesn't exist until Day 3, do a manual pass: every relative link written in Tasks 1 and 6 resolves to a file that exists (either real content or a Step 11 stub). Note any that don't and fix them now.

- [ ] **Step 3: Confirm the two BLOCKED items are surfaced, not silently skipped**

Task 2's Steinberger quote is blocked pending real quote text from the user — confirm the `<!-- BLOCKED: awaiting real quote -->` marker is present in `resources/sources.md` and raise it explicitly when reporting Day 1 completion.

- [ ] **Step 4: Update `STATE.md`**

Change the Day 1 row's Status to `done`.

- [ ] **Step 5: Append to `loop-run-log.md`**

```markdown
## 2026-07-31 — Day 1 complete

All Day 1 tasks done: root project files, resources/sources.md (blocked on
real Steinberger quote text), .github scaffold, originality-check.mjs,
dogfooding files, 00-start-here/01-prerequisites/02-foundations docs.
originality-check: 0 violations. Awaiting user approval before day-2-plan.md.
```

- [ ] **Step 6: Commit**

```bash
git add STATE.md loop-run-log.md
git commit -m "Day 1 complete: verification passed, STATE.md updated"
```

- [ ] **Step 7: STOP the loop and report to the user**

Per the approval-gated execution mode: do not start `day-2-plan.md`. Summarize what was built, surface the blocked Steinberger quote, and wait for explicit go-ahead.

---

## Day 1 Approval Gate

**Do not proceed to `day-2-plan.md` until the user has:**
1. Reviewed the Day 1 deliverables (or this plan, before execution).
2. Supplied the real Peter Steinberger quote text + exact source/date (Task 2 is blocked without it — a placeholder must never be fabricated).
3. Explicitly said to proceed.
