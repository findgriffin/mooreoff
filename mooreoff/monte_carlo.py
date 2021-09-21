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


# Assumes that never gets called with span[0]_current < span[0]_previous
def insert_with_sla(req_start: int,
                    bucket_array: list[int],
                    req_len: int = 1,
                    max_wait: int = 1,
                    max_threads: int = 1) -> bool:
    actual_start = req_start
    arr_len = len(bucket_array)
    fail_horizon = req_start + req_len + max_wait
    while bucket_array[actual_start] >= max_threads:
        actual_start += 1
        if actual_start >= arr_len or actual_start > fail_horizon:
            return False
    final_bucket = actual_start + req_len
    for index in range(actual_start, final_bucket):
        bucket_array[index % arr_len] += 1
    if final_bucket > fail_horizon:
        return False
    else:
        return True


def insert_many_with_sla(bucket_count: int,
                         req_count: int,
                         req_len: int,
                         max_wait: int = 1,
                         max_threads: int = 1) -> int:
    if bucket_count < 0:
        raise ValueError("There must be a positive number of buckets.")
    if req_count < 1:
        raise ValueError("More than one request is required.")
    if max_threads <= 0 or max_wait <= 0:
        raise ValueError("Max threads and max_wait must be > 0")
    if (req_len * req_count) > (bucket_count * max_threads):
        raise ValueError(f"Over capacity: {req_count} reqs x {req_len} "
                         f"buckets > {bucket_count} buckets x {max_threads} "
                         f"capacity.")
    buckets = [0] * bucket_count
    start_vals = [int(bucket_count * random.random())
                  for idx in range(req_count)]
    start_vals.sort()  # insert_with_sla only supports inserting in order
    successes = 0
    for val in start_vals:
        if insert_with_sla(val, buckets, req_len, max_wait, max_threads):
            successes += 1
    return successes


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
