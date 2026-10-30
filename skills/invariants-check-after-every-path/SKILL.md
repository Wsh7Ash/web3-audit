---
name: invariants-check-after-every-path
description: "Re-check the accounting identity after reverts and partial operations, because a function that reverts after a transfer still moved the tokens. Use when the contract makes external calls before its final state write"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [invariants, failure, reverts]
phase: invariants
---

# Check invariants on failure paths too

> Re-check the accounting identity after reverts and partial operations, because a function that reverts after a transfer still moved the tokens

**Use when:** the contract makes external calls before its final state write

**Avoid when:** the contract performs no external calls and reverts atomically by construction

## Procedure

1. Identify every function that makes an external call before its last state write.
2. Force the call to fail, using a token that reverts on transfer where possible.
3. Check the invariant after the revert and compare with the state before the call.
4. Report any case where the revert did not undo the earlier effect.

## Signals

- external-calls-identified
- failure-forced
- invariant-rechecked

## Patterns

**1. forced failure**

```
token.setRevertOnTransfer(true);
vm.expectRevert();
vault.withdraw(shares);
assertTrue(vault.invariant_solvent());
```

## Pitfalls

- Testing only happy paths, where the invariant trivially holds by construction.
- Assuming a revert rolls back an external call that already succeeded on another contract.

## Done when

- Every external-call-then-state-write path was exercised with a failure.
- The invariant is shown to hold after each forced failure, or a finding is recorded.

## References

- [Solidity security considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)
