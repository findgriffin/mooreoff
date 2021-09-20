#! /usr/bin/env python3
import cProfile  # Replace with 'profile' if 'cProfile' does not work.
import logging
import pstats

from mooreoff import mooreoff
import sys

if __name__ == "__main__":
    args = mooreoff.setup(sys.argv[1:])
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s: %(message)s")
        logging.info("Verbose logging enabled.")
    else:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
    if args.profile:
        logging.info("Running with profiler.")
        with cProfile.Profile() as profiler:
            mooreoff.run(args.output)
        stats = pstats.Stats(profiler).strip_dirs()
        stats.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)
    else:
        mooreoff.run(args.output)
