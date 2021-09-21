import unittest

import mooreoff.mooreoff
from math import log

from mooreoff.types import ModelParameters


def result_tuple(requests: int, max):
    return (requests, log(requests)/log(max)/3, requests**2/(2 * max**2))


class TestPlotting(unittest.TestCase):

    def test_simple_plot(self):
        # Given
        max: int = int(1e6)
        min: int = int(1e3)
        results = [result_tuple(reqs, max) for reqs in
                   range(min, max, min)]
        params = ModelParameters(100)

        # When
        plot = mooreoff.mooreoff.plot_results(results, params)

        # Then
        self.assertTrue(plot)  # Visually inspect.
        # plot.show()
