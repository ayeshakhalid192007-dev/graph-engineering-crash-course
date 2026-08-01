# Environment Setup

Nothing in this course requires a paid API key or a network connection to follow along — every hands-on piece is designed to run locally, on your own machine, with tools you almost certainly already have.

## What you need installed

- **Git.** You'll clone this repo and, if you want to try the practice projects for real, probably fork it. Any reasonably recent version works.
- **Node.js.** A handful of the small verification scripts in this repo (including the originality checker you can see in `scripts/`) run on Node. Any current LTS release is fine.
- **Python 3.** Several of the live labs starting in Part 1 are short, standalone Python scripts — no framework, no package installs, nothing beyond the standard library. They're written that way on purpose: run the script, read what it prints, and you've watched the concept happen instead of just reading about it.
- **At least one agent coding tool: Claude Code or OpenCode.** Starting with Day 2's step pages, code examples are shown in both tools side by side. You only strictly need one of them to follow along, but having both installed lets you compare how the same idea is expressed in each.

## Why both git and Python **and** Node

They're doing different jobs. Git is how you get the material and how you'd submit changes back. Python is what the dependency-free live labs are written in, because it needs no setup beyond "Python is on this machine." Node is what this repository's own quality-gate scripts run on — you don't need it to read the course, but you'll want it if you're contributing back or checking your own work against the same rules this repo checks itself against.

## A note on tool coverage

Not every pattern in the library gets a full example in both agent tools. The seven core patterns — one representative pick per major category — ship with complete, tested kits for both Claude Code and OpenCode. The remaining patterns ship with a working reference implementation in a single tool, plus a written note on how to carry that same implementation over to the other one. This is a disclosed scope decision, not an oversight: it's how a catalog this size stays honest about what's actually been built and tested versus what's a documented path you'd walk yourself.

## Once you're set up

Head back to the [prerequisites index](README.md) for the rest of this section, or jump to [the entry page](../00-start-here/README.md) if you skipped it.
