---
name: upgrade-storage-gap
description: "Count the reserved slots in each base contract and compare them with what the next upgrade needs, because an exhausted gap forces a layout change. Use when the upgradeable contract inherits from base contracts with gaps"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [upgrade, gap, inheritance]
phase: upgrade
---

# Check the storage gap is large enough

> Count the reserved slots in each base contract and compare them with what the next upgrade needs, because an exhausted gap forces a layout change

**Use when:** the upgradeable contract inherits from base contracts with gaps

**Avoid when:** the contract does not use inheritance with reserved gaps

## Procedure

1. List each base contract and the size of its __gap array.
2. Count the variables a planned upgrade adds to that base.
3. Confirm the gap is reduced by exactly the number of added variables.
4. Report any base whose gap is too small for the planned change.

## Signals

- gaps-listed
- planned-vars-counted
- reduction-checked

## Patterns

**1. gap**

```
uint256[49] private __gap;  // reduce by one when adding a variable
```

## Pitfalls

- Adding a variable without reducing the gap, which shifts every child's storage.
- Removing the gap entirely to save gas, which blocks all future upgrades.

## Done when

- Every gap and planned addition is counted.
- The gap arithmetic balances for each base contract.

## References

- [OpenZeppelin upgrades storage layout](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)
