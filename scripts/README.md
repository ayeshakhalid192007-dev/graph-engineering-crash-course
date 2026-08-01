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

### Attributed Quotes

Sections marked with the comment `<!-- attributed-quote:steinberger -->` are exempt from the originality check. Use this marker when including properly attributed quotes or reference material that should not trigger violations.

### Known Limitations

Repeated template boilerplate (e.g., a recurring section header phrase like "Key Concepts:" or "Further Reading:") across multiple pages can produce false positives when the phrase runs 8+ words. Once Day 2 content is added and patterns emerge, this can be refined with an allowlist file to exclude common harmless phrases.

### Usage

```bash
node scripts/originality-check.mjs
```

Exit code:
- `0`: all checks passed (0 violations)
- `1`: one or more violations detected; violation details printed to stderr

## Other Scripts (Coming in Day 3)

- `link-check.mjs` — Validates internal and external links in documentation
- `validate-registry.mjs` — Validates course registry and metadata
- `graph-ready-audit.mjs` — Final pre-release audit checks
