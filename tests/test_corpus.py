"""Corpus rules, generated artifacts and the CLI surface for web3-audit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from web3audit.corpus import BY_SLUG, PACK, SKILLS
from web3audit.render import build_pack, render_skill, sha256_of, word_count
from web3audit.validate import (
    MIN_PATTERNS,
    MIN_PITFALLS,
    MIN_SIGNALS,
    MIN_STEPS,
    MIN_WORDS,
    PHASES,
    validate_pack,
)

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = 50


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


def test_pack_declares_fifty_and_delivers_fifty() -> None:
    assert PACK["expected_skills"] == EXPECTED
    assert len(SKILLS) == EXPECTED


def test_slugs_titles_and_summaries_are_unique() -> None:
    assert len({s.slug for s in SKILLS}) == EXPECTED
    assert len({s.title.lower() for s in SKILLS}) == EXPECTED
    assert len({s.summary for s in SKILLS}) == EXPECTED


def test_every_skill_passes_every_rule() -> None:
    assert validate_pack(PACK, SKILLS) == []


def test_all_phases_are_represented() -> None:
    assert {s.meta_get("phase") for s in SKILLS} == PHASES


def test_strength_floors_hold_for_every_skill() -> None:
    for skill in SKILLS:
        assert len(skill.steps) >= MIN_STEPS, skill.slug
        assert len(skill.signals) >= MIN_SIGNALS, skill.slug
        assert len(skill.patterns) >= MIN_PATTERNS, skill.slug
        assert len(skill.pitfalls) >= MIN_PITFALLS, skill.slug
        assert word_count(render_skill(PACK, skill)) >= MIN_WORDS, skill.slug


def test_every_reference_is_https_and_labelled() -> None:
    for skill in SKILLS:
        assert skill.refs, skill.slug
        for ref in skill.refs:
            assert ref.startswith("[") and "](https://" in ref, f"{skill.slug}: {ref}"


def test_slugs_are_kebab_case() -> None:
    for skill in SKILLS:
        assert skill.slug == skill.slug.lower(), skill.slug
        assert " " not in skill.slug and "_" not in skill.slug, skill.slug


def test_lookup_index_covers_the_corpus() -> None:
    assert set(BY_SLUG) == {s.slug for s in SKILLS}


def test_committed_skills_match_a_fresh_render() -> None:
    for skill in SKILLS:
        path = ROOT / "skills" / skill.slug / "SKILL.md"
        assert path.is_file(), f"missing generated file for {skill.slug}"
        assert path.read_text(encoding="utf-8") == render_skill(PACK, skill), skill.slug


def test_pack_json_lists_fifty_skills_with_digests() -> None:
    manifest = json.loads((ROOT / "pack.json").read_text(encoding="utf-8"))
    assert manifest["skill_count"] == EXPECTED
    assert len(manifest["skills"]) == EXPECTED
    assert all(len(entry["sha256"]) == 64 for entry in manifest["skills"])
    assert {entry["slug"] for entry in manifest["skills"]} == set(BY_SLUG)


def test_manifest_digests_match_committed_files() -> None:
    manifest = json.loads((ROOT / "pack.json").read_text(encoding="utf-8"))
    for entry in manifest["skills"]:
        path = ROOT / "skills" / entry["slug"] / "SKILL.md"
        assert sha256_of(path.read_text(encoding="utf-8")) == entry["sha256"], entry["slug"]


def test_build_is_deterministic() -> None:
    first = build_pack(None, PACK, SKILLS)
    second = build_pack(None, PACK, SKILLS)
    assert first == second
    assert len(first) == EXPECTED + 2


def test_catalog_lists_every_skill() -> None:
    catalog = (ROOT / "results" / "catalog.md").read_text(encoding="utf-8")
    for skill in SKILLS:
        assert f"`{skill.slug}`" in catalog


def test_cli_validate_reports_fifty_of_fifty() -> None:
    result = run_cli("validate")
    assert result.returncode == 0, result.stderr
    assert "50/50 skills valid" in result.stdout


def test_cli_validate_json_is_machine_readable() -> None:
    payload = json.loads(run_cli("validate", "--json").stdout)
    assert payload["valid"] == EXPECTED
    assert payload["passed"] is True
    assert payload["issues"] == []
    assert payload["floors"]["min_words"] == MIN_WORDS


def test_cli_list_filters_by_phase() -> None:
    result = run_cli("list", "--phase", "reentrancy")
    assert result.returncode == 0
    assert result.stdout.strip().splitlines()[-1] == "5 skill(s)"


def test_cli_show_prints_one_skill() -> None:
    result = run_cli("show", "recon-scope-contracts")
    assert result.returncode == 0
    assert result.stdout.startswith("---")
    assert "Enumerate the contracts" in result.stdout


def test_cli_show_rejects_unknown_slug() -> None:
    result = run_cli("show", "nope")
    assert result.returncode == 2
    assert "unknown slug" in result.stderr


def test_cli_version_is_printed() -> None:
    result = run_cli("--version")
    assert result.returncode == 0
    assert "web3-audit 1.0.0" in result.stdout


@pytest.mark.parametrize("command", ["render", "catalog", "build"])
def test_cli_build_commands_succeed(command: str) -> None:
    assert run_cli(command).returncode == 0