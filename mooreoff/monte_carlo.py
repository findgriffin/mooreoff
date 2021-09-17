#! /usr/local/bin/python3
# Use a Monte Carlo approach to model daily request traffic.
import time
import random


DURATION_MS = 10
MIN_PER_HR = 60
MS_PER_SEC = 1000
HR_PER_DAY = 24
SEC_PER_MIN = 60
SIMULATION_HOURS = 1
PERCENT = 100
THOUSAND = 1000
MILLION = 1_000_000


PERCENTILES = [0, 10, 20, 30, 40, 50, 60, 70,
               80, 90, 99, 99.9, 99.99, 99.999, 100]


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
            deflator = (percentiles[index]-percentiles[index-1]) / PERCENT
            running_sum.append(last_bucket / capacity * deflator)
        last_bucket = results[index]
    return (capacity, sum(running_sum))


@timeit
def run_monte_carlo(duration_in_ms, daily_traffic):
    bucket_count = MS_PER_SEC * SEC_PER_MIN * MIN_PER_HR * SIMULATION_HOURS
    PART_1 = f"Monte Carlo: {SIMULATION_HOURS} hours, "
    PART_2 = f"{duration_in_ms} ms request duration, "
    PART_3 = f"and {'{:,}'.format(daily_traffic)} requests per day. "
    print(PART_1 + PART_2 + PART_3)
    buckets = [0] * bucket_count
    run_insert(duration_in_ms, buckets,
               int(daily_traffic / SIMULATION_HOURS / HR_PER_DAY))
    sort_buckets(buckets)
    percentiles = []
    for percentile in PERCENTILES:
        bucket = bucket_for_percentile(percentile, bucket_count)
        percentiles.append(buckets[bucket])
    return percentiles


def format_large_number(number: int) -> str:
    if abs(number) >= MILLION:
        return f"{number/MILLION}MM"
    elif abs(number) >= THOUSAND:
        return f"{number/THOUSAND}k"
    else:
        return str(number)


def print_result(utilization: float, requests: int, containers: int):
    util_p = utilization * PERCENT
    req = format_large_number(requests)
    cont = containers
    print(f"Utilization for {req} is {util_p:.2f}% of {cont} containers.")


SLA = 99.99
print(f"Simulating {SIMULATION_HOURS} hours of one day.")
result_1k = run_monte_carlo(DURATION_MS, 1_000)
result_10k = run_monte_carlo(DURATION_MS, 10_000)
result_100k = run_monte_carlo(DURATION_MS, 100_000)
result_1MM = run_monte_carlo(DURATION_MS, 1_000_000)
result_10MM = run_monte_carlo(DURATION_MS, 10_000_000)
result_100MM = run_monte_carlo(DURATION_MS, 100_000_000)
print_csv_line(PERCENTILES, "", prefix='p')
print_csv_line(result_1k, "1k")
print_csv_line(result_10k, "10k")
print_csv_line(result_100k, "100k")
print_csv_line(result_1MM, "1MM")
print_csv_line(result_10MM, "10MM")
print_csv_line(result_100MM, "100MM")
utilization_1k = calculate_utilization(PERCENTILES, result_1k, SLA)
utilization_10k = calculate_utilization(PERCENTILES, result_10k, SLA)
utilization_100k = calculate_utilization(PERCENTILES, result_100k, SLA)
utilization_1MM = calculate_utilization(PERCENTILES, result_1MM, SLA)
utilization_10MM = calculate_utilization(PERCENTILES, result_10MM, SLA)
utilization_100MM = calculate_utilization(PERCENTILES, result_100MM, SLA)
print(f"Using SLA of {SLA} to calculate utilization.")
print_result(utilization_1k[1], 1000, utilization_1k[0])
print_result(utilization_10k[1], 10_000, utilization_10k[0])
print_result(utilization_100k[1], 100_000, utilization_100k[0])
print_result(utilization_1MM[1], 1_000_000, utilization_1MM[0])
print_result(utilization_10MM[1], 10_000_000, utilization_10MM[0])
print_result(utilization_100MM[1], 100_000_000, utilization_100MM[0])
