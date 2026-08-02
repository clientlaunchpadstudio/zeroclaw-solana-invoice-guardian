"""Run the non-custodial Invoice Guardian terminal demonstration."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ZEROCLAW = PROJECT_ROOT / "runtime" / "zeroclaw.exe"


def run(title: str, command: list[str], expected_codes: tuple[int, ...] = (0,)) -> None:
    print(f"\n== {title} ==", flush=True)
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=False,
        stdout=sys.stdout,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode not in expected_codes:
        raise subprocess.CalledProcessError(completed.returncode, command)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", default="zeroclaw-state")
    args = parser.parse_args()

    if not ZEROCLAW.is_file():
        raise FileNotFoundError(f"Missing local ZeroClaw runtime: {ZEROCLAW}")

    runtime = [str(ZEROCLAW), "--config-dir", args.config_dir]
    run("Invoice Guardian: loaded skill", runtime + ["skills", "list", "--agent", "invoice_guardian"])
    run(
        "Live local ZeroClaw agent: custody boundary",
        runtime
        + [
            "agent",
            "--agent",
            "invoice_guardian",
            "--message",
            "Using only the loaded skill and without invoking any tool, answer in one sentence: what is this agent custody tier and does it hold wallet keys?",
        ],
    )
    run(
        "Accepted unsigned Solana Pay request",
        [sys.executable, "-B", "scripts/invoice_guardian.py", "--policy", "config/policy.example.json", "--request", "fixtures/valid_invoice.json"],
    )
    run(
        "Fail-closed over-cap request",
        [sys.executable, "-B", "scripts/invoice_guardian.py", "--policy", "config/policy.example.json", "--request", "fixtures/over_cap_invoice.json"],
        expected_codes=(2,),
    )
    run(
        "Fail-closed injection-shaped recipient",
        [sys.executable, "-B", "scripts/invoice_guardian.py", "--policy", "config/policy.example.json", "--request", "fixtures/injection_attempt_invoice.json"],
        expected_codes=(2,),
    )
    run("Validated deterministic reference-poll SOP", runtime + ["sop", "validate", "solana-reference-poll"])
    run(
        "Read-only public Solana RPC observation",
        [
            sys.executable,
            "-B",
            "scripts/reference_check.py",
            "--reference",
            "SysvarC1ock11111111111111111111111111111111",
        ],
    )
    print("\nDemo complete: no wallet, transaction, payment, or settlement claim was made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
