"""Part 2 of the web3-audit corpus: reentrancy, arithmetic, oracle, storage, upgrade."""

from __future__ import annotations

from typing import Any

SKILLS: list[dict[str, Any]] = [
    {
        "slug": "reentrancy-read-only",
        "title": "Check read-only reentrancy through view functions",
        "summary": "Test whether a view function reports a stale price or balance while an external call is in flight, because integrators read those views",
        "use_when": "the contract exposes getPrice, getReserves or balanceOf and makes external calls",
        "avoid_when": "no integrator reads the contract mid-transaction and the views are not used by other protocols",
        "tags": ["reentrancy", "views", "integrations"],
        "steps": [
            "List the view functions another contract would read for pricing or accounting.",
            "Identify where the contract makes an external call and whether a view would be stale during it.",
            "Re-enter a view from the callback and record the value it returns mid-call.",
            "Report the stale value with the integrator that would consume it.",
        ],
        "signals": ["views-listed", "callback-view-recorded", "consumer-identified"],
        "patterns": [
            (
                "stale view",
                "function totalAssets() public view returns (uint256) {\n  return asset.balanceOf(address(this)) + pending;\n}",
            )
        ],
        "pitfalls": [
            "Checking only state-changing reentrancy and missing that a lending market prices shares through the view.",
            "Assuming a reentrancy guard on the mutating function protects the view as well.",
        ],
        "done_when": [
            "Every price-relevant view is identified and probed during a callback.",
            "Any stale value is reported with the integrator that would consume it.",
        ],
        "refs": [
            "[EIP-4626 tokenised vault](https://eips.ethereum.org/EIPS/eip-4626)",
        ],
        "meta": {"phase": "reentrancy"},
    },
    {
        "slug": "reentrancy-cross-function",
        "title": "Test cross-function reentrancy on shared state",
        "summary": "Re-enter a sibling function that reads the same balance, so a guard on one entry point does not hide an unguarded path",
        "use_when": "several functions mutate the same mapping or the same total",
        "avoid_when": "every function touching the state has the same guard and there is only one",
        "tags": ["reentrancy", "cross-function", "shared-state"],
        "steps": [
            "Group functions by the state they write and list each group.",
            "For each group, check whether every member has the guard.",
            "From the callback of an unguarded member, call a guarded sibling and observe the effect.",
            "Report the pair, not just the unguarded function.",
        ],
        "signals": ["groups-listed", "guards-compared", "pair-tested"],
        "patterns": [
            (
                "sibling",
                "function withdraw() external nonReentrant { ... }\nfunction transferShares() external { balances[msg.sender] -= n; }  // no guard",
            )
        ],
        "pitfalls": [
            "A guard applied per function rather than per state, which leaves the group partly protected.",
            "Assuming a lock variable is per-user when it is global and therefore blocks the test.",
        ],
        "done_when": [
            "Every shared-state group has its guards compared.",
            "Any unguarded member is reported with the sibling that makes it exploitable.",
        ],
        "refs": [
            "[OpenZeppelin ReentrancyGuard](https://docs.openzeppelin.com/contracts/5.x/api/utils#ReentrancyGuard)",
        ],
        "meta": {"phase": "reentrancy"},
    },
    {
        "slug": "reentrancy-flashloan-context",
        "title": "Test reentrancy under a flash-loan balance",
        "summary": "Repeat the attack with borrowed capital inside one transaction, because a check that depends on the attacker's balance can be satisfied transiently",
        "use_when": "a guard or threshold compares the caller's balance or share of supply",
        "avoid_when": "no authorisation or threshold depends on balances",
        "tags": ["reentrancy", "flash-loan", "capital"],
        "steps": [
            "Identify checks that compare the caller's balance, share or voting weight.",
            "Borrow the required amount inside one transaction from a test liquidity source.",
            "Perform the sequence and repay within the same transaction.",
            "Report the check that the borrowed balance satisfied.",
        ],
        "signals": ["balance-checks-identified", "borrow-simulated", "check-satisfied"],
        "patterns": [
            (
                "transient capital",
                "flashLoan(amount, address(vault), abi.encodeWithSignature(\"attack()\"));\n// repay within the same tx",
            )
        ],
        "pitfalls": [
            "Dismissing a check because the attacker does not hold the balance in a normal block.",
            "Forgetting governance snapshot timing, which can make borrowed weight useless.",
        ],
        "done_when": [
            "Every balance-dependent check is listed and tested with transient capital.",
            "The satisfied check is reported with the sequence that satisfied it.",
        ],
        "refs": [
            "[EIP-3156 flash loans](https://eips.ethereum.org/EIPS/eip-3156)",
        ],
        "meta": {"phase": "reentrancy"},
    },
    {
        "slug": "arithmetic-rounding-direction",
        "title": "Check the rounding direction favours the protocol",
        "summary": "Read every division and confirm it rounds against the user, because a share price that rounds in the user's favour is drained one wei at a time",
        "use_when": "the contract converts between assets and shares or between debt and collateral",
        "avoid_when": "there is no division in value-bearing code",
        "tags": ["arithmetic", "rounding", "shares"],
        "steps": [
            "List every division and the direction the result is used in, deposit or withdraw.",
            "For deposits, confirm the user receives the smaller share count.",
            "For withdrawals, confirm the user receives the smaller asset amount.",
            "Test the one-wei boundary both ways and record the result.",
        ],
        "signals": ["divisions-listed", "direction-checked", "boundary-tested"],
        "patterns": [
            (
                "correct direction",
                "shares = assets.mulDiv(totalSupply, totalAssets, Math.Rounding.Floor);\nassets = shares.mulDiv(totalAssets, totalSupply, Math.Rounding.Floor);",
            )
        ],
        "pitfalls": [
            "Rounding up on deposit, which lets a user mint more shares than the assets they supplied.",
            "Assuming integer division cannot be exploited because each step loses at most one wei.",
        ],
        "done_when": [
            "Every division has a stated direction and a reason.",
            "A one-wei deposit and withdrawal are shown not to favour the user.",
        ],
        "refs": [
            "[OpenZeppelin Math.mulDiv](https://docs.openzeppelin.com/contracts/5.x/api/utils#Math)",
        ],
        "meta": {"phase": "arithmetic"},
    },
    {
        "slug": "arithmetic-precision-loss",
        "title": "Quantify precision loss across a sequence",
        "summary": "Compute the error accumulated by repeated conversions, because one truncation is harmless and a thousand of them is a subsidy",
        "use_when": "the contract converts value repeatedly, such as in a strategy that compounds",
        "avoid_when": "the contract performs a single conversion per call and stores no intermediate value",
        "tags": ["arithmetic", "precision", "accumulation"],
        "steps": [
            "Write the conversion chain and the precision of each step.",
            "Compute the total error for one round and for n rounds symbolically.",
            "Run the chain with a small amount and measure the loss with an assertion.",
            "Report the per-round loss and the amount at which it becomes material.",
        ],
        "signals": ["chain-written", "error-computed", "loss-measured"],
        "patterns": [
            (
                "measure loss",
                "uint256 before = vault.balanceOf(user);\nfor (uint256 i; i < 100; ++i) { vault.harvest(); }\nassertLt(vault.balanceOf(user), before);",
            )
        ],
        "pitfalls": [
            "Reporting one wei of loss as critical without showing it accumulates.",
            "Missing that the loss accrues to the last withdrawer rather than to the protocol.",
        ],
        "done_when": [
            "Precision is stated for every step and the chain error is computed.",
            "The measured loss and the threshold at which it matters are recorded.",
        ],
        "refs": [
            "[Solidity integers](https://docs.soliditylang.org/en/latest/types.html#integers)",
        ],
        "meta": {"phase": "arithmetic"},
    },
    {
        "slug": "arithmetic-overflow-unchecked",
        "title": "Check every unchecked block for reachable overflow",
        "summary": "Read each unchecked block and prove the operands cannot overflow, because the compiler no longer helps inside one",
        "use_when": "the contract uses Solidity 0.8 or later and contains unchecked blocks",
        "avoid_when": "the contract predates 0.8 and has no unchecked blocks",
        "tags": ["arithmetic", "unchecked", "overflow"],
        "steps": [
            "List every unchecked block with its operands and bounds.",
            "Write the maximum value each operand can reach from the contract's own constraints.",
            "Compare the sum or product against the type maximum and record the margin.",
            "Report any block where the margin depends on an assumption rather than a check.",
        ],
        "signals": ["blocks-listed", "bounds-written", "margin-computed"],
        "patterns": [
            (
                "unchecked",
                "unchecked {\n  // i < length <= 256, so i + 1 cannot overflow uint256\n  ++i;\n}",
            )
        ],
        "pitfalls": [
            "An unchecked block that holds a user-supplied amount rather than a loop counter.",
            "Assuming a bound from a modifier that can be changed by an admin after deployment.",
        ],
        "done_when": [
            "Every unchecked block has a written bound and margin.",
            "Any margin that rests on an assumption is reported.",
        ],
        "refs": [
            "[Solidity unchecked](https://docs.soliditylang.org/en/latest/control-structures.html#checked-or-unchecked-arithmetic)",
        ],
        "meta": {"phase": "arithmetic"},
    },
    {
        "slug": "arithmetic-share-inflation",
        "title": "Test the first-depositor share inflation attack",
        "summary": "Deposit a minimal amount, donate to inflate the share price, then check whether the next depositor is rounded to zero shares",
        "use_when": "the vault computes shares from totalAssets divided by totalSupply",
        "avoid_when": "the vault uses a virtual offset or dead shares that make the attack unprofitable",
        "tags": ["arithmetic", "inflation", "vault"],
        "steps": [
            "Confirm the share formula and whether totalAssets can be raised without minting shares.",
            "Deposit one wei as the attacker, then transfer assets directly to the vault.",
            "Deposit a realistic amount as the victim and record the shares minted.",
            "Report the victim's loss and whether a virtual offset prevents it.",
        ],
        "signals": ["formula-confirmed", "donation-made", "victim-shares-recorded"],
        "patterns": [
            (
                "attack shape",
                "vault.deposit(1, attacker);\nasset.transfer(address(vault), 10_000e18);\nvault.deposit(10_000e18, victim); // shares minted?",
            )
        ],
        "pitfalls": [
            "Running the test before the vault has any shares, which changes the formula branch.",
            "Concluding it is safe because the victim loses only rounding, without checking the full deposit.",
        ],
        "done_when": [
            "The donation is shown to change the share price and the victim's shares are recorded.",
            "The presence or absence of a mitigation is stated.",
        ],
        "refs": [
            "[EIP-4626 tokenised vault](https://eips.ethereum.org/EIPS/eip-4626)",
        ],
        "meta": {"phase": "arithmetic"},
    },
    {
        "slug": "oracle-stale-price",
        "title": "Check the oracle freshness bound",
        "summary": "Read the staleness check and confirm it exists and is smaller than the heartbeat, so a price cannot be used long after it stopped updating",
        "use_when": "the contract reads a Chainlink or TWAP price to value collateral",
        "avoid_when": "the price is derived on-chain in the same transaction, such as a pool spot price used only as a reference",
        "tags": ["oracle", "staleness", "chainlink"],
        "steps": [
            "Identify the feed, its heartbeat and its deviation threshold.",
            "Read the contract's staleness constant and compare it with the heartbeat.",
            "Force a stale answer in a fork test and check whether the contract reverts.",
            "Report the bound and whether it is enforced.",
        ],
        "signals": ["feed-identified", "bound-compared", "stale-answer-tested"],
        "patterns": [
            (
                "freshness",
                "(, int256 answer, , uint256 updatedAt, ) = feed.latestRoundData();\nrequire(block.timestamp - updatedAt <= MAX_STALENESS, \"stale\");\nrequire(answer > 0, \"bad answer\");",
            )
        ],
        "pitfalls": [
            "Checking staleness but not the answer sign, so a negative or zero price passes.",
            "Using a bound larger than the heartbeat, which accepts a price that never updated.",
        ],
        "done_when": [
            "The feed's heartbeat and the contract's bound are recorded together.",
            "A stale answer is shown to be rejected, or the finding is written.",
        ],
        "refs": [
            "[Chainlink data feeds](https://docs.chain.link/data-feeds)",
        ],
        "meta": {"phase": "oracle"},
    },
    {
        "slug": "oracle-decimal-mismatch",
        "title": "Check oracle decimals against the maths",
        "summary": "Confirm every price is scaled to the decimals the arithmetic expects, because an 8-decimal feed in an 18-decimal formula is a factor of a billion",
        "use_when": "the contract mixes feeds, tokens or internal units with different decimals",
        "avoid_when": "every value is normalised through one helper with an explicit scale",
        "tags": ["oracle", "decimals", "scaling"],
        "steps": [
            "Record the decimals of every feed and token involved.",
            "Write the arithmetic with its implied scale and compare.",
            "Test with a realistic price and check the resulting value against a hand calculation.",
            "Report any place where the scale differs from the assumption.",
        ],
        "signals": ["decimals-recorded", "scale-compared", "hand-check-done"],
        "patterns": [
            (
                "normalise",
                "uint256 price18 = uint256(answer) * 10 ** (18 - feed.decimals());",
            )
        ],
        "pitfalls": [
            "Assuming all Chainlink USD feeds are 8 decimals; some pairs are 18.",
            "Normalising the price but not the token amount, which reintroduces the mismatch.",
        ],
        "done_when": [
            "Every decimals value is recorded and the formula scale is stated.",
            "A hand calculation matches the contract's output.",
        ],
        "refs": [
            "[Chainlink data feeds](https://docs.chain.link/data-feeds)",
        ],
        "meta": {"phase": "oracle"},
    },
    {
        "slug": "oracle-twap-manipulation",
        "title": "Check how much capital moves a TWAP",
        "summary": "Estimate the cost of shifting the window average and compare it with the value the price controls, because a cheap manipulation is the whole finding",
        "use_when": "the contract prices collateral from a pool-derived average",
        "avoid_when": "the price comes from a decentralised oracle with its own manipulation cost",
        "tags": ["oracle", "twap", "manipulation"],
        "steps": [
            "Identify the pool, the window length and the liquidity depth.",
            "Compute the trade size needed to move the average by the amount that matters.",
            "Compare that cost with the profit available from the mispricing.",
            "Report both numbers, since either alone is not a finding.",
        ],
        "signals": ["pool-identified", "cost-estimated", "profit-compared"],
        "patterns": [
            (
                "window",
                "uint32 public constant TWAP_WINDOW = 1800; // 30 minutes",
            )
        ],
        "pitfalls": [
            "Reporting manipulation without a cost estimate, which a triager will reject.",
            "Ignoring that the window can be short enough that one block dominates it.",
        ],
        "done_when": [
            "Window, liquidity and required trade size are recorded.",
            "The manipulation cost is compared with the value at stake.",
        ],
        "refs": [
            "[Uniswap v3 oracle](https://docs.uniswap.org/contracts/v3/overview)",
        ],
        "meta": {"phase": "oracle"},
    },
    {
        "slug": "oracle-fallback-path",
        "title": "Check the fallback when the primary oracle fails",
        "summary": "Force the primary feed to revert and see what the contract does next, because a silent fallback to a spot price is a downgrade of the whole guarantee",
        "use_when": "the contract has a try/catch or a secondary source around an oracle",
        "avoid_when": "there is a single oracle and failure means the call reverts",
        "tags": ["oracle", "fallback", "degradation"],
        "steps": [
            "Read the fallback path and the source it uses.",
            "Force the primary to revert in a fork test.",
            "Record the price used after the failure and compare it with the last good price.",
            "Report whether the fallback is stronger or weaker than the primary.",
        ],
        "signals": ["fallback-read", "failure-forced", "price-compared"],
        "patterns": [
            (
                "fallback",
                "try feed.latestRoundData() returns (uint80, int256 a, , , ) {\n  price = uint256(a);\n} catch {\n  price = pool.spotPrice();   // silently weaker\n}",
            )
        ],
        "pitfalls": [
            "A fallback to spot price that is manipulable within one transaction.",
            "A fallback with no event, so the operator never learns the primary is down.",
        ],
        "done_when": [
            "The fallback source is identified and exercised.",
            "Its strength relative to the primary is stated.",
        ],
        "refs": [
            "[Chainlink data feeds](https://docs.chain.link/data-feeds)",
        ],
        "meta": {"phase": "oracle"},
    },
    {
        "slug": "storage-layout-collision",
        "title": "Check storage layout between proxy and implementation",
        "summary": "Compare slot maps for the proxy and each implementation, because an added variable in a child contract shifts every slot below it",
        "use_when": "the system uses an upgradeable proxy",
        "avoid_when": "the contract is immutable and not behind a proxy",
        "tags": ["storage", "layout", "proxy"],
        "steps": [
            "Dump the storage layout for the proxy and for each implementation version.",
            "Compare slot numbers and types for every variable.",
            "Check for gaps reserved for future variables in base contracts.",
            "Report any shift and the variable whose value would be reinterpreted.",
        ],
        "signals": ["layouts-dumped", "slots-compared", "shifts-identified"],
        "patterns": [
            (
                "layout dump",
                "forge inspect Vault storage-layout --json > layout.json",
            )
        ],
        "pitfalls": [
            "Adding a variable to a base contract, which shifts storage in every derived contract.",
            "Reordering variables in a struct that is stored in a mapping value.",
        ],
        "done_when": [
            "Layouts for every version are compared slot by slot.",
            "Any shift is reported with the affected variable.",
        ],
        "refs": [
            "[OpenZeppelin upgrades storage layout](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)",
        ],
        "meta": {"phase": "storage"},
    },
    {
        "slug": "storage-delete-gap",
        "title": "Check what a delete actually clears",
        "summary": "Confirm that deleting a struct or mapping entry clears every field that matters, because delete on a nested mapping leaves its children behind",
        "use_when": "the contract deletes records to reclaim storage or reset state",
        "avoid_when": "deletion is not part of the contract's lifecycle",
        "tags": ["storage", "delete", "ghost-state"],
        "steps": [
            "Read each delete and the type it applies to.",
            "List the fields that delete does not recurse into, such as nested mappings.",
            "Attempt to read the deleted record and any child record afterwards.",
            "Report any value that survives deletion and the function that can still read it.",
        ],
        "signals": ["deletes-listed", "fields-checked", "survivors-read"],
        "patterns": [
            (
                "delete",
                "delete positions[id];   // nested mapping positions[id].history is untouched",
            )
        ],
        "pitfalls": [
            "Assuming delete clears a nested mapping, which it does not.",
            "Deleting a record while an array still indexes it, leaving a dangling reference.",
        ],
        "done_when": [
            "Every delete is checked field by field for what survives.",
            "Any surviving state and its reader are reported.",
        ],
        "refs": [
            "[Solidity delete](https://docs.soliditylang.org/en/latest/types.html#delete)",
        ],
        "meta": {"phase": "storage"},
    },
    {
        "slug": "storage-array-removal",
        "title": "Check array removal for skipped elements",
        "summary": "Read every swap-and-pop and every shift-delete, because an off-by-one leaves a hole that later iteration treats as a live record",
        "use_when": "the contract stores records in an array and removes them",
        "avoid_when": "removal is not supported and entries are appended only",
        "tags": ["storage", "arrays", "removal"],
        "steps": [
            "Read each removal and record which index is overwritten and which is popped.",
            "Check that the index mapping is updated for the moved element.",
            "Remove the last, first and middle element and iterate the array after each.",
            "Report any duplicate, hole or stale index found.",
        ],
        "signals": ["removal-read", "mapping-updated", "iteration-checked"],
        "patterns": [
            (
                "swap and pop",
                "uint256 last = items.length - 1;\nitems[index] = items[last];\nindexOf[items[index]] = index;\nitems.pop();\ndelete indexOf[removed];",
            )
        ],
        "pitfalls": [
            "Updating the array but not the index mapping, so the moved element becomes unfindable.",
            "Popping while iterating, which skips the element that was moved into the current index.",
        ],
        "done_when": [
            "Removal is tested at the first, middle and last position.",
            "The array and its index mapping agree after every removal.",
        ],
        "refs": [
            "[Solidity arrays](https://docs.soliditylang.org/en/latest/types.html#arrays)",
        ],
        "meta": {"phase": "storage"},
    },
    {
        "slug": "storage-struct-packing",
        "title": "Check struct packing against gas and correctness assumptions",
        "summary": "Read the struct field order and confirm that a packing optimisation did not create a shared slot that a partial write can corrupt",
        "use_when": "the contract packs several small fields into one struct",
        "avoid_when": "every field is a full 32-byte word",
        "tags": ["storage", "packing", "slots"],
        "steps": [
            "Dump the storage layout and group fields by slot.",
            "Identify every write that touches a field in a shared slot.",
            "Check that each write uses a full assignment rather than an assembly partial store.",
            "Report any write that could clear a neighbouring field.",
        ],
        "signals": ["slots-grouped", "writes-identified", "partial-stores-checked"],
        "patterns": [
            (
                "packed struct",
                "struct Position { uint128 amount; uint64 start; uint64 end; } // one slot",
            )
        ],
        "pitfalls": [
            "Assembly that writes a single field with sstore on the whole slot, wiping its neighbours.",
            "Reordering a packed struct during an upgrade, which changes every field's meaning.",
        ],
        "done_when": [
            "Every shared slot and its writers are listed.",
            "No write can clear a neighbouring field, or the risk is reported.",
        ],
        "refs": [
            "[Solidity storage layout](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)",
        ],
        "meta": {"phase": "storage"},
    },
    {
        "slug": "upgrade-initializer-reinit",
        "title": "Check an upgrade cannot re-run initialization",
        "summary": "Verify the initialized flag survives an upgrade and that no new initializer can be called again, because a re-initializable implementation is a takeover",
        "use_when": "a new implementation adds an initializer or a reinitializer",
        "avoid_when": "the upgrade adds no initialization logic",
        "tags": ["upgrade", "initializer", "takeover"],
        "steps": [
            "Read the new implementation's initializer and its version number.",
            "Check the proxy's stored initialized version before and after the upgrade.",
            "Attempt to call the new initializer from a non-admin address after upgrading.",
            "Report whether the call succeeded and what it changed.",
        ],
        "signals": ["initializer-read", "version-checked", "reinit-attempted"],
        "patterns": [
            (
                "reinitializer",
                "function initializeV2(uint256 fee_) external reinitializer(2) {\n  fee = fee_;\n}",
            )
        ],
        "pitfalls": [
            "A new implementation that resets the initialized flag to zero in its constructor.",
            "An initializer without a version, which can be called again after any upgrade.",
        ],
        "done_when": [
            "The stored initialized version is recorded before and after.",
            "A re-initialization attempt from a non-admin is shown to fail.",
        ],
        "refs": [
            "[OpenZeppelin Initializable](https://docs.openzeppelin.com/contracts/5.x/api/proxy#Initializable)",
        ],
        "meta": {"phase": "upgrade"},
    },
    {
        "slug": "upgrade-storage-gap",
        "title": "Check the storage gap is large enough",
        "summary": "Count the reserved slots in each base contract and compare them with what the next upgrade needs, because an exhausted gap forces a layout change",
        "use_when": "the upgradeable contract inherits from base contracts with gaps",
        "avoid_when": "the contract does not use inheritance with reserved gaps",
        "tags": ["upgrade", "gap", "inheritance"],
        "steps": [
            "List each base contract and the size of its __gap array.",
            "Count the variables a planned upgrade adds to that base.",
            "Confirm the gap is reduced by exactly the number of added variables.",
            "Report any base whose gap is too small for the planned change.",
        ],
        "signals": ["gaps-listed", "planned-vars-counted", "reduction-checked"],
        "patterns": [
            (
                "gap",
                "uint256[49] private __gap;  // reduce by one when adding a variable",
            )
        ],
        "pitfalls": [
            "Adding a variable without reducing the gap, which shifts every child's storage.",
            "Removing the gap entirely to save gas, which blocks all future upgrades.",
        ],
        "done_when": [
            "Every gap and planned addition is counted.",
            "The gap arithmetic balances for each base contract.",
        ],
        "refs": [
            "[OpenZeppelin upgrades storage layout](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)",
        ],
        "meta": {"phase": "upgrade"},
    },
]