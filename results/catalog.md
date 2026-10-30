web3-audit Skill Catalog

50 skills across 13 phases.

| `slug` | title | phase |
|---|---|---|
| `access-initializer-frontrun` | Check the initializer cannot be front-run | access |
| `access-missing-modifier` | Find privileged functions with no guard | access |
| `access-owner-renounce` | Check what renouncing ownership actually breaks | access |
| `access-role-grant-path` | Check who can grant the roles | access |
| `access-signature-replay` | Check signed authorisations cannot be replayed | access |
| `arithmetic-overflow-unchecked` | Check every unchecked block for reachable overflow | arithmetic |
| `arithmetic-precision-loss` | Quantify precision loss across a sequence | arithmetic |
| `arithmetic-rounding-direction` | Check the rounding direction favours the protocol | arithmetic |
| `arithmetic-share-inflation` | Test the first-depositor share inflation attack | arithmetic |
| `invariants-check-after-every-path` | Check invariants on failure paths too | invariants |
| `invariants-differential-testing` | Compare two implementations on the same inputs | invariants |
| `invariants-fuzz-handlers` | Bound fuzz handlers so the search reaches deep states | invariants |
| `invariants-write-in-solidity` | Express invariants as executable Solidity assertions | invariants |
| `model-accounting-identity` | Write the accounting identity the contract must preserve | model |
| `model-privilege-graph` | Draw the privilege graph | model |
| `model-state-machine` | Model the contract as a state machine | model |
| `oracle-decimal-mismatch` | Check oracle decimals against the maths | oracle |
| `oracle-fallback-path` | Check the fallback when the primary oracle fails | oracle |
| `oracle-stale-price` | Check the oracle freshness bound | oracle |
| `oracle-twap-manipulation` | Check how much capital moves a TWAP | oracle |
| `randomness-block-values` | Reject block values as a randomness source | randomness |
| `randomness-commit-reveal` | Check a commit-reveal scheme for grinding and withholding | randomness |
| `randomness-oracle-vrf` | Check a VRF integration for request and fulfilment handling | randomness |
| `recon-bytecode-match` | Prove the reviewed source matches the deployed bytecode | recon |
| `recon-scope-contracts` | Enumerate the contracts and what they trust | recon |
| `recon-value-flow` | Map where value enters and leaves | recon |
| `reentrancy-checks-effects-interactions` | Verify the checks-effects-interactions order | reentrancy |
| `reentrancy-cross-function` | Test cross-function reentrancy on shared state | reentrancy |
| `reentrancy-flashloan-context` | Test reentrancy under a flash-loan balance | reentrancy |
| `reentrancy-read-only` | Check read-only reentrancy through view functions | reentrancy |
| `reentrancy-trace-external-calls` | Trace every external call and what it can re-enter | reentrancy |
| `reporting-finding-template` | Write a finding with location, impact and proof | reporting |
| `reporting-fix-verification` | State how the fix will be verified | reporting |
| `reporting-scanner-leads` | Turn scanner output into reviewed findings, not a dump | reporting |
| `reporting-severity-basis` | Justify severity with reachability and value at risk | reporting |
| `storage-array-removal` | Check array removal for skipped elements | storage |
| `storage-delete-gap` | Check what a delete actually clears | storage |
| `storage-layout-collision` | Check storage layout between proxy and implementation | storage |
| `storage-struct-packing` | Check struct packing against gas and correctness assumptions | storage |
| `testing-fork-reproduction` | Reproduce a finding on a fork at the vulnerable block | testing |
| `testing-gas-and-revert-profile` | Record gas and revert behaviour for the sequence | testing |
| `testing-minimal-sequence` | Cut the exploit to the shortest sequence | testing |
| `testing-negative-control` | Add a control that must not exploit | testing |
| `testing-state-diff-assertions` | Assert on the state diff, not just the balance | testing |
| `triage-duplicate-advisory` | Check advisories and prior audits before reporting | triage |
| `triage-exploitability-verdict` | Give each finding an explicit exploitability verdict | triage |
| `upgrade-implementation-lock` | Check who can swap the implementation and how fast | upgrade |
| `upgrade-initializer-reinit` | Check an upgrade cannot re-run initialization | upgrade |
| `upgrade-selector-collision` | Check new functions do not collide with proxy selectors | upgrade |
| `upgrade-storage-gap` | Check the storage gap is large enough | upgrade |
