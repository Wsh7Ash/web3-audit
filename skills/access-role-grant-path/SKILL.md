---
name: access-role-grant-path
description: "Trace the grant and revoke functions so a role that looks restricted cannot be handed out by a broader role. Use when the contract uses role-based access control"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [access, roles, delegation]
phase: access
---

# Check who can grant the roles

> Trace the grant and revoke functions so a role that looks restricted cannot be handed out by a broader role

**Use when:** the contract uses role-based access control

**Avoid when:** access is a single immutable owner with no delegation

## Procedure

1. Find every call to grantRole, _grantRole and any custom grant function.
2. Record the role required to call each one and whether it is the role's admin.
3. Check whether a role can grant itself or a role above it.
4. Report any grant path reachable by a role that should not have it.

## Signals

- grant-paths-found
- admin-roles-recorded
- escalation-checked

## Patterns

**1. admin role**

```
bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
// admin of MINTER_ROLE is DEFAULT_ADMIN_ROLE by default
```

## Pitfalls

- Forgetting that DEFAULT_ADMIN_ROLE can grant itself to another address.
- Custom grant functions that skip the role-admin check entirely.

## Done when

- Every grant path has its required role recorded.
- Escalation from a lower role to a higher one is ruled out or reported.

## References

- [OpenZeppelin AccessControl](https://docs.openzeppelin.com/contracts/5.x/access-control)
