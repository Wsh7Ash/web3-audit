"""Part 1 of the web3-audit corpus: recon, model, invariants, access, reentrancy."""

from __future__ import annotations

from typing import Any

SKILLS: list[dict[str, Any]] = [
    {
        "slug": "recon-scope-contracts",
        "title": "Enumerate the contracts and what they trust",
        "summary": "List every deployed contract, its proxy target, its admin and the tokens it can move, so the review states what is in scope before reading logic",
        "use_when": "the audit starts from a repository or an address list and the trust graph is unknown",
        "avoid_when": "the engagement covers one immutable contract with no external dependencies",
        "tags": ["recon", "scope", "trust"],
        "steps": [
            "List contracts, their addresses, bytecode hashes and whether each is a proxy.",
            "For every proxy, resolve the implementation address and record how it can be upgraded.",
            "Record admin roles, pausers, minters and any address with privileged withdrawal rights.",
            "Mark each contract as in scope, out of scope or trusted-dependency with the reason.",
        ],
        "signals": ["contracts-listed", "proxies-resolved", "roles-recorded"],
        "patterns": [
            (
                "implementation slot",
                "cast storage 0xProxy 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc",
            )
        ],
        "pitfalls": [
            "Reviewing the repository while the deployed bytecode differs from it; hash both.",
            "Treating a trusted dependency as in scope, which inflates the report with issues the client cannot fix.",
        ],
        "done_when": [
            "Every contract has a scope decision and a bytecode hash.",
            "Every proxy has a resolved implementation and upgrade authority.",
        ],
        "refs": [
            "[EIP-1967 storage slots](https://eips.ethereum.org/EIPS/eip-1967)",
        ],
        "meta": {"phase": "recon"},
    },
    {
        "slug": "recon-bytecode-match",
        "title": "Prove the reviewed source matches the deployed bytecode",
        "summary": "Compare a locally compiled build against on-chain code so a finding cannot be dismissed as applying to a different version",
        "use_when": "the review is of a repository but the finding is about a live deployment",
        "avoid_when": "the contract is not deployed or the audit is source-only by agreement",
        "tags": ["recon", "bytecode", "verification"],
        "steps": [
            "Compile the repository with the exact compiler version and settings recorded in the config.",
            "Fetch the deployed bytecode and strip immutable and metadata sections from both.",
            "Compare the remaining runtime bytecode and record the hash of each side.",
            "If they differ, locate the difference before writing any finding about the deployment.",
        ],
        "signals": ["compiled-locally", "bytecode-stripped", "hashes-compared"],
        "patterns": [
            (
                "compare runtime code",
                "cast code 0xContract > deployed.hex\nforge inspect Vault bytecode > local.hex\ndiff <(xxd -p deployed.hex) <(xxd -p local.hex) | head",
            )
        ],
        "pitfalls": [
            "Diffing raw bytecode including metadata, which differs on every build even when logic is identical.",
            "Using a compiler version that differs from the deployment and reporting the difference as a bug.",
        ],
        "done_when": [
            "Both runtime hashes are recorded and the comparison result is stated.",
            "Any mismatch is explained before findings are written.",
        ],
        "refs": [
            "[Solidity metadata](https://docs.soliditylang.org/en/latest/metadata.html)",
        ],
        "meta": {"phase": "recon"},
    },
    {
        "slug": "recon-value-flow",
        "title": "Map where value enters and leaves",
        "summary": "Draw the flow of ETH and tokens through the system so the review focuses on paths where value can be redirected rather than on every function",
        "use_when": "the system holds or moves funds and the reviewer needs to prioritise",
        "avoid_when": "the contract is a pure registry with no value at stake",
        "tags": ["recon", "value", "flows"],
        "steps": [
            "List every function that can receive ETH or transfer tokens, including internal helpers.",
            "For each, name the precondition and who can call it.",
            "Mark the functions where the amount is computed from a balance, a rate or an oracle.",
            "Rank the paths by value at risk and start the review from the top.",
        ],
        "signals": ["value-paths-listed", "preconditions-named", "paths-ranked"],
        "patterns": [
            (
                "value path",
                "deposit() payable -> shares = amount * totalSupply / totalAssets\nwithdraw(shares) -> assets = shares * totalAssets / totalSupply",
            )
        ],
        "pitfalls": [
            "Reviewing setters first because they are easy, and never reaching the share maths.",
            "Missing value paths that arrive through a callback rather than a payable function.",
        ],
        "done_when": [
            "Every value path has a caller, a precondition and a computed amount.",
            "The paths are ranked and the ranking is recorded in the report.",
        ],
        "refs": [
            "[Ethereum value transfer](https://ethereum.org/en/developers/docs/transactions/)",
        ],
        "meta": {"phase": "recon"},
    },
    {
        "slug": "model-state-machine",
        "title": "Model the contract as a state machine",
        "summary": "Write the states a position can be in and the allowed transitions, so a missing guard shows up as a transition that should not exist",
        "use_when": "the contract has lifecycle stages such as open, locked, settled or paused",
        "avoid_when": "the contract is stateless apart from a single mapping",
        "tags": ["model", "state", "transitions"],
        "steps": [
            "List the state variables that gate behaviour and the values they can take.",
            "Write the allowed transitions with the function that performs each one.",
            "Walk every function and check that it either requires the right state or is state-independent.",
            "Report any transition that is reachable without its guard.",
        ],
        "signals": ["states-listed", "transitions-written", "guards-checked"],
        "patterns": [
            (
                "state machine",
                "states: Open -> Locked -> Settled\nOpen --lock()--> Locked    requires block.timestamp >= end\nLocked --settle()--> Settled  requires oracle.ready()",
            )
        ],
        "pitfalls": [
            "Modelling only the happy path and leaving pause, cancel and emergency exits out of the diagram.",
            "Assuming a guard exists because a modifier is named pauseable without reading what it checks.",
        ],
        "done_when": [
            "Every state and transition is written down with its guard.",
            "Each function is checked against the model and exceptions are listed.",
        ],
        "refs": [
            "[Solidity security considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)",
        ],
        "meta": {"phase": "model"},
    },
    {
        "slug": "model-accounting-identity",
        "title": "Write the accounting identity the contract must preserve",
        "summary": "State an equation such as sum of balances equals total supply plus escrow, so a broken invariant is a failing comparison rather than an opinion",
        "use_when": "the contract tracks shares, debts, collateral or internal balances",
        "avoid_when": "the contract holds no accounting state",
        "tags": ["model", "accounting", "invariant"],
        "steps": [
            "Write the equation that must hold after every external call.",
            "Express each term as a function you can read on-chain or in a test.",
            "Check the equation after each state-changing path, including the failure paths.",
            "Report the smallest sequence that makes it fail, not the equation alone.",
        ],
        "signals": ["identity-written", "terms-expressible", "paths-checked"],
        "patterns": [
            (
                "identity",
                "sum(userShares) == totalSupply\nsum(userBalances) + escrowed == token.balanceOf(vault)",
            )
        ],
        "pitfalls": [
            "An identity that only holds at rest and not after a partial withdrawal.",
            "Writing the identity with a term the contract does not expose, which makes it untestable.",
        ],
        "done_when": [
            "The identity is written and every term is readable on-chain or in a test.",
            "Every state-changing path was checked against it.",
        ],
        "refs": [
            "[EIP-4626 tokenised vault](https://eips.ethereum.org/EIPS/eip-4626)",
        ],
        "meta": {"phase": "model"},
    },
    {
        "slug": "model-privilege-graph",
        "title": "Draw the privilege graph",
        "summary": "Record which role can reach which state change, so a missing modifier is visible against what the role is supposed to be able to do",
        "use_when": "the contract has more than one privileged role",
        "avoid_when": "there is a single owner and no delegated roles",
        "tags": ["model", "roles", "privilege"],
        "steps": [
            "List every role and how it is granted, revoked and renounced.",
            "List every state-changing function and the role that should reach it.",
            "Compare the intended graph with the modifiers actually applied.",
            "Report each function reachable by a broader role than intended.",
        ],
        "signals": ["roles-listed", "intended-graph-written", "actual-modifiers-compared"],
        "patterns": [
            (
                "role check",
                "function setFee(uint256 f) external onlyRole(FEE_ADMIN) { fee = f; }",
            )
        ],
        "pitfalls": [
            "Assuming DEFAULT_ADMIN_ROLE is harmless because it is a role name rather than an owner.",
            "Missing the initializer that grants a role, which leaves the grant path open after deploy.",
        ],
        "done_when": [
            "Every role and every guarded function appear in the graph.",
            "Broader-than-intended reachability is listed with the function.",
        ],
        "refs": [
            "[OpenZeppelin AccessControl](https://docs.openzeppelin.com/contracts/5.x/access-control)",
        ],
        "meta": {"phase": "model"},
    },
    {
        "slug": "invariants-write-in-solidity",
        "title": "Express invariants as executable Solidity assertions",
        "summary": "Turn each written invariant into a function a test or a handler can call, so the invariant is checked by code rather than by memory",
        "use_when": "the accounting identity is written and the next step is proving it holds",
        "avoid_when": "the invariant cannot be observed from outside the contract and no test hook exists",
        "tags": ["invariants", "solidity", "testing"],
        "steps": [
            "Write one external view function per invariant that reverts or returns false when violated.",
            "Keep the function free of state changes so it can be called at any point in a test.",
            "Call it after every state-changing action in the test harness.",
            "Record which invariant each function encodes so a failure names the rule.",
        ],
        "signals": ["invariant-functions-written", "read-only", "checked-every-step"],
        "patterns": [
            (
                "invariant function",
                "function invariant_solvent() external view returns (bool) {\n  return totalAssets() >= totalSupply();\n}",
            )
        ],
        "pitfalls": [
            "An invariant function that reads cached state, so it agrees with itself instead of with reality.",
            "Checking only at the end of a test, which hides the intermediate state where it broke.",
        ],
        "done_when": [
            "Every written invariant has a read-only on-chain check.",
            "The harness calls each check after every action.",
        ],
        "refs": [
            "[Foundry invariant testing](https://book.getfoundry.sh/forge/invariant-testing)",
        ],
        "meta": {"phase": "invariants"},
    },
    {
        "slug": "invariants-fuzz-handlers",
        "title": "Bound fuzz handlers so the search reaches deep states",
        "summary": "Restrict fuzzed actors and amounts to realistic ranges, so the campaign spends its budget on reachable states instead of reverting on the first call",
        "use_when": "an invariant fuzzer keeps finding trivial reverts rather than deep failures",
        "avoid_when": "the campaign is exploratory and the goal is to find any revert",
        "tags": ["invariants", "fuzzing", "handlers"],
        "steps": [
            "Restrict actors to a small set of funded addresses.",
            "Clamp amounts to the range the protocol actually supports.",
            "Add a handler that performs the realistic action sequence rather than a raw call.",
            "Re-run and confirm the campaign reaches states beyond the first deposit.",
        ],
        "signals": ["actors-bounded", "amounts-clamped", "deep-states-reached"],
        "patterns": [
            (
                "handler",
                "function deposit(uint256 amount) public {\n  amount = bound(amount, 1, 1_000e18);\n  vm.prank(actor);\n  vault.deposit(amount);\n}",
            )
        ],
        "pitfalls": [
            "Letting the fuzzer pick arbitrary addresses, which mostly produces calls that revert on authorisation.",
            "Bounding so tightly that the campaign never reaches the boundary where the bug lives.",
        ],
        "done_when": [
            "Actors and amounts are bounded with a stated reason.",
            "The campaign is shown to reach states past the first action.",
        ],
        "refs": [
            "[Foundry invariant testing](https://book.getfoundry.sh/forge/invariant-testing)",
        ],
        "meta": {"phase": "invariants"},
    },
    {
        "slug": "invariants-differential-testing",
        "title": "Compare two implementations on the same inputs",
        "summary": "Run the contract and a simple reference implementation over identical inputs, so a divergence is a concrete counterexample rather than a suspicion",
        "use_when": "the contract reimplements a known formula or a specification exists",
        "avoid_when": "there is no reference implementation and none can be written cheaply",
        "tags": ["invariants", "differential", "reference"],
        "steps": [
            "Write the simplest correct reference for the formula, ignoring gas and structure.",
            "Feed both implementations the same pseudo-random input sequence.",
            "Stop at the first divergence and record the input that caused it.",
            "Check the divergence is real, not a rounding difference the protocol documents.",
        ],
        "signals": ["reference-written", "same-inputs-fed", "divergence-captured"],
        "patterns": [
            (
                "differential",
                "for (uint256 i; i < 256; ++i) {\n  uint256 x = uint256(keccak256(abi.encode(i)));\n  assertEq(contract.f(x), reference.f(x));\n}",
            )
        ],
        "pitfalls": [
            "A reference implementation that copies the contract's own arithmetic and therefore cannot diverge.",
            "Treating a documented rounding direction as a bug.",
        ],
        "done_when": [
            "A reference exists and both run on identical inputs.",
            "The first divergence is recorded with its input and classified.",
        ],
        "refs": [
            "[Solidity math](https://docs.soliditylang.org/en/latest/types.html#integers)",
        ],
        "meta": {"phase": "invariants"},
    },
    {
        "slug": "invariants-check-after-every-path",
        "title": "Check invariants on failure paths too",
        "summary": "Re-check the accounting identity after reverts and partial operations, because a function that reverts after a transfer still moved the tokens",
        "use_when": "the contract makes external calls before its final state write",
        "avoid_when": "the contract performs no external calls and reverts atomically by construction",
        "tags": ["invariants", "failure", "reverts"],
        "steps": [
            "Identify every function that makes an external call before its last state write.",
            "Force the call to fail, using a token that reverts on transfer where possible.",
            "Check the invariant after the revert and compare with the state before the call.",
            "Report any case where the revert did not undo the earlier effect.",
        ],
        "signals": ["external-calls-identified", "failure-forced", "invariant-rechecked"],
        "patterns": [
            (
                "forced failure",
                "token.setRevertOnTransfer(true);\nvm.expectRevert();\nvault.withdraw(shares);\nassertTrue(vault.invariant_solvent());",
            )
        ],
        "pitfalls": [
            "Testing only happy paths, where the invariant trivially holds by construction.",
            "Assuming a revert rolls back an external call that already succeeded on another contract.",
        ],
        "done_when": [
            "Every external-call-then-state-write path was exercised with a failure.",
            "The invariant is shown to hold after each forced failure, or a finding is recorded.",
        ],
        "refs": [
            "[Solidity security considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)",
        ],
        "meta": {"phase": "invariants"},
    },
    {
        "slug": "access-missing-modifier",
        "title": "Find privileged functions with no guard",
        "summary": "Compare every state-changing function against the privilege graph and report the ones reachable by anyone",
        "use_when": "the privilege graph is written and the next step is checking it against code",
        "avoid_when": "the contract is intentionally permissionless and every function is meant to be public",
        "tags": ["access", "modifiers", "review"],
        "steps": [
            "List every external and public function that writes state.",
            "For each, read the declaration and the first lines of the body for a guard.",
            "Cross-check with the privilege graph to see whether the missing guard matters.",
            "Report the function, the intended role and the reachable caller.",
        ],
        "signals": ["writers-listed", "guards-read", "reachability-stated"],
        "patterns": [
            (
                "compare",
                "grep -n 'function .*external' Vault.sol | grep -v 'view\\|pure'",
            )
        ],
        "pitfalls": [
            "Missing a guard that is applied inside an internal function the public one calls.",
            "Assuming a function is safe because its name sounds administrative.",
        ],
        "done_when": [
            "Every state-writing function has a guard decision recorded.",
            "Any missing guard is mapped to the caller who can reach it.",
        ],
        "refs": [
            "[OpenZeppelin AccessControl](https://docs.openzeppelin.com/contracts/5.x/access-control)",
        ],
        "meta": {"phase": "access"},
    },
    {
        "slug": "access-role-grant-path",
        "title": "Check who can grant the roles",
        "summary": "Trace the grant and revoke functions so a role that looks restricted cannot be handed out by a broader role",
        "use_when": "the contract uses role-based access control",
        "avoid_when": "access is a single immutable owner with no delegation",
        "tags": ["access", "roles", "delegation"],
        "steps": [
            "Find every call to grantRole, _grantRole and any custom grant function.",
            "Record the role required to call each one and whether it is the role's admin.",
            "Check whether a role can grant itself or a role above it.",
            "Report any grant path reachable by a role that should not have it.",
        ],
        "signals": ["grant-paths-found", "admin-roles-recorded", "escalation-checked"],
        "patterns": [
            (
                "admin role",
                "bytes32 public constant MINTER_ROLE = keccak256(\"MINTER_ROLE\");\n// admin of MINTER_ROLE is DEFAULT_ADMIN_ROLE by default",
            )
        ],
        "pitfalls": [
            "Forgetting that DEFAULT_ADMIN_ROLE can grant itself to another address.",
            "Custom grant functions that skip the role-admin check entirely.",
        ],
        "done_when": [
            "Every grant path has its required role recorded.",
            "Escalation from a lower role to a higher one is ruled out or reported.",
        ],
        "refs": [
            "[OpenZeppelin AccessControl](https://docs.openzeppelin.com/contracts/5.x/access-control)",
        ],
        "meta": {"phase": "access"},
    },
    {
        "slug": "access-initializer-frontrun",
        "title": "Check the initializer cannot be front-run",
        "summary": "Verify that initialization is atomic with deployment or guarded, so an attacker cannot become the owner of a freshly deployed proxy",
        "use_when": "the contract uses an initializer pattern instead of a constructor",
        "avoid_when": "the contract uses a constructor with immutable arguments",
        "tags": ["access", "initializer", "deployment"],
        "steps": [
            "Locate every initializer and whether it sets an initialized flag.",
            "Check whether deployment and initialization happen in the same transaction.",
            "If they are separate, attempt to call initialize from a different address first.",
            "Report the window and what an attacker gains by taking it.",
        ],
        "signals": ["initializers-found", "atomicity-checked", "window-tested"],
        "patterns": [
            (
                "guarded initializer",
                "function initialize(address owner_) external initializer {\n  __Ownable_init(owner_);\n}",
            )
        ],
        "pitfalls": [
            "A proxy deployed in one transaction and initialized in another, which leaves an open window.",
            "An initializer without the initializer modifier, which can be called twice.",
        ],
        "done_when": [
            "Every initializer has a guard and deployment atomicity is established.",
            "Any open window is demonstrated or ruled out.",
        ],
        "refs": [
            "[OpenZeppelin Initializable](https://docs.openzeppelin.com/contracts/5.x/api/proxy#Initializable)",
        ],
        "meta": {"phase": "access"},
    },
    {
        "slug": "access-signature-replay",
        "title": "Check signed authorisations cannot be replayed",
        "summary": "Verify that a signed message binds chain, contract, nonce and intent, so a signature cannot be reused on another chain or a second time",
        "use_when": "the contract accepts permit, meta-transaction or off-chain approval signatures",
        "avoid_when": "there are no signature-based authorisations",
        "tags": ["access", "signatures", "replay"],
        "steps": [
            "Read the digest construction and list every field it includes.",
            "Check for a nonce that is consumed on use and a domain separator with chain id and verifying contract.",
            "Replay the same signature twice and observe whether the second call succeeds.",
            "Report any field that is missing, with the consequence of its absence.",
        ],
        "signals": ["digest-fields-listed", "nonce-checked", "replay-attempted"],
        "patterns": [
            (
                "domain separator",
                "bytes32 digest = keccak256(abi.encodePacked(\"\\x19\\x01\", DOMAIN_SEPARATOR, structHash));",
            )
        ],
        "pitfalls": [
            "A digest without chain id, which makes signatures replayable across forks and testnets.",
            "A nonce that increments after the external call rather than before it.",
        ],
        "done_when": [
            "Every digest field is listed and its purpose stated.",
            "A second use of the same signature is shown to fail.",
        ],
        "refs": [
            "[EIP-2612 permit](https://eips.ethereum.org/EIPS/eip-2612)",
        ],
        "meta": {"phase": "access"},
    },
    {
        "slug": "access-owner-renounce",
        "title": "Check what renouncing ownership actually breaks",
        "summary": "Trace every onlyOwner path before the owner renounces, so a renounce that is meant to be safe does not freeze withdrawals or leave the contract unupgradeable",
        "use_when": "the deployment plan includes renouncing ownership or burning the admin role",
        "avoid_when": "ownership is intentionally retained and timelocked",
        "tags": ["access", "ownership", "renounce"],
        "steps": [
            "List every function gated by the role that will be renounced.",
            "Classify each as recoverable without the role or permanently broken.",
            "Simulate the renounce in a fork or a test and attempt the affected actions.",
            "Report the functions that become unreachable, with the funds or state they strand.",
        ],
        "signals": ["gated-functions-listed", "renounce-simulated", "stranded-state-identified"],
        "patterns": [
            (
                "renounce then test",
                "vault.renounceOwnership();\nvm.expectRevert();\nvault.emergencyWithdraw();",
            )
        ],
        "pitfalls": [
            "Renouncing ownership while a pause is active, which makes the pause permanent.",
            "Assuming renouncing is safe because the contract is immutable; proxies usually are not.",
        ],
        "done_when": [
            "Every gated function is classified after renounce.",
            "Any stranded funds or state are reported before the renounce happens.",
        ],
        "refs": [
            "[OpenZeppelin Ownable](https://docs.openzeppelin.com/contracts/5.x/api/access#Ownable)",
        ],
        "meta": {"phase": "access"},
    },
    {
        "slug": "reentrancy-trace-external-calls",
        "title": "Trace every external call and what it can re-enter",
        "summary": "List each external call with the state already written and the state still to write, so reentrancy is a property of a specific function rather than a vibe",
        "use_when": "the contract calls tokens, hooks, receivers or other contracts",
        "avoid_when": "the contract makes no external calls",
        "tags": ["reentrancy", "external-calls", "ordering"],
        "steps": [
            "List every external call, including token transfers, hooks and low-level calls.",
            "For each, record the state reads and writes that happen before and after.",
            "Identify the entry points an attacker could call from inside the callback.",
            "Report the call and the entry point that makes it exploitable, or state why none does.",
        ],
        "signals": ["calls-listed", "ordering-recorded", "entry-points-identified"],
        "patterns": [
            (
                "order",
                "balances[msg.sender] -= amount;   // write first\n(bool ok, ) = msg.sender.call{value: amount}(\"\");  // then call\nrequire(ok, \"transfer failed\");",
            )
        ],
        "pitfalls": [
            "Treating a call to a trusted token as safe without checking whether the token has hooks.",
            "Looking only at the function under review and missing a callback into a different entry point.",
        ],
        "done_when": [
            "Every external call has its before/after state recorded.",
            "Each call is either shown exploitable or shown why it is not.",
        ],
        "refs": [
            "[Consensys reentrancy](https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/)",
        ],
        "meta": {"phase": "reentrancy"},
    },
    {
        "slug": "reentrancy-checks-effects-interactions",
        "title": "Verify the checks-effects-interactions order",
        "summary": "Read each value-moving function and confirm state is written before the external call, which is the ordering that makes most reentrancy harmless",
        "use_when": "a function transfers value and updates balances in the same body",
        "avoid_when": "the function is a pure view or its only call is to an immutable trusted contract",
        "tags": ["reentrancy", "ordering", "pattern"],
        "steps": [
            "Read the function body and mark the checks, the effects and the interactions.",
            "Confirm every effect precedes every interaction.",
            "Where an interaction precedes an effect, check for a reentrancy guard.",
            "Report the function and the line where the order inverts.",
        ],
        "signals": ["body-classified", "ordering-confirmed", "guards-checked"],
        "patterns": [
            (
                "guarded",
                "function withdraw(uint256 amount) external nonReentrant {\n  require(balances[msg.sender] >= amount);\n  balances[msg.sender] -= amount;\n  payable(msg.sender).transfer(amount);\n}",
            )
        ],
        "pitfalls": [
            "A guard on one entry point but not the sibling that shares the same balance.",
            "Trusting a guard that was applied to the wrong modifier name after a refactor.",
        ],
        "done_when": [
            "Every value-moving function is classified and its ordering recorded.",
            "Any inversion is either guarded or reported.",
        ],
        "refs": [
            "[Consensys reentrancy](https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/)",
        ],
        "meta": {"phase": "reentrancy"},
    },
]