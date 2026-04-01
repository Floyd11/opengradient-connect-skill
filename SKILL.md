---
name: opengradient-connect
description: >
  Use this skill when the user wants to integrate the OpenGradient Python SDK into any project.
  Triggers on keywords: "opengradient", "og SDK", "TEE inference", "verifiable AI", "x402 gateway",
  "OPG tokens", "build verifiable AI", "on-chain AI", "TEE LLM", "llm.ensure_opg_approval",
  "payment_hash", "Base Sepolia". Handles: environment diagnostics (auto + manual), code template
  fetching from the official cookbook, Golden Rules enforcement (Permit2 approval + TEE proof logging),
  Network Context Guard (Testnet vs Mainnet), Mainnet migration interactive checklist, and
  troubleshooting TEE/gateway errors. Always fetches code from the canonical GitHub source.
last_verified_date: "2026-04-01"
og_sdk_version_tested: "0.9.3"
og_sdk_latest_pypi: "0.9.6"
---

# OpenGradient Connect — Agent Instructions

> **Hybrid Model**: This skill does NOT contain static code. You MUST fetch live templates
> from the canonical cookbook repository. Your role is a strict rule engine + smart fetcher.

---

## STEP 0 — NETWORK CONTEXT GUARD (Run First, Always)

Before generating ANY code, configuration, or command, you MUST ask (or infer from context):

> "Are we targeting **Testnet** (Base Sepolia) or **Mainnet**?"

| Network | `CHAIN_ID` | RPC | Status |
|---------|-----------|-----|--------|
| **Testnet** | `84532` | `https://sepolia.base.org` | ✅ Supported |
| **Mainnet** | TBD (EVM-compatible) | TBD | ⚠️ Not yet launched |

**NEVER generate Mainnet code without issuing the warning in Step 4.**
Substitute the correct constants into every template you fetch.

---

## STEP 1 — ENVIRONMENT DIAGNOSTICS (Pre-flight)

NEVER write or adapt code before completing these checks. Run **both modes**.

### 1A — Manual Analysis (fast, always first)
- Read `requirements.txt`: look for `opengradient`. If missing → stop and instruct installation.
- Read `.env`: look for `OG_PRIVATE_KEY`. If missing → block further steps.
- Check `pyproject.toml` or `setup.py` if `requirements.txt` is absent.
- Detect package manager: `pip` / `poetry` / `venv` / `conda`.
- Detect existing integrations: LangChain, LangGraph, FastAPI, plain Python.
- Report findings explicitly: *"I see opengradient==X.Y.Z is installed but OG_PRIVATE_KEY is missing from .env."*

### 1B — Auto Diagnostics (precise, for complex projects)
Run the bundled diagnostic script and read its JSON output before generating code:
```bash
python .agent/skills/05-opengradient-connect/scripts/og_diagnostics.py
```
The script outputs a JSON report with: `sdk_version`, `env_vars_status`, `latest_pypi_version`, `network_config`, `update_needed`.

### 1C — Installation Commands (emit only what is missing)
```bash
# pip (default)
pip install opengradient

# with LangChain
pip install opengradient langchain-opengradient

# with LangGraph
pip install opengradient langgraph langchain-opengradient

# Update existing
pip install --upgrade opengradient
```

**Check PyPI for latest version** using the bundled script before recommending a version.
Use `og_pypi_check.sh` or simply: `pip index versions opengradient 2>/dev/null | head -1`

---

## STEP 2 — TEMPLATE FETCHING PROTOCOL (Core Hybrid Logic)

You MUST fetch code from the canonical cookbook. NEVER invent boilerplate from memory.

Map the user's intent to the correct raw URL and fetch it using `read_url_content`:

