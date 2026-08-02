# Draft ZeroClaw Discord showcase post

> ## Invoice Guardian — a zero-custody Solana Pay assistant for real-world invoices
>
> I built a Tier-1 ZeroClaw workflow for a small-business operator who wants an agent to prepare a USDC invoice without ever holding a wallet or making a payment decision.
>
> **What it does**
>
> - Validates an invoice against a local recipient allowlist, canonical Solana USDC mint, and strict amount cap.
> - Produces an **unsigned** Solana Pay transfer-request URL. A customer independently reviews and signs in their own wallet.
> - Rejects cap breaches, recipient changes, non-USDC mints, malformed references, and prompt-injection-shaped input before output.
> - Makes an optional read-only, fixed-host RPC query for the exact invoice reference. It marks every response as telemetry, never settlement proof.
> - Loads a deterministic `solana-reference-poll` SOP with manual and six-hour cron triggers; it fails closed without an operator-approved public reference.
>
> **Custody / threat model**
>
> - Tier T1: build only; no seed phrase, private key, wallet connection, transaction signature, broadcast, funding, transfer, or swap path.
> - The fixed policy is the authority, not untrusted channel text.
> - A malicious “send to this new recipient” message fails closed.
>
> **Reproduce**
>
> 1. Clone the repository.
> 2. Run `python -B -m unittest discover -s tests -v`.
> 3. Follow `docs/RUNBOOK.md`, then validate the SOP with `zeroclaw sop validate solana-reference-poll`.
> 4. Follow `docs/DEMO-SCRIPT.md` with the official ZeroClaw portable release.
>
> **Verified locally before publication**
>
> - The official ZeroClaw v0.8.3 runtime passed the skill audit and loaded the local `invoice_guardian` agent.
> - Tool-free agent prompts returned the human-signing boundary and rejected an attempted recipient/cap override.
> - This pre-channel evidence is recorded in `evidence/live-agent-prechannel-transcript.md`; it is not represented as the final real-channel video.
>
> Repo: **[replace with public GitHub repository URL after publication]**
>
> Demo: **[replace with video URL after recording]**

Do not publish this draft until the repository is public, the real-channel demo is recorded, all links are checked, and no evidence is overstated.
