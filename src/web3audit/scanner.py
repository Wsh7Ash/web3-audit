"""A small, honest Solidity scanner.

The rules are line-oriented and deliberately conservative: each one reports the
line it matched, the rule that matched, and why the match matters. None of them
claim to prove exploitable, and the report says so. What they do is put a
reviewer in front of the lines that carry most of the risk in practice,
with a stable rule identifier so findings can be deduplicated across runs.

Every rule is a pure function of (path, lines). Adding a rule means adding a
function with the CONTRACT below and registering it in RULES.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

SEVERITIES = ("info", "low", "medium", "high")
SEVERITY_RANK = {name: index for index, name in enumerate(SEVERITIES)}


@dataclass(frozen=True)
class Finding:
    """One rule match at one line."""

    rule: str
    severity: str
    path: str
    line: int
    message: str
    snippet: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


Rule = Callable[[str, Sequence[str]], Iterable[Finding]]


def _finding(rule: str, severity: str, path: str, line: int, message: str, text: str) -> Finding:
    return Finding(
        rule=rule,
        severity=severity,
        path=path,
        line=line,
        message=message,
        snippet=text.strip()[:200],
    )


def _pragma_version(lines: Sequence[str]) -> tuple[int, int] | None:
    for raw in lines:
        match = re.search(r"pragma\s+solidity\s+[^;]*?(\d+)\.(\d+)", raw)
        if match:
            return int(match.group(1)), int(match.group(2))
    return None


def rule_tx_origin_auth(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    for number, text in enumerate(lines, start=1):
        if re.search(r"require\s*\([^)]*tx\.origin", text) or re.search(
            r"if\s*\([^)]*tx\.origin", text
        ):
            yield _finding(
                "tx-origin-auth",
                "high",
                path,
                number,
                "authorisation compares tx.origin, which any contract can satisfy by forwarding a call",
                text,
            )


def rule_delegatecall(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    for number, text in enumerate(lines, start=1):
        if ".delegatecall(" in text:
            yield _finding(
                "delegatecall",
                "high",
                path,
                number,
                "delegatecall runs target code against this contract's storage; the target must be immutable and trusted",
                text,
            )


def rule_selfdestruct(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    for number, text in enumerate(lines, start=1):
        if re.search(r"\bselfdestruct\s*\(", text) or re.search(r"\bsuicide\s*\(", text):
            yield _finding(
                "selfdestruct",
                "medium",
                path,
                number,
                "selfdestruct removes code and can strand funds or break dependents",
                text,
            )


def rule_unchecked_low_level_call(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    for number, text in enumerate(lines, start=1):
        if re.search(r"\.call\s*(?:\{[^}]*\})?\s*\(", text):
            window = " ".join(lines[max(0, number - 3) : number + 2])
            if not re.search(r"(require|assert|bool\s+success|success\s*=)", window):
                yield _finding(
                    "unchecked-call",
                    "high",
                    path,
                    number,
                    "low-level call return value is not checked, so a failed call continues execution",
                    text,
                )


def rule_unchecked_arithmetic(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    version = _pragma_version(lines)
    if version is None or version >= (0, 8):
        return
    joined = "\n".join(lines)
    if "SafeMath" in joined or "using SafeMath" in joined:
        return
    for number, text in enumerate(lines, start=1):
        if re.search(r"[+\-*]\s*=|=\s*[^=;]+[+\-*][^=;]+;", text) and "for (" not in text:
            yield _finding(
                "unchecked-arithmetic",
                "high",
                path,
                number,
                f"pragma {version[0]}.{version[1]} has wrapping arithmetic and no SafeMath usage was found",
                text,
            )


def rule_floating_pragma(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    for number, text in enumerate(lines, start=1):
        if re.search(r"pragma\s+solidity\s+[\^~>]", text):
            yield _finding(
                "floating-pragma",
                "low",
                path,
                number,
                "floating pragma compiles under future compiler versions with different semantics",
                text,
            )


ENTROPY_SOURCE = re.compile(
    r"block\.(timestamp|difficulty|prevrandao|blockhash|number|coinbase)|\bblockhash\s*\(|\bnow\b"
)


def rule_block_timestamp_randomness(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    for number, text in enumerate(lines, start=1):
        # A modulo anywhere on a line that also derives from block entropy is the
        # shape that matters: hashing first does not add unpredictability.
        if ENTROPY_SOURCE.search(text) and "%" in text:
            yield _finding(
                "weak-randomness",
                "medium",
                path,
                number,
                "block values used with modulo are predictable or miner-influenced and are not a randomness source",
                text,
            )


def rule_timestamp_comparison(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    for number, text in enumerate(lines, start=1):
        if re.search(r"block\.timestamp\s*(==|<=|>=|<|>)", text) or re.search(
            r"(==|<=|>=|<|>)\s*block\.timestamp", text
        ):
            yield _finding(
                "timestamp-comparison",
                "low",
                path,
                number,
                "exact block.timestamp comparison is miner-influenced and should be a range check",
                text,
            )


def rule_privileged_function(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    guarded_window = 4
    for number, text in enumerate(lines, start=1):
        if re.search(
            r"function\s+\w*(mint|burn|pause|unpause|upgrade|setOwner|setFee|setAdmin|sweep|rescue|transferOwnership)\w*\s*\(",
            text,
        ):
            window = " ".join(lines[max(0, number - 1) : number + guarded_window])
            if not re.search(r"(onlyOwner|onlyAdmin|onlyRole|onlyGovernance|requiresAuth|modifier)", window):
                yield _finding(
                    "privileged-function",
                    "medium",
                    path,
                    number,
                    "state-changing privileged function has no visible access modifier in its declaration or first lines",
                    text,
                )


def rule_reentrancy_order(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    """External call before a state write in the same function body (CWE-841 heuristic)."""
    in_function = False
    call_line = 0
    for number, text in enumerate(lines, start=1):
        if re.search(r"function\s+\w+", text):
            in_function = True
            call_line = 0
        if not in_function:
            continue
        if re.search(r"\.call\s*(?:\{[^}]*\})?\s*\(|\.transfer\s*\(|\.send\s*\(", text):
            call_line = number
            continue
        if call_line and re.search(r"^\s*[A-Za-z_]\w*(\[[^\]]*\])?\s*(=|\+=|-=)", text):
            yield _finding(
                "reentrancy-order",
                "high",
                path,
                call_line,
                f"external call on line {call_line} precedes the state write on line {number}",
                lines[call_line - 1],
            )
            call_line = 0
        if text.strip().endswith("}"):
            in_function = False
            call_line = 0


def rule_approve_race(path: str, lines: Sequence[str]) -> Iterable[Finding]:
    for number, text in enumerate(lines, start=1):
        if re.search(r"function\s+approve\s*\(", text):
            window = " ".join(lines[max(0, number - 1) : number + 8])
            if not re.search(r"(currentAllowance|safeApprove|increaseAllowance|require\s*\(\s*value\s*==\s*0)", window):
                yield _finding(
                    "approve-race",
                    "low",
                    path,
                    number,
                    "approve overwrites allowance without checking the current value, which is the classic approve race",
                    text,
                )


RULES: tuple[Rule, ...] = (
    rule_tx_origin_auth,
    rule_delegatecall,
    rule_selfdestruct,
    rule_unchecked_low_level_call,
    rule_unchecked_arithmetic,
    rule_floating_pragma,
    rule_block_timestamp_randomness,
    rule_timestamp_comparison,
    rule_privileged_function,
    rule_reentrancy_order,
    rule_approve_race,
)

RULE_IDS: tuple[str, ...] = (
    "tx-origin-auth",
    "delegatecall",
    "selfdestruct",
    "unchecked-call",
    "unchecked-arithmetic",
    "floating-pragma",
    "weak-randomness",
    "timestamp-comparison",
    "privileged-function",
    "reentrancy-order",
    "approve-race",
)


def scan_text(text: str, path: str = "<memory>") -> list[Finding]:
    """Scan Solidity source text and return findings ordered by line then rule."""
    lines = text.splitlines()
    findings: list[Finding] = []
    for rule in RULES:
        findings.extend(rule(path, lines))
    findings.sort(key=lambda f: (f.line, f.rule))
    return findings


def scan_path(target: str | Path, min_severity: str = "info") -> list[Finding]:
    """Scan a file or every ``.sol`` file under a directory."""
    root = Path(target)
    if min_severity not in SEVERITY_RANK:
        raise ValueError(f"unknown severity: {min_severity} (expected one of {SEVERITIES})")

    files: list[Path]
    if root.is_dir():
        files = sorted(root.rglob("*.sol"))
    elif root.is_file():
        files = [root]
    else:
        raise FileNotFoundError(f"no such target: {target}")

    threshold = SEVERITY_RANK[min_severity]
    findings: list[Finding] = []
    for file in files:
        text = file.read_text(encoding="utf-8", errors="replace")
        findings.extend(scan_text(text, str(file)))
    return [f for f in findings if SEVERITY_RANK[f.severity] >= threshold]


def summarise(findings: Sequence[Finding]) -> dict[str, int]:
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        counts[finding.severity] += 1
    counts["total"] = len(findings)
    return counts


def to_json(findings: Sequence[Finding]) -> str:
    payload = {
        "findings": [f.to_dict() for f in findings],
        "summary": summarise(findings),
    }
    return json.dumps(payload, indent=2) + "\n"


def to_text(findings: Sequence[Finding]) -> str:
    lines: list[str] = []
    for finding in findings:
        lines.append(
            f"{finding.path}:{finding.line}  {finding.severity.upper():6s} {finding.rule}: {finding.message}"
        )
        lines.append(f"    {finding.snippet}")
    counts = summarise(findings)
    lines.append(
        "summary: "
        + ", ".join(f"{severity}={counts[severity]}" for severity in SEVERITIES)
        + f", total={counts['total']}"
    )
    return "\n".join(lines)


__all__ = [
    "SEVERITIES",
    "SEVERITY_RANK",
    "Finding",
    "RULES",
    "RULE_IDS",
    "scan_text",
    "scan_path",
    "summarise",
    "to_json",
    "to_text",
]