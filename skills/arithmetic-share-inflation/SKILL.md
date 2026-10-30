---
name: arithmetic-share-inflation
description: "Deposit a minimal amount, donate to inflate the share price, then check whether the next depositor is rounded to zero shares. Use when the vault computes shares from totalAssets divided by totalSupply"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [arithmetic, inflation, vault]
phase: arithmetic
---

# Test the first-depositor share inflation attack

> Deposit a minimal amount, donate to inflate the share price, then check whether the next depositor is rounded to zero shares

**Use when:** the vault computes shares from totalAssets divided by totalSupply

**Avoid when:** the vault uses a virtual offset or dead shares that make the attack unprofitable

## Procedure

1. Confirm the share formula and whether totalAssets can be raised without minting shares.
2. Deposit one wei as the attacker, then transfer assets directly to the vault.
3. Deposit a realistic amount as the victim and record the shares minted.
4. Report the victim's loss and whether a virtual offset prevents it.

## Signals

- formula-confirmed
- donation-made
- victim-shares-recorded

## Patterns

**1. attack shape**

```
vault.deposit(1, attacker);
asset.transfer(address(vault), 10_000e18);
vault.deposit(10_000e18, victim); // shares minted?
```

## Pitfalls

- Running the test before the vault has any shares, which changes the formula branch.
- Concluding it is safe because the victim loses only rounding, without checking the full deposit.

## Done when

- The donation is shown to change the share price and the victim's shares are recorded.
- The presence or absence of a mitigation is stated.

## References

- [EIP-4626 tokenised vault](https://eips.ethereum.org/EIPS/eip-4626)
