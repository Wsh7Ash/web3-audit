# Changelog

## 1.0.0 — 2026-10-30

Initial release.

- 50 authored skills across 13 phases: recon, model, invariants, access, reentrancy, arithmetic, oracle, storage, upgrade, randomness, testing, reporting, triage.
- Eleven line-oriented scanner rules with stable ids, severities, line numbers and snippets.
- `scan` with `--json`, `--min-severity`, `--fail-on` and `--rules`; exit codes suitable for CI.
- Committed skills, manifest with sha256 digests, catalog; all drift-checked.
- 56 tests, including positive and negative coverage for every rule.
