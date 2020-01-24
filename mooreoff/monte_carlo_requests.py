#! /usr/local/bin/python3
# Use a Monte Carlo approach to model daily request traffic.
import time
import random
from itertools import repeat


MS_PER_SEC = 1000
SEC_PER_MIN = 60
MIN_PER_HR = 60
HR_PER_DAY = 1
DURATION_MS = 100

MIN_PER_DAY = MIN_PER_HR * HR_PER_DAY
SEC_PER_DAY = MIN_PER_DAY * SEC_PER_MIN
MS_PER_DAY = SEC_PER_DAY * MS_PER_SEC

PERCENT = 100
PERCENTILES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 99.9, 99.99, 99.999, 100]


def insert(buckets_per_req, bucket_array):
    start = random.randint(0, len(bucket_array))
    for index in range(start, start + buckets_per_req):
        bucket_array[index % len(bucket_array)] += 1


def timeit(func):
    def timer(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Ran {func.__name__} in {total_time} secs.")
        return res
    return timer


def run_insert(duration, buckets, requests):
    for req in range(requests):
        insert(duration, buckets)

def sort_buckets(buckets):
    buckets.sort()

def print_csv_line(collection, prefix=''):
    print(",\t".join([f"{prefix}{i}" for i in collection]))
    


def bucket_for_percentile(percentile, bucket_count):
    return min(int(bucket_count*percentile/PERCENT), bucket_count-1)

@timeit
def run_monte_carlo(duration_in_buckets, bucket_count, daily_traffic):
    PART_1 = f"Monte Carlo: {bucket_count} buckets, "
    PART_2 = f"{duration_in_buckets} buckets request duration, "
    PART_3 = f"and {daily_traffic} requests per day "
    print(PART_1 + PART_2 + PART_3)
    buckets = [0] * bucket_count
    run_insert(duration_in_buckets, buckets, daily_traffic)
    sort_buckets(buckets)
    percentiles = [] 
    for percentile in PERCENTILES:
        bucket = bucket_for_percentile(percentile, bucket_count)
        percentiles.append(buckets[bucket])
    return percentiles


result_1k = run_monte_carlo(DURATION_MS, MS_PER_DAY, int(1_000/24))
result_10k = run_monte_carlo(DURATION_MS, MS_PER_DAY, int(10_000/24))
result_100k = run_monte_carlo(DURATION_MS, MS_PER_DAY, int(100_000/24))
result_1MM = run_monte_carlo(DURATION_MS, MS_PER_DAY, int(1_000_000/24))
result_10MM = run_monte_carlo(DURATION_MS, MS_PER_DAY, int(10_000_000/24))
print_csv_line(PERCENTILES, prefix='p')
print_csv_line(result_1k)
print_csv_line(result_10k)
print_csv_line(result_100k)
print_csv_line(result_1MM)
print_csv_line(result_10MM)

