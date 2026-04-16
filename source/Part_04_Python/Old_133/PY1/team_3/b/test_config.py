import unittest

from generic_grader.utils.options import Options

DUE_DATE = "2025-09-12 10:00 PM"

file_set_up_options = Options()


class TestNone(unittest.TestCase):
    def test_none(self):
        """This assignment will be manually graded."""
        self.assertTrue(True)