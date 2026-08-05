# Porting `supersession-chain` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/supersede-claim/SKILL.md`. No OpenCode equivalent ships
with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill by its path under `.claude/skills/` alone —
no separate registration. OpenCode needs an `opencode.json` at the kit
root declaring the skill as a tool and giving it a workflow step, in the
shape `starters/receipt-per-edge/opencode/opencode.json.example` uses for
its `attach-receipts` skill:

```json
{
  "tools": [
    { "name": "supersede-claim", "type": "skill", "path": "skills/supersede-claim/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "correct", "tool": "supersede-claim", "input": { "claims": "claims.json", "evidence": "new-evidence.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the two existing claims and the 2024 SDS
excerpt as prose for a Claude Code model to read directly. Porting means
splitting those into `claims.json` (the claim nodes, their values,
sources, and statuses) and `new-evidence.json` (the correcting SDS
revision), since OpenCode workflow steps consume file paths rather than a
model reading a README section.

## Skill-invocation model

Claude Code invocation is conversational: a user asks for the
`supersede-claim` skill by name against a given claim set and new
evidence, in the same turn. OpenCode instead drives the equivalent
through `workflow.steps` — the `correct` step above names the tool and
its inputs, and runs structurally rather than by natural-language
request. The eight-step check-each-claim loop in `SKILL.md` — read
claims, read evidence, test each claim for direct correction, leave
unaffected claims alone, create the new node and edge for corrected ones,
flip old-node status, report — becomes the body of that step's handler,
executed once per claim in the input set per workflow run.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific and
have no direct equivalent in OpenCode's skill frontmatter, which uses a
`context` field instead (see `receipt-per-edge`'s OpenCode skill for the
pattern) and takes its file-access permissions from the `opencode.json`
tool declaration rather than from the skill file itself.

The rule most worth preserving carefully when porting is step 3's test
for direct correction versus mere same-source proximity — the density
claim in this kit's worked example comes from the same 2019 document as
the flash-point claim the new evidence corrects, but nothing in the 2024
revision addresses density, so it must stay untouched. That distinction
is tool-agnostic and carries over unchanged, but it's easy to lose if a
port collapses "which claims does this evidence touch" and "which claims
does this evidence correct" into a single workflow step instead of
keeping them as separate checks the way steps 3 and 4 do here.
