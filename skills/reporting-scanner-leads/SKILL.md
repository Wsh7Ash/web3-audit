---
name: reporting-scanner-leads
description: "Treat each scanner hit as a lead: confirm it in code, then report only the ones you can explain, with the rule id as a cross-reference. Use when you ran the static scanner and it produced more hits than you can report"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reporting, scanner, triage]
phase: reporting
---

# Turn scanner output into reviewed findings, not a dump

> Treat each scanner hit as a lead: confirm it in code, then report only the ones you can explain, with the rule id as a cross-reference

**Use when:** you ran the static scanner and it produced more hits than you can report

**Avoid when:** the client explicitly asked for raw tool output as an appendix

## Procedure

1. Run the scanner and group hits by rule and file.
2. For each group, read the code and decide whether the pattern is reachable and harmful.
3. Report confirmed issues with the rule id; put the rest in an appendix marked false positive with a reason.
4. Never report a scanner hit you have not read.

## Signals

- hits-grouped
- code-read
- false-positives-labelled

## Patterns

**1. scan**

```
web3-audit scan contracts/ --min-severity medium --json > scan.json
```

## Pitfalls

- Submitting the scanner output verbatim, which includes hits the client can disprove in a minute.
- Dropping false positives silently, which hides that the pattern was considered.

## Done when

- Every scanner group is either reported or labelled false positive with a reason.
- No reported finding lacks a code reading.

## References

- [Slither detectors](https://github.com/crytic/slither)
