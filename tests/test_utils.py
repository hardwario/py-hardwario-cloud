import unittest
from hardwario.cloud import utils


class TestUtils(unittest.TestCase):

    def test_get_timestamp_datetime(self):
        self.assertEqual(utils.get_timestamp('2022-05-27 00:00:00'), 1653602400000)

    def test_get_timestamp_datetime_1(self):
        self.assertEqual(utils.get_timestamp('2022-05-27 12:31:22'), 1653647482000)

    def test_get_timestamp_date(self):
        self.assertEqual(utils.get_timestamp('2022-05-27'), 1653602400000)

    def test_get_timestamp_z(self):
        self.assertEqual(utils.get_timestamp('2022-05-27 00:00:00+2'), 1653606000000)

    def test_get_timestamp_iso(self):
        self.assertEqual(utils.get_timestamp('2022-05-27T12:31:22'), 1653647482000)
