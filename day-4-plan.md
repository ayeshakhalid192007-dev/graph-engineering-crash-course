# Day 4 Implementation Plan — The Website (`web/`), Polish, and Ship

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Execution mode:** This project uses **four separate, independent `/loop` instances — one per day — not one loop reused across days and not one combined loop spanning the whole project.** This document governs only Day 4's own dedicated loop, created fresh once the Day 3 approval gate clears — it shares no runtime state with Days 1–3's loops, all of which already stopped permanently. Task 1 (scaffold) and Task 2 (content libs) must land before anything else, since every page/component depends on them. Tasks 3–11 (components + pages) are then fanned out to parallel subagents grouped by the interfaces they share (see each task). Tasks 12–15 (polish, build verification, deploy, close-out) run sequentially at the end. **Task 14 (deploy) is blocked on two open decisions the user must make — see that task and the Approval Gate.** This is the fourth and final loop in the project — there is no Day 5 loop to hand off to.
>
> **Prerequisite:** Days 1–3 complete and approved. `docs/`, `patterns/`, `starters/` are feature-complete; this plan only reads from them, it does not modify their content.

**Goal:** Ship Deliverable 2 — a Next.js (App Router) site that renders every `docs/` page as an interactive course: sidebar navigation, reading progress, light/dark themes, animated diagrams, dual-tool code tabs, self-check quizzes, an interactive pattern browser and starter viewer, and the Graph Ready certification flow — responsive, accessible, and (pending the Task 14 decision) deployed.

