---
name: reporting-fix-verification
description: "Give the test that must pass after remediation, so the fix can be accepted or rejected on evidence rather than on a diff. Use when the report includes recommendations"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reporting, remediation, verification]
phase: reporting
---

# State how the fix will be verified

> Give the test that must pass after remediation, so the fix can be accepted or rejected on evidence rather than on a diff

**Use when:** the report includes recommendations

**Avoid when:** the client has explicitly said remediation is out of scope

## Procedure

1. Name the test that currently fails because of the bug.
2. State the exact change in behaviour that makes it pass, such as the invariant holding after a failure path.
3. List the sibling paths the same test should cover.
4. Record the test as the acceptance criterion in the finding.

## Signals

- test-named
- behaviour-change-stated
- siblings-listed

## Patterns

**1. acceptance**

```
accept when: test_withdraw_reentrancy passes with balances decremented before the call
and: test_withdraw_reentrancy_control still passes
```

## Pitfalls

- An acceptance criterion that only checks the endpoint now reverts for everyone.
- A test that depends on a fork block that the client's CI cannot reach.

## Done when

- A named test and the behaviour it must show are recorded.
- Sibling paths and the control are included in the acceptance criteria.

## References

- [Foundry testing](https://book.getfoundry.sh/forge/tests)
