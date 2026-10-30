---
name: testing-state-diff-assertions
description: "Compare storage before and after the exploit so the test shows exactly which variables moved, which is what the report has to explain. Use when the effect is an accounting change rather than a transfer"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [testing, state-diff, assertions]
phase: testing
---

# Assert on the state diff, not just the balance

> Compare storage before and after the exploit so the test shows exactly which variables moved, which is what the report has to explain

**Use when:** the effect is an accounting change rather than a transfer

**Avoid when:** the effect is a single token balance change that is self-explanatory

## Procedure

1. Snapshot the relevant storage slots before the sequence.
2. Run the sequence and snapshot the same slots after.
3. Assert on each expected change and on each expected non-change.
4. Print the diff in the test output so the report can quote it.

## Signals

- snapshot-before
- snapshot-after
- diff-asserted

## Patterns

**1. storage snapshot**

```
bytes32 before = vm.load(address(vault), bytes32(uint256(3)));
// exploit
bytes32 after_ = vm.load(address(vault), bytes32(uint256(3)));
assertTrue(before != after_);
```

## Pitfalls

- Asserting only that a balance decreased, which does not show where the value went.
- Hardcoding a slot number without confirming it against the layout dump.

## Done when

- Before and after values are captured for each relevant slot.
- The diff is asserted and printed for the report.

## References

- [Foundry cheatcodes](https://book.getfoundry.sh/cheatcodes/)
