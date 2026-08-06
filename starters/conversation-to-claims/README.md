# conversation-to-claims Starter Kit

A single-tool (Claude Code) reference kit for the **conversation-to-claims**
pattern: capturing every factual assertion made in the course of a
conversation as its own provisional claim node, before the transcript
that carried it gets summarized away or closed. This is an extended
kit — see `starters/README.md` for how that differs from the seven core
kits.

Coldharbor Appliances, the customer in this transcript, and the support
conversation itself are all invented for this course, not drawn from any
real support interaction.

## Prerequisites

- Claude Code.
- No external services or API keys — the transcript below is everything
  the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the sample transcript below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Sample transcript

```
Turn 1 — Customer (Priya): My fridge, a Coldharbor CH-220, has started
  rattling. It's been going on for about a week now.

Turn 2 — Agent: Sorry to hear that. Can you tell me when the unit was
  last serviced?

Turn 3 — Customer (Priya): The compressor was replaced under warranty
  back in March 2025. Nothing since then. Also, the rattling started
  right after we moved the fridge out to clean behind it.

Turn 4 — Agent: Thanks. I've pulled up your serial number — this unit's
  warranty extends through April 2027.

Turn 5 — Agent: Based on what you're describing, it might be a loose fan
  blade from when the unit was moved, but I'm not certain without a
  technician visit.

Turn 6 — Customer (Priya): Okay, can you send someone out this week?
```

### Claude Code

1. Load the skill: `.claude/skills/transcript-to-claims/SKILL.md`.
2. Ask it to run: "Use the transcript-to-claims skill on the sample
   transcript in README.md."
3. It prints one claim node per factual assertion, each labeled with its
   speaker, turn number, and whether it's hedged.

## Expected Output

Six claim nodes, roughly:

1. **Turn 1** (Priya): `CH-220 --has_symptom--> rattling` — began
   roughly one week before this conversation. Not hedged.
2. **Turn 3** (Priya): `CH-220's compressor --replaced_under_warranty-->
   March 2025`. Not hedged.
3. **Turn 3** (Priya): rattling onset coincides with the fridge being
   moved to clean behind it. Not hedged.
4. **Turn 4** (Agent): `CH-220's warranty --extends_through--> April
   2027`. Not hedged.
5. **Turn 5** (Agent): possible cause — loose fan blade from being
   moved. **Hedged** ("might be," "not certain") — must be flagged as
   speculative, not folded in as a stated fact.

Turns 2 and 6 are questions and requests, not assertions, and should
produce no claim nodes.

### Checking the result

- Confirm turn 5's claim is marked hedged/low-confidence and is
  distinguishable from turns 1, 3, and 4, which are stated as fact.
- Confirm no claim node was produced for turn 2 or turn 6.
- Confirm the two separate assertions inside turn 3 (compressor
  replacement date, and the rattling's timing relative to the move) came
  out as two claims, not merged into one.

## Modifying the Example

1. Swap in your own transcript.
2. Re-run the skill and check that every hedge in your transcript is
   still flagged, and that questions/requests still produce no claims.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/transcript-to-claims/SKILL.md` — the Claude Code
  skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Turn 5's claim isn't flagged as hedged. | The skill treated "might be" / "not certain" as ordinary phrasing instead of a confidence signal. Hedge words must set the claim's confidence flag, not just get echoed in the claim text. |
| A claim node appears for turn 2 or turn 6. | The skill extracted a question or a request as if it were an assertion. Only statements that assert something about the world count. |
| The two assertions in turn 3 got merged into a single claim node. | The skill grouped by turn instead of by assertion. One turn can contain more than one claim; each gets its own node. |

## Next Steps

- Review `patterns/conversation-to-claims.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
