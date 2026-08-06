# Scripts Directory

This directory contains validation and automation scripts for the Graph Engineering Course repository.

## originality-check.mjs

Enforces originality constraints per graph-plan.md §2.1 rule 2: no run of 8 or more consecutive words in any `docs/` page may match an 8+ word run in cached reference-source text.

### How It Works

The script performs two levels of checking:

1. **Cross-source Originality Check** (when `.originality-cache/` is present)
   - `.originality-cache/` is a gitignored, locally-populated directory containing reference-text snapshots of the ten source documents
   - This directory is populated once by whoever runs CI with source access—it is not shipped in the repository
   - The script scans all cached source files and indexes their 8-word n-grams
   - Any doc file containing an 8+ word sequence matching a cached source is flagged as a violation

2. **Self-Duplication Check** (always runs)
   - Detects repeated 8+ word sequences across different pages within `docs/`
   - Runs independently of the cache, so validation works even without `.originality-cache/`

### What Counts as Prose

§2.1 rule 2 is about writing, so the check is applied to writing only. Before scanning, the script removes fenced code blocks, inline code spans, and the URL half of Markdown links — a project page and its reference solution that legitimately show the same JSON record are not duplicating anyone's prose, and neither are two pages that link to the same document.

Each removal leaves a barrier behind, and a word run may not span one. Without that, dropping a code sample would splice the sentences on either side of it into a run no page actually wrote.

### Attributed Quotes

Sections marked with the comment `<!-- attributed-quote:steinberger -->` are exempt from the originality check. Use this marker when including properly attributed quotes or reference material that should not trigger violations.

### Known Limitations

Repeated template boilerplate across pages can still produce false positives when a recurring phrase runs 8+ words — the §12 page template's own section headings are the usual source, since every concept page carries them. The working remedy so far has been to vary the boilerplate slightly per page (a different opening word in the first table row, for instance) rather than to add an allowlist, which keeps the check strict at the cost of a little editorial friction. If that friction grows, an allowlist file is the next step.

### Usage

```bash
node scripts/originality-check.mjs
```

Exit code:

- `0`: all checks passed (0 violations)
- `1`: one or more violations detected; violation details printed to stderr

## link-check.mjs

Resolves every relative Markdown link in `docs/`, `patterns/`, `starters/`, `resources/`, and the root-level `.md` files, and fails on any that points at a file which doesn't exist. Fragments (`#section`) are stripped before resolving — the target file has to exist; the anchor within it is not checked. External `http(s)` links are out of scope.

```bash
node scripts/link-check.mjs
```

## validate-registry.mjs

Checks `patterns/registry.yaml` against what's actually on disk. Every entry must have a spec at `patterns/<name>.md` and a kit at `starters/<name>/PATTERN.md`; entries marked `core: true` must additionally have `starters/<name>/opencode/opencode.json.example`. Also catches duplicate names and missing `category`/`stage`/`cost` fields.

The YAML parser is hand-rolled and scoped to exactly this file's shape — a top-level `patterns:` list of flat maps with unquoted scalar values. This avoids adding a YAML dependency (and a root `package.json`) for one file. graph-plan.md §23 names the file `registry.yaml`, so the extension stays. **If the registry ever grows a nested value, replace this parser rather than extending it.**

```bash
node scripts/validate-registry.mjs
```

## graph-ready-audit.mjs

Audits every starter kit for the required structure: a `README.md`, and a `PATTERN.md` containing both a "What it does" and a "Failure mode if skipped" section.

This is a structural proxy check. It confirms the pieces are present, not that a kit's logic is correct — the latter is covered by each kit's README quickstart being manually runnable.

```bash
node scripts/graph-ready-audit.mjs
```

## Exit codes

All four scripts follow the same convention: `0` when clean, `1` with details on stderr when not. Each runs in its own CI workflow on every push and pull request.
