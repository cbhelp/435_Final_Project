"""Attacker actions run against a Bucket.

Two profiles:
  anonymous  - no account (the threat model in the proposal)
  signed_up  - makes a throwaway account via open sign-up (extension)

Assumption: the attacker knows the path naming pattern
(verification/user_NNNN/{id,selfie}.jpg). This is a choice made for the
demo; the incident reports do not confirm it.
"""

from dataclasses import dataclass
from typing import Set

from bucket import ANONYMOUS, FILES_PER_USER, NUM_USERS, Bucket, Requester


@dataclass
class AttackResult:
    list_works: bool
    downloaded_via_listing: int
    guess_attempts: int
    guess_hits: int
    unique_files_exposed: int


def make_attacker(profile: str, bucket: Bucket) -> Requester:
    if profile == "anonymous":
        return ANONYMOUS
    if profile == "signed_up":
        return bucket.sign_up()
    raise ValueError(f"unknown attacker profile: {profile}")


def attack(bucket: Bucket, requester: Requester) -> AttackResult:
    obtained: Set[str] = set()

    # 1. List everything, then download everything listed.
    listing = bucket.list(requester)
    downloaded = 0
    if listing is not None:
        for path in listing:
            if bucket.read(requester, path) is not None:
                obtained.add(path)
                downloaded += 1

    # 2. Guess paths from the predictable naming pattern.
    attempts = 0
    hits = 0
    for i in range(1, NUM_USERS + 1):
        for name in FILES_PER_USER:
            path = f"verification/user_{i:04d}/{name}"
            attempts += 1
            if bucket.read(requester, path) is not None:
                hits += 1
                obtained.add(path)

    return AttackResult(
        list_works=listing is not None,
        downloaded_via_listing=downloaded,
        guess_attempts=attempts,
        guess_hits=hits,
        unique_files_exposed=len(obtained),
    )
