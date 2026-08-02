# ZeroClaw Solana Invoice Guardian

An entry for the Superteam Brasil ZeroClaw/Solana bounty. The project demonstrates a Tier-1 invoice workflow that turns approved invoice data into an unsigned Solana Pay request and safely polls a public reference address for a payment observation.

The workflow is intentionally constrained to preparation and read-only observation. It creates no transactions and does not broadcast or fund payments; payment execution remains outside this workflow.

## Evidence target

- Run the official ZeroClaw Windows release locally.
- Exercise the supported, pairing-protected local gateway webhook surface and a public Solana RPC read for reproducible local channel evidence. This is deliberately distinguished from the bounty's later public messaging-channel showcase requirement.
- Provide reproducible configuration, a policy-oriented skill, deterministic fixture tests, a validated read-only polling SOP, and a short demo recording.

See the repository documentation for the setup guide, runbook, threat model, and local evidence.