| User Intent | Fetch URL |
|-------------|-----------|
| Basic LLM / prompting / completion | `https://raw.githubusercontent.com/Floyd11/OpenGradient-Developer-Cookbook/main/snippets/01_llm_completion_basic.py` |
| Agents, tool calling, multi-turn chat | `https://raw.githubusercontent.com/Floyd11/OpenGradient-Developer-Cookbook/main/snippets/02_llm_chat_with_tools.py` |
| LangChain integration / agent | `https://raw.githubusercontent.com/Floyd11/OpenGradient-Developer-Cookbook/main/snippets/11_langchain_agent.py` |
| FastAPI / REST backend / async API | `https://raw.githubusercontent.com/Floyd11/OpenGradient-Developer-Cookbook/main/boilerplates/fastapi-verifiable-backend/main.py` |

**After fetching:**
1. Read the template fully.
2. Adapt it to the user's project (rename vars, inject their env setup, add their logic).
3. Apply the Golden Rules from Step 3 before returning to the user.
4. If a URL returns 404, inform the user that the cookbook template is unavailable and offer to write a minimal version following the Golden Rules manually.

---

## STEP 3 — OPENGRADIENT SDK GOLDEN RULES (Mandatory Constraints)

You MUST enforce both rules in every piece of OG code you write or review.

### Rule 1 — Permit2 Pre-Approval (Application Startup)
```python
# MANDATORY: Call ONCE at app startup, before any inference.
# This grants the x402 Gateway permission to spend OPG tokens on behalf of the user.
llm.ensure_opg_approval(opg_amount=5.0)
```
- Place in `main()`, `lifespan()` (FastAPI), or module `__init__`.
- NEVER call it inside an inference loop — it is a one-time startup action.
- If missing in the user's code, flag it as a **critical bug**.

### Rule 2 — TEE Proof Extraction (Every Inference Call)
```python
result = llm.chat(messages=[...])

# MANDATORY: Extract and surface the TEE proof.
# This is the cryptographic attestation that inference ran in a Trusted Execution Environment.
payment_hash = result.payment_hash
print(f"[TEE PROOF] Transaction hash: {payment_hash}")
```
- Always explain to the user: "This hash proves your inference was executed inside a TEE. It is verifiable on-chain."
- Return or log `payment_hash` in every integration (API response, DB record, log line).
- If it is missing from user's code, flag it as a **silent data-loss bug**.

---

## STEP 4 — NETWORK GUARD (Mainnet Warning)

If the user mentions "mainnet", "production", "real tokens", "live", or changes `CHAIN_ID`:

> ⚠️ **STOP. Do not proceed without an explicit safety acknowledgment.**

Issue this exact warning:

> The OpenGradient SDK and x402 Gateway currently operate on **Base Sepolia Testnet** (Chain ID: 84532).
> Mainnet has not yet launched with a confirmed chain ID or RPC endpoint.
> Deploying with real `$OPG` tokens before Mainnet is ready risks permanent loss of funds.
> **Action required:** Initiate the Mainnet Migration Checklist from `references/mainnet_checklist.md`.

Then load and follow `references/mainnet_checklist.md` for the interactive step-by-step process.

---

## STEP 5 — HYBRID UPDATER (SDK Version Freshness)

At the top of every integration session, check if the skill's knowledge is stale:

1. Run: `pip index versions opengradient 2>/dev/null | head -1` to get latest PyPI version.
2. Compare with `og_sdk_version_tested` field at the top of this file.
3. If they differ, inform the user:
   > "The skill was last verified against opengradient `0.9.3`. The latest PyPI version is `X.Y.Z`.
   > I will apply this skill's logic but recommend verifying API changes in the
   > [OpenGradient changelog](https://docs.opengradient.ai) before production use."
4. Run `scripts/og_diagnostics.py` — it also checks PyPI and reports `update_needed: true/false`.

---

## REFERENCES (Load On Demand)

- **Troubleshooting** → load `references/troubleshooting.md` when user reports errors with TEE, gateway, tokens, or timeouts.
- **Mainnet Migration** → load `references/mainnet_checklist.md` when Mainnet transition is discussed.
