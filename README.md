# ZeroClaw Solana Invoice Guardian

An entry for the Superteam Brasil ZeroClaw/Solana bounty. The project demonstrates a Tier-1, non-custodial agent that turns a human-approved invoice request into an unsigned Solana Pay URL and safely polls a public reference address for a payment observation.

The entry deliberately never stores a seed phrase, private key, or wallet connection. It does not create, sign, broadcast, or fund a transaction. A human wallet signs any payment outside the agent.

## Evidence target

- Run the official ZeroClaw Windows release locally.
- Exercise the supported, pairing-protected local gateway webhook surface and a public Solana RPC read for reproducible local channel evidence. This is deliberately distinguished from the bounty's later public messaging-channel showcase requirement.
- Provide reproducible configuration, a policy-oriented skill, deterministic fixture tests, a validated read-only polling SOP, and a short demo recording.

See the repository documentation for the setup guide, runbook, threat model, and local evidence.
