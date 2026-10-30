---
name: randomness-block-values
description: "Find every use of block.timestamp, blockhash or prevrandao in a draw and show how a validator or a caller can bias it. Use when the contract picks winners, assigns traits or samples from a set"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [randomness, block-values, bias]
phase: randomness
---

# Reject block values as a randomness source

> Find every use of block.timestamp, blockhash or prevrandao in a draw and show how a validator or a caller can bias it

**Use when:** the contract picks winners, assigns traits or samples from a set

**Avoid when:** the value is used only for timing and nothing of value depends on it

## Procedure

1. Find every expression that derives a random-looking value.
2. Identify who can influence each input and how much.
3. Simulate two consecutive blocks and show the outcome difference.
4. Report the input, the influencer and the advantage.

## Signals

- sources-found
- influencers-identified
- bias-shown

## Patterns

**1. bad draw**

```
uint256 winner = uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao))) % players.length;
```

## Pitfalls

- Concluding there is no bias because the attacker cannot predict the hash exactly.
- Missing that a caller can revert and retry until the draw favours them.

## Done when

- Every random-looking derivation has its inputs and influencers listed.
- The advantage gained is demonstrated or bounded.

## References

- [Solidity block values](https://docs.soliditylang.org/en/latest/units-and-global-variables.html#block-and-transaction-properties)
