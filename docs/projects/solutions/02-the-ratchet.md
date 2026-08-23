# Solution · Project 2: The Ratchet

This works through [Project 2](../02-the-ratchet.md)'s fixed five-session table using five weight triples, in the order they were tried. Your own weight choices will differ — check the shape of your `.jsonl` files against this one, not the specific numbers.

## Scoring five attempts

Recall the scoring rule from the project: a candidate's score is its weighted genre match, plus its weighted inverse-recency term, minus its weighted skip rate. Accuracy is how many of the five sessions the higher-scoring candidate matches the listener's actual choice.

| Attempt | Weights (genre, recency, skip) | Correct sessions | Accuracy |
| --- | --- | --- | --- |
| 1 | (1, 1, 1) | s1, s3, s5 | 0.6 |
| 2 | (2, 1, 1) | s1, s3, s5 | 0.6 |
| 3 | (1, 3, 1) | s1, s3, s5 | 0.6 |
| 4 | (1, 1, 3) | s1, s2, s3, s5 | 0.8 |
| 5 | (1, 1, 5) | s1, s2, s5 | 0.6 |

Worked arithmetic for attempt 4, the one that actually improves on the baseline — session by session:

- **s1**: Harbor Lights scores `1 + 1/3 − 3(0.10) = 1.033`; Faded Static scores `0 + 1/2 − 3(0.40) = −0.70`. Predicted Harbor Lights — correct.
- **s2**: Quiet Radio scores `1 + 1/11 − 3(0.20) = 0.491`; Neon Drift scores `1 + 1/2 − 3(0.60) = −0.30`. Predicted Quiet Radio — correct. (This is the session every other attempt got wrong.)
- **s3**: Neon Drift scores `1 + 1/4 − 3(0.30) = 0.35`; Slow Static scores `0 + 1/3 − 3(0.10) = 0.033`. Predicted Neon Drift — correct.
- **s4**: Faded Static scores `0 + 1/6 − 3(0.20) = −0.433`; Harbor Lights scores `1 + 1/21 − 3(0.05) = 0.898`. Predicted Harbor Lights, but the listener actually chose Faded Static — incorrect.
- **s5**: Slow Static scores `1 + 1/2 − 3(0.15) = 1.05`; Quiet Radio scores `1 + 1/3 − 3(0.50) = −1.167`. Predicted Slow Static — correct.

Four out of five: 0.8.

## Applying the ratchet

| Attempt | Accuracy | Current best before this attempt | Outcome |
| --- | --- | --- | --- |
| 1 | 0.6 | none | no baseline yet — automatic pass, becomes `h1` |
| 2 | 0.6 | 0.6 (`h1`) | tie, not strictly greater — discarded, logged against `h1` |
| 3 | 0.6 | 0.6 (`h1`) | tie, not strictly greater — discarded, logged against `h1` |
| 4 | 0.8 | 0.6 (`h1`) | strictly greater — becomes `h2`, beats `h1` |
| 5 | 0.6 | 0.8 (`h2`) | worse than the current best — discarded, logged against `h2` |

Notice attempts 2 and 3 are both logged against `h1`, but attempt 5 is logged against `h2` — the comparison point moved once attempt 4 raised the bar. A discard log that always pointed at `h1` would be lying about what the current best was at the time each attempt ran.

## Final file contents

`durable-history.jsonl`:

```jsonl
{"id":"h1","weights":{"w_genre":1,"w_recency":1,"w_skip":1},"accuracy":0.6,"beats":null}
{"id":"h2","weights":{"w_genre":1,"w_recency":1,"w_skip":3},"accuracy":0.8,"beats":"h1"}
```text

`discarded.jsonl`:

```jsonl
{"id":"d1","weights":{"w_genre":2,"w_recency":1,"w_skip":1},"accuracy":0.6,"lost_to":"h1","reason":"tied the current best, not strictly greater"}
{"id":"d2","weights":{"w_genre":1,"w_recency":3,"w_skip":1},"accuracy":0.6,"lost_to":"h1","reason":"tied the current best, not strictly greater"}
{"id":"d3","weights":{"w_genre":1,"w_recency":1,"w_skip":5},"accuracy":0.6,"lost_to":"h2","reason":"scored lower than the current best"}
```text

## Checking your own attempt

- Does `durable-history.jsonl` only grow when an attempt's accuracy is a strictly higher number than the last entry's, with no exceptions for "close enough"?
- Does every line in `discarded.jsonl` record which kept entry it lost to, not just a bare score?
- If you re-ran your five attempts in a different order, would the ratchet rule still produce a two-entry `durable-history.jsonl` — or does your logic depend on the order you happened to try them in?
