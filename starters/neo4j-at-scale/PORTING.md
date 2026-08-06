# Porting `neo4j-at-scale` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/traverse-multi-hop/SKILL.md`. No OpenCode equivalent
ships with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/`
alone. OpenCode needs an `opencode.json` at the kit root declaring the
skill as a tool backed by a graph-database connection, referenced through
an environment variable rather than embedded in the skill file:

```json
{
  "tools": [
    { "name": "traverse-multi-hop", "type": "skill", "path": "skills/traverse-multi-hop/SKILL.md", "env": ["NEO4J_URI", "NEO4J_AUTH"] }
  ],
  "workflow": {
    "steps": [
      { "name": "trace-contamination", "tool": "traverse-multi-hop", "input": { "start": "RL-2291", "relTypes": ["USED_IN", "PRODUCES", "DERIVED_FROM"], "maxHops": 10 } }
    ]
  }
}
```

This kit's `README.md` embeds the relationship types and the derivation
chain as prose for a Claude Code model to reason through directly.
Porting means pointing the `trace-contamination` step at a live Neo4j
instance over `NEO4J_URI`, since an OpenCode workflow step executes a
real Cypher query rather than a model narrating a described traversal.

## Skill-invocation model

Claude Code invocation is conversational and ad hoc — someone asks for
the `traverse-multi-hop` skill by name once a contaminated lot is
identified, in the same turn the incident is being investigated.
OpenCode's `workflow.steps` model is built more for scheduled or
triggered steps, but this pattern's actual invocation pattern —
triggered by a one-off incident, not a recurring schedule — maps better
onto a step invoked on demand (the way `receipt-per-edge`'s `attach`
step is invoked per batch) than onto a timer. The seven-step process in
`SKILL.md` — treat as a single variable-length path match, name allowed
relationship types, bound the depth, guard against cycles, exclude
property-coincidence matches, tag hop count and path, report the deepest
hop reached — becomes the body of that on-demand step's handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern). More substantively,
this kit's SKILL.md has the model compose the traversal logic itself
(step 1's "treat this as a variable-length path match") as prose
instructions a Claude Code model reasons through at invocation time. An
OpenCode port needs that same logic expressed as an actual parameterized
Cypher query the declared tool executes — the relationship-type
allowlist and hop bound from steps 2 and 3 becoming query parameters
(`relTypes`, `maxHops` above) rather than instructions a model
re-derives fresh on every call.

## Kit-specific porting risk

The part most worth preserving exactly on a port is steps 2 and 3
together: the explicit relationship-type allowlist and the explicit hop
bound. Those two constraints are what keep a variable-length native
traversal from doing exactly what made the old relational query slow and
convoluted in the first place, just faster — quietly walking into an
unrelated part of Amberlynn Genomics Consortium's graph, the way
`R-91004` shares RL-2291's chain's date and facility without sharing any
real derivation relationship to it. If a port exposes `relTypes` and
`maxHops` as free-form parameters a calling step can override per
invocation, an incident response under time pressure could widen both to
"just find everything reachable" and pull in results with no real
derivation link — trading a fast, precise contamination trace for a
noisy list the lab has to hand-verify anyway, which defeats the entire
point of moving this query onto native graph storage.
