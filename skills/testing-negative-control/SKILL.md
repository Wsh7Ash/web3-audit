---
name: testing-negative-control
description: "Run the same sequence with one precondition removed and assert nothing happens, so the test proves the precondition rather than the call. Use when the exploit test passes and you need to show why it passes"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [testing, control, precondition]
phase: testing
---

# Add a control that must not exploit

> Run the same sequence with one precondition removed and assert nothing happens, so the test proves the precondition rather than the call

**Use when:** the exploit test passes and you need to show why it passes

**Avoid when:** the effect is an exact state change that cannot occur accidentally

## Procedure

1. Pick the precondition the exploit depends on, such as a donation or a stale price.
2. Run the same calls without it and assert the effect does not occur.
3. Record both tests and the single difference between them.
4. Report the precondition as part of the finding.

## Signals

- control-written
- difference-single
- effect-absent

## Patterns

**1. control**

```
function test_control_no_donation() public {
  vm.prank(attacker); vault.deposit(1);
  vm.prank(victim); vault.deposit(1e18);
  assertGt(vault.balanceOf(victim), 0);
}
```

## Pitfalls

- A control that differs in several ways, which makes the result unattributable.
- Skipping the control and letting a reviewer assume the calls alone are sufficient.

## Done when

- A control test exists and differs from the exploit by one precondition.
- The control asserts the absence of the effect.

## References

- [Foundry testing](https://book.getfoundry.sh/forge/tests)
