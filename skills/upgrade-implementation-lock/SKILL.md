---
name: upgrade-implementation-lock
description: "Trace the upgrade authority and any delay, because an EOA with immediate upgrade rights can redirect every deposit without a code bug. Use when the system uses a proxy with an upgrade admin"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [upgrade, admin, trust]
phase: upgrade
---

# Check who can swap the implementation and how fast

> Trace the upgrade authority and any delay, because an EOA with immediate upgrade rights can redirect every deposit without a code bug

**Use when:** the system uses a proxy with an upgrade admin

**Avoid when:** the implementation is immutable

## Procedure

1. Read the proxy's upgrade function and its access control.
2. Determine whether the admin is an EOA, a multisig or a timelock, and the delay.
3. Check whether the upgrade can be performed while paused or mid-withdrawal.
4. Report the authority, the delay and what an immediate upgrade would let it do.

## Signals

- authority-read
- delay-recorded
- window-assessed

## Patterns

**1. upgradeToAndCall**

```
function _authorizeUpgrade(address impl) internal override onlyOwner {}
```

## Pitfalls

- Treating a multisig as a mitigation without checking its threshold and signer set.
- Missing that the upgrade function is exposed on the implementation as well as the proxy.

## Done when

- The upgrade authority and delay are recorded.
- The consequence of an immediate upgrade is stated.

## References

- [EIP-1967 storage slots](https://eips.ethereum.org/EIPS/eip-1967)
