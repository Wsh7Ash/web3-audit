---
name: testing-gas-and-revert-profile
description: "Measure the gas the exploit needs and whether it reverts under realistic limits, because an exploit that cannot be included in a block is not reachable. Use when the exploit involves loops, many calls or large calldata"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [testing, gas, reachability]
phase: testing
---

# Record gas and revert behaviour for the sequence

> Measure the gas the exploit needs and whether it reverts under realistic limits, because an exploit that cannot be included in a block is not reachable

**Use when:** the exploit involves loops, many calls or large calldata

**Avoid when:** the exploit is three calls with fixed cost

## Procedure

1. Measure gas per call and the total for the sequence.
2. Compare the total with the block gas limit on the target chain.
3. Test the sequence with a loop bound that grows, and find where it exceeds the limit.
4. Report the gas cost and whether the exploit fits in one block.

## Signals

- gas-measured
- limit-compared
- growth-tested

## Patterns

**1. gas**

```
uint256 before = gasleft();
// exploit
emit log_named_uint("gas used", before - gasleft());
```

## Pitfalls

- Reporting an exploit that needs more gas than a block allows without noting it.
- Measuring gas on a fork with a raised limit, which hides the constraint.

## Done when

- Per-call and total gas are recorded and compared with the chain's limit.
- Any size dependence is tested and reported.

## References

- [Ethereum gas](https://ethereum.org/en/developers/docs/gas/)
