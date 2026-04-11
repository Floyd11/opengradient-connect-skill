# Troubleshooting — OpenGradient SDK & x402 Gateway

> Load this file when the user reports errors related to TEE inference, gateway,
> OPG token balance, or timeouts. Use the diagnostic commands to pinpoint the issue.

---

## Error Index

| # | Error / Symptom | Section |
|---|-----------------|---------|
| 1 | `InsufficientFundsError` / balance too low | [→ §1](#1-insufficient-opg-balance) |
| 2 | `GatewayTimeoutError` / x402 request timed out | [→ §2](#2-gateway-timeout-x402) |
| 3 | `TEEAttestationError" / proof not returned | [→ §3](#3-tee-attestation-failure) |
| 4 | `payment_hash` is `None` | [→ §4](#4-payment_hash-is-none) |
| 5 | `PermissionError" / Permit2 not approved | [→ §5](#5-permit2-approval-missing) |
| 6 | `InvalidPrivateKeyError" | [→ §6](#6-invalid-private-key) |
| 7 | `ConnectionRefusedError" / RPC unreachable | [→ §7](#7-rpc-connection-refused) |
| 8 | `ModuleNotFoundError: opengradient` | [→ §8](#8-sdk-not-installed) |
| 9 | Wrong Chain ID / transactions fail silently | [→ §9](#9-wrong-chain-id) |
| 10 | LangChain integration returning generic errors | [→ §10](#10-langchain-integration-errors) |

---

## 1. Insufficient OPG Balance

**Symptom:** `InsufficientFundsError`, `insufficient balance for x402 payment`

**Cause:** Wallet has no `$OPG` testnet tokens on Base Sepolia.

**Diagnostic:**
```python
import os
import opengradient as og
llm = og.LLM(private_key=os.environ["OG_PRIVATE_KEY"])
print(llm.get_balance())  # should be > 0
```

**Fix:**
1. Get testnet tokens from the OpenGradient Discord faucet or: https://faucet.opengradient.ai/
2. Verify wallet address matches your `OG_PRIVATE_KEY`.
3. Re-run `llm.ensure_opg_approval(min_allowance=5.0)` after topping up.

---

## 2. Gateway Timeout (x402)

**Symptom:** `GatewayTimeoutError`, `ReadTimeout`, request hangs for >30s

**Cause:** x402 Gateway is temporarily overloaded, or Base Sepolia RPC is congested.

**Diagnostic:**
```bash
curl -w "%{time_total}s\n" -o /dev/null -s https://sepolia.base.org
# Healthy: < 2s. If > 5s, the RPC is congested.
```

**Fix:**
- Add a retry wrapper with exponential backoff (minimum 3 retries).
- Set an explicit timeout: `og.LLM(private_key=..., timeout=60)`.
- Check https://status.base.org for network incidents.

---

## 3. TEE Attestation Failure

**Symptom:** `TEEAttestationError`, `attestation verification failed`

**Cause:** The TEE enclave returned an invalid or expired attestation quote.

**Diagnostic:**
```python
result = llm.chat(messages=[...])
print(result.tee_attestation)  # inspect raw attestation object
```

**Fix:**
- This is typically a transient infrastructure error. Retry after 60 seconds.
- If persistent (>3 failures), report to OpenGradient support with the full `result` object.
- Do NOT cache TEE results — each inference must produce a fresh attestation.

---

## 4. `payment_hash` is `None`

**Symptom:** `result.payment_hash` returns `None` even on a "successful" call.

**Cause:** Inference did not route through the TEE gateway (e.g., used a non-TEE model name).

**Fix:**
- Verify you are using a TEE-enabled model (e.g., `og.TEE_LLM.CLAUDE_SONNET_4_5`).
- Do NOT use plain string model names — always use the `og.TEE_LLM` enum.
- A non-None `payment_hash` is the ONLY proof of TEE execution. Treat `None` as a failure.

---

## 5. Permit2 Approval Missing

**Symptom:** `PermissionError: Gateway not authorized to spend OPG`, or first inference fails.

**Cause:** `llm.ensure_opg_approval()` was never called, or called with `min_allowance=0`.

**Fix:**
```python
# Add to application startup — once, not per-request:
llm.ensure_opg_approval(min_allowance=5.0)
```

For FastAPI, place inside the `lifespan` context manager:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    llm.ensure_opg_approval(min_allowance=5.0)  # startup
    yield
```

---

## 6. Invalid Private Key

**Symptom:** `InvalidPrivateKeyError`, `could not parse private key`

**Diagnostic:**
```bash
python3 -c "
from eth_account import Account
import os
try:
    acc = Account.from_key(os.environ['OG_PRIVATE_KEY'])
    print('Valid. Address:', acc.address)
except Exception as e:
    print('Invalid key:', e)
"
```

**Fix:**
- Key must be a 64-char hex string, optionally prefixed with `0x`.
- NEVER commit it to git. Store in `.env` only. Add `.env` to `.gitignore`.
- Generate a new wallet if compromised: `python3 -c "from eth_account import Account; print(Account.create().key.hex())"`

---

## 7. RPC Connection Refused

**Symptom:** `ConnectionRefusedError`, `HTTPSConnectionPool`, `Max retries exceeded`

**Diagnostic:**
```bash
curl -X POST https://sepolia.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
# Expect: {"result": "0x..."}
```

**Fix:**
- Default RPC `https://sepolia.base.org` may have rate limits. Use a dedicated RPC from Alchemy or Infura if needed.
- Check for proxy/firewall blocking outbound HTTPS on port 443.

---

## 8. SDK Not Installed

**Symptom:** `ModuleNotFoundError: No module named 'opengradient'`

**Fix:**
```bash
pip install opengradient           # basic
pip install opengradient langchain-opengradient  # with LangChain

# Verify:
python3 -c "import opengradient; print(opengradient.__version__)"
```

Check that you are using the correct Python interpreter / virtual environment.

---

## 9. Wrong Chain ID

**Symptom:** Transactions broadcast but never confirm, or silent failures on-chain.

**Diagnostic:**
```python
import os
import opengradient as og
llm = og.LLM(private_key=os.environ["OG_PRIVATE_KEY"])
print(llm.chain_id)  # must be 84532 for Testnet
```

**Fix:**
- Set `CHAIN_ID=84532` in `.env`.
- Do NOT hardcode chain ID in your business logic — always read from env vars.
- If migrating to Mainnet, follow `mainnet_checklist.md` — do NOT change this manually.

---

## 10. LangChain Integration Errors

**Symptom:** `AttributeError`, `ChatModel not found`, or LangChain chain returns empty results.

**Diagnostic:**
```bash
pip show langchain-opengradient  # verify it's installed
python3 -c "from langchain_opengradient import ChatOpenGradient; print('OK')"
```

**Fix:**
- Install: `pip install langchain-opengradient`
- Use `ChatOpenGradient` as a drop-in for `ChatOpenAI`.
- Ensure `OG_PRIVATE_KEY` is set — LangChain reads it from the environment.
- Golden Rules still apply inside LangChain chains: call `ensure_opg_approval()` before invoking the chain, and extract `payment_hash` from the raw response metadata.
