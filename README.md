# 🔗 opengradient-connect

> **An AI Agent Skill that makes integrating the OpenGradient SDK safe, fast, and always up-to-date.**

![Version](https://img.shields.io/badge/version-1.0.2-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Network](https://img.shields.io/badge/network-Base%20Sepolia-orange)
![SDK](https://img.shields.io/badge/og--sdk-0.9.9%20tested-purple)
![Status](https://img.shields.io/badge/mainnet-not%20yet%20launched-red)

---

## What is this?

`opengradient-connect` is a **modular AI Agent Skill** that turns any AI coding agent into a senior OpenGradient integration engineer. Instead of hallucinating API calls or generating outdated boilerplate, the agent follows a strict **Safety-First & Fetch** protocol:

1. 🩺 **Diagnose first** — audits your project before writing a single line of code.
2. 📥 **Fetch, don't invent** — pulls live, verified templates from the [official Cookbook](https://github.com/Floyd11/OpenGradient-Developer-Cookbook).
3. 🔒 **Enforce Golden Rules** — ensures `Permit2` approval and TEE proof extraction are present every time.
4. 🛡️ **Guard the network** — prevents accidental Mainnet deployments before you're ready.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Hybrid Architecture** | The skill acts as a rule engine and fetches live code from the Cookbook. No stale boilerplate. |
| **Environment Diagnostics** | Dual-mode audit: manual file analysis + automated `og_diagnostics.py` JSON report. |
| **TEE Proof Enforcement** | Every inference call is checked for `payment_hash` — the cryptographic proof of TEE execution. |
| **Permit2 Golden Rule** | `ensure_opg_approval()` is enforced at startup — the most common integration bug, automatically caught. |
| **Network Context Guard** | The agent always asks Testnet or Mainnet? before generating constants or config. |
| **Mainnet Migration Checklist** | An interactive 8-step safety protocol for moving from Sepolia to Mainnet — requires manual confirmation at each step. |
| **PyPI Freshness Check** | Compares installed SDK version with latest on PyPI and warns if stale. |
| **Troubleshooting Database** | Top 10 TEE / Gateway / x402 Gateway Gateway errors with exact diagnostic commands and fixes. |

---

## 🏗️ Architecture

### The Hybrid Model

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Agent (You)                           │
│                                                                 │
│   User: "Help me build a verifiable FastAPI backend with OG"   │
└────────────────────────────┬────────────────────────────────────┘
                             │  triggers skill
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  opengradient-connect (SKILL.md)                 │
│                                                                 │
│  Step 0: Network Context Guard ──► Testnet or Mainnet?          │
│  Step 1: Environment Diagnostics ─► Read .env + run og_diag.py │
│  Step 2: Template Fetching ───────► GET from Cookbook GitHub    │
│  Step 3: Golden Rules Check ──────► Permit2 + payment_hash      │
│  Step 4: Network Guard ───────────► Warn if Mainnet             │
│  Step 5: Hybrid Updater ──────────► Check PyPI freshness        │
└────────────────────────────┬────────────────────────────────────┘
                             │  fetches live code
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│         OpenGradient Developer Cookbook (GitHub)                │
│                                                                 │
│  snippets/01_llm_completion_basic.py                            │
│  snippets/02_llm_chat_with_tools.py                             │
│  snippets/11_langchain_agent.py                                 │
│  boilerplates/fastapi-verifiable-backend/main.py                │
└─────────────────────────────────────────────────────────────────┘
```

### File Structure

```
opengradient-connect-skill/
│
├── SKILL.md                          # 🧠 Core agent instructions & trigger conditions
│
├── scripts/
│   ├── og_diagnostics.py             # 🩺 Full environment auditor (JSON output)
│   └── og_pypi_check.sh              # 📦 Quick SDK version checker (PyPI vs installed)
│
└── references/
    ├── troubleshooting.md            # 🔧 Top-10 TEE/Gateway error database
    └── mainnet_checklist.md          # 🚀 Interactive 8-step Mainnet migration protocol
```

---

## 📦 Installation

### Option 1 — Antigravity / Generic CLI (Recommended)

Drop the skill folder directly into your agent's skills directory:

```bash
# Clone the repository
git clone https://github.com/Floyd11/opengradient-connect-skill.git

# Copy into your agent's skills folder
cp -r opengradient-connect-skill/ /path/to/your/project/.agent/skills/05-opengradient-connect/
```

Your agent will auto-discover `SKILL.md` at startup due to the keywords in its `description` field.

**Expected directory after setup:**
```
your-project/
└── .agent/
    └── skills/
        └── 05-opengradient-connect/
            ├── SKILL.md
            ├── scripts/
            └── references/
```

---

### Option 2 — Claude Code (`claude` CLI)

Claude Code supports loading custom skill context via its `--add-dir` flag or by pointing to the skill folder in your project.

```bash
# Install claude CLI (if not yet installed)
npm install -g @anthropic-ai/claude-code

# Start a session with the skill in context
claude --add-dir .agent/skills/05-opengradient-connect/

# Or, add it permanently to your project's allowed paths
# in .claude/settings.json:
```

```json
{
  "allowedDirectories": [
    ".",
    ".agent/skills/05-opengradient-connect"
  ]
}
```

> The agent will load `SKILL.md` when it detects OpenGradient-related keywords in your request.

---

### Option 3 — Cursor / Windsurf / Codex

These editors support injecting context via `.cursorrules` or a system prompt file.

**Step 1:** Create or append to `.cursorrules` at your project root:

```
# OpenGradient SDK Integration Rules
# Auto-loaded from: .agent/skills/05-opengradient-connect/SKILL.md

@.agent/skills/05-opengradient-connect/SKILL.md
```

**Step 2:** Windsurf users — add to `.windsurfrules`:

```
@.agent/skills/05-opengradient-connect/SKILL.md
```

**Step 3 (Optional):** For Cursor's AI Pane, manually paste the contents of `SKILL.md` into the **System Prompt** section under `Cursor Settings → AI → Rules for AI`.

> **Tip for Cursor / Windsurf:** The `og_diagnostics.py` script always exits with code `0` regardless of findings, so it won't break your agent's tool-calling chain. The agent reads the JSON output and decides what to do.

---

### Option 4 — Manus / SkillsMP (Hypothetical Package Manager)

If your agent platform supports a skills package manager:

```bash
# Install via skills CLI (if supported by your platform)
skills add opengradient-connect

# Or install from GitHub directly
skills install github:Floyd11/opengradient-connect-skill
```

---

## 💬 Usage — What to Say to Your Agent

Once installed, trigger the skill naturally. Here are example prompts:

### 🚀 Basic Integration
```
"Integrate OpenGradient into my project. Check my environment first."
```

### ⚡ FastAPI Verifiable Backend
```
"Help me deploy a verifiable FastAPI backend using OpenGradient with TEE inference on Base Sepolia."
```

### 🤖 LangGraph Agent with On-Chain Proofs
```
"Build a LangGraph agent that uses OpenGradient for verifiable LLM calls and logs the TEE proof to my database."
```

### 🔗 LangChain Drop-in Replacement
```
"Replace my existing ChatOpenAI usage with OpenGradient's TEE-verified LLM. Use LangChain integration."
```

### 🩺 Environment Health Check
```
"Run a full OpenGradient environment diagnostic on my project and tell me what's missing."
```

### 🔒 Mainnet Migration
```
"I'm ready to migrate my OpenGradient integration to Mainnet. Guide me through the checklist."
```

---

## 🔑 Environment Variables

The skill will check for the following in your `.env`:

| Variable | Required | Description |
|----------|----------|-------------|
| `OG_PRIVATE_KEY` | ✅ Yes | Your Ethereum-compatible wallet private key (hex, 64 chars, optionally `0x`-prefixed). Used to authenticate with the x402 Gateway. |

**Example `.env`:**
```bash
# OpenGradient SDK Configuration
OG_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
```

> ⚠️ **Security:** Always add `.env` to `.gitignore`. Never commit your private key.

---

## 🌐 Network Reference

| Network | Chain ID | RPC URL | Status |
|---------|----------|---------|--------|
| **Base Sepolia (Testnet)** | `84532` | `https://sepolia.base.org` | ✅ Active |
| **OpenGradient Mainnet** | TBD | TBD | 🔜 Coming Soon |

To get testnet `$OPG` tokens: join the [OpenGradient Discord](https://discord.gg/opengradient) or use the [OpenGradient Faucet](https://faucet.opengradient.ai/).

---

## 🛡️ The Two Golden Rules

Every piece of code this skill generates or reviews enforces these two rules *without exception*:

### Rule 1 — Permit2 Pre-Approval
```python
# Called ONCE at application startup — never inside a loop.
# Grants the x402 Gateway permission to spend $OPG on behalf of the user.
llm.ensure_opg_approval(min_allowance=5.0)
```
**If missing → flagged as a critical bug.**

### Rule 2 — TEE Proof Extraction
```python
result = llm.chat(messages=[{"role": "user", "content": "your prompt"}])

# Every inference call must surface the cryptographic proof of TEE execution.
payment_hash = result.payment_hash
print(f"[TEE PROOF] {payment_hash}")  # verifiable on-chain
```
**If `payment_hash` is `None` → treated as a silent data-loss failure.**

---

## 🩺 Diagnostic Script

Run the bundled auditor from your project root to get a full JSON health report:

```bash
python .agent/skills/05-opengradient-connect/scripts/og_diagnostics.py
```

**Example output:**
```json
{
  "project_root": "/your/project",
  "package_manager": "pip",
  "sdk": {
    "installed": true,
    "installed_version": "0.9.9",
    "latest_pypi_version": "0.9.9",
    "update_needed": false
  },
  "env_vars": {
    "env_file_exists": true,
    "vars": { "OG_PRIVATE_KEY": true },
    "all_present": true
  },
  "network_config": {
    "detected_chain_id": null,
    "is_testnet": null
  },
  "detected_integrations": ["langchain", "langgraph", "fastapi"],
  "ready_to_integrate": true
}
```

---

## 📋 Mainnet Migration

When you're ready to go live, the skill will guide you through an **8-step interactive checklist** (`references/mainnet_checklist.md`):

1. ✅ Confirm Mainnet is officially launched
2. 💾 Backup your Testnet `.env`
3. 💰 Validate Mainnet wallet and `$OPG` balance (min. 10 OPG)
4. ✏️ Update `.env` manually (agent never auto-writes keys)
5. 🩺 Re-run diagnostics on Mainnet config
6. 🤝 Permit2 re-approval on Mainnet (irreversible — requires explicit YES)
7. 🔬 Smoke test with minimal inference + TEE proof verification
8. 🔍 Grep codebase for hardcoded Testnet constants

> ⚠️ Every step requires explicit user confirmation. The agent will **HALT** if any validation fails.

---

## 📚 Template Recipes (Fetched Live from Cookbook)

The skill never generates boilerplate from memory. It fetches from:

| Recipe | Description | Source |
|--------|-------------|--------|
| **Basic LLM Completion** | Simple TEE chat inference | [`01_llm_completion_basic.py`](https://github.com/Floyd11/OpenGradient-Developer-Cookbook/blob/main/snippets/01_llm_completion_basic.py) |
| **Tool Calling Agent** | Multi-turn chat with function calling | [`02_llm_chat_with_tools.py`](https://github.com/Floyd11/OpenGradient-Developer-Cookbook/blob/main/snippets/02_llm_chat_with_tools.py) |
| **LangChain Integration** | Drop-in for `ChatOpenAI` | [`11_langchain_agent.py`](https://github.com/Floyd11/OpenGradient-Developer-Cookbook/blob/main/snippets/11_langchain_agent.py) |
| **FastAPI Backend** | Async REST endpoint with TEE verification | [`fastapi-verifiable-backend/main.py`](https://github.com/Floyd11/OpenGradient-Developer-Cookbook/blob/main/boilerplates/fastapi-verifiable-backend/main.py) |

---

## 🔧 Troubleshooting

Quick reference for the most common errors. The full database is in [`references/troubleshooting.md`](references/troubleshooting.md).

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| `InsufficientFundsError` | No `$OPG` on Sepolia | Get tokens from Discord faucet |
| `GatewayTimeoutError` | x402 Gateway overloaded | Add retry with exponential backoff |
| `payment_hash` is `None` | Not using a TEE model | Use `og.TEE_LLM` enum, not string names |
| `PermissionError` on inference | Permit2 not approved | Call `ensure_opg_approval()` at startup |
| `ModuleNotFoundError` | SDK not installed | `pip install opengradient` |
| `InvalidPrivateKeyError` | Malformed `OG_PRIVATE_KEY` | Must be 64-char hex, optionally `0x`-prefixed |

---

## 📖 Resources

- 📘 [OpenGradient Documentation](https://docs.opengradient.ai)
- 🍳 [Developer Cookbook](https://github.com/Floyd11/OpenGradient-Developer-Cookbook)
- 💬 [OpenGradient Discord](https://discord.gg/opengradient)
- 🔗 [OpenGradient Faucet](https://faucet.opengradient.ai/)
- 📦 [opengradient on PyPI](https://pypi.org/project/opengradient/)

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built for the <strong>OpenGradient</strong> ecosystem · Safety-First · Verifiable AI
</p>
