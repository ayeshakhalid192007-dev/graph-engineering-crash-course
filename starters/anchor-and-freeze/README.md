# anchor-and-freeze Starter Kit

A single-tool (Claude Code) reference kit for the **anchor-and-freeze**
pattern: wiring in a check that reaches outside the loop system entirely,
and marking a named set of facts or rules as off-limits to every loop,
no matter how convergent its own reasoning looks. This is an extended
kit — see `starters/README.md` for how that differs from the seven core
kits.

Cinder Hollow Grantmakers and the applicants below are invented for this
course, not drawn from any real grant fund, applicant organization, or
county registry.

## Prerequisites

- Claude Code.
- No external services or API keys — the review set and registry
  lookups below are everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the frozen criteria and the 2026-cycle review set below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Frozen criteria (no loop may rewrite these)

- `criterion:501c3-status` — registered 501(c)(3) status, verified at
  time of application.
- `criterion:service-area` — principal service area within Cinder Hollow
  county.
- `criterion:repayment-status` — no unresolved repayment issues on any
  prior Cinder Hollow Grantmakers grant.

### The 2026-cycle review set

- **Tallow Ridge Youth Makers** — internal scoring loop, after three
  review passes reading its budget, mission-alignment, and
  prior-compliance nodes, has converged its computed eligibility-score
  edge to `eligible`. Every fact behind that convergence was written or
  re-derived by the loop's own earlier passes.
- **Fenmoor Youth Choir** — internal scoring loop score: `eligible`,
  reached in a single pass with no disputed nodes.
- **Briar Hollow Repair Collective** — internal scoring loop, unable to
  clear `criterion:repayment-status` as written (an unresolved $640
  repayment issue on file), proposes instead loosening that criterion's
  own definition to "no repayment issues over $500" so the applicant
  clears it.

### External anchor: county business-registry lookup (outside the loop system)

- Tallow Ridge Youth Makers — status: **administratively dissolved**,
  effective 2026-04-02.
- Fenmoor Youth Choir — status: **active, good standing**.
- Briar Hollow Repair Collective — status: **active, good standing**
  (the registry has no bearing on the repayment dispute; it only speaks
  to whether the organization itself still legally exists).

### Claude Code

1. Load the skill: `.claude/skills/anchor-and-lock/SKILL.md`.
2. Ask it to run: "Use the anchor-and-lock skill on the 2026-cycle
   review set in README.md, checking the county registry anchor and the
   frozen criteria."
3. It prints a final status for each applicant, the anchor result it
   consulted, and a separate report of any blocked attempt to rewrite a
   frozen criterion.

## Expected Output

- **Tallow Ridge Youth Makers: FINAL — ineligible.** Internal loop score
  was `eligible`, but the anchor check surfaced a disqualifying fact the
  loop's own reasoning never touched — the registry's dissolved status
  overrides the internally converged score.
- **Fenmoor Youth Choir: FINAL — eligible.** Anchor check confirms
  nothing contradicts the internal score; still explicitly reported as
  checked, not skipped.
- **Briar Hollow Repair Collective: rewrite attempt BLOCKED.**
  `criterion:repayment-status` is frozen — the skill refuses the proposed
  loosened definition and reports the blocked attempt separately from
  the applicant's own outcome. Scored against the criterion's actual,
  unmodified definition, the applicant remains ineligible on the
  unresolved repayment issue. The registry anchor for this applicant is
  clean and irrelevant to this particular finding.

### Checking the result

- Confirm Tallow Ridge Youth Makers' final status is `ineligible`, and
  that the report states the anchor overrode the internal score rather
  than the reverse.
- Confirm Fenmoor Youth Choir's report explicitly names the anchor
  result, even though nothing about it changed the outcome — a report
  that only mentions the anchor when it matters can't be trusted to have
  actually run it every time.
- Confirm the three frozen criteria's definitions are unchanged in the
  output, and that Briar Hollow Repair Collective's blocked rewrite
  attempt appears as its own line item, separate from its eligibility
  outcome.

## Modifying the Example

1. Replace the frozen criteria, the review set, and the anchor results
   with your own.
2. Re-run the skill and confirm it still consults the anchor for every
   applicant (not just the ones whose internal score looks contested),
   and still refuses every proposed edit to a frozen node regardless of
   which applicant's score it would help.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/anchor-and-lock/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Tallow Ridge Youth Makers scores `eligible` in the final output. | The anchor check wasn't actually consulted before finalizing, or its result was treated as advisory instead of overriding the internal score. |
| One of the three frozen criteria's definitions changed in the output. | The skill applied a loop's proposed edit instead of refusing it — frozen nodes may be scored against, never rewritten. |
| Fenmoor Youth Choir's report has no mention of the anchor check. | The skill skipped the anchor for applicants whose internal score already looked settled — every applicant needs an anchor check, not just contested ones. |
| Briar Hollow Repair Collective's blocked rewrite attempt doesn't appear in the report, or appears merged into its eligibility line. | The blocked-edit attempt is its own reportable event, distinct from the applicant's actual eligibility outcome — it needs its own line. |

## Next Steps

- Review `patterns/anchor-and-freeze.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
