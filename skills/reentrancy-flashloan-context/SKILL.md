---
name: reentrancy-flashloan-context
description: "Repeat the attack with borrowed capital inside one transaction, because a check that depends on the attacker's balance can be satisfied transiently. Use when a guard or threshold compares the caller's balance or share of supply"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reentrancy, flash-loan, capital]
phase: reentrancy
---

# Test reentrancy under a flash-loan balance

> Repeat the attack with borrowed capital inside one transaction, because a check that depends on the attacker's balance can be satisfied transiently

**Use when:** a guard or threshold compares the caller's balance or share of supply

**Avoid when:** no authorisation or threshold depends on balances

## Procedure

1. Identify checks that compare the caller's balance, share or voting weight.
2. Borrow the required amount inside one transaction from a test liquidity source.
3. Perform the sequence and repay within the same transaction.
4. Report the check that the borrowed balance satisfied.

## Signals

- balance-checks-identified
- borrow-simulated
- check-satisfied

## Patterns

**1. transient capital**

```
flashLoan(amount, address(vault), abi.encodeWithSignature("attack()"));
// repay within the same tx
```

## Pitfalls

- Dismissing a check because the attacker does not hold the balance in a normal block.
- Forgetting governance snapshot timing, which can make borrowed weight useless.

## Done when

- Every balance-dependent check is listed and tested with transient capital.
- The satisfied check is reported with the sequence that satisfied it.

## References

- [EIP-3156 flash loans](https://eips.ethereum.org/EIPS/eip-3156)
