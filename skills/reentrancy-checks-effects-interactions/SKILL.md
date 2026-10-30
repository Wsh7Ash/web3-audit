---
name: reentrancy-checks-effects-interactions
description: "Read each value-moving function and confirm state is written before the external call, which is the ordering that makes most reentrancy harmless. Use when a function transfers value and updates balances in the same body"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reentrancy, ordering, pattern]
phase: reentrancy
---

# Verify the checks-effects-interactions order

> Read each value-moving function and confirm state is written before the external call, which is the ordering that makes most reentrancy harmless

**Use when:** a function transfers value and updates balances in the same body

**Avoid when:** the function is a pure view or its only call is to an immutable trusted contract

## Procedure

1. Read the function body and mark the checks, the effects and the interactions.
2. Confirm every effect precedes every interaction.
3. Where an interaction precedes an effect, check for a reentrancy guard.
4. Report the function and the line where the order inverts.

## Signals

- body-classified
- ordering-confirmed
- guards-checked

## Patterns

**1. guarded**

```
function withdraw(uint256 amount) external nonReentrant {
  require(balances[msg.sender] >= amount);
  balances[msg.sender] -= amount;
  payable(msg.sender).transfer(amount);
}
```

## Pitfalls

- A guard on one entry point but not the sibling that shares the same balance.
- Trusting a guard that was applied to the wrong modifier name after a refactor.

## Done when

- Every value-moving function is classified and its ordering recorded.
- Any inversion is either guarded or reported.

## References

- [Consensys reentrancy](https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/)
