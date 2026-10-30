---
name: invariants-write-in-solidity
description: "Turn each written invariant into a function a test or a handler can call, so the invariant is checked by code rather than by memory. Use when the accounting identity is written and the next step is proving it holds"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [invariants, solidity, testing]
phase: invariants
---

# Express invariants as executable Solidity assertions

> Turn each written invariant into a function a test or a handler can call, so the invariant is checked by code rather than by memory

**Use when:** the accounting identity is written and the next step is proving it holds

**Avoid when:** the invariant cannot be observed from outside the contract and no test hook exists

## Procedure

1. Write one external view function per invariant that reverts or returns false when violated.
2. Keep the function free of state changes so it can be called at any point in a test.
3. Call it after every state-changing action in the test harness.
4. Record which invariant each function encodes so a failure names the rule.

## Signals

- invariant-functions-written
- read-only
- checked-every-step

## Patterns

**1. invariant function**

```
function invariant_solvent() external view returns (bool) {
  return totalAssets() >= totalSupply();
}
```

## Pitfalls

- An invariant function that reads cached state, so it agrees with itself instead of with reality.
- Checking only at the end of a test, which hides the intermediate state where it broke.

## Done when

- Every written invariant has a read-only on-chain check.
- The harness calls each check after every action.

## References

- [Foundry invariant testing](https://book.getfoundry.sh/forge/invariant-testing)
