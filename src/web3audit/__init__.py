"""web3-audit: Solidity review skills plus a line-oriented static scanner."""

from __future__ import annotations

from .cli import main
from .model import Skill, skill_from_dict
from .render import build_pack, render_catalog, render_skill, sha256_of, word_count
from .scanner import (
    RULE_IDS,
    RULES,
    SEVERITIES,
    Finding,
    scan_path,
    scan_text,
    summarise,
    to_json,
    to_text,
)
from .validate import PHASES, validate_pack, validate_skill

__all__ = [
    "main",
    "Skill",
    "skill_from_dict",
    "build_pack",
    "render_catalog",
    "render_skill",
    "sha256_of",
    "word_count",
    "RULE_IDS",
    "RULES",
    "SEVERITIES",
    "Finding",
    "scan_path",
    "scan_text",
    "summarise",
    "to_json",
    "to_text",
    "PHASES",
    "validate_pack",
    "validate_skill",
]
