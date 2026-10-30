---
name: reporting-severity-basis
description: "Rate each finding by who can trigger it, what it costs them and what it moves, so the rating follows from facts rather than from the defect class. Use when findings are being triaged into high, medium and low"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [reporting, severity, risk]
phase: reporting
---

# Justify severity with reachability and value at risk

> Rate each finding by who can trigger it, what it costs them and what it moves, so the rating follows from facts rather than from the defect class

**Use when:** findings are being triaged into high, medium and low

**Avoid when:** the platform assigns severity from a fixed mapping

## Procedure

1. State the caller: unauthenticated, any depositor, a privileged role.
2. State the capital required and whether it can be borrowed in the same transaction.
3. State the value at risk with the balance or supply it is measured against.
4. Derive the severity from those three and record the reasoning.

## Signals

- caller-stated
- capital-stated
- value-measured

## Patterns

**1. severity basis**

```
caller: any depositor, no privilege
capital: 2 wei plus one donation
effect: next depositor's shares round to zero
```

## Pitfalls

- Rating critical because the defect class is critical, even when the trigger needs admin.
- Ignoring that borrowed capital can satisfy a deposit threshold within one transaction.

## Done when

- Caller, capital and value at risk are all stated.
- The severity follows explicitly from those three.

## References

- [SWC registry](https://swcregistry.io/)
