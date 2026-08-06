# audit-loop Starter Kit

A single-tool (Claude Code) reference kit for the **audit-loop** pattern:
running a separate loop with a wider vantage point that periodically
reviews territory the main loop structurally can't see from inside its
own one-item-at-a-time scope. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Marrow Creek Mutual and the claims below are invented for this course,
not drawn from any real insurer, policyholder, or repair shop.

## Prerequisites

- Claude Code.
- No external services or API keys — the claims below are everything the
  kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the week's claims below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### This week's claims (already approved by the main claims-adjustment loop)

- `MC-8801` — policyholder Reyes, fender damage. Repair estimate from
  Alder Street Auto Body: quarter panel replacement $1,050, paint-match
  respray $890, sensor recalibration $200. Approved — within coverage
  limit, invoice and photo on file.
- `MC-8809` — policyholder Okafor, unrelated accident, filed three days
  later. Repair estimate from Alder Street Auto Body: quarter panel
  replacement $1,050, paint-match respray $890, sensor recalibration
  $200. Approved — within coverage limit, invoice and photo on file.
- `MC-8815` — policyholder Danville, filed the same week. Repair estimate
  from Alder Street Auto Body: bumper-only repair, $410. Approved —
  within coverage limit, invoice and photo on file.

Each claim was checked individually by the main loop against its own
policy's coverage terms, and each passed on its own merits.

### Claude Code

1. Load the skill: `.claude/skills/audit-sweep/SKILL.md`.
2. Ask it to run: "Use the audit-sweep skill on the week's claims in
   README.md."
3. It prints every cross-claim pattern found, naming which claims it
   spans, plus an explicit clear note for any claim reviewed and not
   part of a pattern.

## Expected Output

- **Pattern found:** `MC-8801` and `MC-8809` — both estimated by Alder
  Street Auto Body, both carrying an identical three-line breakdown
  ($1,050 / $890 / $200), despite unrelated policyholders and unrelated
  accidents. The report notes this is exactly the class of problem the
  main loop couldn't have caught, since it only ever reviewed one claim
  at a time.
- **Reviewed, no pattern:** `MC-8815` — also from Alder Street Auto Body,
  but a distinct bumper-only breakdown at a different amount. Shop match
  alone isn't the pattern; the line items don't recur.

### Checking the result

- Confirm the flagged pattern names both `MC-8801` and `MC-8809`
  explicitly, with the specific matching detail (the identical
  three-line breakdown) stated, not just "same shop."
- Confirm `MC-8815` is **not** swept into the flagged pattern — it shares
  a shop with the other two but not a matching breakdown.
- Confirm the report doesn't re-check any claim against its own policy
  terms — that's the main loop's job, already done.

## Modifying the Example

1. Replace the week's claims with your own main-loop output set.
2. Re-run the skill and confirm it only flags patterns backed by an
   actual recurring detail across multiple items, and states an explicit
   cleared outcome for every item it reviewed but didn't flag.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/audit-sweep/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `MC-8815` gets swept into the flagged pattern. | The skill matched on the shop name alone instead of requiring the line-item breakdown to actually recur. Same vendor is not itself the pattern. |
| The pattern report only names `MC-8801`, not `MC-8809`. | Every claim the pattern spans must be named — a flag naming only one claim gives a reviewer nothing to compare against. |
| The skill re-approves or re-denies a claim. | Audit-sweep surfaces patterns; it doesn't resolve them. Re-run and check step 6 of `SKILL.md` wasn't skipped. |
| A claim is missing from the report entirely. | Every claim in the review window needs an explicit outcome — part of a named pattern, or cleared — not silence. |

## Next Steps

- Review `patterns/audit-loop.md` in the course repo for the general
  (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
