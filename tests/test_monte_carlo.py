import unittest
from datetime import datetime

import mooreoff.monte_carlo as mc


class TestInsert(unittest.TestCase):

    def test_insert_with_sla_happy(self):
        # Given
        buckets = [0]
        # When
        result = mc.insert_with_sla(0, buckets, len(buckets))
        # Then
        self.assertTrue(result)
        self.assertListEqual(buckets, [1])

    # Kind of nonsense because len(bucket_array) should be >> req_len
    def test_short_array_does_not_insert(self):
        # Given
        buckets = [0]
        # When
        result = mc.insert_with_sla(0, buckets, len(buckets), 2)
        # Then
        self.assertTrue(result)
        self.assertListEqual(buckets, [2])

    def test_insert_near_end(self):
        # Given
        buckets = [0, 0, 0, 0]
        # When
        result = mc.insert_with_sla(3, buckets, len(buckets), req_len=2)
        # Then
        self.assertListEqual(buckets, [1, 0, 0, 1])
        self.assertTrue(result)

    def test_full_does_not_insert(self):
        # Given
        buckets = [1, 1, 1, 1, 1]
        # When
        result = mc.insert_with_sla(3, buckets, len(buckets), req_len=2)
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
        result = mc.insert_with_sla(3, buckets, len(buckets), req_len=2)
        # Then
        self.assertTrue(result)
        self.assertListEqual(buckets, [0] * start + [1] * req_len + [0] * (
            num_buckets - start - req_len))

    def test_many_with_sla_single(self):
        # Given
        bucket_count = 10
        request_count = 1

        # When
        result = mc.insert_many_with_sla(bucket_count, request_count, 1)

        # Then
        self.assertEqual(result[1], 1)

    def test_insert_many_easy(self):
        # Given
        bucket_count = 10000
        request_count = 100

        # When
        result = mc.insert_many_with_sla(bucket_count, request_count, 1)

        # Then
        self.assertGreater(result[1], 98,
                           "Very unlikely to breach SLA in this case.")

    def test_insert_many_max_capacity(self):
        # Given
        bucket_count = 200
        req_count = 20
        req_len = 5

        # When
        result = mc.insert_many_with_sla(bucket_count, req_count, req_len)

        # Then
        self.assertLess(result[1], 50,
                        "Very likely to breach SLA in this case.")

    def test_insert_many_over_capacity(self):
        # Given
        bucket_count = 100
        req_count = 11
        req_len = 10

        # When
        with self.assertRaises(ValueError) as context:
            mc.insert_many_with_sla(bucket_count, req_count, req_len)

        # Then
        self.assertEqual(str(context.exception),
                         "Over capacity: 11 reqs x 10 buckets > 100 buckets "
                         "x 1 capacity.")


class TestMonteCarloPerformance(unittest.TestCase):

    def test_insert_performance_hundred_k_reqs(self):
        # Given
        bucket_count, req_count, req_len = (3_600_000, 100_000, 2)
        # When
        start = datetime.now()
        mc.insert_many_with_sla(bucket_count, req_count, req_len)
        delta = datetime.now() - start
        # Then
        self.assertEqual(delta.days, 0)
        self.assertLess(delta.seconds, 1)

    @unittest.skip("Don't run slow perf tests as part of build")
    def test_insert_performance_million_reqs(self):
        # Given
        bucket_count, req_count, req_len = (3_600_000, 1_000_000, 2)
        # When
        start = datetime.now()
        mc.insert_many_with_sla(bucket_count, req_count, req_len)
        delta = datetime.now() - start
        # Then
        self.assertEqual(delta.days, 0)
        self.assertLess(delta.seconds, 6)

    @unittest.skip("Don't run slow perf tests as part of build")
    def test_insert_performance_more_reqs(self):
        # Given
        bucket_count, req_count, req_len = (3_600, 1_000_000, 2)
        # When
        start = datetime.now()
        mc.insert_many_with_sla(bucket_count, req_count, req_len,
                                max_threads=1000)
        delta = datetime.now() - start

        # Then
        self.assertEqual(delta.days, 0)
        self.assertLess(delta.seconds, 6)
