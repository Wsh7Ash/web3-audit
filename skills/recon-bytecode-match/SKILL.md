---
name: recon-bytecode-match
description: "Compare a locally compiled build against on-chain code so a finding cannot be dismissed as applying to a different version. Use when the review is of a repository but the finding is about a live deployment"
pack: web3-audit
version: 1.0.0
category: web3-security
tags: [recon, bytecode, verification]
phase: recon
---

# Prove the reviewed source matches the deployed bytecode

> Compare a locally compiled build against on-chain code so a finding cannot be dismissed as applying to a different version

**Use when:** the review is of a repository but the finding is about a live deployment

**Avoid when:** the contract is not deployed or the audit is source-only by agreement

## Procedure

1. Compile the repository with the exact compiler version and settings recorded in the config.
2. Fetch the deployed bytecode and strip immutable and metadata sections from both.
3. Compare the remaining runtime bytecode and record the hash of each side.
4. If they differ, locate the difference before writing any finding about the deployment.

## Signals

- compiled-locally
- bytecode-stripped
- hashes-compared

## Patterns

**1. compare runtime code**

```
cast code 0xContract > deployed.hex
forge inspect Vault bytecode > local.hex
diff <(xxd -p deployed.hex) <(xxd -p local.hex) | head
```

## Pitfalls

- Diffing raw bytecode including metadata, which differs on every build even when logic is identical.
- Using a compiler version that differs from the deployment and reporting the difference as a bug.

## Done when

- Both runtime hashes are recorded and the comparison result is stated.
- Any mismatch is explained before findings are written.

## References

- [Solidity metadata](https://docs.soliditylang.org/en/latest/metadata.html)
