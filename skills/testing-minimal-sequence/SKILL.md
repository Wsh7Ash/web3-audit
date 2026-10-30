---
name: testing-minimal-sequence
description: "Remove every action that is not required for the effect, so the test reads as a proof and not as a transcript of exploration. Use when the exploit was found by trial and the test still contains the trials"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [testing, minimal, sequence]
phase: testing
---

# Cut the exploit to the shortest sequence

> Remove every action that is not required for the effect, so the test reads as a proof and not as a transcript of exploration

**Use when:** the exploit was found by trial and the test still contains the trials

**Avoid when:** the sequence is already three calls and each one is load-bearing

## Procedure

1. Record the sequence that works as an ordered list of calls.
2. Remove one call at a time from the start and re-run.
3. Keep only the calls whose removal stops the effect.
4. Confirm the reduced sequence still fails the invariant or drains the balance.

## Signals

- sequence-recorded
- calls-removed
- reduced-sequence-verified

## Patterns

**1. three calls**

```
vm.prank(attacker); vault.deposit(1);
asset.transfer(address(vault), 1e18);
vm.prank(victim); vault.deposit(1e18);
```

## Pitfalls

- Leaving a setup call that only funds the attacker in the proof, which hides the real precondition.
- Removing a call that sets an approval and then reporting the exploit as unauthenticated.

## Done when

- Every remaining call is shown to be required.
- The reduced sequence still produces the effect.

## References

- [Foundry testing](https://book.getfoundry.sh/forge/tests)
