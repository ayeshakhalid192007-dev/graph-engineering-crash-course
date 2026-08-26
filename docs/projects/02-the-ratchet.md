# Project 2 · The Ratchet

**Difficulty:** Beginner–Intermediate
**Time:** 45–60 minutes
**Concepts:** ratchet, durable history, discard log, strictly-greater comparison
**Maps to:** Step 4 (Part 2 of the course) — the page that introduces the ratchet rule for keeping a search's history honest. Look it up in the [full roadmap](../README.md) if you need the exact page.

> **Throwaway repo, small data first.** Five fixed listening sessions and a handful of weight combinations — small enough to score by hand if your script has a bug, which is exactly how you'll catch the bug.

## The scenario

You're hand-tuning a toy scoring formula for a personal "what to play next" tool. It ranks two candidate songs at a time using three weighted signals — how well the genre matches, how recent the track is, how often it's been skipped — and you're adjusting the three weights to see how often the formula's top pick matches what the listener actually chose, across a small fixed set of past sessions.

Every time you nudge a weight, you re-run the check. After a dozen nudges you've lost track of which combination was actually best, and you're pretty sure you already tried something close to your current idea an hour ago — you just can't remember if it worked.

## Starting material

Five sessions, each with two candidate songs and the one the listener actually picked. Feature values are already computed for you.

| Session | Candidate | genre_match | recency_days | skip_rate | Chosen? |
| --- | --- | --- | --- | --- | --- |
| s1 | Harbor Lights | 1 | 2 | 0.10 | **yes** |
| s1 | Faded Static | 0 | 1 | 0.40 | no |
| s2 | Quiet Radio | 1 | 10 | 0.20 | **yes** |
| s2 | Neon Drift | 1 | 1 | 0.60 | no |
| s3 | Neon Drift | 1 | 3 | 0.30 | **yes** |
| s3 | Slow Static | 0 | 2 | 0.10 | no |
| s4 | Faded Static | 0 | 5 | 0.20 | **yes** |
| s4 | Harbor Lights | 1 | 20 | 0.05 | no |
| s5 | Slow Static | 1 | 1 | 0.15 | **yes** |
| s5 | Quiet Radio | 1 | 2 | 0.50 | no |

Scoring formula for a candidate, given weights `(w_genre, w_recency, w_skip)`:

```text
score = w_genre * genre_match + w_recency * (1 / (1 + recency_days)) - w_skip * skip_rate
```text

For each session, the formula's "prediction" is whichever candidate scores higher. **Accuracy** for one set of weights is the fraction of the five sessions where the prediction matches who the listener actually chose.

## Your task

1. Create a throwaway repo containing two empty files, `durable-history.jsonl` and `discarded.jsonl`.
2. Write a short script (any language) that takes a `(w_genre, w_recency, w_skip)` triple, computes accuracy against the table above, and applies the ratchet rule:
   - No current best yet: the attempt becomes the first entry in `durable-history.jsonl`, automatically.
   - Strictly greater accuracy than the current best: append to `durable-history.jsonl`, recording which entry it beat.
   - Tie or worse: append to `discarded.jsonl`, recording the id of the durable-history entry it was compared against and why it didn't win.
3. Run the script against at least five different weight triples of your own choosing. Include at least one you're fairly sure will tie or lose — the discard log is only worth having if it actually has entries in it.
4. Never edit or delete a line in either file once written. If a mistake makes it into a file, add a corrected line after it — don't rewrite history in place.

## Done when

- `durable-history.jsonl` contains only attempts that strictly beat whatever the current best was at the time they were tried — no ties, no attempt that only matched the leader.
- `discarded.jsonl` contains every non-improving attempt you actually ran, each one naming the durable-history entry it lost to.
- You can point at one line in `discarded.jsonl` and explain, from that line alone, why it didn't get promoted — without re-running the scoring formula.
- The comparison point recorded in `discarded.jsonl` entries changes over the course of your run, as `durable-history.jsonl` grows — an attempt tried late in your session should be compared against a later entry than one tried early on.

## Reference solution

[`solutions/02-the-ratchet.md`](solutions/02-the-ratchet.md) — five worked weight triples against the table above, with the full contents of both `.jsonl` files and the arithmetic behind each accuracy score.
