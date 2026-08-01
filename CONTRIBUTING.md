# Contributing to Graph Engineering

We welcome contributions to the Graph Engineering course—whether that's bug reports, improvements to the documentation, new pattern implementations, or tools to help others build and audit their graphs.

## Contribution Ladder

**Everyone starts here.** Pick a good-first-issue from our issue tracker to familiarize yourself with the course structure, the originality policy (§2.1 in `graph-plan.md`), and our patterns and conventions. Good first issues are kept simple: typo fixes, small docs clarifications, or minor examples.

**Pattern authors come next.** Once you've contributed a few updates to the existing course material, you can author a new pattern or port an existing pattern to a second tool. See the "How to add a pattern" section below for the full walkthrough—it involves writing a spec, example code, and documentation that others can clone and run.

**Track maintainers.** As you build expertise in one area of the course (e.g., resolution patterns, or the OpenCode toolchain), you become the maintainer for that track. Maintainers review and approve pattern PRs in their domain, help onboard new pattern authors, and maintain the quality of implementations.

## How to Add a Pattern

Every pattern in the library follows the same shape. This walkthrough assumes you have an idea for a new pattern (or a port of an existing one to a new tool) and want to get it into the library.

### 1. Check the spec first

Before writing code, make sure your pattern fits:

- **It solves a recurring problem in multi-agent systems.** (E.g., "how do I merge duplicate facts while keeping the merge reversible?" vs. "here's a clever optimization for one specific scenario.")
- **It's documented and demonstrated, not maintained as a package.** (We ship specs and example code, not a live maintained library.)
- **It fits into one of seven categories:** Extraction (A), Resolution (B), Provenance (C), Subgraph construction (D), Checking (E), Governance (F), or Storage & scale (G). (See `graph-plan.md` §17 for the full catalog.)

### 2. Fork and create a branch

<!-- Placeholder: Replace with real GitHub repository URL once a remote is created -->
```bash
git clone https://github.com/graph-engineering-course/graph-engineering-course.git
cd graph-engineering-course
git checkout -b pattern/your-pattern-name
```

### 3. Write the pattern kit

Every pattern directory has this exact shape:

```text
patterns/your-pattern-name/
├── PATTERN.md                    # what it does, inputs/outputs, failure mode if skipped
├── README.md                      # quickstart: how to run the example
├── schema.example.json            # for write-path patterns; shows the node/edge shape
├── .claude/                       # Claude Code agent definitions and skills
│   └── skills/
│       └── <skill>.SKILL.md
└── opencode/                      # OpenCode implementations
    ├── opencode.json.example
    └── skills/
        └── <skill>.SKILL.md
```

#### PATTERN.md

The spec. Include:

- **What it does:** one sentence summary.
- **When to use it:** the problem it solves.
- **Inputs:** what the pattern expects from the graph (e.g., a set of candidate facts, a schema).
- **Outputs:** what the pattern produces or modifies.
- **Failure mode if skipped:** what breaks if you don't use this pattern.
- **Example scenario:** a concrete before/after.

#### README.md

The quickstart guide. Include:

- **How to run the example:** step-by-step (no external dependencies; uses local data).
- **Code walkthrough:** explain the key parts of the implementation.
- **Adapt it for your use case:** how to customize the pattern for a different schema or domain.

#### schema.example.json

For write-path patterns (extraction, resolution, provenance): a JSON file showing the node and edge structure your pattern produces. This helps readers understand the contract.

#### .claude/ and opencode/

Complete, runnable implementations. Each should:

- Include one SKILL.md per skill (per the Claude Code / OpenCode definitions).
- Work standalone with `graph-engineering-course` cloned and no other dependencies (besides the agent tool itself).
- Have a working example command or script that runs the pattern start-to-finish.

### 4. Write from your own understanding

Per the originality policy in `graph-plan.md` §2.1:

- **Read for concepts, write from memory.** If you're adapting a pattern from another source, read it once, then write your own version without the source open.
- **No 8+ consecutive word runs.** None of your prose can match verbatim any cited source for 8 words in a row.
- **Credit the idea, not the words.** If the pattern concept comes from an external source, cite it in your README and in `resources/sources.md`.

### 5. Add your pattern to the registry

Edit `patterns/registry.yaml` and add an entry for your pattern:

```yaml
- name: your-pattern-name
  title: Your Pattern Title
  category: <A-G>                 # Extraction, Resolution, Provenance, Subgraph, Checker, Governance, Storage
  stage: read|write|governance    # which phase of the graph lifecycle
  cost: Low|Medium|High           # computational or cognitive cost
  tools: [Claude Code, OpenCode]  # which agent tools have full examples
```

### 6. Open a pull request

Push your branch and open a PR against `main`. The PR runs automated checks:

- **Originality check** — ensures no 8+ consecutive words match any cited source.
- **Registry validation** — confirms your pattern is correctly listed in `patterns/registry.yaml`.
- **Link check** — verifies all internal links work.

Address any feedback, and once approved, your pattern is merged into the library.

## Other Contribution Types

**Docs corrections:** Typo fixes, clarity improvements, and broken link reports are welcome. File an issue or a quick PR.

**Tool ports:** If you've ported an existing pattern to Claude Code or OpenCode and want to share it, follow the pattern author path above.

**Live labs & examples:** If you've built a runnable demo of a concept from the course, we'd love to add it to `examples/` or `docs/`.

**Tooling:** Improvements to `scripts/` (link checker, registry validator, originality checker, graph-ready auditor) are welcome.

## Questions?

- Check `docs/00-start-here/` if you're new to the course.
- Read `SECURITY.md` for responsible disclosure.
- Open an issue if you have a question or suggestion.

Thank you for helping grow the Graph Engineering community!
