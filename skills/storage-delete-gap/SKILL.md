---
name: storage-delete-gap
description: "Confirm that deleting a struct or mapping entry clears every field that matters, because delete on a nested mapping leaves its children behind. Use when the contract deletes records to reclaim storage or reset state"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [storage, delete, ghost-state]
phase: storage
---

# Check what a delete actually clears

> Confirm that deleting a struct or mapping entry clears every field that matters, because delete on a nested mapping leaves its children behind

**Use when:** the contract deletes records to reclaim storage or reset state

**Avoid when:** deletion is not part of the contract's lifecycle

## Procedure

1. Read each delete and the type it applies to.
2. List the fields that delete does not recurse into, such as nested mappings.
3. Attempt to read the deleted record and any child record afterwards.
4. Report any value that survives deletion and the function that can still read it.

## Signals

- deletes-listed
- fields-checked
- survivors-read

## Patterns

**1. delete**

```
delete positions[id];   // nested mapping positions[id].history is untouched
```

## Pitfalls

- Assuming delete clears a nested mapping, which it does not.
- Deleting a record while an array still indexes it, leaving a dangling reference.

## Done when

- Every delete is checked field by field for what survives.
- Any surviving state and its reader are reported.

## References

- [Solidity delete](https://docs.soliditylang.org/en/latest/types.html#delete)
