---
name: recon-value-flow
description: "Draw the flow of ETH and tokens through the system so the review focuses on paths where value can be redirected rather than on every function. Use when the system holds or moves funds and the reviewer needs to prioritise"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [recon, value, flows]
phase: recon
---

# Map where value enters and leaves

> Draw the flow of ETH and tokens through the system so the review focuses on paths where value can be redirected rather than on every function

**Use when:** the system holds or moves funds and the reviewer needs to prioritise

**Avoid when:** the contract is a pure registry with no value at stake

## Procedure

1. List every function that can receive ETH or transfer tokens, including internal helpers.
2. For each, name the precondition and who can call it.
3. Mark the functions where the amount is computed from a balance, a rate or an oracle.
4. Rank the paths by value at risk and start the review from the top.

## Signals

- value-paths-listed
- preconditions-named
- paths-ranked

## Patterns

**1. value path**

```
deposit() payable -> shares = amount * totalSupply / totalAssets
withdraw(shares) -> assets = shares * totalAssets / totalSupply
```

## Pitfalls

- Reviewing setters first because they are easy, and never reaching the share maths.
- Missing value paths that arrive through a callback rather than a payable function.

## Done when

- Every value path has a caller, a precondition and a computed amount.
- The paths are ranked and the ranking is recorded in the report.

## References

- [Ethereum value transfer](https://ethereum.org/en/developers/docs/transactions/)
