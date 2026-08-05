# Graph Engineering — A Crash Course

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
<!-- TODO: replace with real CI badge once a GitHub remote exists -->

## Overview

A single automated agent can work with a thin memory file—read it in, act, write it back—because only one reader and one writer exist at a time. The moment you deploy multiple agents working in parallel or split a task across several workers, that approach breaks. Two writers corrupt each other's updates, and a reader has no way to distinguish a verified fact from someone's half-finished guess.

**Graph Engineering** teaches the practice of building a shared, structured memory—a graph of facts and a graph of work history—that lets independent agents collaborate safely. This course packages that discipline into a complete learning system with two surfaces: a GitHub-hosted markdown course (with runnable starter kits) and an interactive website. Everything you need to understand, build, and audit graphs that power multi-agent systems.

## Navigation

| Section | Description |
| --- | --- |
| **[Start here →](docs/00-start-here/)** | Begin with the learning path and prerequisite checks |
| **[Course docs →](docs/README.md)** | The complete 17-step curriculum (foundations through advanced patterns) |
| **[Pattern library →](patterns/README.md)** | Production-ready graph patterns and example implementations |
| **[Starter kits →](starters/README.md)** | Clone-and-run templates for Claude Code and OpenCode |
| **[Sources →](resources/sources.md)** | Full attribution for the ten primary sources |

## Quickstart

1. **Clone this repo:**
   <!-- Placeholder: Replace with real GitHub repository URL once a remote is created -->
   ```bash
   git clone https://github.com/graph-engineering-course/graph-engineering-course.git
   cd graph-engineering-course
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

<!-- Placeholder: Replace repository URL once a GitHub remote is created -->
```bibtex
@software{graph-eng-course-2026,
  title = {Graph Engineering — A Crash Course},
  author = {{Graph Engineering Course Contributors}},
  year = {2026},
  url = {https://github.com/graph-engineering-course/graph-engineering-course},
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
