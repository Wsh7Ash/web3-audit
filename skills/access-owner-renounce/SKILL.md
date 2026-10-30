---
name: access-owner-renounce
description: "Trace every onlyOwner path before the owner renounces, so a renounce that is meant to be safe does not freeze withdrawals or leave the contract unupgradeable. Use when the deployment plan includes renouncing ownership or burning the admin role"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [access, ownership, renounce]
phase: access
---

# Check what renouncing ownership actually breaks

> Trace every onlyOwner path before the owner renounces, so a renounce that is meant to be safe does not freeze withdrawals or leave the contract unupgradeable

**Use when:** the deployment plan includes renouncing ownership or burning the admin role

**Avoid when:** ownership is intentionally retained and timelocked

## Procedure

1. List every function gated by the role that will be renounced.
2. Classify each as recoverable without the role or permanently broken.
3. Simulate the renounce in a fork or a test and attempt the affected actions.
4. Report the functions that become unreachable, with the funds or state they strand.

## Signals

- gated-functions-listed
- renounce-simulated
- stranded-state-identified

## Patterns

**1. renounce then test**

```
vault.renounceOwnership();
vm.expectRevert();
vault.emergencyWithdraw();
```

## Pitfalls

- Renouncing ownership while a pause is active, which makes the pause permanent.
- Assuming renouncing is safe because the contract is immutable; proxies usually are not.

## Done when

- Every gated function is classified after renounce.
- Any stranded funds or state are reported before the renounce happens.

## References

- [OpenZeppelin Ownable](https://docs.openzeppelin.com/contracts/5.x/api/access#Ownable)
