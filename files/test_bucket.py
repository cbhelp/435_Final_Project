"""Checks that each policy behaves as intended. Run: python -m unittest -v"""

import unittest

from attacker import attack
from bucket import (ANONYMOUS, NUM_USERS, POLICY_A, POLICY_B, POLICY_C,
                    POLICY_D, Bucket, Requester)

OWN = "verification/user_0001/id.jpg"
OTHER = "verification/user_0002/id.jpg"


class TestPolicies(unittest.TestCase):
    def test_a_anonymous_can_list_and_read(self):
        b = Bucket(POLICY_A)
        self.assertIsNotNone(b.list(ANONYMOUS))
        self.assertIsNotNone(b.read(ANONYMOUS, OTHER))

    def test_b_blocks_anonymous_but_not_signup(self):
        b = Bucket(POLICY_B)
        self.assertIsNone(b.list(ANONYMOUS))
        self.assertIsNone(b.read(ANONYMOUS, OTHER))
        attacker = b.sign_up()
        self.assertEqual(len(b.list(attacker)), NUM_USERS * 2)
        self.assertIsNotNone(b.read(attacker, OTHER))

    def test_c_owner_only(self):
        b = Bucket(POLICY_C)
        owner = Requester("user", "user_0001")
        self.assertIsNotNone(b.read(owner, OWN))
        self.assertIsNone(b.read(owner, OTHER))
        self.assertIsNone(b.list(owner))
        self.assertIsNone(b.read(b.sign_up(), OTHER))

    def test_c_keeps_verified_files(self):
        b = Bucket(POLICY_C)
        b.run_retention()
        self.assertGreater(b.verified_files_still_stored(), 0)

    def test_d_deletes_verified_files(self):
        b = Bucket(POLICY_D)
        deleted = b.run_retention()
        self.assertGreater(deleted, 0)
        self.assertEqual(b.verified_files_still_stored(), 0)

    def test_missing_file_returns_none(self):
        b = Bucket(POLICY_A)
        self.assertIsNone(b.read(ANONYMOUS, "verification/user_9999/id.jpg"))

    def test_attack_totals(self):
        b = Bucket(POLICY_A)
        result = attack(b, ANONYMOUS)
        self.assertEqual(result.unique_files_exposed, NUM_USERS * 2)
        c = Bucket(POLICY_C)
        self.assertEqual(attack(c, ANONYMOUS).unique_files_exposed, 0)


if __name__ == "__main__":
    unittest.main()
