---
name: storage-layout-collision
description: "Compare slot maps for the proxy and each implementation, because an added variable in a child contract shifts every slot below it. Use when the system uses an upgradeable proxy"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [storage, layout, proxy]
phase: storage
---

# Check storage layout between proxy and implementation

> Compare slot maps for the proxy and each implementation, because an added variable in a child contract shifts every slot below it

**Use when:** the system uses an upgradeable proxy

**Avoid when:** the contract is immutable and not behind a proxy

## Procedure

1. Dump the storage layout for the proxy and for each implementation version.
2. Compare slot numbers and types for every variable.
3. Check for gaps reserved for future variables in base contracts.
4. Report any shift and the variable whose value would be reinterpreted.

## Signals

- layouts-dumped
- slots-compared
- shifts-identified

## Patterns

**1. layout dump**

```
forge inspect Vault storage-layout --json > layout.json
```

## Pitfalls

- Adding a variable to a base contract, which shifts storage in every derived contract.
- Reordering variables in a struct that is stored in a mapping value.

## Done when

- Layouts for every version are compared slot by slot.
- Any shift is reported with the affected variable.

## References

- [OpenZeppelin upgrades storage layout](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)
