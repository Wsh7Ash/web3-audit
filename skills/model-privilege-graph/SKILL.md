---
name: model-privilege-graph
description: "Record which role can reach which state change, so a missing modifier is visible against what the role is supposed to be able to do. Use when the contract has more than one privileged role"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [model, roles, privilege]
phase: model
---

# Draw the privilege graph

> Record which role can reach which state change, so a missing modifier is visible against what the role is supposed to be able to do

**Use when:** the contract has more than one privileged role

**Avoid when:** there is a single owner and no delegated roles

## Procedure

1. List every role and how it is granted, revoked and renounced.
2. List every state-changing function and the role that should reach it.
3. Compare the intended graph with the modifiers actually applied.
4. Report each function reachable by a broader role than intended.

## Signals

- roles-listed
- intended-graph-written
- actual-modifiers-compared

## Patterns

**1. role check**

```
function setFee(uint256 f) external onlyRole(FEE_ADMIN) { fee = f; }
```

## Pitfalls

- Assuming DEFAULT_ADMIN_ROLE is harmless because it is a role name rather than an owner.
- Missing the initializer that grants a role, which leaves the grant path open after deploy.

## Done when

- Every role and every guarded function appear in the graph.
- Broader-than-intended reachability is listed with the function.

## References

- [OpenZeppelin AccessControl](https://docs.openzeppelin.com/contracts/5.x/access-control)
