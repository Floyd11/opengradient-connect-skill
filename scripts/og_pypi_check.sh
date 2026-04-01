#!/usr/bin/env env bash
# og_pypi_check.sh — Fetch the latest opengradient version from PyPI.
# Usage: bash .agent/skills/05-opengradient-connect/scripts/og_pypi_check.sh
#
# Outputs a single line: "latest=X.Y.Z" for easy parsing.
# Requires: curl or python3 (fallback).

set -euo pipefail

PACKAGE="opengradient"

# Try curl + PyPI JSON API first (no pip needed)
if command -v curl &>/dev/null; then
    LATEST=$(curl -sf "https://pypi.org/pypi/${PACKAGE}/json" \
        | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])" 2>/dev/null || echo "")
fi

# Fallback: pip index versions
if [[ -z "${LATEST:-}" ]]; then
    LATEST=$(python3 -m pip index versions "${PACKAGE}" 2>/dev/null \
        | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown")
fi

echo "latest=${LATEST}"

# Also show installed version for comparison
INSTALLED=$(python3 -m pip show "${PACKAGE}" 2>/dev/null \
    | grep "^Version:" | awk '{print $2}' || echo "not-installed")

echo "installed=${INSTALLED}"

if [[ "${LATEST}" != "${INSTALLED}" && "${INSTALLED}" != "not-installed" ]]; then
    echo "update_needed=true"
    echo "hint: Run 'pip install --upgrade ${PACKAGE}' to update."
else
    echo "update_needed=false"
fi
