# Architecture

Two components share one repository: a validated skill corpus and a line-oriented scanner. They do
not depend on each other at runtime, which keeps the scanner usable on its own.

```
corpus/part1..part3.py --skill_from_dict--> Skill --validate--> issues
                                            +--render--> skills/, pack.json, catalog

scanner.py: (path, lines) -> [Finding] ; scan_path(root) -> [Finding] -> text | json
```

## The scanner

Each rule is a pure function `(path, lines) -> Iterable[Finding]`. That signature is the whole
contract, and it has two consequences:

- a rule cannot see other rules, so output does not depend on registration order;
- a rule cannot read the filesystem, so a scan is deterministic and testable from a literal string.

`scan_text` runs every rule and sorts by `(line, rule)`, so output is stable across runs. `scan_path`
expands a directory with `rglob("*.sol")`, applies the severity filter once at the end, and raises
`FileNotFoundError` for a missing target — an empty result should mean "clean", not "not found".

Severity is a closed set of four values with an explicit rank, and the filter uses `>=` on that rank,
which is why `--min-severity medium` includes high findings.

## Why line-oriented

A real analyser needs a parser, an inheritance graph and a taint model. This scanner has none, so
every rule is defensible from one line plus a small window:

- `unchecked-call` looks three lines back and two forward for a check;
- `reentrancy-order` tracks a function boundary with braces and reports the call line;
- `privileged-function` reads the declaration and the first four lines for a modifier.

The rules are documented as heuristics. Claiming more analysis than exists would be worse than no
scanner, because a reviewer would trust it.

## The corpus

Skills are data. `skill_from_dict` validates shape once and returns a frozen `Skill`; the validator
applies nine per-skill rules plus package rules (count, phase coverage, uniqueness); the renderer is
a pure function whose output is committed and drift-checked against a fresh render.

## Exit codes

`scan` returns 0 when nothing meets `--fail-on`, 1 when something does, 2 for usage errors.

## Non-goals

- No compiler integration, import resolution or SMT.
- No automatic remediation; skills describe the fix, the scanner does not apply it.
- No chain interaction. Nothing here reads a node.
