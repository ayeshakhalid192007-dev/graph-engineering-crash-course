# Porting `anchor-and-freeze` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/anchor-and-lock/SKILL.md`. No OpenCode equivalent ships
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
    { "name": "anchor-and-lock", "type": "skill", "path": "skills/anchor-and-lock/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "finalize", "tool": "anchor-and-lock", "input": { "frozenNodes": "frozen-criteria.json", "reviewSet": "applicants.json", "anchorResults": "registry-lookups.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the frozen criteria, the review set, and
the registry lookups as prose for a Claude Code model to read directly.
Porting means splitting those into `frozen-criteria.json`,
`applicants.json`, and `registry-lookups.json`, since OpenCode workflow
steps consume file paths rather than a model reading a README section.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`anchor-and-lock` skill by name against a given review set, in the same
turn, and the anchor check and the frozen-node check both happen inline
in that one reasoning pass. OpenCode instead drives the equivalent
through `workflow.steps`, and the natural port would split "compute the
internal score" and "consult the anchor" into two separate steps feeding
a `finalize` step — since the internal scoring loop and the anchor lookup
are conceptually independent processes in this pattern's own framing.
The seven-step process in `SKILL.md` — read frozen nodes, read the
anchor, consult it for every item, compare against the internal score,
watch for rewrite attempts, refuse them, report both outcomes — becomes
the body of the `finalize` step's handler, but only if that step is
given the internal score and the anchor result as inputs rather than
being trusted to fetch or trust either one after the fact.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The part most worth preserving carefully on a port is the ordering
guarantee behind step 3 and step 4: the anchor must be consulted *before*
any status is finalized, for every item, not fetched afterward as a
sanity check on items that already look settled. In a single
conversational Claude Code turn, "consult the anchor" and "finalize"
sit inside the same instructions and naturally happen in that order. An
OpenCode port that splits scoring, anchoring, and finalizing into three
separate workflow steps risks the `finalize` step running against a
cached or stale anchor result — or worse, running before the anchor step
has completed at all, exactly reproducing the failure this pattern
exists to prevent: a decision that looks settled from inside the loop
system while the one check that could have caught Tallow Ridge Youth
Makers' dissolved status never actually ran in time to matter. The same
risk applies to the frozen-node check in step 5: if a downstream step is
ever given direct write access to the criteria file to "simplify" the
workflow, nothing in `opencode.json` stops it from applying an edit that
this kit's single-turn skill would have refused outright.
