#!/usr/bin/env python3
"""
og_diagnostics.py — OpenGradient SDK Environment Auditor
Outputs a JSON report for the opengradient-connect skill agent.
Run from any project root: python .agent/skills/05-opengradient-connect/scripts/og_diagnostics.py
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKILL_SDK_VERSION = "0.9.9"  # version this skill was last verified against
TESTNET_CHAIN_ID = "84532"


def _run(cmd: list[str]) -> str:
    """Run a safe, read-only subprocess and return stdout. Never raises."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip()
    except Exception:
        return ""


def check_sdk_installed() -> dict:
    """Detect installed opengradient version from the active Python env."""
    output = _run([sys.executable, "-m", "pip", "show", "opengradient"])
    version = None
    for line in output.splitlines():
        if line.startswith("Version:"):
            version = line.split(":", 1)[1].strip()
    return {"installed": version is not None, "installed_version": version}


def check_latest_pypi() -> str | None:
    """Fetch latest opengradient version from PyPI."""
    output = _run(
        [sys.executable, "-m", "pip", "index", "versions", "opengradient"]
    )
    # Output format: "opengradient (X.Y.Z)"  or  "Available versions: X.Y.Z, ..."
    match = re.search(r"(\d+\.\d+\.\d+)", output)
    return match.group(1) if match else None


def check_requirements_txt(root: Path) -> dict:
    """Check requirements.txt for opengradient presence."""
    req_file = root / "requirements.txt"
    if not req_file.exists():
        # Try pyproject.toml as fallback
        pyproject = root / "pyproject.toml"
        return {
            "file": str(req_file),
            "exists": False,
            "has_opengradient": pyproject.exists()
            and "opengradient" in pyproject.read_text(),
        }
    content = req_file.read_text()
    match = re.search(r"opengradient[>=<~!]*\s*([\d.]+)?", content)
    return {
        "file": str(req_file),
        "exists": True,
        "has_opengradient": match is not None,
        "pinned_version": match.group(1) if (match and match.group(1)) else None,
    }


def check_env_vars(root: Path) -> dict:
    """Check .env file for required OpenGradient variables."""
    required = ["OG_PRIVATE_KEY", "OPENGRADIENT_PRIVATE_KEY"]
    env_file = root / ".env"
    found: dict[str, bool] = {k: False for k in required}

    # Also check actual process environment (already exported vars)
    for key in required:
        if os.environ.get(key):
            found[key] = True

    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k = line.split("=", 1)[0].strip()
            if k in found:
                found[k] = True

    # Consider it present if EITHER name is found
    all_present = found["OG_PRIVATE_KEY"] or found["OPENGRADIENT_PRIVATE_KEY"]

    return {
        "env_file_exists": env_file.exists(),
        "vars": found,
        "all_present": all_present,
    }


def check_network_config(root: Path) -> dict:
    """Scan .env and config files for CHAIN_ID / RPC settings."""
    files_to_check = [".env", "config.py", "settings.py", "config.yaml"]
    chain_id = None
    rpc = None

    for fname in files_to_check:
        fpath = root / fname
        if not fpath.exists():
            continue
        content = fpath.read_text()
        m_chain = re.search(r"CHAIN_ID[^\d]*(\d+)", content)
        m_rpc = re.search(r"RPC[_URL]*\s*=\s*['\"]([^'\"]+)['\"]", content, re.IGNORECASE)
        if m_chain and not chain_id:
            chain_id = m_chain.group(1)
        if m_rpc and not rpc:
            rpc = m_rpc.group(1)

    is_testnet = chain_id == TESTNET_CHAIN_ID if chain_id else None
    return {
        "detected_chain_id": chain_id,
        "detected_rpc": rpc,
        "is_testnet": is_testnet,
        "warning": (
            "⚠️  CHAIN_ID not set to Base Sepolia (84532). Verify network before proceeding."
            if (chain_id and not is_testnet)
            else None
        ),
    }


def detect_package_manager(root: Path) -> str:
    """Detect active package manager."""
    if (root / "poetry.lock").exists():
        return "poetry"
    if (root / "Pipfile").exists():
        return "pipenv"
    if (root / "conda-meta").exists():
        return "conda"
    return "pip"


def detect_integrations(root: Path) -> list[str]:
    """Detect which OG-adjacent frameworks are already installed."""
    detected = []
    output = _run([sys.executable, "-m", "pip", "list"])
    checks = {
        "langchain": "langchain",
        "langgraph": "langgraph",
        "fastapi": "fastapi",
        "langchain-opengradient": "langchain_opengradient",
    }
    for label, pkg in checks.items():
        if pkg.lower() in output.lower():
            detected.append(label)
    return detected


def main() -> None:
    root = Path.cwd()
    sdk_info = check_sdk_installed()
    latest_pypi = check_latest_pypi()

    report = {
        "project_root": str(root),
        "package_manager": detect_package_manager(root),
        "sdk": {
            **sdk_info,
            "latest_pypi_version": latest_pypi,
            "skill_verified_against": SKILL_SDK_VERSION,
            "update_needed": (
                sdk_info["installed_version"] != latest_pypi
                if (sdk_info["installed_version"] and latest_pypi)
                else None
            ),
        },
        "requirements_txt": check_requirements_txt(root),
        "env_vars": check_env_vars(root),
        "network_config": check_network_config(root),
        "detected_integrations": detect_integrations(root),
        "ready_to_integrate": (
            sdk_info["installed"]
            and check_env_vars(root)["all_present"]
        ),
    }

    print(json.dumps(report, indent=2))

    # NOTE: Always exit 0 so AI agents (Cursor, Windsurf, etc.) read the full JSON
    # output and make their own decisions based on the `ready_to_integrate` field,
    # instead of treating a non-zero exit code as a fatal error.


if __name__ == "__main__":
    main()
