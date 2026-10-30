---
name: reentrancy-cross-function
description: "Re-enter a sibling function that reads the same balance, so a guard on one entry point does not hide an unguarded path. Use when several functions mutate the same mapping or the same total"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reentrancy, cross-function, shared-state]
phase: reentrancy
---

# Test cross-function reentrancy on shared state

> Re-enter a sibling function that reads the same balance, so a guard on one entry point does not hide an unguarded path

**Use when:** several functions mutate the same mapping or the same total

**Avoid when:** every function touching the state has the same guard and there is only one

## Procedure

1. Group functions by the state they write and list each group.
2. For each group, check whether every member has the guard.
3. From the callback of an unguarded member, call a guarded sibling and observe the effect.
4. Report the pair, not just the unguarded function.

## Signals

- groups-listed
- guards-compared
- pair-tested

## Patterns

**1. sibling**

```
function withdraw() external nonReentrant { ... }
function transferShares() external { balances[msg.sender] -= n; }  // no guard
```

## Pitfalls

- A guard applied per function rather than per state, which leaves the group partly protected.
- Assuming a lock variable is per-user when it is global and therefore blocks the test.

## Done when

- Every shared-state group has its guards compared.
- Any unguarded member is reported with the sibling that makes it exploitable.

## References

- [OpenZeppelin ReentrancyGuard](https://docs.openzeppelin.com/contracts/5.x/api/utils#ReentrancyGuard)
