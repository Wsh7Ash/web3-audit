---
name: access-initializer-frontrun
description: "Verify that initialization is atomic with deployment or guarded, so an attacker cannot become the owner of a freshly deployed proxy. Use when the contract uses an initializer pattern instead of a constructor"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [access, initializer, deployment]
phase: access
---

# Check the initializer cannot be front-run

> Verify that initialization is atomic with deployment or guarded, so an attacker cannot become the owner of a freshly deployed proxy

**Use when:** the contract uses an initializer pattern instead of a constructor

**Avoid when:** the contract uses a constructor with immutable arguments

## Procedure

1. Locate every initializer and whether it sets an initialized flag.
2. Check whether deployment and initialization happen in the same transaction.
3. If they are separate, attempt to call initialize from a different address first.
4. Report the window and what an attacker gains by taking it.

## Signals

- initializers-found
- atomicity-checked
- window-tested

## Patterns

**1. guarded initializer**

```
function initialize(address owner_) external initializer {
  __Ownable_init(owner_);
}
```

## Pitfalls

- A proxy deployed in one transaction and initialized in another, which leaves an open window.
- An initializer without the initializer modifier, which can be called twice.

## Done when

- Every initializer has a guard and deployment atomicity is established.
- Any open window is demonstrated or ruled out.

## References

- [OpenZeppelin Initializable](https://docs.openzeppelin.com/contracts/5.x/api/proxy#Initializable)
