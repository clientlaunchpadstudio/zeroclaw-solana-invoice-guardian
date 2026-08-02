# SOP Validation Evidence

Date: 2026-08-02  
Runtime: official ZeroClaw v0.8.3 portable release

The local ZeroClaw CLI loaded `solana-reference-poll` from the project source and reported:

```text
Mode: deterministic  Steps: 4  Triggers: manual, cron:0 */6 * * *
✅ solana-reference-poll — valid
All SOPs passed validation.
```

The generated outline was:

```text
1. Validate the reference -> 2
2. Make the fixed-host read-only check -> 3
3. Shape the observation -> 4
4. Stop safely
manual -> 1
cron -> 1
```

This validates the definition only. No SOP run, wallet connection, payment, Solana transaction, or settlement claim occurred.
