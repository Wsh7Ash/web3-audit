---
name: upgrade-selector-collision
description: "Compare the implementation's function selectors against the proxy's own, because a collision routes the call to the proxy instead of the implementation. Use when a new implementation adds functions to an existing proxy"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [upgrade, selectors, collision]
phase: upgrade
---

# Check new functions do not collide with proxy selectors

> Compare the implementation's function selectors against the proxy's own, because a collision routes the call to the proxy instead of the implementation

**Use when:** a new implementation adds functions to an existing proxy

**Avoid when:** the proxy uses a fallback that delegates everything and has no other functions

## Procedure

1. List the proxy's own external functions and their selectors.
2. List the new implementation's selectors.
3. Compute the intersection and check for the proxy's upgrade or admin selectors.
4. Report any new function whose selector the proxy already uses.

## Signals

- selectors-listed
- intersection-computed
- collisions-reported

## Patterns

**1. selector**

```
cast sig 'upgradeTo(address)'   # 0x3659cfe6
```

## Pitfalls

- Assuming four-byte collisions are impossible at this size; they happen with cloned codebases.
- Forgetting the transparent proxy rule that makes admin calls bypass the fallback.

## Done when

- Both selector sets are listed and intersected.
- Any collision is reported with the function that becomes unreachable.

## References

- [EIP-1967 storage slots](https://eips.ethereum.org/EIPS/eip-1967)
