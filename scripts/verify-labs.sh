#!/usr/bin/env bash
# Discovers and runs every live-lab script under docs/**/labs/, per graph-plan.md §21:
# "runnable via a single ./verify.sh that checks every demo still behaves as documented."
set -uo pipefail
fail=0
for script in docs/*/labs/*; do
  [ -f "$script" ] || continue
  case "$script" in
    *.py) runner="python3" ;;
    *.sh) runner="bash" ;;
    *) echo "SKIP (unknown type): $script"; continue ;;
  esac
  echo "--- running $script ---"
  if $runner "$script"; then
    echo "PASS: $script"
  else
    echo "FAIL: $script"
    fail=1
  fi
done
exit $fail
