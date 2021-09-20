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


def run(output: Optional[str] = None) -> None:
    if output:
        logging.debug(f"Output file: {output}.")
    else:
        logging.debug("No output file given.")
    request_range = [10_000 * 10 ** (n - 1) for n in range(1, 5)]
    percentiles = const.PERCENTILES
    sla = 99
    logging.info(f"Using SLA of {sla} to calculate utilization.")
    results: list[tuple[int, list[int]]] = []
    for requests in request_range:
        params = SimulationParameters(request_duration_ms=10,
                                      requests_per_day=requests)
        result = monte_carlo.simulate(params)
        results.append((requests, result))
        utilization = monte_carlo.calculate_utilization(
            percentiles, result, sla)
        print_result(utilization[1], requests, utilization[0])
