# Harness Engineering Primer

## Hook

Picture an agent given real permission to open pull requests against a production codebase. Left completely alone, that's terrifying — it could rewrite half the repo in one commit, invent an API that doesn't exist, or quietly skip the test suite because nobody told it not to. A harness is the scaffolding built around that agent so its freedom to act stays useful instead of becoming a liability. This course assumes you've already built one and know its five moving parts by name.

## Explanation

Harness Engineering organizes the scaffolding around an agent into five jobs, and each one answers a different question about what the agent is allowed to do.

**Constrain** narrows the space of actions before the agent ever takes a turn — a diff size cap, a list of files it's not allowed to touch, a rule that it can propose a merge but never execute one itself. Constraint is prevention: it removes a category of mistake by making it unreachable, rather than catching it afterward.

**Inform** hands the agent the context it needs to act well — the team's style guide, the ticket it's working from, the result of the last test run. An agent that constrains without informing just produces safe, useless output; informing is what makes the constrained space worth acting inside.

**Verify** checks the agent's output against something outside the agent's own opinion of itself — a test suite passing, a schema validating, a lint rule holding. This is the step that stops "I'm confident this is right" from being treated as evidence that it actually is.

**Correct** takes a verification failure and, where the fix is narrow and well understood, applies it automatically — reformatting a file, retrying a flaky call, filling in a missing field — so a human isn't paged for something a script could have handled.

**Escalate** is the honest fallback: when a failure doesn't fit a known correction, the harness stops pretending it can handle everything and hands the decision to a person, with enough context attached that the handoff doesn't cost them another hour of digging.

## Check yourself

An agent's tests fail after it opens a pull request. The harness reformats a misindented line automatically, then still can't get the suite green, and pings a human with the failing test output attached. Which job did the reformat belong to, and which job did the ping belong to?

<details>
<summary>Reveal the answer</summary>

The reformat is a correction — a narrow, understood fix applied without asking. The ping is an escalation — the harness recognizing the remaining failure doesn't match anything it knows how to fix on its own, and handing it off with the context a person needs to act on it.

</details>

---

Hold on to that last job in particular: the shared graph this course teaches you to build is exactly the kind of outside evidence a harness's verify stage reaches for when "trust the agent's own report" isn't good enough anymore.
