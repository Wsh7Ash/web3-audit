---
name: invariants-fuzz-handlers
description: "Restrict fuzzed actors and amounts to realistic ranges, so the campaign spends its budget on reachable states instead of reverting on the first call. Use when an invariant fuzzer keeps finding trivial reverts rather than deep failures"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [invariants, fuzzing, handlers]
phase: invariants
---

# Bound fuzz handlers so the search reaches deep states

> Restrict fuzzed actors and amounts to realistic ranges, so the campaign spends its budget on reachable states instead of reverting on the first call

**Use when:** an invariant fuzzer keeps finding trivial reverts rather than deep failures

**Avoid when:** the campaign is exploratory and the goal is to find any revert

## Procedure

1. Restrict actors to a small set of funded addresses.
2. Clamp amounts to the range the protocol actually supports.
3. Add a handler that performs the realistic action sequence rather than a raw call.
4. Re-run and confirm the campaign reaches states beyond the first deposit.

## Signals

- actors-bounded
- amounts-clamped
- deep-states-reached

## Patterns

**1. handler**

```
function deposit(uint256 amount) public {
  amount = bound(amount, 1, 1_000e18);
  vm.prank(actor);
  vault.deposit(amount);
}
```

## Pitfalls

- Letting the fuzzer pick arbitrary addresses, which mostly produces calls that revert on authorisation.
- Bounding so tightly that the campaign never reaches the boundary where the bug lives.

## Done when

- Actors and amounts are bounded with a stated reason.
- The campaign is shown to reach states past the first action.

## References

- [Foundry invariant testing](https://book.getfoundry.sh/forge/invariant-testing)
