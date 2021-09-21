import unittest

from mooreoff.mooreoff import large_formatter


class TestMooreoff(unittest.TestCase):

    def test_large_formatter_hundreds(self):
        self.assertEqual("1", large_formatter(1.35, 10))
        self.assertEqual("14", large_formatter(14.3, 10))
        self.assertEqual("134", large_formatter(134.4, 10))

    def test_large_formatter_thousands(self):
        self.assertEqual("2k", large_formatter(1.6e3, 10))
        self.assertEqual("13k", large_formatter(1.344e4, 10))
        self.assertEqual("134k", large_formatter(1.344e5, 10))

    def test_large_formatter_millions(self):
        self.assertEqual("2M", large_formatter(1.5e6, 10))
        self.assertEqual("13M", large_formatter(1.344e7, 10))
        self.assertEqual("134M", large_formatter(1.344e8, 10))

    def test_large_formatter_billions(self):
        self.assertEqual("2B", large_formatter(1.5e9, 10))
        self.assertEqual("13B", large_formatter(1.344e10, 10))
        self.assertEqual("134B", large_formatter(1.344e11, 10))
        self.assertEqual("1,344B", large_formatter(1.344e12, 10))
