import unittest

import mooreoff.monte_carlo as mc


class TestInsert(unittest.TestCase):

    def test_insert_with_sla_happy(self):
        # Given
        buckets = [0]
        # When
        result = mc.insert_with_sla(0, buckets)
        # Then
        self.assertTrue(result)
        self.assertListEqual(buckets, [1])

    # Kind of nonsense because len(bucket_array) should be >> req_len
    def test_short_array_double_inserts(self):
        # Given
        buckets = [0]
        # When
        result = mc.insert_with_sla(0, buckets, 2)
        # Then
        self.assertTrue(result)
        self.assertListEqual(buckets, [2])

    def test_insert_near_end(self):
        # Given
        buckets = [0, 0, 0, 0]
        # When
        result = mc.insert_with_sla(3, buckets, 2)
        # Then
        self.assertListEqual(buckets, [1, 0, 0, 1])
        self.assertTrue(result)

    def test_full_does_not_insert(self):
        # Given
        buckets = [1, 1, 1, 1, 1]
        # When
        result = mc.insert_with_sla(3, buckets, 2)
        # Then
        self.assertFalse(result)
        self.assertListEqual(buckets, [1, 1, 1, 1, 1])

    def test_big_array(self):
        # Given
        num_buckets = 1000
        buckets = [0] * num_buckets
        start = 3
        req_len = 2
        # When
        result = mc.insert_with_sla(3, buckets, 2)
        # Then
        self.assertTrue(result)
        self.assertListEqual(buckets, [0] * start + [1] * req_len + [0] * (
            num_buckets - start - req_len))
