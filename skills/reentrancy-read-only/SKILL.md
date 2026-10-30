---
name: reentrancy-read-only
description: "Test whether a view function reports a stale price or balance while an external call is in flight, because integrators read those views. Use when the contract exposes getPrice, getReserves or balanceOf and makes external calls"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reentrancy, views, integrations]
phase: reentrancy
---

# Check read-only reentrancy through view functions

> Test whether a view function reports a stale price or balance while an external call is in flight, because integrators read those views

**Use when:** the contract exposes getPrice, getReserves or balanceOf and makes external calls

**Avoid when:** no integrator reads the contract mid-transaction and the views are not used by other protocols

## Procedure

1. List the view functions another contract would read for pricing or accounting.
2. Identify where the contract makes an external call and whether a view would be stale during it.
3. Re-enter a view from the callback and record the value it returns mid-call.
4. Report the stale value with the integrator that would consume it.

## Signals

- views-listed
- callback-view-recorded
- consumer-identified

## Patterns

**1. stale view**

```
function totalAssets() public view returns (uint256) {
  return asset.balanceOf(address(this)) + pending;
}
```

## Pitfalls

- Checking only state-changing reentrancy and missing that a lending market prices shares through the view.
- Assuming a reentrancy guard on the mutating function protects the view as well.

## Done when

- Every price-relevant view is identified and probed during a callback.
- Any stale value is reported with the integrator that would consume it.

## References

- [EIP-4626 tokenised vault](https://eips.ethereum.org/EIPS/eip-4626)
