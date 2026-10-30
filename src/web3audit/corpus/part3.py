"""Part 3 of the web3-audit corpus: upgrade, randomness, testing, reporting, triage."""

from __future__ import annotations

from typing import Any

SKILLS: list[dict[str, Any]] = [
    {
        "slug": "upgrade-implementation-lock",
        "title": "Check who can swap the implementation and how fast",
        "summary": "Trace the upgrade authority and any delay, because an EOA with immediate upgrade rights can redirect every deposit without a code bug",
        "use_when": "the system uses a proxy with an upgrade admin",
        "avoid_when": "the implementation is immutable",
        "tags": ["upgrade", "admin", "trust"],
        "steps": [
            "Read the proxy's upgrade function and its access control.",
            "Determine whether the admin is an EOA, a multisig or a timelock, and the delay.",
            "Check whether the upgrade can be performed while paused or mid-withdrawal.",
            "Report the authority, the delay and what an immediate upgrade would let it do.",
        ],
        "signals": ["authority-read", "delay-recorded", "window-assessed"],
        "patterns": [
            (
                "upgradeToAndCall",
                "function _authorizeUpgrade(address impl) internal override onlyOwner {}",
            )
        ],
        "pitfalls": [
            "Treating a multisig as a mitigation without checking its threshold and signer set.",
            "Missing that the upgrade function is exposed on the implementation as well as the proxy.",
        ],
        "done_when": [
            "The upgrade authority and delay are recorded.",
            "The consequence of an immediate upgrade is stated.",
        ],
        "refs": [
            "[EIP-1967 storage slots](https://eips.ethereum.org/EIPS/eip-1967)",
        ],
        "meta": {"phase": "upgrade"},
    },
    {
        "slug": "upgrade-selector-collision",
        "title": "Check new functions do not collide with proxy selectors",
        "summary": "Compare the implementation's function selectors against the proxy's own, because a collision routes the call to the proxy instead of the implementation",
        "use_when": "a new implementation adds functions to an existing proxy",
        "avoid_when": "the proxy uses a fallback that delegates everything and has no other functions",
        "tags": ["upgrade", "selectors", "collision"],
        "steps": [
            "List the proxy's own external functions and their selectors.",
            "List the new implementation's selectors.",
            "Compute the intersection and check for the proxy's upgrade or admin selectors.",
            "Report any new function whose selector the proxy already uses.",
        ],
        "signals": ["selectors-listed", "intersection-computed", "collisions-reported"],
        "patterns": [
            (
                "selector",
                "cast sig 'upgradeTo(address)'   # 0x3659cfe6",
            )
        ],
        "pitfalls": [
            "Assuming four-byte collisions are impossible at this size; they happen with cloned codebases.",
            "Forgetting the transparent proxy rule that makes admin calls bypass the fallback.",
        ],
        "done_when": [
            "Both selector sets are listed and intersected.",
            "Any collision is reported with the function that becomes unreachable.",
        ],
        "refs": [
            "[EIP-1967 storage slots](https://eips.ethereum.org/EIPS/eip-1967)",
        ],
        "meta": {"phase": "upgrade"},
    },
    {
        "slug": "randomness-block-values",
        "title": "Reject block values as a randomness source",
        "summary": "Find every use of block.timestamp, blockhash or prevrandao in a draw and show how a validator or a caller can bias it",
        "use_when": "the contract picks winners, assigns traits or samples from a set",
        "avoid_when": "the value is used only for timing and nothing of value depends on it",
        "tags": ["randomness", "block-values", "bias"],
        "steps": [
            "Find every expression that derives a random-looking value.",
            "Identify who can influence each input and how much.",
            "Simulate two consecutive blocks and show the outcome difference.",
            "Report the input, the influencer and the advantage.",
        ],
        "signals": ["sources-found", "influencers-identified", "bias-shown"],
        "patterns": [
            (
                "bad draw",
                "uint256 winner = uint256(keccak256(abi.encodePacked(block.timestamp, block.prevrandao))) % players.length;",
            )
        ],
        "pitfalls": [
            "Concluding there is no bias because the attacker cannot predict the hash exactly.",
            "Missing that a caller can revert and retry until the draw favours them.",
        ],
        "done_when": [
            "Every random-looking derivation has its inputs and influencers listed.",
            "The advantage gained is demonstrated or bounded.",
        ],
        "refs": [
            "[Solidity block values](https://docs.soliditylang.org/en/latest/units-and-global-variables.html#block-and-transaction-properties)",
        ],
        "meta": {"phase": "randomness"},
    },
    {
        "slug": "randomness-commit-reveal",
        "title": "Check a commit-reveal scheme for grinding and withholding",
        "summary": "Verify that the reveal window, the deposit and the ordering prevent a participant from choosing whether to reveal after seeing others",
        "use_when": "the contract implements commit-reveal for a draw or an auction",
        "avoid_when": "randomness comes from an external oracle with its own guarantees",
        "tags": ["randomness", "commit-reveal", "grinding"],
        "steps": [
            "Read the commit and reveal windows and what happens if a participant never reveals.",
            "Check whether the last revealer can compute the outcome before revealing.",
            "Test withholding the final reveal and observe the fallback.",
            "Report the advantage available to the last actor in the window.",
        ],
        "signals": ["windows-read", "last-actor-analysed", "withholding-tested"],
        "patterns": [
            (
                "commit",
                "commit = keccak256(abi.encode(secret, msg.sender, nonce));",
            )
        ],
        "pitfalls": [
            "A commit that omits the sender, which lets anyone reveal another's secret.",
            "No penalty for withholding, which makes the last reveal optional and therefore a choice.",
        ],
        "done_when": [
            "The windows and the withholding behaviour are recorded.",
            "The last actor's advantage is stated or shown to be zero.",
        ],
        "refs": [
            "[Commit-reveal schemes](https://ethereum.org/en/developers/docs/smart-contracts/)",
        ],
        "meta": {"phase": "randomness"},
    },
    {
        "slug": "randomness-oracle-vrf",
        "title": "Check a VRF integration for request and fulfilment handling",
        "summary": "Verify that the request id is bound to the consumer, the callback is authorised, and a missing fulfilment cannot be re-requested to reroll",
        "use_when": "the contract uses a verifiable random function oracle",
        "avoid_when": "randomness is generated on-chain and no external callback exists",
        "tags": ["randomness", "vrf", "callback"],
        "steps": [
            "Read the request function and confirm the request id is stored with the consumer.",
            "Read the fulfilment callback and confirm it checks both the sender and the request id.",
            "Attempt to call the callback directly with a chosen random word.",
            "Report any path that lets a caller supply or reroll the randomness.",
        ],
        "signals": ["request-stored", "callback-authorised", "direct-call-tested"],
        "patterns": [
            (
                "fulfilment",
                "function fulfillRandomWords(uint256 requestId, uint256[] memory words)\n  internal override {\n  require(msg.sender == vrfCoordinator);\n  require(requestId == pendingRequest);\n}",
            )
        ],
        "pitfalls": [
            "A callback that trusts the caller, which lets anyone supply a favourable random word.",
            "Allowing a new request before the old one is fulfilled, which gives a reroll.",
        ],
        "done_when": [
            "Request id binding and callback authorisation are both verified.",
            "A direct callback call is shown to fail.",
        ],
        "refs": [
            "[Chainlink VRF](https://docs.chain.link/vrf)",
        ],
        "meta": {"phase": "randomness"},
    },
    {
        "slug": "testing-fork-reproduction",
        "title": "Reproduce a finding on a fork at the vulnerable block",
        "summary": "Pin the fork to the block before the fix or the exploit and replay the sequence, so the reproduction matches the state the finding described",
        "use_when": "the finding is about a deployed contract and the state has moved on",
        "avoid_when": "the finding is about code that is not deployed",
        "tags": ["testing", "fork", "reproduction"],
        "steps": [
            "Record the block number where the vulnerable state existed.",
            "Create the fork with that block pinned and confirm the bytecode hash.",
            "Replay the minimal sequence and assert the effect.",
            "Store the block number, the RPC source and the bytecode hash with the test.",
        ],
        "signals": ["block-pinned", "bytecode-confirmed", "sequence-replayed"],
        "patterns": [
            (
                "pin a fork",
                "vm.createSelectFork(vm.envString(\"RPC_URL\"), 21_000_000);",
            )
        ],
        "pitfalls": [
            "Forking at latest, where a fix or a state change has already removed the condition.",
            "Depending on a public RPC that prunes old state, which makes the test unreproducible.",
        ],
        "done_when": [
            "The block number and bytecode hash are recorded with the test.",
            "The sequence reproduces the finding on the pinned fork.",
        ],
        "refs": [
            "[Foundry fork testing](https://book.getfoundry.sh/forge/fork-testing)",
        ],
        "meta": {"phase": "testing"},
    },
    {
        "slug": "testing-minimal-sequence",
        "title": "Cut the exploit to the shortest sequence",
        "summary": "Remove every action that is not required for the effect, so the test reads as a proof and not as a transcript of exploration",
        "use_when": "the exploit was found by trial and the test still contains the trials",
        "avoid_when": "the sequence is already three calls and each one is load-bearing",
        "tags": ["testing", "minimal", "sequence"],
        "steps": [
            "Record the sequence that works as an ordered list of calls.",
            "Remove one call at a time from the start and re-run.",
            "Keep only the calls whose removal stops the effect.",
            "Confirm the reduced sequence still fails the invariant or drains the balance.",
        ],
        "signals": ["sequence-recorded", "calls-removed", "reduced-sequence-verified"],
        "patterns": [
            (
                "three calls",
                "vm.prank(attacker); vault.deposit(1);\nasset.transfer(address(vault), 1e18);\nvm.prank(victim); vault.deposit(1e18);",
            )
        ],
        "pitfalls": [
            "Leaving a setup call that only funds the attacker in the proof, which hides the real precondition.",
            "Removing a call that sets an approval and then reporting the exploit as unauthenticated.",
        ],
        "done_when": [
            "Every remaining call is shown to be required.",
            "The reduced sequence still produces the effect.",
        ],
        "refs": [
            "[Foundry testing](https://book.getfoundry.sh/forge/tests)",
        ],
        "meta": {"phase": "testing"},
    },
    {
        "slug": "testing-negative-control",
        "title": "Add a control that must not exploit",
        "summary": "Run the same sequence with one precondition removed and assert nothing happens, so the test proves the precondition rather than the call",
        "use_when": "the exploit test passes and you need to show why it passes",
        "avoid_when": "the effect is an exact state change that cannot occur accidentally",
        "tags": ["testing", "control", "precondition"],
        "steps": [
            "Pick the precondition the exploit depends on, such as a donation or a stale price.",
            "Run the same calls without it and assert the effect does not occur.",
            "Record both tests and the single difference between them.",
            "Report the precondition as part of the finding.",
        ],
        "signals": ["control-written", "difference-single", "effect-absent"],
        "patterns": [
            (
                "control",
                "function test_control_no_donation() public {\n  vm.prank(attacker); vault.deposit(1);\n  vm.prank(victim); vault.deposit(1e18);\n  assertGt(vault.balanceOf(victim), 0);\n}",
            )
        ],
        "pitfalls": [
            "A control that differs in several ways, which makes the result unattributable.",
            "Skipping the control and letting a reviewer assume the calls alone are sufficient.",
        ],
        "done_when": [
            "A control test exists and differs from the exploit by one precondition.",
            "The control asserts the absence of the effect.",
        ],
        "refs": [
            "[Foundry testing](https://book.getfoundry.sh/forge/tests)",
        ],
        "meta": {"phase": "testing"},
    },
    {
        "slug": "testing-state-diff-assertions",
        "title": "Assert on the state diff, not just the balance",
        "summary": "Compare storage before and after the exploit so the test shows exactly which variables moved, which is what the report has to explain",
        "use_when": "the effect is an accounting change rather than a transfer",
        "avoid_when": "the effect is a single token balance change that is self-explanatory",
        "tags": ["testing", "state-diff", "assertions"],
        "steps": [
            "Snapshot the relevant storage slots before the sequence.",
            "Run the sequence and snapshot the same slots after.",
            "Assert on each expected change and on each expected non-change.",
            "Print the diff in the test output so the report can quote it.",
        ],
        "signals": ["snapshot-before", "snapshot-after", "diff-asserted"],
        "patterns": [
            (
                "storage snapshot",
                "bytes32 before = vm.load(address(vault), bytes32(uint256(3)));\n// exploit\nbytes32 after_ = vm.load(address(vault), bytes32(uint256(3)));\nassertTrue(before != after_);",
            )
        ],
        "pitfalls": [
            "Asserting only that a balance decreased, which does not show where the value went.",
            "Hardcoding a slot number without confirming it against the layout dump.",
        ],
        "done_when": [
            "Before and after values are captured for each relevant slot.",
            "The diff is asserted and printed for the report.",
        ],
        "refs": [
            "[Foundry cheatcodes](https://book.getfoundry.sh/cheatcodes/)",
        ],
        "meta": {"phase": "testing"},
    },
    {
        "slug": "testing-gas-and-revert-profile",
        "title": "Record gas and revert behaviour for the sequence",
        "summary": "Measure the gas the exploit needs and whether it reverts under realistic limits, because an exploit that cannot be included in a block is not reachable",
        "use_when": "the exploit involves loops, many calls or large calldata",
        "avoid_when": "the exploit is three calls with fixed cost",
        "tags": ["testing", "gas", "reachability"],
        "steps": [
            "Measure gas per call and the total for the sequence.",
            "Compare the total with the block gas limit on the target chain.",
            "Test the sequence with a loop bound that grows, and find where it exceeds the limit.",
            "Report the gas cost and whether the exploit fits in one block.",
        ],
        "signals": ["gas-measured", "limit-compared", "growth-tested"],
        "patterns": [
            (
                "gas",
                "uint256 before = gasleft();\n// exploit\nemit log_named_uint(\"gas used\", before - gasleft());",
            )
        ],
        "pitfalls": [
            "Reporting an exploit that needs more gas than a block allows without noting it.",
            "Measuring gas on a fork with a raised limit, which hides the constraint.",
        ],
        "done_when": [
            "Per-call and total gas are recorded and compared with the chain's limit.",
            "Any size dependence is tested and reported.",
        ],
        "refs": [
            "[Ethereum gas](https://ethereum.org/en/developers/docs/gas/)",
        ],
        "meta": {"phase": "testing"},
    },
    {
        "slug": "reporting-finding-template",
        "title": "Write a finding with location, impact and proof",
        "summary": "Use one structure per finding: location with line numbers, the invariant broken, the sequence that breaks it, and the impact with its evidence",
        "use_when": "you are writing up any confirmed issue",
        "avoid_when": "the issue is informational and a sentence is enough",
        "tags": ["reporting", "template", "structure"],
        "steps": [
            "Give the location as file plus function plus line range, not a link that can rot.",
            "State the invariant or expectation that is violated.",
            "Give the minimal sequence with the test name that reproduces it.",
            "State the impact with the artifact or assertion that proves it.",
        ],
        "signals": ["location-precise", "invariant-stated", "proof-linked"],
        "patterns": [
            (
                "finding",
                "Location: Vault.sol:118-126 (withdraw)\nInvariant: sum(shares) == totalSupply after any call\nProof: test_withdraw_reentrancy (drains 12.4 ETH)\nImpact: attacker receives assets without burning shares",
            )
        ],
        "pitfalls": [
            "A location that points at the file rather than the line, which forces the reader to search.",
            "An impact statement with no artifact or assertion behind it.",
        ],
        "done_when": [
            "Every finding has location, invariant, proof and impact.",
            "The proof names a test or a command that a reviewer can run.",
        ],
        "refs": [
            "[SWC registry](https://swcregistry.io/)",
        ],
        "meta": {"phase": "reporting"},
    },
    {
        "slug": "reporting-severity-basis",
        "title": "Justify severity with reachability and value at risk",
        "summary": "Rate each finding by who can trigger it, what it costs them and what it moves, so the rating follows from facts rather than from the defect class",
        "use_when": "findings are being triaged into high, medium and low",
        "avoid_when": "the platform assigns severity from a fixed mapping",
        "tags": ["reporting", "severity", "risk"],
        "steps": [
            "State the caller: unauthenticated, any depositor, a privileged role.",
            "State the capital required and whether it can be borrowed in the same transaction.",
            "State the value at risk with the balance or supply it is measured against.",
            "Derive the severity from those three and record the reasoning.",
        ],
        "signals": ["caller-stated", "capital-stated", "value-measured"],
        "patterns": [
            (
                "severity basis",
                "caller: any depositor, no privilege\ncapital: 2 wei plus one donation\neffect: next depositor's shares round to zero",
            )
        ],
        "pitfalls": [
            "Rating critical because the defect class is critical, even when the trigger needs admin.",
            "Ignoring that borrowed capital can satisfy a deposit threshold within one transaction.",
        ],
        "done_when": [
            "Caller, capital and value at risk are all stated.",
            "The severity follows explicitly from those three.",
        ],
        "refs": [
            "[SWC registry](https://swcregistry.io/)",
        ],
        "meta": {"phase": "reporting"},
    },
    {
        "slug": "reporting-scanner-leads",
        "title": "Turn scanner output into reviewed findings, not a dump",
        "summary": "Treat each scanner hit as a lead: confirm it in code, then report only the ones you can explain, with the rule id as a cross-reference",
        "use_when": "you ran the static scanner and it produced more hits than you can report",
        "avoid_when": "the client explicitly asked for raw tool output as an appendix",
        "tags": ["reporting", "scanner", "triage"],
        "steps": [
            "Run the scanner and group hits by rule and file.",
            "For each group, read the code and decide whether the pattern is reachable and harmful.",
            "Report confirmed issues with the rule id; put the rest in an appendix marked false positive with a reason.",
            "Never report a scanner hit you have not read.",
        ],
        "signals": ["hits-grouped", "code-read", "false-positives-labelled"],
        "patterns": [
            (
                "scan",
                "web3-audit scan contracts/ --min-severity medium --json > scan.json",
            )
        ],
        "pitfalls": [
            "Submitting the scanner output verbatim, which includes hits the client can disprove in a minute.",
            "Dropping false positives silently, which hides that the pattern was considered.",
        ],
        "done_when": [
            "Every scanner group is either reported or labelled false positive with a reason.",
            "No reported finding lacks a code reading.",
        ],
        "refs": [
            "[Slither detectors](https://github.com/crytic/slither)",
        ],
        "meta": {"phase": "reporting"},
    },
    {
        "slug": "reporting-fix-verification",
        "title": "State how the fix will be verified",
        "summary": "Give the test that must pass after remediation, so the fix can be accepted or rejected on evidence rather than on a diff",
        "use_when": "the report includes recommendations",
        "avoid_when": "the client has explicitly said remediation is out of scope",
        "tags": ["reporting", "remediation", "verification"],
        "steps": [
            "Name the test that currently fails because of the bug.",
            "State the exact change in behaviour that makes it pass, such as the invariant holding after a failure path.",
            "List the sibling paths the same test should cover.",
            "Record the test as the acceptance criterion in the finding.",
        ],
        "signals": ["test-named", "behaviour-change-stated", "siblings-listed"],
        "patterns": [
            (
                "acceptance",
                "accept when: test_withdraw_reentrancy passes with balances decremented before the call\nand: test_withdraw_reentrancy_control still passes",
            )
        ],
        "pitfalls": [
            "An acceptance criterion that only checks the endpoint now reverts for everyone.",
            "A test that depends on a fork block that the client's CI cannot reach.",
        ],
        "done_when": [
            "A named test and the behaviour it must show are recorded.",
            "Sibling paths and the control are included in the acceptance criteria.",
        ],
        "refs": [
            "[Foundry testing](https://book.getfoundry.sh/forge/tests)",
        ],
        "meta": {"phase": "reporting"},
    },
    {
        "slug": "triage-duplicate-advisory",
        "title": "Check advisories and prior audits before reporting",
        "summary": "Search the vendor's advisories and the published audits for the same root cause, because an issue already known and accepted is not a new finding",
        "use_when": "the contract has a public history or a previous audit report",
        "avoid_when": "the deployment is new and no audit or advisory exists",
        "tags": ["triage", "duplicates", "advisories"],
        "steps": [
            "Search advisories for the contract and for the library version in use.",
            "Read the previous audit's findings and compare root causes, not descriptions.",
            "Check whether the client accepted the risk explicitly, and cite where.",
            "Report the difference if the new issue is a variant, or drop it if it is the same.",
        ],
        "signals": ["advisories-searched", "root-causes-compared", "acceptance-cited"],
        "patterns": [
            (
                "search",
                "web3-audit list --phase triage",
            )
        ],
        "pitfalls": [
            "Reporting a known issue that the client documented as accepted risk.",
            "Assuming a patched library version is in use without checking the dependency lock.",
        ],
        "done_when": [
            "Advisories and prior audits are searched and the result recorded.",
            "Any near duplicate is cited with the difference stated.",
        ],
        "refs": [
            "[SWC registry](https://swcregistry.io/)",
        ],
        "meta": {"phase": "triage"},
    },
    {
        "slug": "triage-exploitability-verdict",
        "title": "Give each finding an explicit exploitability verdict",
        "summary": "End every finding with exploitable, conditional or theoretical and the reason, so a reviewer knows whether to act now",
        "use_when": "findings are a mix of confirmed exploits and code smells",
        "avoid_when": "every finding has a passing exploit test and the verdict is obvious",
        "tags": ["triage", "verdict", "exploitability"],
        "steps": [
            "Classify as exploitable when a test drains value or breaks an invariant with stated preconditions.",
            "Classify as conditional when the preconditions are outside the attacker's control, and name them.",
            "Classify as theoretical when the pattern exists but no path reaches it.",
            "Put the verdict and its reason in the finding, not only in the summary table.",
        ],
        "signals": ["verdict-assigned", "reason-recorded", "preconditions-named"],
        "patterns": [
            (
                "verdict",
                "exploitability: conditional — requires the owner to set fee above 100%, which the setter allows but never does by default",
            )
        ],
        "pitfalls": [
            "Labelling something theoretical because you did not find the path, rather than because none exists.",
            "Omitting the verdict, which leaves a code smell looking like an exploit in the table.",
        ],
        "done_when": [
            "Every finding has a verdict and a reason.",
            "Conditional findings name the precondition outside the attacker's control.",
        ],
        "refs": [
            "[SWC registry](https://swcregistry.io/)",
        ],
        "meta": {"phase": "triage"},
    },
]