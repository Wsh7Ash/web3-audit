"""Behavioural tests for the Solidity scanner."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from web3audit.scanner import (
    RULE_IDS,
    SEVERITIES,
    scan_path,
    scan_text,
    summarise,
    to_json,
    to_text,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def rules_of(findings) -> set[str]:
    return {f.rule for f in findings}


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "web3audit", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={"PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8"},
        timeout=120,
    )


# ------------------------------------------------------------------ rule by rule


def test_tx_origin_auth_is_flagged() -> None:
    source = "contract C { function f() external { require(tx.origin == owner); } }"
    assert "tx-origin-auth" in rules_of(scan_text(source))


def test_delegatecall_is_flagged() -> None:
    source = "contract C { function f(address t) external { t.delegatecall(\"\"); } }"
    assert "delegatecall" in rules_of(scan_text(source))


def test_selfdestruct_is_flagged() -> None:
    source = "contract C { function f() external { selfdestruct(payable(msg.sender)); } }"
    assert "selfdestruct" in rules_of(scan_text(source))


def test_unchecked_call_is_flagged() -> None:
    source = (
        "contract C {\n"
        "  function f() external {\n"
        "    (bool ok, ) = msg.sender.call{value: 1}(\"\");\n"
        "    balances[msg.sender] = 0;\n"
        "  }\n"
        "}"
    )
    assert "unchecked-call" in rules_of(scan_text(source))


def test_checked_call_is_not_flagged() -> None:
    source = (
        "contract C {\n"
        "  function f() external {\n"
        "    (bool ok, ) = msg.sender.call{value: 1}(\"\");\n"
        "    require(ok, \"failed\");\n"
        "  }\n"
        "}"
    )
    assert "unchecked-call" not in rules_of(scan_text(source))


def test_unchecked_arithmetic_flagged_only_before_0_8_without_safemath() -> None:
    pre = "pragma solidity ^0.7.6;\ncontract C { function f() external { x += 1; } }"
    assert "unchecked-arithmetic" in rules_of(scan_text(pre))

    post = "pragma solidity ^0.8.20;\ncontract C { function f() external { x += 1; } }"
    assert "unchecked-arithmetic" not in rules_of(scan_text(post))

    safe = (
        "pragma solidity ^0.7.6;\n"
        "import SafeMath.sol;\n"
        "contract C { using SafeMath for uint256; function f() external { x = x.add(1); } }"
    )
    assert "unchecked-arithmetic" not in rules_of(scan_text(safe))


def test_floating_pragma_is_flagged_but_pinned_is_not() -> None:
    assert "floating-pragma" in rules_of(scan_text("pragma solidity ^0.8.20;"))
    assert "floating-pragma" not in rules_of(scan_text("pragma solidity 0.8.20;"))


def test_weak_randomness_is_flagged_through_a_hash() -> None:
    source = (
        "contract C { function r() external view returns (uint256) { "
        "return uint256(keccak256(abi.encodePacked(block.timestamp))) % 10; } }"
    )
    assert "weak-randomness" in rules_of(scan_text(source))


def test_timestamp_comparison_is_flagged() -> None:
    assert "timestamp-comparison" in rules_of(
        scan_text("contract C { function f() external view returns (bool) { return block.timestamp > 1; } }")
    )


def test_privileged_function_without_modifier_is_flagged() -> None:
    source = "contract C { function setOwner(address a) external { owner = a; } }"
    assert "privileged-function" in rules_of(scan_text(source))


def test_public_withdraw_is_not_treated_as_privileged() -> None:
    source = "contract C { function withdraw(uint256 a) external { balances[msg.sender] -= a; } }"
    assert "privileged-function" not in rules_of(scan_text(source))


def test_privileged_function_with_only_owner_is_not_flagged() -> None:
    source = "contract C { function setOwner(address a) external onlyOwner { owner = a; } }"
    assert "privileged-function" not in rules_of(scan_text(source))


def test_reentrancy_order_is_flagged() -> None:
    source = (
        "contract C {\n"
        "  function f() external {\n"
        "    (bool ok, ) = msg.sender.call{value: 1}(\"\");\n"
        "    balances[msg.sender] = 0;\n"
        "  }\n"
        "}"
    )
    assert "reentrancy-order" in rules_of(scan_text(source))


def test_checks_effects_interactions_is_not_flagged() -> None:
    source = (
        "contract C {\n"
        "  function f() external {\n"
        "    balances[msg.sender] = 0;\n"
        "    (bool ok, ) = msg.sender.call{value: 1}(\"\");\n"
        "    require(ok, \"failed\");\n"
        "  }\n"
        "}"
    )
    assert "reentrancy-order" not in rules_of(scan_text(source))


def test_approve_race_is_flagged() -> None:
    source = "contract C { function approve(address s, uint256 v) external { allowance[msg.sender][s] = v; } }"
    assert "approve-race" in rules_of(scan_text(source))


def test_approve_with_allowance_check_is_not_flagged() -> None:
    source = (
        "contract C { function approve(address s, uint256 v) external { "
        "require(value == 0 || allowance[msg.sender][s] == 0); allowance[msg.sender][s] = v; } }"
    )
    assert "approve-race" not in rules_of(scan_text(source))


# ------------------------------------------------------------------- collections


def test_findings_carry_line_numbers_and_snippets() -> None:
    source = "line one\ncontract C { function f() external { selfdestruct(payable(msg.sender)); } }"
    findings = scan_text(source)
    assert findings
    assert all(f.line >= 1 and f.snippet for f in findings)


def test_findings_are_sorted_by_line_then_rule() -> None:
    findings = scan_text((EXAMPLES / "vulnerable.sol").read_text(encoding="utf-8"))
    keys = [(f.line, f.rule) for f in findings]
    assert keys == sorted(keys)


def test_every_rule_id_is_registered_and_used() -> None:
    findings = scan_path(EXAMPLES)
    assert rules_of(findings) <= set(RULE_IDS)
    assert len(RULE_IDS) == len(set(RULE_IDS)) == 11


def test_vulnerable_example_triggers_the_high_rules() -> None:
    findings = scan_path(EXAMPLES / "vulnerable.sol")
    assert {"reentrancy-order", "unchecked-call"} <= rules_of(findings)


def test_safe_example_has_no_findings() -> None:
    assert scan_path(EXAMPLES / "safe.sol") == []


def test_min_severity_filters() -> None:
    high_only = scan_path(EXAMPLES, min_severity="high")
    assert high_only
    assert all(f.severity == "high" for f in high_only)
    assert len(high_only) <= len(scan_path(EXAMPLES))


def test_unknown_severity_raises() -> None:
    with pytest.raises(ValueError):
        scan_path(EXAMPLES, min_severity="critical")


def test_missing_path_raises() -> None:
    with pytest.raises(FileNotFoundError):
        scan_path(EXAMPLES / "does-not-exist.sol")


def test_summary_counts_match_findings() -> None:
    findings = scan_path(EXAMPLES)
    counts = summarise(findings)
    assert counts["total"] == len(findings)
    assert sum(counts[s] for s in SEVERITIES) == len(findings)


def test_json_output_is_parseable() -> None:
    payload = json.loads(to_json(scan_path(EXAMPLES)))
    assert payload["summary"]["total"] == len(payload["findings"])
    assert all(set(f) == {"rule", "severity", "path", "line", "message", "snippet"} for f in payload["findings"])


def test_text_output_names_every_finding() -> None:
    findings = scan_path(EXAMPLES)
    text = to_text(findings)
    for finding in findings:
        assert f"{finding.path}:{finding.line}" in text


# ------------------------------------------------------------------------- CLI


def test_cli_scan_text_output() -> None:
    result = run_cli("scan", "examples/vulnerable.sol")
    assert result.returncode == 0
    assert "reentrancy-order" in result.stdout
    assert "summary:" in result.stdout


def test_cli_scan_json_output() -> None:
    payload = json.loads(run_cli("scan", "examples", "--json").stdout)
    assert payload["summary"]["total"] >= 1


def test_cli_fail_on_high_exits_nonzero_for_vulnerable() -> None:
    assert run_cli("scan", "examples/vulnerable.sol", "--fail-on", "high").returncode == 1


def test_cli_fail_on_high_exits_zero_for_safe() -> None:
    result = run_cli("scan", "examples/safe.sol", "--fail-on", "high")
    assert result.returncode == 0
    assert "no findings" in result.stdout


def test_cli_scan_lists_rules() -> None:
    result = run_cli("scan", "--rules")
    assert result.returncode == 0
    assert "reentrancy-order" in result.stdout
    assert len(result.stdout.strip().splitlines()) == 11


def test_cli_scan_missing_path_exits_2() -> None:
    result = run_cli("scan", "examples/nope.sol")
    assert result.returncode == 2
    assert "no such target" in result.stderr


def test_cli_scan_requires_a_path() -> None:
    assert run_cli("scan").returncode == 2