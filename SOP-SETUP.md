# Solana Reference Poll SOP

`sops/solana-reference-poll/` is a ZeroClaw SOP definition that provides a safe recurring observation workflow. It is intentionally not a payment verifier and cannot create, sign, submit, or refund a transaction.

## Install

1. Copy the version-controlled `sops/solana-reference-poll/` directory into the operator's ZeroClaw SOP directory, normally `<config-dir>/shared/sops/solana-reference-poll/`.
2. Configure the operator-local ZeroClaw config with a filesystem path appropriate to that installation:

   ```toml
   [sop]
   default_execution_mode = "deterministic"
   persist_runs = true
   sops_dir = "shared/sops"
   step_scope_enforce = true
   untrusted_input_guard = "block"
   ```

3. Validate the loaded definition:

   ```powershell
   zeroclaw sop validate solana-reference-poll
   zeroclaw sop show solana-reference-poll
   zeroclaw sop graph solana-reference-poll --format outline
   ```

No seed phrase, wallet key, provider API key, recipient, or customer reference belongs in the SOP files or this repository.

## Triggers

- `manual` is intended for an operator-approved reference observation.
- `cron: 0 */6 * * *` is a six-hour poll. It must fail closed unless the operator has already supplied an approved public reference through an appropriate runtime context.

## Boundaries

The only networked work named by the SOP is `scripts/reference_check.py`, which fixes the RPC host and calls Solana `getSignaturesForAddress`. The agent must describe any output as an observation with `settlement_proven: false` until an operator independently checks the approved recipient, canonical USDC mint, amount, reference, and finality.
