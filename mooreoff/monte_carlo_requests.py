#! /usr/local/bin/python3
# Use a Monte Carlo approach to model daily request traffic.
import time
import random
from itertools import repeat


DURATION_MS = 100
MIN_PER_HR = 60
MS_PER_SEC = 1000
HR_PER_DAY = 24
SEC_PER_MIN = 60
SIMULATION_HOURS = 1
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

def print_csv_line(collection, row, prefix=''):
    print(f"{row}\t" + ",\t".join([f"{prefix}{i}" for i in collection]))
    


def bucket_for_percentile(percentile, bucket_count):
    return min(int(bucket_count*percentile/PERCENT), bucket_count-1)

@timeit
def run_monte_carlo(duration_in_ms, daily_traffic):
    bucket_count = MS_PER_SEC * SEC_PER_MIN * MIN_PER_HR * SIMULATION_HOURS
    PART_1 = f"Monte Carlo: {SIMULATION_HOURS} hours, "
    PART_2 = f"{duration_in_ms} ms request duration, "
    PART_3 = f"and {'{:,}'.format(daily_traffic)} requests per day. "
    print(PART_1 + PART_2 + PART_3)
    buckets = [0] * bucket_count
    run_insert(duration_in_ms, buckets, int(daily_traffic / SIMULATION_HOURS / HR_PER_DAY))
    sort_buckets(buckets)
    percentiles = [] 
    for percentile in PERCENTILES:
        bucket = bucket_for_percentile(percentile, bucket_count)
        percentiles.append(buckets[bucket])
    return percentiles


print(f"Simulating {SIMULATION_HOURS} hours of one day.")
result_1k = run_monte_carlo(DURATION_MS, 1_000)
result_10k = run_monte_carlo(DURATION_MS, 10_000)
result_100k = run_monte_carlo(DURATION_MS, 100_000)
result_1MM = run_monte_carlo(DURATION_MS, 1_000_000)
result_10MM = run_monte_carlo(DURATION_MS, 10_000_000)
#result_100MM = run_monte_carlo(DURATION_MS, 100_000_000)
print_csv_line(PERCENTILES, "", prefix='p')
print_csv_line(result_1k, "1k")
print_csv_line(result_10k, "10k")
print_csv_line(result_100k, "100k")
print_csv_line(result_1MM, "1MM")
print_csv_line(result_10MM, "10MM")
#print_csv_line(result_100MM, "100MM")
