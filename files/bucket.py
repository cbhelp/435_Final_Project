"""Simulated storage bucket with four access policies.

Everything here is synthetic: no real images, names, or personal data.
This models access-policy *logic*, not real Firebase rules evaluation.
"""

import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

NUM_USERS = 500
VERIFIED_FRACTION = 0.8  # share of users whose verification is complete
FILES_PER_USER = ("id.jpg", "selfie.jpg")


@dataclass(frozen=True)
class Requester:
    """Who is making a request. kind is 'anonymous' or 'user'."""
    kind: str
    uid: Optional[str] = None


ANONYMOUS = Requester("anonymous")


@dataclass
class StoredObject:
    path: str
    owner: str
    data: bytes
    verified: bool  # True once the owner's verification is complete


@dataclass(frozen=True)
class Policy:
    name: str
    description: str
    can_list: Callable[[Requester], bool]
    can_read: Callable[[Requester, StoredObject], bool]
    delete_after_verification: bool


# --- The four policies -----------------------------------------------------

POLICY_A = Policy(
    name="A: Legacy open",
    description="Anyone can list and read (the forgotten, unsecured bucket).",
    can_list=lambda r: True,
    can_read=lambda r, o: True,
    delete_after_verification=False,
)

POLICY_B = Policy(
    name="B: Auth required",
    description="Any signed-in user can list and read.",
    can_list=lambda r: r.kind == "user",
    can_read=lambda r, o: r.kind == "user",
    delete_after_verification=False,
)

POLICY_C = Policy(
    name="C: Owner-only",
    description="Owners read only their own files; nobody can list.",
    can_list=lambda r: False,
    can_read=lambda r, o: r.kind == "user" and r.uid == o.owner,
    delete_after_verification=False,
)

POLICY_D = Policy(
    name="D: Owner-only + retention",
    description="Same as C, and verified files are deleted.",
    can_list=lambda r: False,
    can_read=lambda r, o: r.kind == "user" and r.uid == o.owner,
    delete_after_verification=True,
)

ALL_POLICIES: List[Policy] = [POLICY_A, POLICY_B, POLICY_C, POLICY_D]


# --- The bucket ------------------------------------------------------------

class Bucket:
    """A bucket of synthetic verification files governed by one Policy."""

    def __init__(self, policy: Policy, seed: int = 435):
        self.policy = policy
        self.objects: Dict[str, StoredObject] = {}
        self._populate(random.Random(seed))
        self._signups = 0

    def _populate(self, rng: random.Random) -> None:
        for i in range(1, NUM_USERS + 1):
            uid = f"user_{i:04d}"
            verified = rng.random() < VERIFIED_FRACTION
            for name in FILES_PER_USER:
                path = f"verification/{uid}/{name}"
                placeholder = f"SYNTHETIC:{path}".encode()
                self.objects[path] = StoredObject(path, uid, placeholder, verified)

    def sign_up(self) -> Requester:
        """Open self-registration: anyone can make an account."""
        self._signups += 1
        return Requester("user", f"throwaway_{self._signups:04d}")

    def list(self, requester: Requester) -> Optional[List[str]]:
        """Return all paths, or None if the policy denies listing."""
        if not self.policy.can_list(requester):
            return None
        return sorted(self.objects)

    def read(self, requester: Requester, path: str) -> Optional[bytes]:
        """Return file bytes, or None if missing or denied."""
        obj = self.objects.get(path)
        if obj is None or not self.policy.can_read(requester, obj):
            return None
        return obj.data

    def run_retention(self) -> int:
        """Delete verified files if the policy requires it. Returns count deleted."""
        if not self.policy.delete_after_verification:
            return 0
        doomed = [p for p, o in self.objects.items() if o.verified]
        for p in doomed:
            del self.objects[p]
        return len(doomed)

    def verified_files_still_stored(self) -> int:
        """Sensitive files that should have been deleted but are still here."""
        return sum(1 for o in self.objects.values() if o.verified)
