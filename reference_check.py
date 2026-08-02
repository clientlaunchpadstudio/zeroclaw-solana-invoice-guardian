#!/usr/bin/env python3
"""Read the latest public Solana signature for an invoice reference address.

This is intentionally a read-only JSON-RPC client. It has no wallet support,
private key handling, transaction builder, transaction sender, or signing path.
An observed signature is operational telemetry, never settlement proof by itself.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from invoice_guardian import PolicyViolation, require_address


ALLOWED_RPC_URL = "https://api.mainnet-beta.solana.com"


def get_latest_reference_observation(reference: str, rpc_url: str = ALLOWED_RPC_URL) -> dict[str, Any]:
    """Return a compact, non-settlement observation from the allowed public RPC."""
    require_address(reference, "reference")
    if rpc_url != ALLOWED_RPC_URL:
        raise PolicyViolation("RPC URL is fixed to the approved public Solana endpoint")

    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": "invoice-guardian-readonly",
            "method": "getSignaturesForAddress",
            "params": [reference, {"limit": 1, "commitment": "finalized"}],
        }
    ).encode("utf-8")
    request = Request(
        rpc_url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "InvoiceGuardian/0.1"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:  # nosec B310: host is fixed above
            decoded = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        return {
            "reference": reference,
            "rpc_url": rpc_url,
            "read_only": True,
            "settlement_proven": False,
            "observation": "unavailable",
            "reason": str(error),
        }

    result = decoded.get("result")
    if not isinstance(result, list) or not result:
        return {
            "reference": reference,
            "rpc_url": rpc_url,
            "read_only": True,
            "settlement_proven": False,
            "observation": "no finalized signatures returned",
        }

    first = result[0]
    if not isinstance(first, dict):
        return {
            "reference": reference,
            "rpc_url": rpc_url,
            "read_only": True,
            "settlement_proven": False,
            "observation": "malformed RPC result",
        }
    return {
        "reference": reference,
        "rpc_url": rpc_url,
        "read_only": True,
        "settlement_proven": False,
        "observation": "latest finalized signature returned; amount, mint, recipient, and reference context still require independent verification",
        "signature": first.get("signature"),
        "slot": first.get("slot"),
        "block_time": first.get("blockTime"),
        "err": first.get("err"),
        "confirmation_status": first.get("confirmationStatus"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, help="Solana reference public key")
    parser.add_argument("--rpc-url", default=ALLOWED_RPC_URL, help="Must remain the approved public endpoint")
    args = parser.parse_args()
    try:
        result = get_latest_reference_observation(args.reference, args.rpc_url)
    except PolicyViolation as error:
        print(json.dumps({"accepted": False, "reason": str(error)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps({"accepted": True, **result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
