---
name: arithmetic-precision-loss
description: "Compute the error accumulated by repeated conversions, because one truncation is harmless and a thousand of them is a subsidy. Use when the contract converts value repeatedly, such as in a strategy that compounds"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [arithmetic, precision, accumulation]
phase: arithmetic
---

# Quantify precision loss across a sequence

> Compute the error accumulated by repeated conversions, because one truncation is harmless and a thousand of them is a subsidy

**Use when:** the contract converts value repeatedly, such as in a strategy that compounds

**Avoid when:** the contract performs a single conversion per call and stores no intermediate value

## Procedure

1. Write the conversion chain and the precision of each step.
2. Compute the total error for one round and for n rounds symbolically.
3. Run the chain with a small amount and measure the loss with an assertion.
4. Report the per-round loss and the amount at which it becomes material.

## Signals

- chain-written
- error-computed
- loss-measured

## Patterns

**1. measure loss**

```
uint256 before = vault.balanceOf(user);
for (uint256 i; i < 100; ++i) { vault.harvest(); }
assertLt(vault.balanceOf(user), before);
```

## Pitfalls

- Reporting one wei of loss as critical without showing it accumulates.
- Missing that the loss accrues to the last withdrawer rather than to the protocol.

## Done when

- Precision is stated for every step and the chain error is computed.
- The measured loss and the threshold at which it matters are recorded.

## References

- [Solidity integers](https://docs.soliditylang.org/en/latest/types.html#integers)
