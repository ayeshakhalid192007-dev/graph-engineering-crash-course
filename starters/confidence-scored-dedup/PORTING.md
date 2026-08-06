# Porting `confidence-scored-dedup` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/score-and-merge/SKILL.md`. No OpenCode equivalent ships
with this kit; here's what porting it would take.

## Config file location

Claude Code needs nothing beyond the skill's path under
`.claude/skills/`. OpenCode instead requires an `opencode.json` at the
kit root registering the skill as a tool and giving it a workflow step,
following the shape used in
`starters/receipt-per-edge/opencode/opencode.json.example`:

```json
{
  "tools": [
    { "name": "score-and-merge", "type": "skill", "path": "skills/score-and-merge/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "dedup", "tool": "score-and-merge", "input": { "pairs": "candidates.json", "rule": "scoring-rule.json" } }
    ]
  }
}
```

This kit's README embeds the scoring rule (signal weights, threshold) and
the three candidate pairs directly as prose tables for a Claude Code
model to read. Porting to OpenCode means splitting those into two
separate JSON files — a `scoring-rule.json` with the weights and
threshold, and a `candidates.json` array of pairs — since OpenCode's
`workflow.steps` takes file paths as input, not README sections.

## Skill-invocation model

Claude Code invocation here is conversational: a user asks for the
`score-and-merge` skill by name against a named data source, and the
model works through `SKILL.md`'s seven steps in the same turn. OpenCode
runs the equivalent as a structural workflow step — the `dedup` step
above — driven by `opencode.json` rather than a natural-language request.
Porting `SKILL.md`'s instructions means turning them into a
workflow-step handler that reads `scoring-rule.json` and
`candidates.json`, computes the per-pair scores, and writes both outputs
(auto-merged set, review queue) to files rather than printing them
directly to a conversation.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` fields in this skill's frontmatter are
Claude-Code-specific and have no direct OpenCode equivalent in skill
frontmatter — OpenCode skills instead carry a `context` field (see
`receipt-per-edge`'s OpenCode skill for the pattern) and inherit their
file-access permissions from the `opencode.json` tool declaration, not
from anything declared inside the skill file itself.

The scoring arithmetic in steps 2 through 4 — summing weighted signals
and comparing the total to a single threshold, with no signal allowed to
veto the sum on its own — is plain logic with nothing Claude-Code-specific
in it, and ports unchanged. The one thing worth calling out explicitly in
an OpenCode version: step 4's "the total decides, not any one signal"
rule is easy to accidentally violate if a workflow author adds a
conditional branch on the address-match signal alone later — it's worth
a comment in the ported handler warning against that, since nothing in
OpenCode's workflow-step structure enforces it automatically.
