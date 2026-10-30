# Contributing

## Adding a skill

1. Add a dict to `src/web3audit/corpus/part1.py`..`part3.py`.
2. Meet every floor: 3+ steps, 2+ signals, 1+ pattern, 2+ pitfalls, a phase from the closed set, an HTTPS-labelled reference, and 80+ rendered words.
3. `web3-audit validate` must print `50/50 skills valid`; then `web3-audit build`.
4. `python -m pytest -q`.

## Adding a scanner rule

1. Write `(path, lines) -> Iterable[Finding]` in `scanner.py`.
2. Register it in `RULES` and add its id to `RULE_IDS`.
3. Add a positive and a negative test. A rule without a negative test fires on something it should not, and a noisy scanner gets ignored.
4. Keep the message specific: what matched and why it matters.

## What will be rejected

- A rule that flags a normal pattern such as a public `withdraw`.
- A skill that duplicates an existing title or summary.
- Lowering a floor or severity to make a noisy hit disappear.
