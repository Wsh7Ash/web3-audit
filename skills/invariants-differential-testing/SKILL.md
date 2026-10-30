---
name: invariants-differential-testing
description: "Run the contract and a simple reference implementation over identical inputs, so a divergence is a concrete counterexample rather than a suspicion. Use when the contract reimplements a known formula or a specification exists"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [invariants, differential, reference]
phase: invariants
---

# Compare two implementations on the same inputs

> Run the contract and a simple reference implementation over identical inputs, so a divergence is a concrete counterexample rather than a suspicion

**Use when:** the contract reimplements a known formula or a specification exists

**Avoid when:** there is no reference implementation and none can be written cheaply

## Procedure

1. Write the simplest correct reference for the formula, ignoring gas and structure.
2. Feed both implementations the same pseudo-random input sequence.
3. Stop at the first divergence and record the input that caused it.
4. Check the divergence is real, not a rounding difference the protocol documents.

## Signals

- reference-written
- same-inputs-fed
- divergence-captured

## Patterns

**1. differential**

```
for (uint256 i; i < 256; ++i) {
  uint256 x = uint256(keccak256(abi.encode(i)));
  assertEq(contract.f(x), reference.f(x));
}
```

## Pitfalls

- A reference implementation that copies the contract's own arithmetic and therefore cannot diverge.
- Treating a documented rounding direction as a bug.

## Done when

- A reference exists and both run on identical inputs.
- The first divergence is recorded with its input and classified.

## References

- [Solidity math](https://docs.soliditylang.org/en/latest/types.html#integers)
