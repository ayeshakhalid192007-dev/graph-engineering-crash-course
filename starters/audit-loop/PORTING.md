# Porting `audit-loop` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/audit-sweep/SKILL.md`. No OpenCode equivalent ships with
this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/` alone.
OpenCode needs an `opencode.json` at the kit root declaring the skill as
a tool and giving it a workflow step, matching the shape
`starters/receipt-per-edge/opencode/opencode.json.example` uses for its
`attach-receipts` skill:

```json
{
  "tools": [
    { "name": "audit-sweep", "type": "skill", "path": "skills/audit-sweep/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "audit", "tool": "audit-sweep", "input": { "claims": "weekly-claims.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the three claims as prose for a Claude Code
model to read directly. Porting means moving them into
`weekly-claims.json` — a list of claims, each with its policyholder, shop,
line-item breakdown, and the main loop's own approval outcome — since
OpenCode workflow steps consume file paths rather than a model reading a
README section. Unlike the main claims-adjustment loop, which would run
per-claim as items arrive, the `audit` step here needs to run on a
schedule (weekly, in this kit's scenario) over the accumulated batch, not
per item — its whole value depends on seeing the full set at once.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`audit-sweep` skill by name against a batch of claims, in the same turn,
and the skill reviews the whole set and reports inline. OpenCode instead
drives the equivalent through `workflow.steps`, and the scheduling
difference matters more here than in most patterns: the main loop's own
workflow would run once per claim, while the `audit` step needs to be a
separate, wider-scoped workflow entirely — triggered on a timer against
the accumulated output of many runs of the main loop, not chained
directly after any single one of them. The seven-step process in
`SKILL.md` — read the full output set as one batch, skip re-checking any
single item's own governing rule, look for cross-item recurrence,
require the recurring detail to actually match rather than just the
actor, name every item a pattern spans, refuse to resolve the pattern,
report reviewed-and-cleared items explicitly — becomes the body of that
separate workflow's step.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The mechanism-specific risk on this one is scope leakage in the other
direction from most patterns: because OpenCode workflows are built from
discrete steps, it's tempting to fold the audit step into the same
workflow definition as the main claims-adjustment loop, reasoning that
they're "part of the same claims pipeline." Doing that risks scoping the
`audit` step's input to whatever single run triggered it — exactly the
one-item view this pattern exists to escape. `MC-8815` in this kit's
worked example only gets correctly cleared (rather than wrongly flagged
or wrongly ignored) because the audit step can see all three claims
together; a port that wires `audit-sweep` to fire per-claim inside the
main loop's own workflow, instead of as an independently scheduled step
over the accumulated batch, reproduces the exact blind spot this pattern
was built to fix.
