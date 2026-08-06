# Porting `arbitration-edge` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/arbitrate-collision/SKILL.md`. No OpenCode equivalent
ships with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/` alone.
OpenCode needs an `opencode.json` at the kit root declaring the skill as
a tool and giving it a workflow step, matching the shape
`starters/receipt-per-edge/opencode/opencode.json.example` uses for its
`attach-receipts` skill:

```json
{
  "tools": [
    { "name": "arbitrate-collision", "type": "skill", "path": "skills/arbitrate-collision/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "arbitrate", "tool": "arbitrate-collision", "input": { "writes": "proposed-writes.json", "rule": "arbitration-rule.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the four proposed writes and the
arbitration rule as prose for a Claude Code model to read directly.
Porting means splitting those into `proposed-writes.json` (each write's
loop, node, field, value, and timestamp) and `arbitration-rule.json` (the
priority logic itself), since OpenCode workflow steps consume file paths
rather than a model reading a README section. In an OpenCode pipeline,
the `arbitrate` step would sit downstream of both loops' write steps and
upstream of whichever step actually commits a write to the graph, since
its whole job is to intercept a collision before either loop's write
lands unchallenged.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`arbitrate-collision` skill by name against a set of proposed writes and
a rule, in the same turn, and the skill groups, compares, and decides
inline. OpenCode instead drives the equivalent through `workflow.steps`:
the `arbitrate` step above names the tool and its inputs and runs as a
gate between both loops' write steps and the graph's actual write path.
The seven-step process in `SKILL.md` — read every proposed write, group
by (node, field), confirm a genuine value disagreement rather than
duplicate agreement, apply the stated rule, record the rejected write
with its reason, never merge or average colliding values, report per
group — becomes the body of that step's handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The step-splitting risk specific to this pattern sits in step 2's
grouping by (node, field) rather than by node alone. This kit's
`DO-5820` case exists precisely to test that: two writes share a node id
but target different fields, and treating that as a collision would
block a perfectly independent write for no reason. If an OpenCode port
separates "detect same-node writes" into one workflow step and "check
whether they actually target the same field" into a later one, a write
to an unrelated field on a busy node could get held at the gate waiting
on a collision that was never real — the two checks need to stay fused
into a single grouping key, exactly as step 2 does here, or the port
starts blocking writes this pattern was never meant to touch.
