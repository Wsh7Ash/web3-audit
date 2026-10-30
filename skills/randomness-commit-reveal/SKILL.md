---
name: randomness-commit-reveal
description: "Verify that the reveal window, the deposit and the ordering prevent a participant from choosing whether to reveal after seeing others. Use when the contract implements commit-reveal for a draw or an auction"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [randomness, commit-reveal, grinding]
phase: randomness
---

# Check a commit-reveal scheme for grinding and withholding

> Verify that the reveal window, the deposit and the ordering prevent a participant from choosing whether to reveal after seeing others

**Use when:** the contract implements commit-reveal for a draw or an auction

**Avoid when:** randomness comes from an external oracle with its own guarantees

## Procedure

1. Read the commit and reveal windows and what happens if a participant never reveals.
2. Check whether the last revealer can compute the outcome before revealing.
3. Test withholding the final reveal and observe the fallback.
4. Report the advantage available to the last actor in the window.

## Signals

- windows-read
- last-actor-analysed
- withholding-tested

## Patterns

**1. commit**

```
commit = keccak256(abi.encode(secret, msg.sender, nonce));
```

## Pitfalls

- A commit that omits the sender, which lets anyone reveal another's secret.
- No penalty for withholding, which makes the last reveal optional and therefore a choice.

## Done when

- The windows and the withholding behaviour are recorded.
- The last actor's advantage is stated or shown to be zero.

## References

- [Commit-reveal schemes](https://ethereum.org/en/developers/docs/smart-contracts/)
