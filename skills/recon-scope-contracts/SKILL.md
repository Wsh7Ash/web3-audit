---
name: recon-scope-contracts
description: "List every deployed contract, its proxy target, its admin and the tokens it can move, so the review states what is in scope before reading logic. Use when the audit starts from a repository or an address list and the trust graph is unknown"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [recon, scope, trust]
phase: recon
---

# Enumerate the contracts and what they trust

> List every deployed contract, its proxy target, its admin and the tokens it can move, so the review states what is in scope before reading logic

**Use when:** the audit starts from a repository or an address list and the trust graph is unknown

**Avoid when:** the engagement covers one immutable contract with no external dependencies

## Procedure

1. List contracts, their addresses, bytecode hashes and whether each is a proxy.
2. For every proxy, resolve the implementation address and record how it can be upgraded.
3. Record admin roles, pausers, minters and any address with privileged withdrawal rights.
4. Mark each contract as in scope, out of scope or trusted-dependency with the reason.

## Signals

- contracts-listed
- proxies-resolved
- roles-recorded

## Patterns

**1. implementation slot**

```
cast storage 0xProxy 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc
```

## Pitfalls

- Reviewing the repository while the deployed bytecode differs from it; hash both.
- Treating a trusted dependency as in scope, which inflates the report with issues the client cannot fix.

## Done when

- Every contract has a scope decision and a bytecode hash.
- Every proxy has a resolved implementation and upgrade authority.

## References

- [EIP-1967 storage slots](https://eips.ethereum.org/EIPS/eip-1967)
