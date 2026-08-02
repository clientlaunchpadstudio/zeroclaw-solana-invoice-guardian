#!/usr/bin/env python3
"""Build policy-bounded, unsigned Solana Pay requests for Invoice Guardian.

This utility intentionally does not contain a wallet, signing code, transaction
broadcast, or any network call. It gives a ZeroClaw skill a deterministic guard
rail that it can invoke before showing a customer an unsigned payment URL.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from urllib.parse import urlencode


BASE58_ADDRESS = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
INVOICE_ID = re.compile(r"^INV-[A-Z0-9-]{3,40}$")
MAINNET_USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
USDC_DECIMALS = Decimal("0.000001")


class PolicyViolation(ValueError):
    """Raised when untrusted request data conflicts with the local policy."""


@dataclass(frozen=True)
class Policy:
    recipient_allowlist: tuple[str, ...]
    max_amount_usdc: Decimal
    accepted_mint: str
    label: str
    message_prefix: str


def load_json(path: Path) -> dict[str, Any]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise PolicyViolation(f"File not found: {path}") from error
    except json.JSONDecodeError as error:
        raise PolicyViolation(f"Invalid JSON in {path}: {error.msg}") from error
    if not isinstance(parsed, dict):
        raise PolicyViolation(f"JSON object required in {path}")
    return parsed


def require_address(value: Any, field: str) -> str:
    if not isinstance(value, str) or not BASE58_ADDRESS.fullmatch(value):
        raise PolicyViolation(f"{field} must be a 32-44 character base58 Solana address")
    return value


def parse_amount(value: Any, field: str) -> Decimal:
    if not isinstance(value, str):
        raise PolicyViolation(f"{field} must be a decimal string, never a number")
    try:
        amount = Decimal(value)
    except InvalidOperation as error:
        raise PolicyViolation(f"{field} is not a valid decimal amount") from error
    if not amount.is_finite() or amount <= 0:
        raise PolicyViolation(f"{field} must be greater than zero")
    if amount.as_tuple().exponent < -6:
        raise PolicyViolation(f"{field} exceeds USDC's six decimal places")
    return amount.quantize(USDC_DECIMALS).normalize()


def load_policy(path: Path) -> Policy:
    raw = load_json(path)
    recipients = raw.get("recipient_allowlist")
    if not isinstance(recipients, list) or not recipients:
        raise PolicyViolation("policy.recipient_allowlist must contain at least one address")
    validated_recipients = tuple(require_address(item, "policy recipient") for item in recipients)
    accepted_mint = require_address(raw.get("accepted_mint"), "policy.accepted_mint")
    if accepted_mint != MAINNET_USDC_MINT:
        raise PolicyViolation("policy.accepted_mint must be the canonical Solana mainnet USDC mint")
    label = raw.get("label")
    message_prefix = raw.get("message_prefix")
    if not isinstance(label, str) or not label.strip():
        raise PolicyViolation("policy.label must be a non-empty string")
    if not isinstance(message_prefix, str) or not message_prefix.strip():
        raise PolicyViolation("policy.message_prefix must be a non-empty string")
    return Policy(
        recipient_allowlist=validated_recipients,
        max_amount_usdc=parse_amount(raw.get("max_amount_usdc"), "policy.max_amount_usdc"),
        accepted_mint=accepted_mint,
        label=label.strip(),
        message_prefix=message_prefix.strip(),
    )


def compact_decimal(value: Decimal) -> str:
    return format(value, "f").rstrip("0").rstrip(".")


def create_invoice_url(policy: Policy, request: dict[str, Any]) -> dict[str, str]:
    invoice_id = request.get("invoice_id")
    if not isinstance(invoice_id, str) or not INVOICE_ID.fullmatch(invoice_id):
        raise PolicyViolation("invoice_id must match INV- followed by uppercase letters, digits, or hyphens")

    recipient = require_address(request.get("recipient"), "recipient")
    if recipient not in policy.recipient_allowlist:
        raise PolicyViolation("recipient is not in the local policy allowlist")

    mint = require_address(request.get("mint"), "mint")
    if mint != policy.accepted_mint:
        raise PolicyViolation("only canonical mainnet USDC is allowed")

    reference = require_address(request.get("reference"), "reference")
    amount = parse_amount(request.get("amount_usdc"), "amount_usdc")
    if amount > policy.max_amount_usdc:
        raise PolicyViolation(
            f"amount exceeds the local cap of {compact_decimal(policy.max_amount_usdc)} USDC"
        )

    note = request.get("note", "")
    if not isinstance(note, str) or len(note) > 80 or "\n" in note or "\r" in note:
        raise PolicyViolation("note must be a single line no longer than 80 characters")

    params = urlencode(
        {
            "amount": compact_decimal(amount),
            "spl-token": mint,
            "reference": reference,
            "label": policy.label,
            "message": f"{policy.message_prefix} {invoice_id}" + (f": {note}" if note else ""),
        }
    )
    return {
        "invoice_id": invoice_id,
        "recipient": recipient,
        "amount_usdc": compact_decimal(amount),
        "mint": mint,
        "reference": reference,
        "solana_pay_url": f"solana:{recipient}?{params}",
        "custody_tier": "T1",
        "signing": "not performed",
        "network": "not contacted",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True, help="Path to a local policy JSON file")
    parser.add_argument("--request", type=Path, required=True, help="Path to an invoice request JSON file")
    args = parser.parse_args()
    try:
        result = create_invoice_url(load_policy(args.policy), load_json(args.request))
    except PolicyViolation as error:
        print(json.dumps({"accepted": False, "reason": str(error)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps({"accepted": True, **result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
