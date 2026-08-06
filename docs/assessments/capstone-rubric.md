# Capstone Rubric · Project 8

Grading criteria for [Project 8 · Wire Two Loops Together](../projects/08-wire-two-loops-together-capstone.md). Usable for self-assessment or for reviewing someone else's submission.

The rubric is built from the seven-item [Graph Ready checklist](graph-ready-certification.md), narrowed to what the capstone actually exercises, plus two criteria specific to this project. Three of the seven checklist items — schema before extraction, reversible resolution, and a subgraph budget — are not scored here, because Project 8 does not ask for extraction, resolution, or retrieval. Those are covered by Projects 3, 4, and 6.

## How to score

Each criterion is scored **Met**, **Partial**, or **Not met**. There is no weighted total, and this is deliberate: criteria 1 and 2 are gates. A submission that fails either has not built the thing the capstone is about, however well the rest is done.

---

## Gate criteria

### 1. There is a real arbitration edge, not a comment saying one exists

The single most common way this capstone is failed. A submission passes when the `can-overrule` relationship is a structure in `governance.json` that a program could read and act on — with a named source loop, a named target loop, and a scope.

| Score | What it looks like |
| --- | --- |
| **Met** | An edge object in the graph, with `from`, `to`, a relation naming the authority, and a `scope` limiting it to a specific field. A reader could determine the winner of a collision from the file alone. |
| **Partial** | An edge exists but grants blanket authority — one loop outranks another on everything, with no scope. The mechanism is real; the discipline is not. |
| **Not met** | The precedence rule is described in prose, in a README, or in a `note` field, with nothing structural backing it. A comment stating that one loop wins is a plan to arbitrate, not arbitration. |

Ask of any submission: *if both loops wrote right now, and I had only this file, could I say which value stands and why?* If the answer requires reading prose, this criterion is not met.

### 2. The rejected value survives, with its reason

A collision output showing only the winner is indistinguishable from one that silently dropped the loser.

| Score | What it looks like |
| --- | --- |
| **Met** | Output names both proposed values, marks which was accepted and which rejected, and gives the rejected one a reason referring to the rule applied. |
| **Partial** | Both values appear, but the rejection carries no reason, or the reason restates the outcome ("not selected") rather than the rule. |
| **Not met** | Only the accepted value appears. Alternatively: the two values were averaged, or resolved by "most recent write wins" — both of which discard the collision rather than settling it. |

---

## Scored criteria

### 3. Provenance — every edge in the governance graph can be accounted for

Drawn from checklist item 3.

- **Met** — every edge carries enough to explain why it exists: for the arbitration edge, the reasoning behind the precedence; for the collision output, which rule produced the verdict.
- **Partial** — the arbitration edge is justified, but `feeds` and `checks` edges appear with no indication of what relationship they record.
- **Not met** — edges are present with no accompanying reasoning anywhere.

### 4. A grounded check, not a plausibility check

Drawn from checklist item 5. The capstone's checker loop verifies against something, and what it verifies against is what is being scored.

- **Met** — the verdict rests on a specific, checkable property of the competing writes. Whether a write is anchored to an observed event is such a property: it can be confirmed from the record.
- **Partial** — the rule is stated in checkable terms but the worked collision does not actually apply it, resolving on timing or ordering instead.
- **Not met** — the verdict rests on which value seems more reasonable, or on which loop is generally more trusted, with nothing in the record that could be checked.

### 5. At least one anchor to outside reality

Drawn from checklist item 6.

- **Met** — one loop's writes are tied to something neither loop produced — an observed event, an external measurement, a human sign-off — and the submission says explicitly which loop that is and what the anchor is.
- **Partial** — an anchor exists in the scenario but the submission never identifies it as the anchor, so the property is present by accident rather than by design.
- **Not met** — both loops write model output, estimates, or derived values only. Nothing in the system answers to anything outside it.

### 6. At least one frozen node, with a stated consequence

Drawn from checklist item 7.

- **Met** — a value is marked frozen, a note states that neither loop may modify it, **and** the submission explains concretely which discrepancy a loop would be able to bury if it could move that value. The explanation is the part that shows the point landed.
- **Partial** — the value is marked frozen with no explanation of what the freeze prevents, or with a generic one that would apply to any frozen value anywhere.
- **Not met** — nothing is frozen, or the frozen value is one no loop would have had any reason to modify, which makes the freeze decorative.

### 7. No authority cycle

- **Met** — the submission states that it checked, and shows the check: the set of authority edges, and the observation that no path leads back.
- **Partial** — no cycle exists, but the submission never checked. Correct by construction is not the same as verified, and with more than two loops it stops being reliable.
- **Not met** — a cycle exists. Collisions between the affected loops have no determinate outcome.

---

## Common failure modes

Seen often enough to be worth naming in advance:

| Pattern | Why it fails |
| --- | --- |
| Blanket authority — one loop outranks the other on everything. | Scope is what keeps an arbitration edge from being a hierarchy. Unscoped authority means the subordinate loop's independent judgment is void everywhere, including on fields where it is the better source. |
| "Most recent write wins" as the rule. | It is a tiebreaker, not a rule — it settles collisions without reference to anything about the writes themselves, which means it will confidently prefer a stale estimate that happened to land second. |
| Averaging the two values. | Produces a number neither loop proposed and no evidence supports. Arbitration selects; it does not blend. |
| The frozen node is a constant nobody would touch. | Freezing something no loop has an incentive to change demonstrates the syntax and misses the reason. Freeze what a loop would benefit from moving. |
| The governance graph describes loops that do not write anything. | Without a real collision the arbitration edge is untested. A capstone that never exercises its own rule has not shown the rule works. |

## Self-assessment

Before checking against this rubric, answer these three from your own submission alone:

1. If both loops wrote at the same instant, which value stands — and can you show me where in the file that is decided?
2. Where is the losing value, and what does the record say about why it lost?
3. What could a loop get away with if your frozen node were editable? Name the specific thing, not the category.

If any of the three needs prose outside the graph to answer, that is the criterion to revisit first.

---

Related: the [final exam](final-exam.md) covers all seventeen steps; the [Graph Ready certification](graph-ready-certification.md) covers the full seven-item checklist, including the three this rubric does not score.
