# Graph Engineering — A Crash Course

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/ayeshakhalid192007-dev/graph-engineering-crash-course/actions/workflows/originality-check.yml/badge.svg)](https://github.com/ayeshakhalid192007-dev/graph-engineering-crash-course/actions)
[![npm](https://img.shields.io/npm/v/@graph-engineering-kits/graph-kit.svg)](https://www.npmjs.com/package/@graph-engineering-kits/graph-kit)

## Overview

A single automated agent can work with a thin memory file—read it in, act, write it back—because only one reader and one writer exist at a time. The moment you deploy multiple agents working in parallel or split a task across several workers, that approach breaks. Two writers corrupt each other's updates, and a reader has no way to distinguish a verified fact from someone's half-finished guess.

**Graph Engineering** teaches the practice of building a shared, structured memory—a graph of facts and a graph of work history—that lets independent agents collaborate safely. This course packages that discipline into a complete learning system with two surfaces: a GitHub-hosted markdown course (with runnable starter kits) and an interactive website. Everything you need to understand, build, and audit graphs that power multi-agent systems.

## Navigation

| Section | Description |
| --- | --- |
| **[Start here →](docs/00-start-here/)** | Begin with the learning path and prerequisite checks |
| **[Course docs →](docs/README.md)** | The complete 17-step curriculum (foundations through advanced patterns) |
| **[Pattern library →](patterns/README.md)** | Production-ready graph patterns and example implementations |
| **[Starter kits →](starters/README.md)** | 23 runnable kits for Claude Code and OpenCode — installable via `npx @graph-engineering-kits/graph-kit` |
| **[Sources →](resources/sources.md)** | Full attribution for the ten primary sources |

## Quickstart

**Just want a starter kit?** You don't need this repo at all:

```bash
npx @graph-engineering-kits/graph-kit list              # all 23 kits
npx @graph-engineering-kits/graph-kit document-to-facts # install one here
```

No clone, no build, no API keys. See [`packages/graph-kit`](packages/graph-kit/README.md).

**Want the course?**

1. **Clone this repo:**

   ```bash
   git clone https://github.com/ayeshakhalid192007-dev/graph-engineering-crash-course.git
   cd graph-engineering-crash-course
   ```

2. **Read the prerequisites** — this course assumes you've already worked through Loop Engineering and Harness Engineering. If not, [start there](docs/00-start-here/).

3. **Follow [docs/00-start-here/](docs/00-start-here/)** — the entry point for all learning paths.

4. **No build step required.** All course material is readable on GitHub with relative links; interactive features and diagrams are available on the website.

## Prerequisites

This course builds on two prerequisites:

- **Loop Engineering** — the patterns for single-agent loops (heartbeat, spine, maker/checker).
- **Harness Engineering** — the vocabulary for agent control (constrain, inform, verify, correct, escalate).

If you haven't completed these courses, [start with the prerequisite section →](docs/00-start-here/).

## Contributing

We welcome contributions: bug reports, pattern additions, example implementations, and improvements to the course material. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution ladder and a concrete walkthrough of how to add a new pattern.

## Citation

If you use this course in your work, please cite it:

```bibtex
@software{graph-eng-course-2026,
  title = {Graph Engineering — A Crash Course},
  author = {{Graph Engineering Course Contributors}},
  year = {2026},
  url = {https://github.com/ayeshakhalid192007-dev/graph-engineering-crash-course},
  license = {MIT}
}
```

Or use the [CITATION.cff](CITATION.cff) file directly.

## Security

For responsible disclosure of security vulnerabilities, see [SECURITY.md](SECURITY.md).

## License

This course is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

**Built by:** Graph Engineering Course Contributors  
**Version:** 1.0  
**Last updated:** 2026-07-31
