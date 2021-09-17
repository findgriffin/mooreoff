#! /usr/local/bin/python3
# Use a Monte Carlo approach to model daily request traffic.
import time
import random

from mooreoff import constants as const


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


def print_csv_line(collection, row, prefix=''):
    print(f"{row}\t" + ",\t".join([f"{prefix}{i}" for i in collection]))


def bucket_for_percentile(percentile, bucket_count):
    return min(int(bucket_count*percentile/const.PERCENT), bucket_count-1)


def calculate_utilization(percentiles, results, sla_percentile):
    sla_index = None
    for index in range(len(percentiles)):
        if percentiles[index] == sla_percentile:
            sla_index = index
            break
    if sla_index is None:
        raise ValueError(f"Could not find {sla_percentile} in percentiles.")
    capacity = int(max(results[sla_index], 1))
    last_bucket = None
    running_sum = []
    for index in range(len(percentiles)):
        if last_bucket is not None:
            deflator = (percentiles[index]-percentiles[index-1]) / \
                       const.PERCENT
            running_sum.append(last_bucket / capacity * deflator)
        last_bucket = results[index]
    return (capacity, sum(running_sum))


@timeit
def simulate(duration_in_ms, daily_traffic):
    bucket_count = const.MS_PER_SEC * const.SEC_PER_MIN * const.MIN_PER_HR * \
                   const.SIMULATION_HOURS
    PART_1 = f"Monte Carlo: {const.SIMULATION_HOURS} hours, "
    PART_2 = f"{duration_in_ms} ms request duration, "
    PART_3 = f"and {'{:,}'.format(daily_traffic)} requests per day. "
    print(PART_1 + PART_2 + PART_3)
    buckets = [0] * bucket_count
    run_insert(duration_in_ms, buckets,
               int(daily_traffic / const.SIMULATION_HOURS / const.HR_PER_DAY))
    buckets.sort()
    percentiles = []
    for percentile in const.PERCENTILES:
        bucket = bucket_for_percentile(percentile, bucket_count)
        percentiles.append(buckets[bucket])
    return percentiles
