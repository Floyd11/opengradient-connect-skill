# Mainnet Migration Checklist — OpenGradient

> **Safety-First Protocol.** This is an interactive checklist.
> The agent MUST walk through each step in order, await explicit `yes/no` confirmation before
> proceeding, and HALT the entire process if any validation fails.
>
> NEVER automate the full migration. Each step requires the user's manual confirmation.

---

## ⚠️ Pre-Conditions (Read Before Starting)

- You are about to move from **Base Sepolia Testnet** (Chain ID: `84532`) to **Mainnet**.
- Mainnet uses **real `$OPG` tokens with real monetary value**.
- A misconfiguration can result in **permanent loss of funds** or transactions on the wrong network.
- This checklist is designed to be run once, in a dedicated migration session.

> Ask the user: **"Are you ready to begin the Mainnet migration? Type YES to confirm."**
> If response is not explicit YES — stop and return.

---

## Step 1 — Confirm Mainnet is Live

**Agent instruction:** Before proceeding, verify that OpenGradient Mainnet has officially launched.

- [ ] Check the official announcement: https://docs.opengradient.ai or the OpenGradient Discord.
- [ ] Confirm the official Mainnet `CHAIN_ID` and `RPC_URL`.
  - Note: As of skill `last_verified_date: 2026-04-01`, Mainnet is **NOT YET LAUNCHED**.
  - The EVM-compatible chain ID and RPC endpoint are TBD.

> Ask: **"Have you confirmed with the OpenGradient team that Mainnet is live? Provide the Chain ID and RPC URL."**
> Record the values. HALT if not confirmed.

---

## Step 2 — Backup Current Configuration

- [ ] Verify `.env` is in `.gitignore` (CRITICAL — never commit private keys).
- [ ] Create a dated backup: `cp .env .env.testnet.backup.$(date +%Y%m%d)`
- [ ] Confirm backup exists:
  ```bash
  ls -la .env.testnet.backup.*
  ```

> Ask: **"Backup created and verified? Type YES to continue."**

---

## Step 3 — Validate Mainnet Wallet & OPG Balance

- [ ] Confirm the wallet address for Mainnet (may differ from testnet wallet).
- [ ] Check real `$OPG` token balance on Mainnet:
  ```python
  import opengradient as og
  llm = og.LLM(private_key="YOUR_MAINNET_PRIVATE_KEY", chain_id=MAINNET_CHAIN_ID)
  print(f"Balance: {llm.get_balance()} OPG")
  ```
- [ ] Minimum recommended balance: **10 OPG** for initial Permit2 approval + first inferences.

> Ask: **"Is the Mainnet wallet funded and balance confirmed? Type YES to continue."**

---

## Step 4 — Update Environment Variables

Only after steps 1–3 are confirmed, update `.env`:

```bash
# OLD (Testnet) — keep in .env.testnet.backup
# OG_PRIVATE_KEY=<testnet_key>
# CHAIN_ID=84532
# RPC_URL=https://sepolia.base.org

# NEW (Mainnet) — values from Step 1
OG_PRIVATE_KEY=<mainnet_private_key>
CHAIN_ID=<mainnet_chain_id_from_step_1>
RPC_URL=<mainnet_rpc_from_step_1>
```

> Ask: **"`.env` has been updated with Mainnet values? Type YES to continue."**
> ⚠️ **The agent must NOT auto-write these values.** Instruct the user to edit manually.

---

## Step 5 — Re-run Diagnostics

Confirm the new environment is clean:

```bash
python .agent/skills/05-opengradient-connect/scripts/og_diagnostics.py
```

Expected output:
- `env_vars.all_present: true`
- `network_config.is_testnet: false`  ← Mainnet confirmed
- `network_config.detected_chain_id`: matches Mainnet Chain ID from Step 1
- `sdk.update_needed: false` (update SDK if needed)

> Ask: **"Diagnostics show correct Mainnet config? No warnings? Type YES to continue."**

---

## Step 6 — Permit2 Re-Approval on Mainnet

Permit2 approval is **per-network**. The Testnet approval is not valid on Mainnet.

```python
import opengradient as og
import os

llm = og.LLM(private_key=os.environ["OG_PRIVATE_KEY"])
# This spends real OPG. Confirm the amount is intentional.
llm.ensure_opg_approval(min_allowance=5.0)
print("Mainnet Permit2 approval granted.")
```

> Ask: **"Ready to approve spending 5 OPG on Mainnet? This is irreversible. Type YES to execute."**

---

## Step 7 — Smoke Test with Minimal Inference

Run one low-cost inference to verify end-to-end connectivity:

```python
result = llm.chat(messages=[{"role": "user", "content": "ping"}])
assert result.payment_hash is not None, "TEE proof missing — do NOT proceed"
print(f"[MAINNET SMOKE TEST PASS] Hash: {result.payment_hash}")
```

- [ ] `payment_hash` is not None ✅
- [ ] Response content is non-empty ✅
- [ ] No exceptions thrown ✅

> Ask: **"Smoke test passed? Type YES to finalize migration."**

---

## Step 8 — Update Code & Documentation

- [ ] Search codebase for any hardcoded `84532` or `sepolia`:
  ```bash
  grep -rn "84532\|sepolia\|base-sepolia" --include="*.py" --include="*.ts" .
  ```
- [ ] Replace with environment variable references (never hardcode).
- [ ] Update `README.md` or docs: note that the service now runs on Mainnet.
- [ ] Commit with conventional commit message:
  ```
  feat(network): migrate opengradient integration to mainnet
  ```

---

## Migration Complete ✅

> Summarize to the user:
> - Network: Mainnet (Chain ID: `<confirmed>`)
> - Permit2 approved: ✅
> - TEE proof verified: ✅
> - Testnet backup saved: `.env.testnet.backup.<date>`
>
> **Keep `.env.testnet.backup.*` safe.** If you need to roll back to Testnet, restore it manually.
