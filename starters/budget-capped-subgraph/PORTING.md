# Porting `budget-capped-subgraph` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/trim-to-budget/SKILL.md`. No OpenCode equivalent ships
with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/`
alone. OpenCode needs an `opencode.json` at the kit root declaring the
skill as a tool and giving it a workflow step, matching the shape
`starters/receipt-per-edge/opencode/opencode.json.example` uses for its
`attach-receipts` skill:

```json
{
  "tools": [
    { "name": "trim-to-budget", "type": "skill", "path": "skills/trim-to-budget/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "cap", "tool": "trim-to-budget", "input": { "candidate": "candidate-subgraph.json", "budget": 8 } }
    ]
  }
}
```

This kit's `README.md` embeds the candidate subgraph (anchor, scored
nodes, edges) as a Markdown table and list for a Claude Code model to
read directly, with the budget stated as a plain sentence. Porting means
moving the candidate subgraph into `candidate-subgraph.json` and the
budget into a plain numeric field on the workflow step's `input`, since
OpenCode workflow steps consume structured input rather than a model
reading a README's prose and tables.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`trim-to-budget` skill by name against a candidate subgraph and a budget,
in the same turn, and the skill decides node-by-node inline. OpenCode
instead drives the equivalent through `workflow.steps`: the `cap` step
above names the tool and its inputs and runs as a distinct pipeline
stage, typically right after whatever step produced the candidate draw
(e.g., the port of `task-scoped-retrieval`) and right before the step
that hands the trimmed subgraph to a worker. The six-step process in
`SKILL.md` — fix the anchor, sort by relevance, fill the budget, state
the rule, re-check edges, report all four pieces together — becomes the
body of that step's handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The logic most worth preserving carefully on the way over is step 5's
requirement that edge survival be decided as its own pass, strictly after
node trimming is finalized — an OpenCode port that tries to fold node and
edge trimming into one combined workflow step risks evaluating an edge
against a node-kept-or-dropped decision that hasn't actually been made
yet. Keeping "decide which nodes survive" and "re-check every edge
against that final set" as two ordered sub-steps inside the handler, the
way `SKILL.md` does here, avoids that race.
