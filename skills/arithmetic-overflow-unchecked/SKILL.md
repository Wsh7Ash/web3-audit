---
name: arithmetic-overflow-unchecked
description: "Read each unchecked block and prove the operands cannot overflow, because the compiler no longer helps inside one. Use when the contract uses Solidity 0.8 or later and contains unchecked blocks"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [arithmetic, unchecked, overflow]
phase: arithmetic
---

# Check every unchecked block for reachable overflow

> Read each unchecked block and prove the operands cannot overflow, because the compiler no longer helps inside one

**Use when:** the contract uses Solidity 0.8 or later and contains unchecked blocks

**Avoid when:** the contract predates 0.8 and has no unchecked blocks

## Procedure

1. List every unchecked block with its operands and bounds.
2. Write the maximum value each operand can reach from the contract's own constraints.
3. Compare the sum or product against the type maximum and record the margin.
4. Report any block where the margin depends on an assumption rather than a check.

## Signals

- blocks-listed
- bounds-written
- margin-computed

## Patterns

**1. unchecked**

```
unchecked {
  // i < length <= 256, so i + 1 cannot overflow uint256
  ++i;
}
```

## Pitfalls

- An unchecked block that holds a user-supplied amount rather than a loop counter.
- Assuming a bound from a modifier that can be changed by an admin after deployment.

## Done when

- Every unchecked block has a written bound and margin.
- Any margin that rests on an assumption is reported.

## References

- [Solidity unchecked](https://docs.soliditylang.org/en/latest/control-structures.html#checked-or-unchecked-arithmetic)
