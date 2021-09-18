import logging
from datetime import timedelta
from typing import Optional
import argparse
from mooreoff import monte_carlo
from mooreoff import constants as const
from mooreoff.types import SimulationParameters


def setup(argv) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This is a Python 3 project.")
    parser.add_argument("--output", type=str, required=False,
                        help="A filename to write the output to.")
    parser.add_argument("-v", "--verbose",  action="store_true",
                        help="Enable verbose logging.")
    return parser.parse_args(argv)


def format_large_number(number: int) -> str:
    if abs(number) >= const.MILLION:
        return f"{number/const.MILLION}MM"
    elif abs(number) >= const.THOUSAND:
        return f"{number/const.THOUSAND}k"
    else:
        return str(number)


def print_result(utilization: float, requests: int, containers: int):
    util_p = utilization * const.PERCENT
    req = format_large_number(requests)
    cont = containers
    print(f"Utilization for {req} is {util_p:.2f}% of {cont} containers.")


def print_csv_line(collection, row, prefix=''):
    print(f"{row}\t" + ",\t".join([f"{prefix}{i}" for i in collection]))


def run(output: Optional[str] = None) -> str:
    request_range = [1000 * 10 ** (n - 1) for n in range(1, 6)]
    percentiles = const.PERCENTILES
    sla = 99
    simulation_length = timedelta(hours=const.SIMULATION_HOURS)
    print(f"Simulating {const.SIMULATION_HOURS} hours of one day.")
    print(f"Using SLA of {sla} to calculate utilization.")
    for requests in request_range:
        params = SimulationParameters(request_duration_ms=10,
                                      requests_per_day=requests,
                                      simulation_length=simulation_length)
        result = monte_carlo.simulate(params)
        print_csv_line(
            result, format_large_number(requests))
        utilization = monte_carlo.calculate_utilization(
            percentiles, result, sla)
        print_result(utilization[1], requests, utilization[0])
    if output:
        logging.debug("Output file given.")
        return f"Hello, {output}!"
    else:
        logging.debug("No output files given.")
        return "Hello, world!"
