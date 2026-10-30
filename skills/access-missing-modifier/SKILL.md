---
name: access-missing-modifier
description: "Compare every state-changing function against the privilege graph and report the ones reachable by anyone. Use when the privilege graph is written and the next step is checking it against code"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [access, modifiers, review]
phase: access
---

# Find privileged functions with no guard

> Compare every state-changing function against the privilege graph and report the ones reachable by anyone

**Use when:** the privilege graph is written and the next step is checking it against code

**Avoid when:** the contract is intentionally permissionless and every function is meant to be public

## Procedure

1. List every external and public function that writes state.
2. For each, read the declaration and the first lines of the body for a guard.
3. Cross-check with the privilege graph to see whether the missing guard matters.
4. Report the function, the intended role and the reachable caller.

## Signals

- writers-listed
- guards-read
- reachability-stated

## Patterns

**1. compare**

```
grep -n 'function .*external' Vault.sol | grep -v 'view\|pure'
```

## Pitfalls

- Missing a guard that is applied inside an internal function the public one calls.
- Assuming a function is safe because its name sounds administrative.

## Done when

- Every state-writing function has a guard decision recorded.
- Any missing guard is mapped to the caller who can reach it.

## References

- [OpenZeppelin AccessControl](https://docs.openzeppelin.com/contracts/5.x/access-control)
