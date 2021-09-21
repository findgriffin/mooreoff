import logging
from typing import Optional
import argparse
from mooreoff import monte_carlo
from mooreoff import constants as const
from mooreoff.types import SimulationParameters


def setup(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This is a Python 3 project.")
    parser.add_argument("--output", type=str, required=False,
                        help="A filename to write the output to.")
    parser.add_argument("--profile", action="store_true",
                        help="Run with the profiler (cProfile) enabled.")
    parser.add_argument("-v", "--verbose",  action="store_true",
                        help="Enable verbose logging.")
    return parser.parse_args(argv)


def format_large_number(number: int) -> str:
    if abs(number) >= const.BILLION:
        return f"{number/const.BILLION} Billion"
    if abs(number) >= const.MILLION:
        return f"{number/const.MILLION}MM"
    elif abs(number) >= const.THOUSAND:
        return f"{number/const.THOUSAND}k"
    else:
        return str(number)


def print_result(utilization: float, requests: int, containers: int):
    util_p = utilization * const.PERCENT
    logging.info(f"Utilization for {format_large_number(requests)} is "
                 f"{util_p:.2f}% of {containers} containers.")


def print_csv_line(collection, row, prefix=''):
    logging.info(f"{row}\t" + ",\t".join([f"{prefix}{i}" for i in collection]))


def calculate_daily_capacity(request_duration_ms: int = 1,
                             max_threads: int = 1) -> int:
    requests_per_sec = const.MS_PER_SEC / request_duration_ms
    request_per_day_per_thread = requests_per_sec * const.SEC_PER_DAY
    return int(request_per_day_per_thread * max_threads)


def run(output: Optional[str] = None) -> None:
    if output:
        logging.debug(f"Output file: {output}.")
    else:
        logging.debug("No output file given.")
    request_duration_ms = 100
    max_threads = 1
    max_wait = request_duration_ms
    capacity = calculate_daily_capacity(request_duration_ms, max_threads)
    logging.info(f"Request duration of {request_duration_ms}ms, "
                 f"and max_threads of {max_threads} gives a daily capacity "
                 f"of {capacity} requests.")
    num_runs = 10
    step = int(capacity/num_runs)
    request_range = [i for i in range(step, capacity, step)]
    logging.info(f"Running for {request_range}")
    logging.info(f"Max wait for SLA is {max_wait}ms.")
    results: list[tuple[int, float, float]] = []
    for requests in request_range:
        params = SimulationParameters(request_duration_ms=request_duration_ms,
                                      requests_per_day=requests,
                                      max_wait=max_wait)
        utilization_fraction, fail_fraction = monte_carlo.simulate(params)
        fail_percent = fail_fraction * const.PERCENT
        utilization_percent = utilization_fraction * const.PERCENT
        logging.info(f"For {requests} requests per day, got utilization of"
                     f" {utilization_percent:.1f}%, with {fail_percent:.1f}% "
                     "requests failing SLA.")
        results.append((requests, utilization_fraction, fail_fraction))
