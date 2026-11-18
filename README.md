# Spilling the Tea: Tea Branch Simulator

COMP 435 Final Project checkpoint: *Spilling the Tea: An Analysis of the 2025 Tea App Security Breach* (Track 1).

A small, standard-library-only Python simulation (Python 3.9+, no installs). It runs the same attacker against four storage-bucket configurations to show which ones would have stopped the Tea exposure. **All data is synthetic.**

## Question

Which bucket configuration would have stopped an unauthenticated attacker from listing and downloading users' verification photos, and which failures does access control alone *not* fix?

## Threat model (from the proposal)

- **Assets:** government ID images, selfies, private messages, user anonymity
- **Adversary:** anonymous attacker with no internal access who can reach the bucket
- **Trust assumptions:** storage is only reachable via the app, rules restrict access, images are deleted after verification, legacy data is migrated or deleted
- **Key violation modeled:** the forgotten legacy bucket (open access, and verified files never deleted)

## How to run

```
python run_experiment.py     # prints the table, writes results/results.md
python -m unittest -v        # checks each policy behaves as intended
```

## Files

| File | Purpose |
|---|---|
| `bucket.py` | Synthetic bucket (500 users, 2 files each) and the four policies |
| `attacker.py` | Attacker actions: list, bulk download, path guessing |
| `run_experiment.py` | Runs 2 attacker profiles x 4 configs, writes results |
| `test_bucket.py` | Unit tests for policy behavior |
| `PLAN.md` | Project plan, status, and next steps |

## Configurations

| Config | Rule |
|---|---|
| A: Legacy open | Anyone can list and read |
| B: Auth required | Any signed-in user can list and read |
| C: Owner-only | Owners read only their own files; no listing |
| D: Owner-only + retention | Same as C, and verified files are deleted |

Attackers: **anonymous** (no account) and **signed_up** (throwaway account via open sign-up).

## Results (seed 435)

| Config | Attacker | Listing works | Downloaded via listing | Guess hits | Unique files exposed | Verified files still stored |
|---|---|---|---|---|---|---|
| A: Legacy open | anonymous | yes | 1000 | 1000/1000 | 1000/1000 | 778 |
| A: Legacy open | signed_up | yes | 1000 | 1000/1000 | 1000/1000 | 778 |
| B: Auth required | anonymous | no | 0 | 0/1000 | 0/1000 | 778 |
| B: Auth required | signed_up | yes | 1000 | 1000/1000 | 1000/1000 | 778 |
| C: Owner-only | anonymous | no | 0 | 0/1000 | 0/1000 | 778 |
| C: Owner-only | signed_up | no | 0 | 0/1000 | 0/1000 | 778 |
| D: Owner-only + retention | anonymous | no | 0 | 0/1000 | 0/1000 | 0 |
| D: Owner-only + retention | signed_up | no | 0 | 0/1000 | 0/1000 | 0 |

## What the results show

1. **A reproduces the exposure.** An open bucket exposes every file, by listing or by guessing paths.
2. **B is not a fix.** "Requires login" blocks the anonymous attacker but not one who signs up. This is an extension and is not from the incident reports.
3. **C stops both attackers, but C and D look identical to an attacker.** The difference is the 778 verified files that C still stores. Those files are the blast radius if the access rules are ever misconfigured again, which is the Tea failure mode.
4. **Retention (D) is a separate control from access control.** It addresses the "images deleted after verification" trust assumption.

## Limitations

- Models access-policy logic, not real Firebase rules evaluation (the Firebase Emulator Suite is the next step).
- Path guessing assumes a predictable naming scheme chosen for this demo; the incident reports do not confirm one.
- Open sign-up in config B is an assumption about the app, not a confirmed Tea detail.
- Does not model the network, the migration process, or the second leak of private messages.
- Policies are hand-written to match the intended design, so the results confirm the logic rather than discover anything unexpected.
