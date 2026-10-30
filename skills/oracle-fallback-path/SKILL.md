---
name: oracle-fallback-path
description: "Force the primary feed to revert and see what the contract does next, because a silent fallback to a spot price is a downgrade of the whole guarantee. Use when the contract has a try/catch or a secondary source around an oracle"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [oracle, fallback, degradation]
phase: oracle
---

# Check the fallback when the primary oracle fails

> Force the primary feed to revert and see what the contract does next, because a silent fallback to a spot price is a downgrade of the whole guarantee

**Use when:** the contract has a try/catch or a secondary source around an oracle

**Avoid when:** there is a single oracle and failure means the call reverts

## Procedure

1. Read the fallback path and the source it uses.
2. Force the primary to revert in a fork test.
3. Record the price used after the failure and compare it with the last good price.
4. Report whether the fallback is stronger or weaker than the primary.

## Signals

- fallback-read
- failure-forced
- price-compared

## Patterns

**1. fallback**

```
try feed.latestRoundData() returns (uint80, int256 a, , , ) {
  price = uint256(a);
} catch {
  price = pool.spotPrice();   // silently weaker
}
```

## Pitfalls

- A fallback to spot price that is manipulable within one transaction.
- A fallback with no event, so the operator never learns the primary is down.

## Done when

- The fallback source is identified and exercised.
- Its strength relative to the primary is stated.

## References

- [Chainlink data feeds](https://docs.chain.link/data-feeds)
