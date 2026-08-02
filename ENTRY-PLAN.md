# Entry plan

## Use case

`Invoice Guardian` is a small-business payment assistant. An operator requests an invoice in USDC; the agent validates a strict, local policy, renders an unsigned Solana Pay transfer-request URL, and presents it for the customer to open in their own wallet. A scheduled read-only check looks only for signatures tied to an approved invoice reference key and reports an observation, never a settlement confirmation.

## Custody and safety

- **Tier:** T1 (build, never sign).
- **Keys held:** none.
- **Allowed outbound destinations:** configured public Solana RPC host only.
- **Spend authority:** none; transaction construction is a URL string, never a signature or broadcast.
- **Prompt-injection defense:** the payment recipient, USDC mint, amount cap, and reference format are supplied by a local policy file; untrusted chat text cannot override them.
- **Failure mode:** reject malformed, over-cap, unexpected-mint, or altered-recipient invoice requests; do not generate a payment URL.

## Deliverables

1. A ZeroClaw skill and config that reproduce the safe workflow.
2. A small deterministic local policy/fixture harness for valid and malicious requests.
3. A run log showing the official release executing the safe local workflow and a separate fixed-host public read-only RPC observation.
4. A three-minute-or-shorter terminal demo and a concise showcase write-up.
5. A public repository and the bounty-required Discord showcase post.

## Explicit non-goals

- No real payment, wallet funding, wallet connection, account funding, private key, seed phrase, or transaction signature.
- No financial advice, trading, or automated asset movement.
- No invented customer, payment, or payout evidence.
