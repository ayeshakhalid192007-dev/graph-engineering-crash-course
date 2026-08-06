# Porting `file-graph-for-small-teams` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/propose-graph-diff/SKILL.md`. No OpenCode equivalent
ships with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/`
alone. OpenCode needs an `opencode.json` at the kit root declaring the
skill as a tool and giving it a workflow step, matching the shape
`starters/receipt-per-edge/opencode/opencode.json.example` uses for its
`attach-receipts` skill:

```json
{
  "tools": [
    { "name": "propose-graph-diff", "type": "skill", "path": "skills/propose-graph-diff/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "propose", "tool": "propose-graph-diff", "input": { "graph": "graph.json", "proposal": "proposed-reel.json" } }
    ]
  }
}
```

This kit's `README.md` embeds `graph.json`'s current state and both
proposed additions as prose and inline JSON blocks for a Claude Code
model to read directly. Porting means pointing the `propose` step at the
actual `graph.json` file and a separate `proposed-reel.json` per
submission, since OpenCode workflow steps consume file paths rather than
a model reading a README section.

## Skill-invocation model

Claude Code invocation is conversational — a volunteer asks for the
`propose-graph-diff` skill by name against a specific addition, in the
same turn, and gets a diff and a flag list back immediately. OpenCode
instead drives the equivalent through `workflow.steps`, and this
pattern's "every change goes through a normal pull request" framing maps
naturally onto a `propose` step triggered whenever a new catalog entry
file is committed to a proposal branch — the step would run automatically
on push, producing the diff and flag list as a commit status check or PR
comment rather than something a volunteer has to remember to ask for.
The seven-step process in `SKILL.md` — read current state, read the
proposal, produce a minimal diff, cross-check against on-file facts, flag
conflicts without dropping them, never write directly to the shared
file, report both outputs — becomes the body of that step's handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The one line worth reading twice before porting is step 6: "never write
directly to the shared graph file." In this kit's single Claude Code
turn, that boundary is easy to hold, because the skill's only declared
tools are `Read` and `Write`, and `Write` here means "write the diff
output," not "write graph.json." An OpenCode port that gives the
`propose` step write access to the repository — so it can, say, open the
pull request itself rather than just producing diff text — has to be
careful that "open a PR" and "merge a PR" stay two different actions
gated by a human's approval, or the step collapses into exactly the
single-writer shortcut this pattern exists to avoid. The whole reason
Larkspur Tape Archive's second volunteer caught the LT-0452 misattribution
was that the proposal sat as a diff for review before it touched the
shared file — an OpenCode workflow that auto-merges its own `propose`
step's output onto the branch `graph.json` lives on would remove exactly
the review window that catch depended on.
