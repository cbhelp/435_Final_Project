# Experiment results

Seed: 435. Synthetic data only.

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