**Architecture:** `web/lib/content.ts` reads Markdown/MDX directly from `../docs` and `../patterns` at build time (no CMS, no database — the filesystem *is* the content store, matching graph-plan.md §3's invariant that `docs/` is the single source of truth). `mdx-components.tsx` maps specific Markdown conventions (fenced code-tab blocks, `> [!NOTE]` callouts, mermaid fences) to React components at render time, so the Markdown itself stays plain and GitHub-readable.

**Tech Stack:** Next.js 15 (App Router), TypeScript, Tailwind CSS, MDX (`@next/mdx` or `next-mdx-remote` — decided in Task 1), mermaid (client-rendered to SVG).

## Global Constraints

- **Content-to-component mapping (§24):** ` ```claude ` / ` ```opencode ` fenced pairs → `CodeTabs`; `> [!NOTE]` / `> [!WARNING]` → `Callout`; `<!-- check -->` marker → `CheckYourself`; mermaid fences → a rendered diagram component. These four conventions must be decided and documented once (Task 3) and used identically by every page-rendering task afterward.
- **No content is written or edited in `web/`** — every word of course content already exists in `docs/`; `web/` only renders it. If a page reads wrong once rendered, the fix goes in `docs/`, not in a page component.
- **Package manager:** npm (not yarn/pnpm) — a plain default since the master plan doesn't specify one; flagging this as a low-stakes judgment call the user can override at the Day 4 approval gate if they have a preference.
- **Definition of Done for Day 4** (§27 Day 4 + §29 Deliverable 2): `web/` renders every `docs/` file; nav/progress/theme work; the four content-to-component mappings work; pattern browser, starter viewer, and Graph Ready checklist work; responsive; passes a basic accessibility check; `web-build` CI gate green. Full production deploy is conditional on Task 14's open decisions.

---

## Task 1: Scaffold `web/`

**Files:**
- Create: `web/package.json`
- Create: `web/tsconfig.json`
- Create: `web/next.config.mjs`
- Create: `web/tailwind.config.ts`
- Create: `web/postcss.config.mjs`
- Create: `web/app/globals.css`
- Create: `web/app/layout.tsx`
- Create: `web/.eslintrc.json`
- Create: `web/.gitignore`

**Interfaces:**
- Consumes: nothing.
- Produces: the Next.js project every later task builds inside. `layout.tsx` exports the root `<html>`/`<body>` shell that Task 4's `Sidebar` and `ThemeToggle` slot into.

- [ ] **Step 1: Write `web/package.json`**

```json
{
  "name": "graph-engineering-course-web",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@next/mdx": "^15.0.0",
    "gray-matter": "^4.0.3",
    "mermaid": "^11.0.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "^15.0.0"
  }
}
```

- [ ] **Step 2: Write `web/tsconfig.json`** — standard Next.js App Router TS config (`"jsx": "preserve"`, `"moduleResolution": "bundler"`, path alias `"@/*": ["./*"]`).

- [ ] **Step 3: Write `web/next.config.mjs`**

```javascript
import createMDX from "@next/mdx";

const withMDX = createMDX({});

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ["ts", "tsx", "mdx"],
};

export default withMDX(nextConfig);
```

- [ ] **Step 4: Write `web/tailwind.config.ts`** — content globs (`./app/**/*.{ts,tsx,md,mdx}`, `./components/**/*.{ts,tsx}`), `darkMode: "class"` (so `ThemeToggle`, Task 4, can toggle a class rather than relying only on `prefers-color-scheme`).

- [ ] **Step 5: Write `web/postcss.config.mjs`** — standard Tailwind/Autoprefixer setup.

- [ ] **Step 6: Write `web/app/globals.css`** — Tailwind directives plus CSS custom properties for the light/dark palette (two small palettes, not a full design system — this course's own visual identity, not copied from Loop Engineering's site despite sharing a stack per §26).

- [ ] **Step 7: Write `web/app/layout.tsx`**

```tsx
import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
import { ThemeToggle } from "@/components/ThemeToggle";

export const metadata: Metadata = {
  title: "Graph Engineering — A Crash Course",
  description: "Shared, structured memory for multi-loop and multi-agent systems.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="flex min-h-screen">
        <Sidebar />
        <div className="flex-1">
          <ThemeToggle />
          <main className="mx-auto max-w-3xl px-6 py-10">{children}</main>
        </div>
      </body>
    </html>
  );
}
```
(References `Sidebar` and `ThemeToggle`, built in Task 4 — this file compiles once Task 4 lands; note the dependency order in execution.)

- [ ] **Step 8: Write `web/.eslintrc.json`** — `{"extends": "next/core-web-vitals"}`.

- [ ] **Step 9: Write `web/.gitignore`** — `node_modules/`, `.next/`, `.env*.local` (redundant with root `.gitignore` from Day 1, but `web/` is a semi-independent package so its own `.gitignore` is conventional).

- [ ] **Step 10: Install and smoke-test**

```bash
cd web && npm install && npm run typecheck
```
Expected: install succeeds; typecheck fails only on missing `Sidebar`/`ThemeToggle` imports (expected until Task 4) — confirm the failure is exactly that, not a config error.

- [ ] **Step 11: Commit**

```bash
cd .. && git add web/package.json web/tsconfig.json web/next.config.mjs web/tailwind.config.ts web/postcss.config.mjs web/app/globals.css web/app/layout.tsx web/.eslintrc.json web/.gitignore
git commit -m "Scaffold web/: Next.js App Router project, Tailwind, MDX config"
```

---

## Task 2: `web/lib/` content loaders

**Files:**
- Create: `web/lib/content.ts`
- Create: `web/lib/roadmap.ts`
- Create: `web/lib/patterns.ts`

**Interfaces:**
- Consumes: the filesystem tree in `../docs` and `../patterns` (relative to `web/`, i.e. the repo root's `docs/` and `patterns/`).
- Produces: `getDocBySlug(slug: string[]): { frontmatter: Record<string, unknown>; content: string; filePath: string }`, `getAllDocSlugs(): string[][]`, `getRoadmap(): { parts: { title: string; steps: { title: string; slug: string[] }[] }[] }`, `getAllPatterns(): PatternMeta[]`, `getPatternBySlug(slug: string): PatternMeta & { patternMd: string; kitPath: string }` — every later task that renders `docs/`, `patterns/`, or the roadmap imports one of these four functions by this exact name and signature.

- [ ] **Step 1: Write `web/lib/content.ts`**

```typescript
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";

const DOCS_ROOT = join(process.cwd(), "..", "docs");

export function getAllDocSlugs(): string[][] {
  const slugs: string[][] = [];
  function walk(dir: string, prefix: string[]) {
    for (const entry of readdirSync(dir)) {
      const p = join(dir, entry);
      if (statSync(p).isDirectory()) {
        walk(p, [...prefix, entry]);
      } else if (entry.endsWith(".md")) {
        const name = entry.replace(/\.md$/, "");
        slugs.push(name === "README" ? prefix : [...prefix, name]);
      }
    }
  }
  walk(DOCS_ROOT, []);
  return slugs;
}

export function getDocBySlug(slug: string[]) {
  const candidates = [
    join(DOCS_ROOT, ...slug, "README.md"),
    join(DOCS_ROOT, `${slug.join("/")}.md`),
  ];
  const filePath = candidates.find((c) => existsSync(c));
  if (!filePath) throw new Error(`No doc found for slug: ${slug.join("/")}`);
  const raw = readFileSync(filePath, "utf8");
  const { data, content } = matter(raw);
  return { frontmatter: data, content, filePath };
}
```

- [ ] **Step 2: Write `web/lib/roadmap.ts`**

Derives the 7-part, 17-step roadmap structure by walking `docs/03-part-1-*` through `docs/09-part-7-*` (fixed list of the seven directory names, matching graph-plan.md §23 exactly) and reading each step file's first `#` heading as its title. Exports `getRoadmap()` per the Interfaces signature above.

- [ ] **Step 3: Write `web/lib/patterns.ts`**

Reads `../patterns/registry.yaml` (same hand-rolled flat-list parsing approach as `scripts/validate-registry.mjs`, Day 3 Task 15 — reuse that exact parsing logic rather than inventing a second implementation) plus each `../patterns/<name>.md` and `../starters/<name>/PATTERN.md`. Exports `getAllPatterns()` and `getPatternBySlug()` per the Interfaces signature.

- [ ] **Step 4: Add `gray-matter` typecheck pass**

```bash
cd web && npm run typecheck
```

- [ ] **Step 5: Commit**

```bash
cd .. && git add web/lib
git commit -m "Add web/lib content loaders: content.ts, roadmap.ts, patterns.ts"
```

---

## Task 3: `mdx-components.tsx` + content-to-component mapping primitives

**Files:**
- Create: `web/mdx-components.tsx`
- Create: `web/components/CodeTabs.tsx`
- Create: `web/components/Callout.tsx`
- Create: `web/components/CheckYourself.tsx`
- Create: `web/components/GraphDiagram.tsx`

**Interfaces:**
- Consumes: the four Markdown conventions from Global Constraints.
- Produces: `useMDXComponents()` export required by `@next/mdx`; `GraphDiagram` takes `{ chart: string }` (raw mermaid source) and is reused by `docs/[...slug]/page.tsx` (Task 6) for every mermaid fence in every rendered page.

- [ ] **Step 1: Write `web/components/CodeTabs.tsx`**

Props: `{ claude: string; opencode: string }` (two code strings). Renders a tab switcher (client component, `"use client"`) with local `useState` for the active tab, syntax-highlighted `<pre><code>` blocks (no external highlighting library required for v1 — plain monospace with the existing Tailwind typography is enough; note this as a v1 scope limit, not a bug).

- [ ] **Step 2: Write `web/components/Callout.tsx`**

Props: `{ type: "note" | "warning"; children: React.ReactNode }`. Renders a colored, bordered box per type.

- [ ] **Step 3: Write `web/components/CheckYourself.tsx`**

Props: `{ question: string; answer: string }`. Client component: renders the question, a "Reveal answer" button, and shows `answer` on click (local `useState`).

- [ ] **Step 4: Write `web/components/GraphDiagram.tsx`**

Props: `{ chart: string }`. Client component that calls `mermaid.render()` on mount (via `useEffect`) and injects the resulting SVG — this is the "mermaid (GitHub) upgraded to an animated SVG (site)" requirement from §12 Step 3; animation itself (nodes fading/drawing in) is a `Task 7` enhancement layered on top of this base renderer, not required for this task's definition of done.

- [ ] **Step 5: Write `web/mdx-components.tsx`**

```tsx
import type { MDXComponents } from "mdx/types";
import { CodeTabs } from "@/components/CodeTabs";
import { Callout } from "@/components/Callout";
import { CheckYourself } from "@/components/CheckYourself";
import { GraphDiagram } from "@/components/GraphDiagram";

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    CodeTabs,
    Callout,
    CheckYourself,
    GraphDiagram,
  };
}
```

Document (in a code comment) the exact preprocessing rule Task 6's page component must apply before passing content to the MDX renderer: a ` ```mermaid ` fence becomes `<GraphDiagram chart={\`...\`} />`, a `> [!NOTE]` block becomes `<Callout type="note">...</Callout>`, and so on — this string-preprocessing step lives in `docs/[...slug]/page.tsx` (Task 6), not in this file, since this file only registers the components.

- [ ] **Step 6: Commit**

```bash
git add web/mdx-components.tsx web/components/CodeTabs.tsx web/components/Callout.tsx web/components/CheckYourself.tsx web/components/GraphDiagram.tsx
git commit -m "Add MDX component mapping: CodeTabs, Callout, CheckYourself, GraphDiagram"
```

---

## Task 4: Core layout components

**Files:**
- Create: `web/components/Sidebar.tsx`
- Create: `web/components/ProgressNav.tsx`
- Create: `web/components/ThemeToggle.tsx`
- Create: `web/components/ProgressTracker.tsx`
- Create: `web/components/TrackSelector.tsx`

**Interfaces:**
- Consumes: `getRoadmap()` from `web/lib/roadmap.ts` (Task 2).
- Produces: `Sidebar` and `ThemeToggle` are imported directly by `web/app/layout.tsx` (Task 1) — their export names and zero-required-props signatures must match exactly what Task 1 Step 7 already imports (`Sidebar`, `ThemeToggle`, both no-prop components).

- [ ] **Step 1: Write `web/components/ThemeToggle.tsx`**

```tsx
"use client";
import { useEffect, useState } from "react";

export function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    setDark(stored ? stored === "dark" : prefersDark);
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  return (
    <button onClick={() => setDark((d) => !d)} aria-label="Toggle theme" className="p-2">
      {dark ? "🌙" : "☀️"}
    </button>
  );
}
```

- [ ] **Step 2: Write `web/components/Sidebar.tsx`**

Server component reading `getRoadmap()` and rendering a nested nav list (7 parts, 17 steps as links to `/docs/03-part-1-.../step-1-...` etc.), plus top-level links to `/tracks`, `/patterns`, `/projects`, `/resources`, `/certification`. Delegates the "which item is active" / progress-bar rendering to `ProgressNav` (Step 3).

- [ ] **Step 3: Write `web/components/ProgressNav.tsx`**

Props: `{ currentSlug: string[] }`. Client component: highlights the current page in the nav and computes "Step N of 17" from `getRoadmap()`'s flattened step list.

- [ ] **Step 4: Write `web/components/ProgressTracker.tsx`**

Props: `{ totalSteps: number }`. Client component: reads/writes a `localStorage` set of completed step slugs (marked complete when a reader visits a step's `CheckYourself`, wiring detailed in Task 6), renders a progress bar `completed/total`.

- [ ] **Step 5: Write `web/components/TrackSelector.tsx`**

Props: none. Renders the four skill tracks (G1–G4) as selectable cards (client component, `useState` for selection), each linking to its first step per graph-plan.md §12.1's table — data for the four tracks lives in a small local constant in this file (name, level, "you start knowing," "you finish able to," which steps it covers), not fetched from `docs/` (the table itself isn't a rendered doc page, so this is legitimate hardcoded structural data, not a content placeholder).

- [ ] **Step 6: Typecheck and commit**

```bash
cd web && npm run typecheck && cd ..
git add web/components/Sidebar.tsx web/components/ProgressNav.tsx web/components/ThemeToggle.tsx web/components/ProgressTracker.tsx web/components/TrackSelector.tsx
git commit -m "Add core layout components: Sidebar, ProgressNav, ThemeToggle, ProgressTracker, TrackSelector"
```

---

## Task 5: Landing page + tracks page

**Files:**
- Create: `web/app/page.tsx`
- Create: `web/app/tracks/page.tsx`

**Interfaces:**
- Consumes: `getRoadmap()` (Task 2), `TrackSelector` (Task 4).

- [ ] **Step 1: Write `web/app/page.tsx`** — the landing hero: the memory-problem pitch (fresh wording, same constraint as Day 1's README — don't reuse README's own sentences either, a third independent phrasing of the same pitch), a compact roadmap preview (first 3 steps + "see full roadmap" link to `/tracks`), and a "start here" CTA linking to `/docs/00-start-here`.
- [ ] **Step 2: Write `web/app/tracks/page.tsx`** — renders `<TrackSelector />` plus the full roadmap list from `getRoadmap()`.
- [ ] **Step 3: Typecheck, dev-server smoke test, and commit**

```bash
cd web && npm run typecheck && npm run dev &
sleep 3 && curl -sf http://localhost:3000 > /dev/null && echo "landing page OK"
kill %1
cd ..
git add web/app/page.tsx web/app/tracks/page.tsx
git commit -m "Add landing page and tracks page"
```

---

## Task 6: `docs/[...slug]/page.tsx` — the doc renderer

**Files:**
- Create: `web/app/docs/[...slug]/page.tsx`
- Create: `web/components/TryWithAI.tsx`
- Create: `web/components/TroubleshootBox.tsx`
- Create: `web/components/GlossaryTerm.tsx`

**Interfaces:**
- Consumes: `getDocBySlug`, `getAllDocSlugs` (Task 2), `useMDXComponents` (Task 3), `ProgressNav` (Task 4).
- Produces: this is the single page component that renders all ~50+ Day-1/2/3 markdown pages — every later fix to how a doc renders happens here, not in a per-page component.

- [ ] **Step 1: Write `web/components/TryWithAI.tsx`** — props `{ children: React.ReactNode }`, renders the "Try With AI" exercise box with a distinct visual treatment from `Callout` (this is an exercise prompt, not a note/warning).
- [ ] **Step 2: Write `web/components/TroubleshootBox.tsx`** — props `{ symptom: string; cause: string; fix: string }`, renders the "When it goes wrong" three-part box.
- [ ] **Step 3: Write `web/components/GlossaryTerm.tsx`** — props `{ term: string; children: React.ReactNode }`, renders an inline `<abbr>`-style popover using the term's definition looked up from `docs/02-foundations/glossary.md` (parsed once at build time via `getDocBySlug(["02-foundations", "glossary"])` and cached in a module-level map).
- [ ] **Step 4: Write `web/app/docs/[...slug]/page.tsx`**

```tsx
import { getDocBySlug, getAllDocSlugs } from "@/lib/content";
import { MDXRemote } from "next-mdx-remote/rsc";
import { useMDXComponents } from "@/mdx-components";
import { ProgressNav } from "@/components/ProgressNav";

export function generateStaticParams() {
  return getAllDocSlugs().map((slug) => ({ slug }));
}

export default function DocPage({ params }: { params: { slug: string[] } }) {
  const { content, frontmatter } = getDocBySlug(params.slug);
  return (
    <article>
      <ProgressNav currentSlug={params.slug} />
      <MDXRemote source={content} components={useMDXComponents({})} />
    </article>
  );
}
```
Note: this requires adding `next-mdx-remote` to `web/package.json` (Task 1's dependency list is amended here — `next-mdx-remote` is the correct choice over static `@next/mdx` imports because content lives outside `web/app` in `../docs`, which `@next/mdx`'s file-based compilation can't reach directly). Update `web/package.json` dependencies to add `"next-mdx-remote": "^5.0.0"` and rerun `npm install`.

- [ ] **Step 5: Typecheck, build, and commit**

```bash
cd web && npm install && npm run typecheck && npm run build && cd ..
git add web/app/docs web/components/TryWithAI.tsx web/components/TroubleshootBox.tsx web/components/GlossaryTerm.tsx web/package.json web/package-lock.json
git commit -m "Add docs/[...slug] page renderer and TryWithAI, TroubleshootBox, GlossaryTerm"
```

---

## Task 7: Interactive diagram components

**Files:**
- Create: `web/components/TwoGraphsSplit.tsx`
- Create: `web/components/LifecycleDiagram.tsx`
- Create: `web/components/SubgraphViewer.tsx`

**Interfaces:**
- Consumes: `GraphDiagram`'s mermaid-rendering approach (Task 3) as a base, extended with hand-built SVG/DOM animation (not mermaid-generated) for these three specific, named diagrams from §25.

- [ ] **Step 1: Write `web/components/TwoGraphsSplit.tsx`** — a hand-built animated side-by-side diagram (work-history graph vs. fact graph, illustrating Step 3 / `docs/02-foundations/the-two-graphs.md`), props `{ highlightSide?: "work-history" | "fact" }` so a page can call it out.
- [ ] **Step 2: Write `web/components/LifecycleDiagram.tsx`** — animated extraction → resolution → provenance pipeline (Steps 6–8), props `{ activeStage?: "extraction" | "resolution" | "provenance" }`.
- [ ] **Step 3: Write `web/components/SubgraphViewer.tsx`** — an interactive full-graph-vs-bounded-subgraph view (Step 9), props `{ fullGraph: { nodes: string[]; edges: [string, string][] }; subgraphNodeIds: string[] }`, dims non-included nodes.
- [ ] **Step 4: Register all three in `web/mdx-components.tsx`** (extend Task 3's `useMDXComponents` return object) so Day 2's step pages can embed them directly via MDX component syntax once a page author chooses to (this is opt-in enhancement on top of the plain mermaid fences that already render via `GraphDiagram` — no `docs/` page is required to be rewritten to use these).
- [ ] **Step 5: Typecheck and commit**

```bash
cd web && npm run typecheck && cd ..
git add web/components/TwoGraphsSplit.tsx web/components/LifecycleDiagram.tsx web/components/SubgraphViewer.tsx web/mdx-components.tsx
git commit -m "Add interactive diagram components: TwoGraphsSplit, LifecycleDiagram, SubgraphViewer"
```

---

## Task 8: Pattern browser

**Files:**
- Create: `web/app/patterns/page.tsx`
- Create: `web/app/patterns/[slug]/page.tsx`
- Create: `web/components/PatternBrowser.tsx`
- Create: `web/components/StarterViewer.tsx`

**Interfaces:**
- Consumes: `getAllPatterns()`, `getPatternBySlug()` (Task 2).

- [ ] **Step 1: Write `web/components/PatternBrowser.tsx`** — props `{ patterns: PatternMeta[] }` (client component), filter controls for category (A–G), stage (write/read/governance/storage), and tool (core/extended), rendering a grid of pattern cards linking to `/patterns/[slug]`.
- [ ] **Step 2: Write `web/components/StarterViewer.tsx`** — props `{ slug: string; kitFiles: { path: string; content: string }[] }`, a file-tree-plus-content-pane viewer for a kit's actual files, with a Claude Code / OpenCode tool switcher for core kits (reusing `CodeTabs`, Task 3, where the kit has both).
- [ ] **Step 3: Write `web/app/patterns/page.tsx`** — calls `getAllPatterns()`, renders `<PatternBrowser patterns={...} />`.
- [ ] **Step 4: Write `web/app/patterns/[slug]/page.tsx`** — calls `getPatternBySlug(params.slug)`, renders the spec plus `<StarterViewer />` with that kit's files read directly from `starters/<slug>/`.
- [ ] **Step 5: Typecheck, build, and commit**

```bash
cd web && npm run typecheck && npm run build && cd ..
git add web/app/patterns web/components/PatternBrowser.tsx web/components/StarterViewer.tsx
git commit -m "Add pattern browser and starter viewer"
```

---

## Task 9: Quiz and flashcards

**Files:**
- Create: `web/app/quiz/[part]/page.tsx`
- Create: `web/app/flashcards/[part]/page.tsx`
- Create: `web/components/Quiz.tsx`
- Create: `web/components/Flashcards.tsx`

**Interfaces:**
- Consumes: `getDocBySlug(["0N-part-...", "quiz"])` / `["...", "flashcards"])` (Task 2) — parses each `quiz.md`/`flashcards.md`'s question/answer or term/definition pairs from a fixed Markdown structure (each Day 2 quiz/flashcards file uses a consistent `### Q: ...` / `**A:** ...` and `**Term:**` / `**Definition:**` pattern — Task 2's Day-2-authored files must follow this exact structure for Task 9's parser to work; note this as a cross-day interface contract to confirm at the Day 4 approval gate if Day 2's files used a different structure).

- [ ] **Step 1: Write `web/components/Quiz.tsx`** — props `{ questions: { question: string; answer: string }[] }`, client component, one-at-a-time question flow with reveal, score tally at the end.
- [ ] **Step 2: Write `web/components/Flashcards.tsx`** — props `{ cards: { term: string; definition: string }[] }`, client component, flip-card UI, shuffle button.
- [ ] **Step 3: Write `web/app/quiz/[part]/page.tsx`** and **`web/app/flashcards/[part]/page.tsx`** — each parses its part's `quiz.md`/`flashcards.md` into the props shape above and renders the corresponding component.
- [ ] **Step 4: Typecheck, build, and commit**

```bash
cd web && npm run typecheck && npm run build && cd ..
git add web/app/quiz web/app/flashcards web/components/Quiz.tsx web/components/Flashcards.tsx
git commit -m "Add quiz and flashcards pages"
```

---

## Task 10: Projects and resources pages

**Files:**
- Create: `web/app/projects/page.tsx`
- Create: `web/app/resources/page.tsx`
- Create: `web/components/ProjectCard.tsx`
- Create: `web/components/AntiPatternCard.tsx`

**Interfaces:**
- Consumes: `getDocBySlug(["projects", "README"])` and per-project files (Task 2); `getDocBySlug(["operating", "anti-patterns"])` for `AntiPatternCard`'s data.

- [ ] **Step 1: Write `web/components/ProjectCard.tsx`** — props `{ title: string; difficulty: string; time: string; slug: string[] }`.
- [ ] **Step 2: Write `web/components/AntiPatternCard.tsx`** — props `{ category: "design" | "governance" | "judgment"; text: string }`.
- [ ] **Step 3: Write `web/app/projects/page.tsx`** — grid of `<ProjectCard>`s from the 8 projects.
- [ ] **Step 4: Write `web/app/resources/page.tsx`** — renders `resources/sources.md` (all ten sources) plus a compact anti-patterns section using `AntiPatternCard`.
- [ ] **Step 5: Typecheck, build, and commit**

```bash
cd web && npm run typecheck && npm run build && cd ..
git add web/app/projects web/app/resources web/components/ProjectCard.tsx web/components/AntiPatternCard.tsx
git commit -m "Add projects and resources pages"
```

---

## Task 11: Certification page

**Files:**
- Create: `web/app/certification/page.tsx`
- Create: `web/components/GraphReadyChecklist.tsx`
- Create: `web/components/CertificateGenerator.tsx`

**Interfaces:**
- Consumes: `getDocBySlug(["assessments", "graph-ready-certification"])` (Task 2) for the seven-item checklist text.

- [ ] **Step 1: Write `web/components/GraphReadyChecklist.tsx`** — client component, seven checkboxes (schema before extraction · reversible resolution · every edge has provenance · a subgraph budget is set · a grounded checker exists · at least one anchor · at least one frozen node — the exact seven from §19), local `useState`, all-seven-checked unlocks `CertificateGenerator`.
- [ ] **Step 2: Write `web/components/CertificateGenerator.tsx`** — props `{ unlocked: boolean; learnerName?: string }`, renders a downloadable (client-side canvas or SVG-to-PNG, no server/database — no learner accounts exist in this v1 scope) certificate once unlocked; takes a plain text-input name field, no auth.
- [ ] **Step 3: Write `web/app/certification/page.tsx`** — composes both.
- [ ] **Step 4: Typecheck, build, and commit**

```bash
cd web && npm run typecheck && npm run build && cd ..
git add web/app/certification web/components/GraphReadyChecklist.tsx web/components/CertificateGenerator.tsx
git commit -m "Add certification page: Graph Ready checklist and certificate generator"
```

---

## Task 12: Responsive, accessibility, and light/dark polish pass

**Files:** Modify: various files across `web/components/` and `web/app/` as issues are found (no new files expected).

- [ ] **Step 1: Manual responsive check** — resize to a mobile viewport (375px) and a tablet viewport (768px) for the landing page, a doc page, the pattern browser, and the certification page; fix any overflow (the Sidebar in particular needs a collapsed/hamburger state below 768px — add that to `web/components/Sidebar.tsx` now if it's missing).
- [ ] **Step 2: Basic accessibility pass** — every interactive element (`ThemeToggle`, `Quiz`, `Flashcards`, `PatternBrowser` filters, `GraphReadyChecklist` checkboxes) has a visible focus state and an `aria-label` or associated `<label>`; run the browser's built-in accessibility audit (e.g. Chrome DevTools Lighthouse accessibility category) against the landing page and one doc page, fix anything scoring below "no critical issues."
- [ ] **Step 3: Light/dark pass** — visually check every page in both themes (toggle via `ThemeToggle`); confirm `GraphDiagram`'s rendered mermaid SVGs are legible in dark mode (mermaid's default theme may need a dark-mode override passed to `mermaid.initialize()` in `GraphDiagram.tsx`).
- [ ] **Step 4: OG images** — add a single shared Open Graph image (`web/public/og-image.png`, a static original graphic — not AI-generated placeholder text — sized 1200×630) and reference it in `web/app/layout.tsx`'s `metadata.openGraph`.
- [ ] **Step 5: Commit**

```bash
git add web
git commit -m "Responsive, accessibility, and light/dark polish pass"
```

---

## Task 13: `web-build` CI verification

**Files:** Modify `.github/workflows/web-build.yml` (remove the Day 1 existence guard, since `web/package.json` now exists).

- [ ] **Step 1: Remove the guard** added in Day 1 Task 3, so the workflow runs `npm ci && npm run build && npm run typecheck` unconditionally.
- [ ] **Step 2: Run the full build locally one more time to confirm it's green**

```bash
cd web && npm ci && npm run build && npm run typecheck && cd ..
```
- [ ] **Step 3: Commit**

```bash
git add .github/workflows/web-build.yml
git commit -m "Un-guard web-build workflow now that web/ exists"
```

---

## Task 14: Deploy — BLOCKED, needs two user decisions

**This task cannot start without the user answering:**

1. **Where to deploy.** graph-plan.md §26 names Vercel or GitHub Pages as options. Vercel suits this Next.js App Router site (including the dynamic bits like `CertificateGenerator`) better than GitHub Pages, which needs a static export and would require reworking any server-rendered routes — but it needs a Vercel account. GitHub Pages needs a static export (`next export`-style config) and would need revisiting Task 8/9's dynamic routes for static compatibility. **Ask the user which one, or whether to skip deployment entirely for now and just ship the build-passes-locally state.**
2. **Whether a GitHub remote exists yet.** Both deploy targets are far easier with a real GitHub remote (Vercel's Git integration; GitHub Pages requires GitHub itself). Day 1's decision was "local only for now" — **check whether that has changed before Day 4 starts.**

**Do not create any hosting account, deploy token, or remote repository without explicit user confirmation at this point** — this is exactly the kind of hard-to-reverse, externally-visible action that needs a direct go-ahead, not an inference from earlier context.

- [ ] **Step 1 (once unblocked): follow whichever path the user chose** — this plan does not pre-specify deploy steps further, since the two branches (Vercel vs. GitHub Pages vs. skip) lead to materially different task lists that shouldn't be drafted until the decision is made.

---

## Task 15: Day 4 verification & close-out

**Files:** Modify `STATE.md`, `loop-run-log.md`.

- [ ] **Step 1: Run the full Definition of Done check for both deliverables** (graph-plan.md §29): re-run all four Deliverable-1 CI gates (`originality-check`, `link-check`, `validate-registry`, `graph-ready-audit`) plus `web`'s `build`/`typecheck`, and manually confirm every item in §29's "Both" section (content lives once in `docs/`, all ten sources attributed, every step page has all required elements, the Graph Ready checklist works end to end).
- [ ] **Step 2: Update `STATE.md`** — mark the Day 4 row `done` (or `blocked on deploy decision` if Task 14 is still open).
- [ ] **Step 3: Append to `loop-run-log.md`**

```markdown
## <date> — Day 4 complete (pending deploy decision)

web/ built: all pages and components render, web-build CI gate green,
responsive/accessibility/dark-mode pass done. Deploy (Task 14) blocked
on user decision: hosting target (Vercel/GitHub Pages/skip) and whether
a GitHub remote now exists. Both deliverables otherwise meet the §29
definition of done.
```

- [ ] **Step 4: Commit**

```bash
git add STATE.md loop-run-log.md
git commit -m "Day 4 complete pending deploy decision: both deliverables meet DoD locally"
```

- [ ] **Step 5: STOP Day 4's loop permanently and report to the user**, explicitly surfacing Task 14's open decision rather than assuming an answer. Per the "separate loop per day" execution mode: this is the fourth and final loop — it ends here, and there is no Day 5 loop for it to hand off to.

---

## Day 4 Approval Gate

**This is the final gate.** Before calling the project done, the user must resolve Task 14 (deploy target + remote status) and confirm Task 9's cross-day interface assumption (that Day 2's `quiz.md`/`flashcards.md` files used the exact Markdown structure `Quiz.tsx`/`Flashcards.tsx` expect — verify this in practice once Day 2 content actually exists, since Day 2 was planned before Day 4's parser shape was fixed).
