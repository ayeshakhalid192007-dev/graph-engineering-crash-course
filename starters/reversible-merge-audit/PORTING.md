# Porting `reversible-merge-audit` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/recheck-merges/SKILL.md`. No OpenCode equivalent ships
with this kit; here's what porting it would take.

## Config file location

Claude Code needs only the skill's path under `.claude/skills/` to find
it. OpenCode requires an `opencode.json` at the kit root declaring the
skill as a tool and giving it a workflow step, matching the shape used in
`starters/receipt-per-edge/opencode/opencode.json.example`:

```json
{
  "tools": [
    { "name": "recheck-merges", "type": "skill", "path": "skills/recheck-merges/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "audit", "tool": "recheck-merges", "input": { "history": "merge-history.json", "evidence": "new-evidence.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the merge history (two merges, their
bases) and the new evidence (the preprint, the grant record) as prose for
a Claude Code model to read directly. Porting means splitting those into
`merge-history.json` and `new-evidence.json`, since OpenCode's workflow
steps consume file paths rather than reading a README section by hand.
Because this pattern is meant to run periodically, not once, an OpenCode
port would also want a `schedule` entry on the `audit` step — Claude Code
has no equivalent scheduling concept built into the skill itself; running
this kit again later is just asking the skill again.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`recheck-merges` skill by name against a given history and evidence set,
in the same turn. OpenCode instead drives the equivalent through
`workflow.steps`: the `audit` step above names the tool and its inputs,
and execution is triggered structurally (by running the workflow, on a
schedule or on demand) rather than by a natural-language request. The
seven-step recheck loop in `SKILL.md` — read basis, gather evidence, test
for direct contradiction, reverse or confirm, report — becomes the body
of that step's handler, run once per merge in the history per workflow
execution.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific and
don't carry over to OpenCode's skill frontmatter, which instead uses a
`context` field (see `receipt-per-edge`'s OpenCode skill) and draws its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file.

The substantive rule that needs the most care when porting is step 3's
distinction between direct contradiction and merely-new-but-silent
evidence, and step 4's rule that reaffirming evidence can only ever
support a confirmation, never a reversal. Neither rule depends on
anything Claude-Code-specific, so the logic itself ports unchanged — but
because OpenCode workflow steps are easier to chain than Claude Code
skill instructions are to accidentally reorder, it's worth keeping steps
3 and 4 as one atomic decision in the ported handler rather than splitting
"check for contradiction" and "check for reaffirmation" into separate
workflow steps that could run out of order.
