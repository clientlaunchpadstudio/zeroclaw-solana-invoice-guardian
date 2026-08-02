# End-to-End Local Demo Session

Date: 2026-08-02  
Runtime: official ZeroClaw v0.8.3 portable release  
Command: `python -B scripts/demo_session.py --config-dir zeroclaw-state`

The runner completed with exit code 0 and demonstrated, in order:

1. `invoice-guardian` loaded for the local `invoice_guardian` agent.
2. The configured live ZeroClaw agent reported that it is Tier-1 build-only and has no wallet-key capability.
3. The valid fixture produced an unsigned Solana Pay request with `signing: not performed` and `network: not contacted`.
4. The over-cap fixture was rejected with the local-cap reason.
5. The injection-shaped recipient fixture was rejected as an invalid Solana address.
6. ZeroClaw validated the deterministic `solana-reference-poll` SOP.
7. The same runner made one fixed-host, read-only `getSignaturesForAddress` request to the public Solana RPC for the Clock sysvar sentinel. It returned a finalized signature observation while retaining `settlement_proven: false`; a signature alone does not establish an invoice's amount, mint, recipient, or intended reference context.

This is local CLI-surface demonstration evidence only. It did not connect a wallet, initiate a payment, send a transaction, or prove settlement. A public bounty showcase still requires a real-channel recording and publication steps.
