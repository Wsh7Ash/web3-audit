---
name: reentrancy-trace-external-calls
description: "List each external call with the state already written and the state still to write, so reentrancy is a property of a specific function rather than a vibe. Use when the contract calls tokens, hooks, receivers or other contracts"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reentrancy, external-calls, ordering]
phase: reentrancy
---

# Trace every external call and what it can re-enter

> List each external call with the state already written and the state still to write, so reentrancy is a property of a specific function rather than a vibe

**Use when:** the contract calls tokens, hooks, receivers or other contracts

**Avoid when:** the contract makes no external calls

## Procedure

1. List every external call, including token transfers, hooks and low-level calls.
2. For each, record the state reads and writes that happen before and after.
3. Identify the entry points an attacker could call from inside the callback.
4. Report the call and the entry point that makes it exploitable, or state why none does.

## Signals

- calls-listed
- ordering-recorded
- entry-points-identified

## Patterns

**1. order**

```
balances[msg.sender] -= amount;   // write first
(bool ok, ) = msg.sender.call{value: amount}("");  // then call
require(ok, "transfer failed");
```

## Pitfalls

- Treating a call to a trusted token as safe without checking whether the token has hooks.
- Looking only at the function under review and missing a callback into a different entry point.

## Done when

- Every external call has its before/after state recorded.
- Each call is either shown exploitable or shown why it is not.

## References

- [Consensys reentrancy](https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/)
