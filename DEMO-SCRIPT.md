# Three-minute terminal demo script

This demo is deliberately non-custodial. It proves a real local ZeroClaw skill can be audited and installed beside a deterministic safety harness; it never claims a transaction or payout.

For a single terminal sequence after local ZeroClaw configuration is complete, run:

```powershell
python -B scripts\demo_session.py --config-dir zeroclaw-state
```

The detailed sections below are the narration and fallback commands for recording.

## 1. Show the official runtime (15 seconds)

```powershell
runtime\zeroclaw.exe --version
runtime\zeroclaw.exe --config-dir zeroclaw-state skills list
```

Explain: this is a portable v0.8.3 runtime. The isolated agent loads `invoice_guardian`; there are no enabled channels or provider credentials.

## Optional local gateway channel proof (25 seconds)

This is a real, supported ZeroClaw HTTP/webhook channel surface bound only to `127.0.0.1`. It is useful local integration evidence, but it is not presented as a substitute for the bounty's required public messaging-channel recording.

1. Start the gateway on an unused loopback port with pairing required.
2. Generate a one-time pair code with `zeroclaw gateway get-paircode --new`; keep the code and resulting bearer token out of the terminal recording, repository, and logs.
3. Pair one non-personal test client, then POST a fixed no-tools custody-boundary prompt to `/webhook` using that bearer token.
4. Show the response, which must say the agent cannot accept wallet keys or sign/send a transaction.
5. Revoke the test client with `gateway get-paircode --rotate-device <test-device-id>` and stop the loopback listener.

The recorded local run is in `evidence/gateway-webhook-transcript.md`.

## 2. Show policy-bound invoice rendering (45 seconds)

```powershell
python -B scripts\invoice_guardian.py --policy config\policy.example.json --request fixtures\valid_invoice.json
```

Explain: it returns an unsigned Solana Pay request only. The recipient, canonical USDC mint, and $50 cap come from a local policy. The fixture uses the non-customer System Program sentinel and must never be paid.

## 3. Show two fail-closed refusals (45 seconds)

```powershell
python -B scripts\invoice_guardian.py --policy config\policy.example.json --request fixtures\over_cap_invoice.json
python -B scripts\invoice_guardian.py --policy config\policy.example.json --request fixtures\injection_attempt_invoice.json
```

Explain: a local cap breach and an attacker-shaped recipient each stop before a URL is produced. No chat instruction can override the policy.

## 4. Show a read-only public RPC observation (30 seconds)

```powershell
python -B scripts\reference_check.py --reference SysvarC1ock11111111111111111111111111111111
```

Explain: the host is hard-pinned to the public Solana endpoint and can only fetch one finalized signature. It reports `settlement_proven: false`; the sentinel is not a customer invoice reference.

## 5. Close with reproducibility and threat model (30 seconds)

```powershell
python -B -m unittest discover -s tests -v
```

Show `docs/ENTRY-PLAN.md` and state the custody tier: T1, no private keys, no transaction creation or signing, no funding, and no transfer. A human wallet independently reviews and signs any real payment outside the agent.
