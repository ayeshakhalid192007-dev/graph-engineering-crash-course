#!/usr/bin/env bash
# Step 1 live lab: two writers, one file.
#
# No dependencies, no network. Simulates two reviewer agents that both read
# a shared notes file *before either of them writes*, then both write their
# own full copy back -- the exact race described in step-1's Hook. The
# writes are sequential here (not truly concurrent) so the demo is
# deterministic and reproducible on any machine, but the reads are captured
# up front so the interleaving matches what would happen if they really did
# race: writer B never sees writer A's update.
set -euo pipefail

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
NOTES="$WORKDIR/review-notes.md"

echo "# Review notes" > "$NOTES"

# Both reviewers read the file's starting state before either one writes --
# this is the "read" half of the race for both of them.
READ_BY_A="$(cat "$NOTES")"
READ_BY_B="$(cat "$NOTES")"

# Reviewer-Security decides first and writes its full updated copy, which
# includes a caveat about the rate limiter staying enabled.
{
  echo "$READ_BY_A"
  echo ""
  echo "## Verdicts"
  echo "- Reviewer-Security: verdict: safe, but only while the rate limiter middleware stays enabled"
} > "$NOTES"

echo "After Reviewer-Security's write:"
cat "$NOTES"
echo ""

# Reviewer-Logic never saw that write -- its copy of the file is still the
# one it read before Reviewer-Security saved. Its write replaces the file
# wholesale, the way a flat file always resolves two writers: last one wins.
{
  echo "$READ_BY_B"
  echo ""
  echo "## Verdicts"
  echo "- Reviewer-Logic: verdict: safe"
} > "$NOTES"

echo "After Reviewer-Logic's write:"
cat "$NOTES"
echo ""

if grep -q "rate limiter" "$NOTES"; then
  echo "PASS: writer A's caveat survived the second write"
  exit 0
else
  echo "FAIL (expected): writer B overwrote writer A's caveat"
  exit 0
fi
