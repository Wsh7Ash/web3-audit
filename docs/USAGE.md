# Usage

## Install

```bash
python -m pip install -e .
web3-audit --version
```

## Scan a repository

```bash
web3-audit scan ./contracts
web3-audit scan ./contracts --min-severity medium
web3-audit scan ./contracts --json > scan.json
web3-audit scan ./contracts --fail-on high   # CI gate: exit 1 on any high finding
web3-audit scan --rules                      # list the eleven rule ids
```

## Turn scanner output into findings

1. Group hits by rule and file (`--json` makes this trivial).
2. Read each group in code and decide whether the pattern is reachable and harmful.
3. Report confirmed issues with the rule id as a cross-reference.
4. Put the rest in an appendix labelled false positive with a reason.

`reporting-scanner-leads` and `triage-exploitability-verdict` walk this in detail.

## Pick skills for the review stage

```bash
web3-audit list --phase recon
web3-audit list --phase invariants
web3-audit show reentrancy-checks-effects-interactions
```

A workable order:

1. `recon-scope-contracts`, `recon-bytecode-match` — know what you are reviewing.
2. `model-privilege-graph`, `model-accounting-identity` — write what must be true.
3. `invariants-write-in-solidity`, `invariants-fuzz-handlers` — make it checkable.
4. `reentrancy-trace-external-calls`, `arithmetic-rounding-direction`, `oracle-stale-price` — review
   where value moves.
5. `storage-layout-collision`, `upgrade-initializer-reinit` — review the proxy.
6. `testing-fork-reproduction`, `testing-minimal-sequence`, `testing-negative-control` — prove it.
7. `reporting-finding-template`, `reporting-severity-basis` — write it up.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | clean at the requested threshold |
| 1 | a finding at or above `--fail-on` |
| 2 | usage error: missing path, unknown severity, unknown command |
