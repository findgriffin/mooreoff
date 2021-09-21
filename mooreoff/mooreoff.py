from matplotlib.collections import EventCollection  # type: ignore
from typing import Optional
import argparse
import logging
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.ticker as mtick  # type: ignore

from mooreoff import constants as const
from mooreoff import monte_carlo
from mooreoff.types import SimulationParameters, ModelParameters


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


def large_formatter(x: float, pos) -> str:
    if abs(x) >= const.BILLION:
        return f"{x*1e-9:,.0f}B"
    elif abs(x) >= const.MILLION:
        return f"{x*1e-6:.0f}M"
    elif abs(x) >= const.THOUSAND:
        return f"{x*1e-3:1.0f}k"
    else:
        return f"{x:.0f}"


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


def plot_results(results: list[tuple[int, float, float]],
                 params: ModelParameters):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x_requests = [entry[0] for entry in results]
    y_util = [entry[1]*const.PERCENT for entry in results]
    y_fail = [entry[2]*const.PERCENT for entry in results]
    ax.plot(x_requests, y_util, color='tab:blue')
    ax.plot(x_requests, y_fail, color='tab:orange')
    x_events = EventCollection(x_requests, color='tab:blue', linelength=0.05)
    util_events = EventCollection(y_util, color='tab:blue', linelength=0.05)
    fail_events = EventCollection(y_fail, color='tab:orange', linelength=0.05)

    yticks = mtick.FormatStrFormatter('%.0f%%')
    ax.yaxis.set_major_formatter(yticks)
    ax.xaxis.set_major_formatter(large_formatter)

    ax.add_collection(x_events)
    ax.add_collection(util_events)
    ax.add_collection(fail_events)
    ax.set_ylim([0, const.PERCENT])
    ax.set_title(f"Utilization for {params}")
    plt.show()


def run(output: Optional[str] = None) -> None:
    if output:
        logging.debug(f"Output file: {output}.")
    else:
        logging.debug("No output file given.")
    model = ModelParameters(req_duration=100, threads=4, sla=200)
    capacity = calculate_daily_capacity(model.req_duration, model.threads)
    logging.info(f"Request duration of {model.req_duration}ms, "
                 f"and max_threads of {model.threads} gives a daily capacity "
                 f"of {capacity} requests.")
    num_runs = 10
    step = int(capacity/num_runs)
    request_range = [i for i in range(step, capacity, step)]
    logging.info(f"Running for {request_range}")
    logging.info(f"Max wait for SLA is {model.sla}ms.")
    results: list[tuple[int, float, float]] = []
    for requests in request_range:
        params = SimulationParameters(request_duration_ms=model.req_duration,
                                      requests_per_day=requests,
                                      threads=model.threads,
                                      max_wait=model.sla-model.req_duration)
        utilization_fraction, fail_fraction = monte_carlo.simulate(params)
        fail_percent = fail_fraction * const.PERCENT
        utilization_percent = utilization_fraction * const.PERCENT
        logging.info(f"For {requests} requests per day, got utilization of"
                     f" {utilization_percent:.1f}%, with {fail_percent:.1f}% "
                     "requests failing SLA.")
        results.append((requests, utilization_fraction, fail_fraction))
    plot_results(results, model)
