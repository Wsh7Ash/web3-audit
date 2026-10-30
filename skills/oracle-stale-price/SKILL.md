---
name: oracle-stale-price
description: "Read the staleness check and confirm it exists and is smaller than the heartbeat, so a price cannot be used long after it stopped updating. Use when the contract reads a Chainlink or TWAP price to value collateral"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [oracle, staleness, chainlink]
phase: oracle
---

# Check the oracle freshness bound

> Read the staleness check and confirm it exists and is smaller than the heartbeat, so a price cannot be used long after it stopped updating

**Use when:** the contract reads a Chainlink or TWAP price to value collateral

**Avoid when:** the price is derived on-chain in the same transaction, such as a pool spot price used only as a reference

## Procedure

1. Identify the feed, its heartbeat and its deviation threshold.
2. Read the contract's staleness constant and compare it with the heartbeat.
3. Force a stale answer in a fork test and check whether the contract reverts.
4. Report the bound and whether it is enforced.

## Signals

- feed-identified
- bound-compared
- stale-answer-tested

## Patterns

**1. freshness**

```
(, int256 answer, , uint256 updatedAt, ) = feed.latestRoundData();
require(block.timestamp - updatedAt <= MAX_STALENESS, "stale");
require(answer > 0, "bad answer");
```

## Pitfalls

- Checking staleness but not the answer sign, so a negative or zero price passes.
- Using a bound larger than the heartbeat, which accepts a price that never updated.

## Done when

- The feed's heartbeat and the contract's bound are recorded together.
- A stale answer is shown to be rejected, or the finding is written.

## References

- [Chainlink data feeds](https://docs.chain.link/data-feeds)
