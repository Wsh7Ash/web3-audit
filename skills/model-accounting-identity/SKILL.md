---
name: model-accounting-identity
description: "State an equation such as sum of balances equals total supply plus escrow, so a broken invariant is a failing comparison rather than an opinion. Use when the contract tracks shares, debts, collateral or internal balances"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [model, accounting, invariant]
phase: model
---

# Write the accounting identity the contract must preserve

> State an equation such as sum of balances equals total supply plus escrow, so a broken invariant is a failing comparison rather than an opinion

**Use when:** the contract tracks shares, debts, collateral or internal balances

**Avoid when:** the contract holds no accounting state

## Procedure

1. Write the equation that must hold after every external call.
2. Express each term as a function you can read on-chain or in a test.
3. Check the equation after each state-changing path, including the failure paths.
4. Report the smallest sequence that makes it fail, not the equation alone.

## Signals

- identity-written
- terms-expressible
- paths-checked

## Patterns

**1. identity**

```
sum(userShares) == totalSupply
sum(userBalances) + escrowed == token.balanceOf(vault)
```

## Pitfalls

- An identity that only holds at rest and not after a partial withdrawal.
- Writing the identity with a term the contract does not expose, which makes it untestable.

## Done when

- The identity is written and every term is readable on-chain or in a test.
- Every state-changing path was checked against it.

## References

- [EIP-4626 tokenised vault](https://eips.ethereum.org/EIPS/eip-4626)
