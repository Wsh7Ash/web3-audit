# Security

## Scope

This repository ships a text scanner and skill documents. It does not connect to a node, hold keys or execute Solidity.

## Using the scanner

Scanner output is advisory. A clean scan means the eleven rules found nothing; it does not mean the contract is safe. Treat every finding as a lead that needs a code reading.

## Intended use

Review contracts you are authorised to review. The recon and triage phases describe scoping and duplicate checks; they are not a substitute for a written agreement.

## Reporting a problem

Open an issue with the rule id, the triggering line and what you expected. For a false negative, include the smallest snippet that should have matched.
