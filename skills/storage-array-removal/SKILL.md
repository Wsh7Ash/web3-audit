---
name: storage-array-removal
description: "Read every swap-and-pop and every shift-delete, because an off-by-one leaves a hole that later iteration treats as a live record. Use when the contract stores records in an array and removes them"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [storage, arrays, removal]
phase: storage
---

# Check array removal for skipped elements

> Read every swap-and-pop and every shift-delete, because an off-by-one leaves a hole that later iteration treats as a live record

**Use when:** the contract stores records in an array and removes them

**Avoid when:** removal is not supported and entries are appended only

## Procedure

1. Read each removal and record which index is overwritten and which is popped.
2. Check that the index mapping is updated for the moved element.
3. Remove the last, first and middle element and iterate the array after each.
4. Report any duplicate, hole or stale index found.

## Signals

- removal-read
- mapping-updated
- iteration-checked

## Patterns

**1. swap and pop**

```
uint256 last = items.length - 1;
items[index] = items[last];
indexOf[items[index]] = index;
items.pop();
delete indexOf[removed];
```

## Pitfalls

- Updating the array but not the index mapping, so the moved element becomes unfindable.
- Popping while iterating, which skips the element that was moved into the current index.

## Done when

- Removal is tested at the first, middle and last position.
- The array and its index mapping agree after every removal.

## References

- [Solidity arrays](https://docs.soliditylang.org/en/latest/types.html#arrays)
