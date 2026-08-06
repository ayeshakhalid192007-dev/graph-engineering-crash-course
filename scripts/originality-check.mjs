#!/usr/bin/env node
// Enforces graph-plan.md §2.1 rule 2: no run of 8+ consecutive words of prose
// in any docs/ page may match an 8+ word run in a cached source text.
// Fenced blocks, inline code, and link targets are excluded — see the strip
// helpers below for why.

import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, extname } from "node:path";

const DOCS_DIR = "docs";
const CACHE_DIR = ".originality-cache";
const MIN_RUN = 8;
const ALLOWED_QUOTE_MARKER = "<!-- attributed-quote:steinberger -->";

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    const s = statSync(p);
    if (s.isDirectory()) out.push(...walk(p));
    else if (extname(p) === ".md") out.push(p);
  }
  return out;
}

function tokenize(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean);
}

// A word run may not span a BREAK: the words on either side of a removed code
// sample were never consecutive prose, so counting them as a run would report
// a sentence no page ever wrote.
function ngrams(tokens, n) {
  const set = new Set();
  for (const segment of splitOnBreaks(tokens)) {
    for (let i = 0; i + n <= segment.length; i++) set.add(segment.slice(i, i + n).join(" "));
  }
  return set;
}

function splitOnBreaks(tokens) {
  const segments = [[]];
  for (const t of tokens) {
    if (t === BREAK_TOKEN) segments.push([]);
    else segments[segments.length - 1].push(t);
  }
  return segments;
}

// §2.1 rule 2 governs prose. Code, config, schema samples, and file paths are
// data: two pages that legitimately show the same JSON record or link to the
// same document are not duplicating anyone's writing, so they're removed
// before the word-run scan rather than reported as violations.
// Each removal leaves BREAK behind rather than closing the gap, so words that
// merely sat on either side of a code sample don't become neighbours and
// invent a word run that no page actually contains.
const BREAK_TOKEN = "xstrippedx";
const BREAK = ` ${BREAK_TOKEN} `;

function stripFencedBlocks(text) {
  const kept = [];
  let inFence = false;
  for (const line of text.split("\n")) {
    if (/^\s*(```|~~~)/.test(line)) {
      if (inFence) kept.push(BREAK);
      inFence = !inFence;
      continue;
    }
    if (!inFence) kept.push(line);
  }
  return kept.join("\n");
}

function stripCodeSpans(text) {
  return text.replace(/`[^`\n]*`/g, BREAK);
}

// Drops the URL half of [text](target), and bare autolinks, keeping the
// human-readable link text, which is prose and stays subject to the check.
// The autolink pattern requires a `/` or `:` so that inline HTML such as
// <details> is left alone — removing a tag would splice the sentences on
// either side of it together.
function stripLinkTargets(text) {
  return text
    .replace(/\]\([^)\s]*(?:\s+"[^"]*")?\)/g, "]" + BREAK)
    .replace(/<[^>\s]*[/:][^>\s]*>/g, BREAK);
}

function stripAttributedQuoteBlocks(text) {
  const lines = text.split("\n");
  const kept = [];
  let skipping = false;
  for (const line of lines) {
    if (line.includes(ALLOWED_QUOTE_MARKER)) { skipping = true; continue; }
    if (skipping && line.trim() === "") { skipping = false; continue; }
    if (!skipping) kept.push(line);
  }
  return kept.join("\n");
}

function main() {
  if (!existsSync(DOCS_DIR)) {
    console.error(`originality-check: ${DOCS_DIR}/ not found`);
    process.exit(1);
  }

  const docFiles = walk(DOCS_DIR);
  let sourceNgrams = null;

  if (existsSync(CACHE_DIR)) {
    sourceNgrams = new Set();
    for (const f of walk(CACHE_DIR)) {
      for (const g of ngrams(tokenize(readFileSync(f, "utf8")), MIN_RUN)) sourceNgrams.add(g);
    }
  } else {
    console.warn(
      `originality-check: ${CACHE_DIR}/ not present — skipping cross-source check, ` +
      `running self-duplication check only. See scripts/README.md.`
    );
  }

  let violations = 0;
  const seenBySelf = new Map();

  for (const file of docFiles) {
    const raw = stripAttributedQuoteBlocks(readFileSync(file, "utf8"));
    const cleaned = stripLinkTargets(stripCodeSpans(stripFencedBlocks(raw)));
    const grams = ngrams(tokenize(cleaned), MIN_RUN);

    for (const g of grams) {
      if (sourceNgrams && sourceNgrams.has(g)) {
        console.error(`originality violation in ${file}: matches cached source text: "${g}"`);
        violations++;
      }
      if (seenBySelf.has(g) && seenBySelf.get(g) !== file) {
        console.error(`self-duplication in ${file}: matches ${seenBySelf.get(g)}: "${g}"`);
        violations++;
      } else if (!seenBySelf.has(g)) {
        seenBySelf.set(g, file);
      }
    }
  }

  if (violations > 0) {
    console.error(`\noriginality-check: ${violations} violation(s) found.`);
    process.exit(1);
  }
  console.log(`originality-check: ${docFiles.length} files checked, 0 violations.`);
}

main();
