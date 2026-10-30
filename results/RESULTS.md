# Results

Reproducible evidence for the claims in `README.md`.

## Environment

- OS: Windows (MSYS2 shell), Python 3.14
- Runtime: Python 3.10+ standard library only; `pytest` as a dev dependency
- Network: not required

## 1. Corpus validation

```
$ PYTHONPATH=src python -m web3audit validate
50/50 skills valid

$ PYTHONPATH=src python -m web3audit build
Built 52 artifacts, 9786 rendered skill words
```

## 2. Test suite

```
$ python -m pytest -q
........................................................                 [100%]
```

56 tests. Each scanner rule is tested both positively and negatively:

- `tx-origin-auth`, `delegatecall`, `selfdestruct` fire on their shapes.
- `unchecked-call` fires on an unchecked `.call` and does **not** fire when `require(ok)` follows.
- `unchecked-arithmetic` fires on `pragma ^0.7.6` with `x += 1`, and does not fire on `^0.8.20` or
  when SafeMath is used.
- `floating-pragma` fires on `^0.8.20` and not on pinned `0.8.20`.
- `weak-randomness` fires through `keccak256(...block.timestamp...) % 10`.
- `privileged-function` fires on an unguarded `setOwner`, and does **not** fire on a public
  `withdraw` or on `setOwner ... onlyOwner`.
- `reentrancy-order` fires on call-then-write and not on write-then-call.
- `approve-race` fires without an allowance check and not with one.
- Findings are sorted by line then rule and always carry a line and snippet.
- `scan_path` filters by severity, rejects an unknown severity and raises on a missing path.
- `summarise` totals agree with the findings; JSON keys are exact; text names every hit.
- CLI: `--fail-on high` exits 1 on `examples/vulnerable.sol` and 0 on `examples/safe.sol`;
  `scan --rules` lists 11 rules; missing path and missing argument exit 2.

## 3. Scanner runs on committed fixtures

`results/demo_transcript.txt` records verbatim:

- `examples/vulnerable.sol` → 6 findings (2 low, 2 medium, 2 high).
- `examples/safe.sol` → `no findings`.
- `--fail-on high` exit codes of 1 and 0 for those two files.
- `--min-severity high --json` → 2 findings, both `high`.

## 4. Defects found while building this

1. **`privileged-function` matched `withdraw`**, so the "safe" example produced a medium finding.
   A public withdraw is not privileged. The name list is now
   mint/burn/pause/unpause/upgrade/setOwner/setFee/setAdmin/sweep/rescue/transferOwnership.
2. **`weak-randomness` required `%` immediately after a block value**, so
   `uint256(keccak256(abi.encodePacked(block.timestamp))) % 100` was missed. The rule now flags any
   line containing both a block entropy source and a `%`: hashing first adds no unpredictability.
3. **CLI `scan --rules` exited 2** because the argument check ran before the flag was read. The flag
   is handled first now, and a test covers it.

## What was not run

- **No Solidity compiler or fork.** The scanner reads text; the fixtures are never compiled or run.
- **No comparison against Slither.** Precision is not measured on a corpus of real contracts.
- **No performance claim.** One pass per file.
