# Graph Ready Certification

Seven items. A system that satisfies all seven is Graph Ready.

The list is deliberately short and deliberately hard to satisfy by accident. Each item corresponds to a failure this course spends a Part explaining, and each is written so that you can check it against a real system rather than against your intentions for one. Nothing here asks whether you understand a concept; every item asks whether a specific thing exists in your graph.

## The checklist

| # | Item | Where it comes from |
| - | ---- | ------------------- |
| 1 | Schema defined before extraction | Step 6 |
| 2 | Resolution is reversible | Step 7 |
| 3 | Every edge has provenance | Step 8 |
| 4 | A subgraph budget is set | Step 9 |
| 5 | A grounded checker exists | Step 10 |
| 6 | At least one anchor to outside reality | Steps 12–13 |
| 7 | At least one frozen node | Step 13 |

## How to self-certify

Work through the seven questions below against one real system — not a project, not a sketch. For each, the standard is the same: **point at the thing**. An item is satisfied when you can name the file, field, or structure that implements it. An item is not satisfied when the honest answer is that you would do it, intend to do it, or generally work that way.

Write your answers down. A checklist walked through in your head passes at a rate that should make you suspicious.

### 1 · Schema defined before extraction

> Show the schema file, and show that it predates the extraction runs that populated the graph.

The order matters and is the whole item. A schema written after the fact — reverse-engineered from what extraction happened to produce — is a description of your data, not a constraint on it, and it will accommodate anything already there by construction.

**Satisfied when:** a schema artifact exists, extraction reads it, and out-of-schema items are dropped and reported rather than absorbed.

**Not satisfied when:** the type list is embedded in a prompt and has been edited whenever something did not fit.

### 2 · Resolution is reversible

> Take one merge that has actually happened in your graph. Undo it, on paper, using only what the graph records.

**Satisfied when:** the original mentions survive the merge, the canonical node records which mentions it absorbed, and the reason for the merge is written down. All three: mentions without a reason leave a merge that can be undone but not evaluated.

**Not satisfied when:** merged mentions were deleted, or the merge is reversible in principle because you could go back to the source documents. That is re-extraction, not reversal.

### 3 · Every edge has provenance

> Pick three edges at random — genuinely at random, including any added by hand during an incident. Trace each to its source.

The random selection is the point. Edges created by the main extraction path almost always carry receipts; the ones that do not are the ones added under pressure, and they are the ones that matter, because a single untraceable edge gives a reader cause to doubt the traceable ones around it.

**Satisfied when:** every edge names what produced it, and the graph can be filtered by source when a source turns out to be unreliable.

**Not satisfied when:** any edge exists that nobody can place.

### 4 · A subgraph budget is set

> Name the number, and name what happens when a request exceeds it.

A budget is a declared limit with a declared consequence. The second half is where this item is usually lost: a cap that silently truncates is worse than no cap, because it returns incomplete answers that look complete.

**Satisfied when:** a limit exists, and results that hit it say so — naming what was excluded.

**Not satisfied when:** retrieval returns whatever it finds, or a cap exists as a constant in the code with nothing reporting when it bites.

### 5 · A grounded checker exists

> Show the checker, and show one claim it rejected.

The rejection is the evidence. A checker that has approved everything it has ever seen has not been demonstrated to be a checker.

**Satisfied when:** the checker settles claims by querying for a specific edge whose presence or absence decides the question, and its verdicts name that edge.

**Not satisfied when:** verdicts rest on how a claim reads, on the confidence of its wording, or on which source is generally trusted.

### 6 · At least one anchor to outside reality

> Name one thing in your system that no loop of yours produced.

An observed event, a measurement from an instrument, a human sign-off, a record from a system you do not control. One is enough — the item is a floor, not a target.

**Satisfied when:** you can name it, and say which loop's output is checked against it.

**Not satisfied when:** everything your loops validate against is something your loops wrote. Note that high internal agreement is not evidence against this failure; it is the symptom.

### 7 · At least one frozen node

> Name the frozen value, and name what a loop could get away with if it were editable.

The second half separates a real freeze from a decorative one. Freezing a constant no loop has any incentive to modify demonstrates the syntax and prevents nothing.

**Satisfied when:** a value your loops are judged by is frozen, the freeze is enforced rather than requested, and you can state the specific manipulation it prevents.

**Not satisfied when:** nothing is frozen at all, or what is frozen is a value your loops had no reason to touch in the first place.

## Scoring

There is no partial credit and no weighting. Seven of seven is Graph Ready; anything less is a system with a named gap.

That strictness is intentional. Six of seven sounds close, but the missing item is not a rounding error — each one corresponds to a distinct failure mode, and a system missing item 6 will reach confident internal agreement about something false no matter how well it does on the other six. The list is short precisely so that "we got most of them" is not available as a resting place.

If you land on five or six, the gap is the finding. Fix it and re-run the checklist rather than recording a score.

## Recording a result

Keep the written answers. A certification is only as good as the evidence behind it, and the answers *are* the evidence — a claim of Graph Ready with nothing behind it is exactly the unprovenanced edge this course spends Part 3 arguing against.

Re-run the checklist when the system changes materially: a new loop, a new writer on a shared field, a store migration, or a schema revision. Items 3 and 6 are the ones that most often lapse quietly — provenance because incident-time edges bypass the normal path, anchors because the one external check gets replaced by a derived value during a refactor and nobody notices the ring has closed.

An interactive version of this checklist, which produces a shareable certificate from your answers, ships with the course website as the `CertificateGenerator` component. This page is the authoritative version; the component implements it and does not extend it.

---

Related: the [final exam](final-exam.md) tests the reasoning behind these seven items across all seventeen steps. The [capstone rubric](capstone-rubric.md) scores Project 8 against the four of them that project exercises.
