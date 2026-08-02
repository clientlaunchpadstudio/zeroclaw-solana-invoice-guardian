# Local runbook

This workspace is intentionally self-contained and uses no wallet, API key, or payment.

## Run deterministic checks

```powershell
python -m unittest discover -s tests -v
```

## Configure ZeroClaw without credentials in source control

1. Copy `config/zeroclaw.example.toml` to an operator-local config directory.
2. Import a current Codex subscription login locally, without adding it to the repository:

   ```powershell
   zeroclaw auth login --model-provider openai-codex --import ~/.codex/auth.json
   ```

3. Install the audited skill into the configured bundle and copy the SOP directory to the configured SOP directory:

   ```powershell
   zeroclaw skills install .\skill --bundle invoice_guardian
   Copy-Item -Recurse .\sops\solana-reference-poll <local-sops-dir>\solana-reference-poll
   zeroclaw sop validate solana-reference-poll
   ```

The provider model string is an operator-local compatibility choice; do not treat the example value as a permanent model catalog guarantee.

## External-channel handoff (operator action only)

The bounty requires a real messaging-channel demonstration. ZeroClaw reports its CLI as available, but this local surface is evidence only; do not claim that it automatically meets the bounty's separate real-channel requirement.

1. Obtain explicit approval for the chosen external channel and public recording before creating or connecting a Discord, Telegram, Slack, or other platform account.
2. The human account owner must complete any platform verification or CAPTCHA. Do not attempt to bypass it or create a synthetic audience.
3. Keep the channel bot token out of this repository, evidence files, terminal history, screen recording, and chat. ZeroClaw's `channel add discord` interface accepts a token-bearing JSON object; if there is no secure operator-local way to provide it, stop rather than place a token on a command line.
4. After an approved operator-local configuration is in place, run `zeroclaw channel doctor` and confirm that the channel is healthy before using `zeroclaw channel start`. Do not run a listener merely to manufacture activity.
5. Record one short, real inbound message and response. Keep the response within the fixed policy: it may render an unsigned test invoice or perform the existing read-only reference observation, but it must never ask for a seed phrase, connect a wallet, sign, send, fund, or claim settlement.
6. Sanitize the recording and supporting transcript. Do not publish the repository, video, Discord showcase post, or final bounty submission automatically; each is a separate public action.

## Render the safe fixture

```powershell
python scripts/invoice_guardian.py --policy config/policy.example.json --request fixtures/valid_invoice.json
```

The example recipient is the Solana System Program sentinel (`11111111111111111111111111111111`). It is a test-only placeholder: do not scan, publish, fund, or sign the rendered URL.

## Prepare a real operator configuration

1. Copy `config/policy.example.json` to a local, uncommitted `config/policy.json`.
2. The owner chooses one or more receiving addresses and a strict USDC cap.
3. The owner, not the agent, independently verifies every address before a production use.
4. The agent never gains any signing authority.

## Read-only reference observation

```powershell
python scripts/reference_check.py --reference <public-reference-key>
```

The endpoint is hard-coded to the public Solana mainnet RPC and exposes only `getSignaturesForAddress`. It cannot send a transaction. Its result is a telemetry observation, not invoice settlement proof.

## Demo claim

The initial demo proves deterministic request validation and refusal behavior. It does **not** claim to prove a completed payment. A future read-only RPC check must use a genuine, operator-approved invoice reference and report only data returned by the public RPC.
