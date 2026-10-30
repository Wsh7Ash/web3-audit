---
name: access-signature-replay
description: "Verify that a signed message binds chain, contract, nonce and intent, so a signature cannot be reused on another chain or a second time. Use when the contract accepts permit, meta-transaction or off-chain approval signatures"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [access, signatures, replay]
phase: access
---

# Check signed authorisations cannot be replayed

> Verify that a signed message binds chain, contract, nonce and intent, so a signature cannot be reused on another chain or a second time

**Use when:** the contract accepts permit, meta-transaction or off-chain approval signatures

**Avoid when:** there are no signature-based authorisations

## Procedure

1. Read the digest construction and list every field it includes.
2. Check for a nonce that is consumed on use and a domain separator with chain id and verifying contract.
3. Replay the same signature twice and observe whether the second call succeeds.
4. Report any field that is missing, with the consequence of its absence.

## Signals

- digest-fields-listed
- nonce-checked
- replay-attempted

## Patterns

**1. domain separator**

```
bytes32 digest = keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash));
```

## Pitfalls

- A digest without chain id, which makes signatures replayable across forks and testnets.
- A nonce that increments after the external call rather than before it.

## Done when

- Every digest field is listed and its purpose stated.
- A second use of the same signature is shown to fail.

## References

- [EIP-2612 permit](https://eips.ethereum.org/EIPS/eip-2612)
