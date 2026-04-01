# OpenGradient Connect Skill

A modular AI Agent skill for integrating the OpenGradient Python SDK (Verifiable AI, TEEs, Web3).

## Overview

This skill is designed for AI agents (like Claude or GPT) to help them properly assist developers in integrating OpenGradient. It focuses on:
- **Safety-First Protocol**: Mandatory pre-flight checks and mainnet migration guardrails.
- **Hybrid Context**: Dynamically fetches the latest verified code templates from the official cookbook.
- **TEE Proofs**: Ensures cryptographic attestations (payment hashes) are always surfaced and logged.
- **Diagnostics**: Includes automated scripts to audit the project environment.

## Structure

```
opengradient-connect-skill/
├── SKILL.md                 # Core instructions and triggers for the agent
├── scripts/
│   ├── og_diagnostics.py    # Python-based environment auditor
│   └── og_pypi_check.sh     # Quick SDK version checker
└── references/
    ├── mainnet_checklist.md # 8-step safety-first migration protocol
    └── troubleshooting.md   # Database of top-10 TEE/Gateway errors
```

## How to use

1. Clone or copy these files into your agent's skill directory (e.g., `.agent/skills/05-opengradient-connect/`).
2. Point your agent to `SKILL.md`.
3. The agent will then follow the "Environment Diagnostics" and "Template Fetching Protocol" described in the instructions.

## License

MIT
