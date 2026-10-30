---
name: oracle-decimal-mismatch
description: "Confirm every price is scaled to the decimals the arithmetic expects, because an 8-decimal feed in an 18-decimal formula is a factor of a billion. Use when the contract mixes feeds, tokens or internal units with different decimals"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [oracle, decimals, scaling]
phase: oracle
---

# Check oracle decimals against the maths

> Confirm every price is scaled to the decimals the arithmetic expects, because an 8-decimal feed in an 18-decimal formula is a factor of a billion

**Use when:** the contract mixes feeds, tokens or internal units with different decimals

**Avoid when:** every value is normalised through one helper with an explicit scale

## Procedure

1. Record the decimals of every feed and token involved.
2. Write the arithmetic with its implied scale and compare.
3. Test with a realistic price and check the resulting value against a hand calculation.
4. Report any place where the scale differs from the assumption.

## Signals

- decimals-recorded
- scale-compared
- hand-check-done

## Patterns

**1. normalise**

```
uint256 price18 = uint256(answer) * 10 ** (18 - feed.decimals());
```

## Pitfalls

- Assuming all Chainlink USD feeds are 8 decimals; some pairs are 18.
- Normalising the price but not the token amount, which reintroduces the mismatch.

## Done when

- Every decimals value is recorded and the formula scale is stated.
- A hand calculation matches the contract's output.

## References

- [Chainlink data feeds](https://docs.chain.link/data-feeds)
