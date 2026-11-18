"""Run every attacker profile against every policy and report results.

Usage:  python run_experiment.py
Output: printed table + results/results.md
"""

import os

from attacker import attack, make_attacker
from bucket import ALL_POLICIES, Bucket

SEED = 435
PROFILES = ["anonymous", "signed_up"]


def run():
    rows = []
    for policy in ALL_POLICIES:
        for profile in PROFILES:
            bucket = Bucket(policy, seed=SEED)
            total = len(bucket.objects)
            bucket.run_retention()  # only policy D actually deletes
            requester = make_attacker(profile, bucket)
            result = attack(bucket, requester)
            rows.append({
                "config": policy.name,
                "attacker": profile,
                "list": "yes" if result.list_works else "no",
                "listed_dl": result.downloaded_via_listing,
                "guess_hits": f"{result.guess_hits}/{result.guess_attempts}",
                "exposed": f"{result.unique_files_exposed}/{total}",
                "retained": bucket.verified_files_still_stored(),
            })
    return rows


def to_markdown(rows):
    header = ("| Config | Attacker | Listing works | Downloaded via listing "
              "| Guess hits | Unique files exposed | Verified files still stored |")
    sep = "|---|---|---|---|---|---|---|"
    lines = [header, sep]
    for r in rows:
        lines.append(
            f"| {r['config']} | {r['attacker']} | {r['list']} | {r['listed_dl']} "
            f"| {r['guess_hits']} | {r['exposed']} | {r['retained']} |"
        )
    return "\n".join(lines)


def main():
    table = to_markdown(run())
    print(table)
    os.makedirs("results", exist_ok=True)
    with open(os.path.join("results", "results.md"), "w") as f:
        f.write("# Experiment results\n\n")
        f.write(f"Seed: {SEED}. Synthetic data only.\n\n")
        f.write(table + "\n")
    print("\nSaved to results/results.md")


if __name__ == "__main__":
    main()
