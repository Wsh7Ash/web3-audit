---
name: arithmetic-rounding-direction
description: "Read every division and confirm it rounds against the user, because a share price that rounds in the user's favour is drained one wei at a time. Use when the contract converts between assets and shares or between debt and collateral"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [arithmetic, rounding, shares]
phase: arithmetic
---

# Check the rounding direction favours the protocol

> Read every division and confirm it rounds against the user, because a share price that rounds in the user's favour is drained one wei at a time

**Use when:** the contract converts between assets and shares or between debt and collateral

**Avoid when:** there is no division in value-bearing code

## Procedure

1. List every division and the direction the result is used in, deposit or withdraw.
2. For deposits, confirm the user receives the smaller share count.
3. For withdrawals, confirm the user receives the smaller asset amount.
4. Test the one-wei boundary both ways and record the result.

## Signals

- divisions-listed
- direction-checked
- boundary-tested

## Patterns

**1. correct direction**

```
shares = assets.mulDiv(totalSupply, totalAssets, Math.Rounding.Floor);
assets = shares.mulDiv(totalAssets, totalSupply, Math.Rounding.Floor);
```

## Pitfalls

- Rounding up on deposit, which lets a user mint more shares than the assets they supplied.
- Assuming integer division cannot be exploited because each step loses at most one wei.

## Done when

- Every division has a stated direction and a reason.
- A one-wei deposit and withdrawal are shown not to favour the user.

## References

- [OpenZeppelin Math.mulDiv](https://docs.openzeppelin.com/contracts/5.x/api/utils#Math)
