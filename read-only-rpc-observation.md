# Read-only RPC observation

**Run:** 2026-08-02 during the local ZeroClaw bounty-entry build

```text
Command: python -B scripts/reference_check.py --reference SysvarC1ock11111111111111111111111111111111
Endpoint: https://api.mainnet-beta.solana.com
Method: getSignaturesForAddress (limit 1, finalized)
Read-only: true
Settlement proven: false
```

The public endpoint returned one finalized signature (`41Gf82c4jf8hW3vMup2ExZc9HqiwuQ8irMYu1XyfbDMYPHZHFZWLcRMYzwrNMKCPEFk1GgRCx5qWbnRQfow93jYG`) at slot `436710382`, with no RPC-reported error.

This is an integration check only. The queried address is the Solana Clock sysvar sentinel, not a customer reference, and the output does **not** prove an invoice payment. The client performed no signing, wallet interaction, transaction submission, funding, or asset transfer.
