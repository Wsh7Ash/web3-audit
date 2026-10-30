---
name: model-state-machine
description: "Write the states a position can be in and the allowed transitions, so a missing guard shows up as a transition that should not exist. Use when the contract has lifecycle stages such as open, locked, settled or paused"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [model, state, transitions]
phase: model
---

# Model the contract as a state machine

> Write the states a position can be in and the allowed transitions, so a missing guard shows up as a transition that should not exist

**Use when:** the contract has lifecycle stages such as open, locked, settled or paused

**Avoid when:** the contract is stateless apart from a single mapping

## Procedure

1. List the state variables that gate behaviour and the values they can take.
2. Write the allowed transitions with the function that performs each one.
3. Walk every function and check that it either requires the right state or is state-independent.
4. Report any transition that is reachable without its guard.

## Signals

- states-listed
- transitions-written
- guards-checked

## Patterns

**1. state machine**

```
states: Open -> Locked -> Settled
Open --lock()--> Locked    requires block.timestamp >= end
Locked --settle()--> Settled  requires oracle.ready()
```

## Pitfalls

- Modelling only the happy path and leaving pause, cancel and emergency exits out of the diagram.
- Assuming a guard exists because a modifier is named pauseable without reading what it checks.

## Done when

- Every state and transition is written down with its guard.
- Each function is checked against the model and exceptions are listed.

## References

- [Solidity security considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)
