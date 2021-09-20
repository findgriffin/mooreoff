#! /usr/local/bin/python3
# Use a Monte Carlo approach to model daily request traffic.
import logging
import random
import time

from mooreoff import constants as const
from mooreoff.types import SimulationParameters


def insert(buckets_per_req: int, bucket_array: list[int]):
    max = len(bucket_array) # Perf: Constant to avoid len(list) calls.
    # Perf: random.randint is slow, so use a different method
    # for generating random integers, from:
    #    * https://eli.thegreenplace.net/2018/
    #      slow-and-fast-methods-for-generating-random-integers-in-python/
    # Original code:
    #    start = random.randint(0, max)
    start = int(max * random.random())
    for index in range(start, start + buckets_per_req):
        bucket_array[index % max] += 1


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


def buckets_and_requests(
        params: SimulationParameters) -> tuple[list[int], int]:
    requests = min(
        int(params.requests_per_day * const.MIN_SIM_LENGTH_DAYS),
        const.MAX_REQUESTS_PER_SIMULATION)
    simulation_secs = requests / params.requests_per_day * const.SEC_PER_DAY
    bucket_count = int(const.MS_PER_SEC * simulation_secs)
    simulation_mins = simulation_secs / const.MIN_PER_HR
    logging.info(f"Simulation mins: {simulation_mins: .2f}.")
    return [0] * bucket_count, requests


@timeit
def simulate(params: SimulationParameters) -> list[int]:
    logging.info(
        f"Monte Carlo: {params.request_duration_ms} ms request duration, "
        f"and {'{:,}'.format(params.requests_per_day)} requests per day. ")
    buckets, request_count = buckets_and_requests(params)
    run_insert(params.request_duration_ms, buckets, request_count)
    buckets.sort()
    percentiles = []
    bucket_count = len(buckets)
    for percentile in const.PERCENTILES:
        bucket = bucket_for_percentile(percentile, bucket_count)
        percentiles.append(buckets[bucket])
    return percentiles
