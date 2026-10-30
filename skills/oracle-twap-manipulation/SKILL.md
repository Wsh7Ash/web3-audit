---
name: oracle-twap-manipulation
description: "Estimate the cost of shifting the window average and compare it with the value the price controls, because a cheap manipulation is the whole finding. Use when the contract prices collateral from a pool-derived average"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [oracle, twap, manipulation]
phase: oracle
---

# Check how much capital moves a TWAP

> Estimate the cost of shifting the window average and compare it with the value the price controls, because a cheap manipulation is the whole finding

**Use when:** the contract prices collateral from a pool-derived average

**Avoid when:** the price comes from a decentralised oracle with its own manipulation cost

## Procedure

1. Identify the pool, the window length and the liquidity depth.
2. Compute the trade size needed to move the average by the amount that matters.
3. Compare that cost with the profit available from the mispricing.
4. Report both numbers, since either alone is not a finding.

## Signals

- pool-identified
- cost-estimated
- profit-compared

## Patterns

**1. window**

```
uint32 public constant TWAP_WINDOW = 1800; // 30 minutes
```

## Pitfalls

- Reporting manipulation without a cost estimate, which a triager will reject.
- Ignoring that the window can be short enough that one block dominates it.

## Done when

- Window, liquidity and required trade size are recorded.
- The manipulation cost is compared with the value at stake.

## References

- [Uniswap v3 oracle](https://docs.uniswap.org/contracts/v3/overview)
