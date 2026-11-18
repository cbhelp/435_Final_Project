# Project Plan: Spilling the Tea (COMP 435)

Track 1: Analyze a Real System or Incident.
Deadlines: Proposal 10/21 (done) | Checkpoint 11/16 | Final artifact, report, presentation 12/2

## Core question
How did improper management of a cloud backend service expose 72,000+ Tea app images, what was the cause, and what could have prevented it?

## Deliverables and status

| Deliverable | Status |
|---|---|
| Threat model (assets, adversary, trust assumptions) | Done (in proposal and README) |
| Python simulation, 4 configs x 2 attackers | Done (this repo) |
| Unit tests for policies | Done (7 passing) |
| Checkpoint write-up | To do: use README results |
| Timeline of the incident | To do |
| Attack tree / attack-flow diagram | To do |
| Firebase Emulator experiment (`storage.rules` + Python test scripts) | To do |
| Mitigation comparison (2-3 mitigations) | To do |
| Policy analysis (terms vs. practice, retention) | To do |
| Final report (4-6 pages) | To do |
| Final presentation or demo (5 min) | To do |

## Design of the simulation
- `bucket.py`: 500 synthetic users, 2 files each, ~80% marked verified. Four policies (A open, B auth required, C owner-only, D owner-only + retention).
- `attacker.py`: list, bulk download, path guessing. Profiles: anonymous and signed_up.
- `run_experiment.py`: fixed seed (435) so results are reproducible.
- `test_bucket.py`: confirms each policy does what it claims.

## Checkpoint write-up outline
1. **Preliminary result:** results table from README. A exposes all; B blocks anonymous only; C and D block both; only D removes stored verified files.
2. **Completed:** threat model, simulation, tests, results.
3. **Biggest unresolved challenge:** how faithfully a simulation captures real Firebase rules behavior. The emulator work addresses this.
4. **Scope change:** added a simulation stage before the emulator, plus the signed_up attacker (config B finding).

## Next steps (after checkpoint)
1. Install Node.js and Java; set up the Firebase Emulator Suite.
2. Write `storage.rules` files matching configs A-D; run Python test scripts against the emulator with synthetic data.
3. Compare emulator results to the simulation and note any differences.
4. Build the timeline and attack tree from the two sources in the proposal (Security Affairs, ABA).
5. Compare mitigations: auth-only rules, owner-only rules, retention/deletion, bucket inventory during migration.
6. Write the report. It must answer: what did I learn that I couldn't have learned just by reading about the topic?

## Open questions
- Add a second bucket (legacy vs. migrated) to model the forgotten-bucket story more explicitly? Currently one bucket; the migration is not modeled.
- Verify naming-scheme and open-sign-up assumptions against the sources, or keep them labeled as assumptions.
- Do I have Node.js and Java locally for the emulator?

## Risks
- Results confirm hand-written logic rather than reveal surprises; the emulator comparison is where new evidence comes from.
- Claims about the incident must be sourced; keep demo assumptions labeled as assumptions.
