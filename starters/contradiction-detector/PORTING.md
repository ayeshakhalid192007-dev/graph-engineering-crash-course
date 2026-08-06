# Porting `contradiction-detector` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/scan-contradictions/SKILL.md`. No OpenCode equivalent
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
    { "name": "scan-contradictions", "type": "skill", "path": "skills/scan-contradictions/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "scan", "tool": "scan-contradictions", "input": { "edges": "pipe-filings.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the six pipe-segment filings as prose for a
Claude Code model to read directly. Porting means moving them into
`pipe-filings.json` — a flat list of edges, each with subject, predicate,
object, source, and date — since OpenCode workflow steps consume file
paths rather than a model reading a README section.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`scan-contradictions` skill by name against a given set of filings, in
the same turn, and the skill groups and compares inline. OpenCode instead
drives the equivalent through `workflow.steps`, and this pattern's
"independent of whatever task happens to be reading the graph" framing
maps naturally onto a scheduled step rather than a request-triggered one:
the `scan` step above would typically run on a timer or after every write
batch, not only when some other workflow step asks for it. The six-step
process in `SKILL.md` — read the full edge set, group by (subject,
predicate), compare object values pairwise within each group, refuse to
compare across different predicates, refuse to resolve any contradiction
found, report every group's outcome — becomes the body of that step's
handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The step most worth preserving carefully on a port is step 2's grouping
rule — comparing values only within a matching (subject, predicate) pair,
never across predicates or across subjects that merely share a source
document. In a single conversational Claude Code turn, that grouping step
and the comparison step that follows it sit right next to each other in
the same instructions, which makes it hard to skip one and not the other.
An OpenCode port that splits grouping into one workflow step and
comparison into a later one risks the later step losing track of exactly
which predicate a given value pair came from — especially if a
downstream step re-joins edges by subject alone for some other purpose
and the contradiction check inherits that looser join instead of running
its own. Keeping grouping and comparison inside a single step, the way
`SKILL.md` does here, is what keeps that risk contained.
