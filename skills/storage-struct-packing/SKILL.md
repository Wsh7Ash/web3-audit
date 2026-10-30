---
name: storage-struct-packing
description: "Read the struct field order and confirm that a packing optimisation did not create a shared slot that a partial write can corrupt. Use when the contract packs several small fields into one struct"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [storage, packing, slots]
phase: storage
---

# Check struct packing against gas and correctness assumptions

> Read the struct field order and confirm that a packing optimisation did not create a shared slot that a partial write can corrupt

**Use when:** the contract packs several small fields into one struct

**Avoid when:** every field is a full 32-byte word

## Procedure

1. Dump the storage layout and group fields by slot.
2. Identify every write that touches a field in a shared slot.
3. Check that each write uses a full assignment rather than an assembly partial store.
4. Report any write that could clear a neighbouring field.

## Signals

- slots-grouped
- writes-identified
- partial-stores-checked

## Patterns

**1. packed struct**

```
struct Position { uint128 amount; uint64 start; uint64 end; } // one slot
```

## Pitfalls

- Assembly that writes a single field with sstore on the whole slot, wiping its neighbours.
- Reordering a packed struct during an upgrade, which changes every field's meaning.

## Done when

- Every shared slot and its writers are listed.
- No write can clear a neighbouring field, or the risk is reported.

## References

- [Solidity storage layout](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)
