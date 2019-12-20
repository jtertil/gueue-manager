import unittest
from datetime import datetime
from unittest.mock import patch

from qman import FakeDatetime, fake_data, show_queue, check_is_absance


class FakeDateTests(unittest.TestCase):

    def setUp(self) -> None:
        self.t_t_obj = FakeDatetime()
        self.s_date = self.t_t_obj.show_date()

    def test_fake_date_initialize(self):
        self.assertEqual(self.t_t_obj.now, datetime(2019, 12, 19, 8, 0))

    def test_show_date_output_string(self):
        self.assertIsInstance(self.t_t_obj.show_date(), str)

    def test_show_date_output_proper_time(self):
        self.assertEqual(self.t_t_obj.show_date(), 'Thu Dec 19 08:00:00 2019')

    def tearDown(self):
        pass


class FakeDateManipulation(unittest.TestCase):

    def setUp(self) -> None:
        self.t_t_obj = FakeDatetime()

    def test_advance_time_default(self):
        self.t_t_obj.add_minutes()
        self.assertEqual(self.t_t_obj.now, datetime(2019, 12, 19, 8, 10))

    def test_advance_time_custom(self):
        self.t_t_obj.add_minutes(45)
        self.assertEqual(self.t_t_obj.now, datetime(2019, 12, 19, 8, 45))


class ShowQueue(unittest.TestCase):

    def test_without_argument(self):
        self.assertEqual(show_queue(), fake_data['q'])

    def test_with_argument(self):
        self.assertEqual(show_queue(1), fake_data['q'][:1])


class CheckAbsance(unittest.TestCase):
    def setUp(self) -> None:
        self.t_t_obj = FakeDatetime()

    @patch('qman.f_date.now', datetime(2019, 12, 19, 8, 10))
    def test_return_false_when_no_absance(self):
        self.assertFalse(check_is_absance(1))

    @patch('qman.f_date.now', datetime(2019, 12, 19, 8, 11))
    def test_return_true_when_absance(self):
        self.assertTrue(check_is_absance(1))


if __name__ == '__main__':
    unittest.main()
