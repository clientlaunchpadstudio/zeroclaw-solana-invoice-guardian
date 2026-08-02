from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "invoice_guardian.py"
POLICY = ROOT / "config" / "policy.example.json"
DEMO_SCRIPT = ROOT / "scripts" / "demo_session.py"


def run_fixture(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--policy", str(POLICY), "--request", str(ROOT / "fixtures" / name)],
        check=False,
        capture_output=True,
        text=True,
    )


def load_demo_session_module():
    spec = importlib.util.spec_from_file_location("invoice_guardian_demo_session", DEMO_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load demo_session.py for isolated testing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InvoiceGuardianTests(unittest.TestCase):
    def test_valid_invoice_creates_unsigned_solana_pay_url(self) -> None:
        result = run_fixture("valid_invoice.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["accepted"])
        self.assertEqual(payload["custody_tier"], "T1")
        self.assertEqual(payload["signing"], "not performed")
        self.assertEqual(payload["network"], "not contacted")
        self.assertTrue(payload["solana_pay_url"].startswith("solana:11111111111111111111111111111111?"))
        self.assertIn("amount=12.5", payload["solana_pay_url"])

    def test_over_cap_request_is_rejected(self) -> None:
        result = run_fixture("over_cap_invoice.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("exceeds the local cap", result.stderr)

    def test_prompt_injection_shaped_destination_is_rejected(self) -> None:
        result = run_fixture("injection_attempt_invoice.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("base58 Solana address", result.stderr)

    def test_reference_checker_rejects_an_unapproved_rpc_host_without_network(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "reference_check.py"),
                "--reference",
                "SysvarC1ock11111111111111111111111111111111",
                "--rpc-url",
                "https://unapproved.example",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("fixed to the approved public Solana endpoint", result.stderr)

    def test_demo_runner_includes_fixed_host_read_only_observation(self) -> None:
        demo = load_demo_session_module()
        calls: list[tuple[str, list[str], tuple[int, ...]]] = []

        def capture_run(title: str, command: list[str], expected_codes: tuple[int, ...] = (0,)) -> None:
            calls.append((title, command, expected_codes))

        with mock.patch.object(demo, "run", side_effect=capture_run), mock.patch.object(
            sys, "argv", ["demo_session.py", "--config-dir", "test-state"]
        ):
            self.assertEqual(demo.main(), 0)

        titles = [title for title, _, _ in calls]
        self.assertEqual(titles[-2:], ["Validated deterministic reference-poll SOP", "Read-only public Solana RPC observation"])
        observation_command = calls[-1][1]
        self.assertEqual(
            observation_command,
            [
                sys.executable,
                "-B",
                "scripts/reference_check.py",
                "--reference",
                "SysvarC1ock11111111111111111111111111111111",
            ],
        )


if __name__ == "__main__":
    unittest.main()
