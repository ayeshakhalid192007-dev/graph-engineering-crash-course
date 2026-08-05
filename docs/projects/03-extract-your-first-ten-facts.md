# Project 3 · Extract Your First Ten Facts

**Difficulty:** Intermediate
**Time:** 30–45 minutes
**Concepts:** schema, extraction, entity/relationship types, out-of-schema rejection
**Maps to:** Step 6 (Part 3 of the course) — the page that argues for fixing a schema before extracting anything against it. See the [course roadmap](../README.md) to jump straight there.

> **Throwaway repo, small data first.** One changelog, a few dozen lines long, is the entire source document for this project — no scraping, no real product, nothing to fetch.

## The scenario

Below is the changelog for a small note-taking app called Fernbank, across three releases. It's the kind of document a support agent, a release-notes bot, or a curious user might skim in thirty seconds — bullet points, no fixed shape, mixing new features, bug fixes, and one policy change into the same list format.

Before touching the document, you'll fix a schema — the same discipline Step 6 asks for on a postmortem. Then you'll extract against it, and find out that not everything in the changelog fits.

## Starting material

```
# Fernbank Changelog

## v2.4.0 — 2026-03-02
- Added: bulk tag rename across all notes at once.
- Added: keyboard shortcut to pin a note to the top of a list.
- Added: dark mode for the web app.
- Fixed: the mobile app losing unsaved edits when the phone auto-locks mid-typing.
- Deprecated: the old "Notebooks" sidebar view, replaced by tag filters.

## v2.3.1 — 2026-02-14
- Fixed: search results not including notes edited in the last five minutes.
- Fixed: shared notes occasionally showing a stale collaborator list.

## v2.3.0 — 2026-01-28
- Added: offline mode for the desktop app.
- Added: a weekly digest email summarizing notes edited that week.
- Changed: the free-tier note limit raised from 200 to 500.
- Fixed: exporting a note to PDF cutting off the last line of long notes.
```

## Your task

1. Before reading the changelog as data, fix a schema for it: three entity types — `Release`, `Feature`, `Issue` — and three relationship types — `introduces` (`Release → Feature`), `fixes` (`Release → Issue`), `deprecates` (`Release → Feature`). Write this schema down first, in its own section of your notes, before extracting anything.
2. Extract every changelog line that fits the schema into a five-field record: `subject_type`, `subject`, `relation`, `object_type`, and `object`. Each `Added:` line should become an `introduces` record, each `Fixed:` line a `fixes` record, and the one `Deprecated:` line a `deprecates` record.
3. You should end up with exactly ten schema-valid records. If you have more or fewer, recheck the changelog against your schema — you likely folded two bullet points into one record, or missed one.
4. One line in the changelog does not fit any relationship type in your schema. Find it, and instead of stretching the schema to admit it, write one sentence explaining why it's rejected and what a schema change would need to look like to accept it deliberately.
5. Ask Claude Code or OpenCode to run the same extraction against your schema, independently of your own pass, and compare its ten items and its one rejection against yours.

## Done when

- You have exactly ten five-field records — `subject_type`, `subject`, `relation`, `object_type`, `object` — each one matching an entity type and relationship type from your fixed, three-and-three schema.
- The one changelog line that doesn't fit is explicitly flagged as rejected, not silently dropped and not force-fit into `introduces`, `fixes`, or `deprecates`.
- Your schema was written down before you extracted anything from the document, not adjusted afterward to make a stray item fit.
- An agent's independent extraction pass over the same schema and document lands on the same ten items and the same one rejection as yours.

## Reference solution

[`solutions/03-extract-your-first-ten-facts.md`](solutions/03-extract-your-first-ten-facts.md) — the full ten-item extraction, the one rejected line explained, and the node/edge list the ten items produce.
