#! /usr/local/bin/python3
# Use a Monte Carlo approach to model daily request traffic.
import logging
import random
import time

from mooreoff import constants as const
from mooreoff.types import SimulationParameters


def insert(buckets_per_req: int, bucket_array: list[int]):
    start = random.randint(0, len(bucket_array))
    for index in range(start, start + buckets_per_req):
        bucket_array[index % len(bucket_array)] += 1


def timeit(func):
    def timer(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        logging.info(f"Ran {func.__name__} in {total_time:.2f} secs.")
        return res
    return timer


def run_insert(duration: int, buckets: list[int], requests: int) -> None:
    for req in range(requests):
        insert(duration, buckets)


def bucket_for_percentile(percentile: float, bucket_count: int) -> int:
    return min(int(bucket_count*percentile/const.PERCENT), bucket_count-1)


def calculate_utilization(percentiles: list[float],
                          results: list[float],
                          sla_percentile: float):
    sla_index = None
    for index in range(len(percentiles)):
        if percentiles[index] == sla_percentile:
            sla_index = index
            break
    if sla_index is None:
        raise ValueError(f"Could not find {sla_percentile} in percentiles.")
    capacity = int(max(results[sla_index], 1))
    last_bucket = None
    running_sum: list[float] = []
    for index in range(len(percentiles)):
        if last_bucket is not None:
            deflator = (percentiles[index]-percentiles[index-1]) / \
                       const.PERCENT
            running_sum.append(last_bucket / capacity * deflator)
        last_bucket = results[index]
    return (capacity, sum(running_sum))


@timeit
def simulate(params: SimulationParameters) -> list[int]:
    bucket_count = const.MS_PER_SEC * params.simulation_length.seconds
    PART_1 = f"Monte Carlo: {params.simulation_length} hours, "
    PART_2 = f"{params.request_duration_ms} ms request duration, "
    PART_3 = f"and {'{:,}'.format(params.requests_per_day)} " \
             f"requests per day. "
    logging.info(PART_1 + PART_2 + PART_3)
    buckets = [0] * bucket_count
    run_insert(params.request_duration_ms, buckets,
               int(params.requests_per_day / const.SIMULATION_HOURS /
                   const.HR_PER_DAY))
    buckets.sort()
    percentiles = []
    for percentile in const.PERCENTILES:
        bucket = bucket_for_percentile(percentile, bucket_count)
        percentiles.append(buckets[bucket])
    return percentiles
