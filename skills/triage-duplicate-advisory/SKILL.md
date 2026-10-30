---
name: triage-duplicate-advisory
description: "Search the vendor's advisories and the published audits for the same root cause, because an issue already known and accepted is not a new finding. Use when the contract has a public history or a previous audit report"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [triage, duplicates, advisories]
phase: triage
---

# Check advisories and prior audits before reporting

> Search the vendor's advisories and the published audits for the same root cause, because an issue already known and accepted is not a new finding

**Use when:** the contract has a public history or a previous audit report

**Avoid when:** the deployment is new and no audit or advisory exists

## Procedure

1. Search advisories for the contract and for the library version in use.
2. Read the previous audit's findings and compare root causes, not descriptions.
3. Check whether the client accepted the risk explicitly, and cite where.
4. Report the difference if the new issue is a variant, or drop it if it is the same.

## Signals

- advisories-searched
- root-causes-compared
- acceptance-cited

## Patterns

**1. search**

```
web3-audit list --phase triage
```

## Pitfalls

- Reporting a known issue that the client documented as accepted risk.
- Assuming a patched library version is in use without checking the dependency lock.

## Done when

- Advisories and prior audits are searched and the result recorded.
- Any near duplicate is cited with the difference stated.

## References

- [SWC registry](https://swcregistry.io/)
