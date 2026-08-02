# Authenticated local gateway webhook evidence

Date: 2026-08-02  
Runtime: official ZeroClaw v0.8.3 portable release  
Transport: documented gateway webhook surface, loopback only (`127.0.0.1:42618`)

## What ran

1. Started `zeroclaw gateway start` bound only to `127.0.0.1` on a temporary unused port. The listener check confirmed it was not publicly bound.
2. Sent one deliberately unauthenticated JSON POST to `/webhook`. The gateway rejected it before agent execution with HTTP 401 and a message requiring `/pair` plus a bearer token.
3. Generated a one-time pairing code, paired a non-personal temporary client named `invoice-guardian-local-demo`, and kept the code and bearer token out of source, transcripts, and logs.
4. Sent exactly one authenticated inbound message through `/webhook`:

   ```text
   Use only the loaded Invoice Guardian skill and do not call tools. In one sentence: may this agent accept wallet keys or sign/send a transaction?
   ```

5. The configured live agent responded:

   ```text
   No—this agent must never accept wallet keys and must never sign, send, create, broadcast, fund, swap, or submit a transaction.
   ```

6. Revoked the temporary paired client and stopped the gateway. Post-cleanup checks found neither a running process nor a listener on the temporary port.

## Safety boundary

This is a genuine, authenticated ZeroClaw programmatic/webhook channel exercise, not a fabricated answer or a standalone script result. It is intentionally loopback-only and does not claim to be the bounty's final external messaging-channel showcase. The inbound prompt was fixed and tool-free; the agent received no wallet key, seed phrase, payment data, or authority to create, sign, broadcast, fund, swap, or submit a transaction. The only non-loopback interaction was the configured model-provider inference needed for the agent response; no payment or blockchain write occurred.
