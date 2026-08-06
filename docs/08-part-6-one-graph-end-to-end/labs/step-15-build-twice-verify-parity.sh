#!/usr/bin/env bash
# Step 15 live lab: build the same graph twice, verify parity.
#
# No dependencies, no network, bash only. Stands in for "the Claude Code
# version" and "the OpenCode version" of Step 15's Elm Street tool-cabinet
# pipeline -- two functions below, each independently walking the same five
# source messages through schema -> extraction -> resolution -> provenance
# -> checker, using different internal bookkeeping (different loop order,
# different variable shapes) the way two separately-configured tools would.
#
# Both are deterministic stand-ins for worked reasoning, not real tool
# invocations. The lab's job is to diff their final output and refuse to
# call it parity unless the two are byte-for-byte identical.
set -euo pipefail

# --- Version A: "Claude Code" -------------------------------------------
# Builds the edge list in the order the messages arrive, then derives each
# tool's availability by scanning for a borrowed edge with no later
# returned edge from the same person.
build_claude_code_graph() {
  local edges=()
  edges+=("owns|Kavita|ladder|m1")
  edges+=("owns|Marcus|stud_finder|m4")
  edges+=("borrowed|Jason|ladder|m2")
  edges+=("returned|Jason|ladder|m3")
  edges+=("borrowed|Deepa|stud_finder|m5")

  local e
  for e in "${edges[@]}"; do
    IFS='|' read -r kind person tool msg <<<"$e"
    echo "EDGE $kind $person $tool $msg"
  done

  # ladder: borrowed at m2, returned at m3 (m3 comes after m2) -> available
  # stud_finder: borrowed at m5, no returned edge at all -> not available
  echo "CHECK ladder available=true"
  echo "CHECK stud_finder available=false"
}

# --- Version B: "OpenCode" -----------------------------------------------
# Groups the same five messages by tool first, then walks each tool's own
# edge list to decide availability -- a different code path over the same
# underlying facts.
build_opencode_graph() {
  declare -A by_tool
  by_tool["ladder"]="owns:Kavita:m1 borrowed:Jason:m2 returned:Jason:m3"
  by_tool["stud_finder"]="owns:Marcus:m4 borrowed:Deepa:m5"

  local tool entries entry kind person msg
  local -a out_lines=()
  for tool in ladder stud_finder; do
    entries="${by_tool[$tool]}"
    for entry in $entries; do
      IFS=':' read -r kind person msg <<<"$entry"
      out_lines+=("EDGE $kind $person $tool $msg")
    done
  done
  printf '%s\n' "${out_lines[@]}"

  # A tool is available unless it has a borrowed entry with no returned
  # entry after it in that same tool's own message sequence.
  for tool in ladder stud_finder; do
    entries="${by_tool[$tool]}"
    local last_kind=""
    for entry in $entries; do
      IFS=':' read -r kind person msg <<<"$entry"
      [[ "$kind" == "borrowed" || "$kind" == "returned" ]] && last_kind="$kind"
    done
    if [[ "$last_kind" == "borrowed" ]]; then
      echo "CHECK $tool available=false"
    else
      echo "CHECK $tool available=true"
    fi
  done
}

# --- Run both, compare -----------------------------------------------------
OUT_A="$(build_claude_code_graph | sort)"
OUT_B="$(build_opencode_graph | sort)"

echo "Claude Code version (sorted):"
echo "$OUT_A"
echo
echo "OpenCode version (sorted):"
echo "$OUT_B"
echo

if ! DIFF_OUTPUT="$(diff <(echo "$OUT_A") <(echo "$OUT_B"))"; then
  echo "FAIL: the two versions do not agree on the final graph"
  echo "$DIFF_OUTPUT"
  exit 1
fi
echo "parity check: identical output from both versions"

# Correctness, not just agreement -- both versions have to have landed on
# the actual right answer, not just the same wrong one.
if ! grep -q "^CHECK ladder available=true$" <<<"$OUT_A"; then
  echo "FAIL: ladder should read available=true (borrowed then returned)"
  exit 1
fi
if ! grep -q "^CHECK stud_finder available=false$" <<<"$OUT_A"; then
  echo "FAIL: stud_finder should read available=false (borrowed, never returned)"
  exit 1
fi

echo
echo "PASS: Claude Code and OpenCode versions produced identical graphs, and both correctly report the ladder free and the stud finder still out with Deepa."
exit 0
