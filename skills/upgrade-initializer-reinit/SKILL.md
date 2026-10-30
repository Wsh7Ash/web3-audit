---
name: upgrade-initializer-reinit
description: "Verify the initialized flag survives an upgrade and that no new initializer can be called again, because a re-initializable implementation is a takeover. Use when a new implementation adds an initializer or a reinitializer"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [upgrade, initializer, takeover]
phase: upgrade
---

# Check an upgrade cannot re-run initialization

> Verify the initialized flag survives an upgrade and that no new initializer can be called again, because a re-initializable implementation is a takeover

**Use when:** a new implementation adds an initializer or a reinitializer

**Avoid when:** the upgrade adds no initialization logic

## Procedure

1. Read the new implementation's initializer and its version number.
2. Check the proxy's stored initialized version before and after the upgrade.
3. Attempt to call the new initializer from a non-admin address after upgrading.
4. Report whether the call succeeded and what it changed.

## Signals

- initializer-read
- version-checked
- reinit-attempted

## Patterns

**1. reinitializer**

```
function initializeV2(uint256 fee_) external reinitializer(2) {
  fee = fee_;
}
```

## Pitfalls

- A new implementation that resets the initialized flag to zero in its constructor.
- An initializer without a version, which can be called again after any upgrade.

## Done when

- The stored initialized version is recorded before and after.
- A re-initialization attempt from a non-admin is shown to fail.

## References

- [OpenZeppelin Initializable](https://docs.openzeppelin.com/contracts/5.x/api/proxy#Initializable)
