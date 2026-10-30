---
name: randomness-oracle-vrf
description: "Verify that the request id is bound to the consumer, the callback is authorised, and a missing fulfilment cannot be re-requested to reroll. Use when the contract uses a verifiable random function oracle"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [randomness, vrf, callback]
phase: randomness
---

# Check a VRF integration for request and fulfilment handling

> Verify that the request id is bound to the consumer, the callback is authorised, and a missing fulfilment cannot be re-requested to reroll

**Use when:** the contract uses a verifiable random function oracle

**Avoid when:** randomness is generated on-chain and no external callback exists

## Procedure

1. Read the request function and confirm the request id is stored with the consumer.
2. Read the fulfilment callback and confirm it checks both the sender and the request id.
3. Attempt to call the callback directly with a chosen random word.
4. Report any path that lets a caller supply or reroll the randomness.

## Signals

- request-stored
- callback-authorised
- direct-call-tested

## Patterns

**1. fulfilment**

```
function fulfillRandomWords(uint256 requestId, uint256[] memory words)
  internal override {
  require(msg.sender == vrfCoordinator);
  require(requestId == pendingRequest);
}
```

## Pitfalls

- A callback that trusts the caller, which lets anyone supply a favourable random word.
- Allowing a new request before the old one is fulfilled, which gives a reroll.

## Done when

- Request id binding and callback authorisation are both verified.
- A direct callback call is shown to fail.

## References

- [Chainlink VRF](https://docs.chain.link/vrf)
