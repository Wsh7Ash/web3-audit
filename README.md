# web3-audit

**50 validated Solidity review skills plus a line-oriented static scanner with stable rule ids.**

The scanner does not pretend to be Slither. It reports the eleven shapes that carry most of the
risk in practice, at the exact line, with an id you can deduplicate and cite. The skills cover
what the scanner cannot: recon, state models, invariants, access paths, oracle trust, storage
layout, upgrade mechanics, randomness, testing and triage.

```
$ web3-audit scan examples/vulnerable.sol
examples/vulnerable.sol:2   LOW    floating-pragma: floating pragma compiles under future compiler versions with different semantics
examples/vulnerable.sol:10  HIGH   reentrancy-order: external call on line 10 precedes the state write on line 11
examples/vulnerable.sol:10  HIGH   unchecked-call: low-level call return value is not checked, so a failed call continues execution
examples/vulnerable.sol:14  MEDIUM privileged-function: state-changing privileged function has no visible access modifier in its declaration or first lines
examples/vulnerable.sol:19  MEDIUM weak-randomness: block values used with modulo are predictable or miner-influenced and are not a randomness source
examples/vulnerable.sol:23  LOW    timestamp-comparison: exact block.timestamp comparison is miner-influenced and should be a range check
summary: info=0, low=2, medium=2, high=2, total=6

$ web3-audit scan examples/safe.sol
no findings
```

## Rules

| Rule id | Severity | What it matches |
|---|---|---|
| `tx-origin-auth` | high | authorisation that compares `tx.origin` |
| `delegatecall` | high | any `delegatecall`, because the target runs against your storage |
| `selfdestruct` | medium | `selfdestruct` / `suicide` |
| `unchecked-call` | high | low-level `.call` with no `require`/`success` check nearby |
| `unchecked-arithmetic` | high | pre-0.8 pragma without SafeMath and an arithmetic assignment |
| `floating-pragma` | low | `pragma solidity ^` or a range |
| `weak-randomness` | medium | block entropy combined with `%` on the same line |
| `timestamp-comparison` | low | exact `block.timestamp` comparison |
| `privileged-function` | medium | mint/burn/pause/upgrade/setOwner/setFee/sweep with no visible guard |
| `reentrancy-order` | high | external call before a state write in the same function |
| `approve-race` | low | `approve` with no current-allowance check |

Every rule is line-oriented and documented as a heuristic. `privileged-function` deliberately does
not flag `withdraw`: a public withdraw is normal, and flagging it is the classic false positive that
trains reviewers to ignore the scanner.

## Commands

| Command | What it does |
|---|---|
| `web3-audit validate [--json]` | Check every skill against the corpus rules |
| `web3-audit list [--phase P]` | List skills, filtered by one of 13 phases |
| `web3-audit show SLUG` | Print one rendered `SKILL.md` |
| `web3-audit render` / `catalog` / `build` | Regenerate committed artifacts |
| `web3-audit scan PATH [--json] [--min-severity S] [--fail-on S] [--rules]` | Scan a `.sol` file or directory |

`scan` exit codes: `0` no findings at or above `--fail-on` (or the flag was absent), `1` a finding
at or above `--fail-on`, `2` usage error. That makes `web3-audit scan contracts --fail-on high` a
usable CI gate without parsing text.

## Phases and counts

| Phase | Skills | Focus |
|---|---|---|
| `recon` | 3 | scope, bytecode match, value flow |
| `model` | 3 | state machine, accounting identity, privilege graph |
| `invariants` | 4 | Solidity assertions, fuzz handlers, differential, failure paths |
| `access` | 5 | missing modifiers, role grants, initializers, signature replay, renounce |
| `reentrancy` | 5 | call tracing, CEI order, read-only, cross-function, flash loans |
| `arithmetic` | 4 | rounding, precision, unchecked blocks, share inflation |
| `oracle` | 4 | staleness, decimals, TWAP cost, fallbacks |
| `storage` | 4 | layout collisions, delete gaps, array removal, packing |
| `upgrade` | 4 | re-initialization, gaps, authority, selector collision |
| `randomness` | 3 | block values, commit-reveal, VRF |
| `testing` | 5 | fork pinning, minimal sequence, control, state diffs, gas |
| `reporting` | 4 | finding template, severity basis, scanner leads, fix verification |
| `triage` | 2 | duplicates, exploitability verdict |

## Install

```bash
python -m pip install -e .
web3-audit validate
web3-audit scan ./contracts --min-severity medium
```

No dependencies. Python 3.10+.

## Layout

```
src/web3audit/
  model.py     immutable Skill shape
  validate.py  per-skill and package rules
  render.py    deterministic SKILL.md, catalog, manifest
  scanner.py   11 line-oriented rules, severity filter, JSON/text output
  cli.py       validate/list/show/render/catalog/build/scan
  corpus/      50 authored skills
examples/      vulnerable.sol and safe.sol used by the tests and the transcript
skills/        50 generated SKILL.md files
tests/         56 tests: every rule positive and negative, CLI exit codes, corpus drift
```

## Limits

- **Not a substitute for Slither or a human review.** The rules are line-oriented and have no
  control-flow or taint analysis.
- **No compiler integration.** The scanner reads text; it does not resolve imports, evaluate
  constants or know your inheritance graph.
- **`unchecked-arithmetic` is pragma-gated and SafeMath-approximate**; a project that uses a custom
  math library will be flagged until `SafeMath` appears in the file or the pragma is 0.8+.
- **`reentrancy-order` is a same-function heuristic.** It does not follow calls across functions.
- **The example contracts are teaching fixtures, not audited code.**

## License

MIT.
