#! /usr/local/bin/python3
# Use a Monte Carlo approach to model daily request traffic.
import time
import random
from itertools import repeat


MS_PER_SEC = 1000
SEC_PER_MIN = 60
MIN_PER_HR = 60
HR_PER_DAY = 24
DURATION_MS = 100
DAILY_TRAFFIC = 100_000


MIN_PER_DAY = MIN_PER_HR * HR_PER_DAY
SEC_PER_DAY = MIN_PER_DAY * SEC_PER_MIN
MS_PER_DAY = SEC_PER_DAY * MS_PER_SEC


bucket_count = MS_PER_DAY
ms_buckets = [0] * bucket_count


print(f"Created {bucket_count} buckets.")
print(f"Request duration is: {DURATION_MS} ms.")
print(f"Requests per day is {DAILY_TRAFFIC}.")
print(f"Requests per hour is constant.")

def insert(buckets_per_req, bucket_array):
    start = random.randint(0, bucket_count)
    for index in range(start, start + buckets_per_req):
        bucket_array[index % bucket_count] += 1


def timeit(func):
    def timer(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Ran {func.__name__} in {total_time} secs.")
        return total_time
    return timer


@timeit
def run_insert(duration, buckets, requests):
    for req in range(requests):
        insert(duration, buckets)

@timeit
def sort_buckets(buckets):
    buckets.sort()

run_insert(DURATION_MS, ms_buckets, DAILY_TRAFFIC)
sort_buckets(ms_buckets)

p50_index = int(bucket_count*0.5)
p90_index = int(bucket_count*0.9)
p99_index = int(bucket_count*0.99)
p999_index = int(bucket_count*0.999)
print(f"p0   is {ms_buckets[0]}")
print(f"p50  is {ms_buckets[p50_index]}")
print(f"p90  is {ms_buckets[p90_index]}")
print(f"p99  is {ms_buckets[p99_index]}")
print(f"p999  is {ms_buckets[p999_index]}")
print(f"p100 is {ms_buckets[-1]}")
