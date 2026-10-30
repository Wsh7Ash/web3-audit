---
name: testing-fork-reproduction
description: "Pin the fork to the block before the fix or the exploit and replay the sequence, so the reproduction matches the state the finding described. Use when the finding is about a deployed contract and the state has moved on"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [testing, fork, reproduction]
phase: testing
---

# Reproduce a finding on a fork at the vulnerable block

> Pin the fork to the block before the fix or the exploit and replay the sequence, so the reproduction matches the state the finding described

**Use when:** the finding is about a deployed contract and the state has moved on

**Avoid when:** the finding is about code that is not deployed

## Procedure

1. Record the block number where the vulnerable state existed.
2. Create the fork with that block pinned and confirm the bytecode hash.
3. Replay the minimal sequence and assert the effect.
4. Store the block number, the RPC source and the bytecode hash with the test.

## Signals

- block-pinned
- bytecode-confirmed
- sequence-replayed

## Patterns

**1. pin a fork**

```
vm.createSelectFork(vm.envString("RPC_URL"), 21_000_000);
```

## Pitfalls

- Forking at latest, where a fix or a state change has already removed the condition.
- Depending on a public RPC that prunes old state, which makes the test unreproducible.

## Done when

- The block number and bytecode hash are recorded with the test.
- The sequence reproduces the finding on the pinned fork.

## References

- [Foundry fork testing](https://book.getfoundry.sh/forge/fork-testing)
