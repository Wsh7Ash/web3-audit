"""web3-audit corpus: pack metadata plus 50 authored Solidity review skills."""

from __future__ import annotations

from typing import Any

from ..model import skill_from_dict
from .part1 import SKILLS as PART1
from .part2 import SKILLS as PART2
from .part3 import SKILLS as PART3

PACK: dict[str, Any] = {
    "name": "web3-audit",
    "version": "1.0.0",
    "category": "web3-security",
    "license": "MIT",
    "runtime": "Claude Code, opencode, or any agent runtime that loads SKILL.md files",
    "description": (
        "50 validated skills for reviewing Solidity: scope and bytecode recon, "
        "state models and invariants, access control, reentrancy, arithmetic, "
        "oracles, storage layout, upgrades, randomness, testing, reporting and triage."
    ),
    "expected_skills": 50,
}

SKILLS: list[Any] = [skill_from_dict(raw) for raw in (*PART1, *PART2, *PART3)]
BY_SLUG: dict[str, Any] = {skill.slug: skill for skill in SKILLS}

__all__ = ["PACK", "SKILLS", "BY_SLUG"]
