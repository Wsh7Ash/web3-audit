---
name: reporting-finding-template
description: "Use one structure per finding: location with line numbers, the invariant broken, the sequence that breaks it, and the impact with its evidence. Use when you are writing up any confirmed issue"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reporting, template, structure]
phase: reporting
---

# Write a finding with location, impact and proof

> Use one structure per finding: location with line numbers, the invariant broken, the sequence that breaks it, and the impact with its evidence

**Use when:** you are writing up any confirmed issue

**Avoid when:** the issue is informational and a sentence is enough

## Procedure

1. Give the location as file plus function plus line range, not a link that can rot.
2. State the invariant or expectation that is violated.
3. Give the minimal sequence with the test name that reproduces it.
4. State the impact with the artifact or assertion that proves it.

## Signals

- location-precise
- invariant-stated
- proof-linked

## Patterns

**1. finding**

```
Location: Vault.sol:118-126 (withdraw)
Invariant: sum(shares) == totalSupply after any call
Proof: test_withdraw_reentrancy (drains 12.4 ETH)
Impact: attacker receives assets without burning shares
```

## Pitfalls

- A location that points at the file rather than the line, which forces the reader to search.
- An impact statement with no artifact or assertion behind it.

## Done when

- Every finding has location, invariant, proof and impact.
- The proof names a test or a command that a reviewer can run.

## References

- [SWC registry](https://swcregistry.io/)
