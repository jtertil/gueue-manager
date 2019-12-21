import unittest
from datetime import datetime
from unittest.mock import patch

from qman import FakeDatetime, DayVisitPlan, fake_data


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
    def setUp(self) -> None:
        self.t_p_obj = DayVisitPlan(fake_data)
        self.t_queue = [p for p in fake_data.keys()]

    def test_output_type_is_list(self):
        self.assertIsInstance(self.t_p_obj.show_queue(), list)

    def test_without_argument(self):
        self.assertEqual(self.t_p_obj.show_queue(), self.t_queue)

    def test_with_argument(self):
        self.assertEqual(self.t_p_obj.show_queue(1), self.t_queue[:1])


class CheckAbsence(unittest.TestCase):
    def setUp(self) -> None:
        self.t_t_obj = FakeDatetime()
        self.t_p_obj = DayVisitPlan(fake_data)
        self.t_queue = [p for p in fake_data.keys()]

    def test_raise_KeyError(self):
        self.p_in_queue = len(self.t_queue)
        self.assertRaises(KeyError,
                          self.t_p_obj.check_is_absence, self.p_in_queue + 1)

    @patch('qman.date.now', datetime(2019, 12, 19, 8, 10))
    def test_return_false_when_no_absence(self):
        self.assertFalse(self.t_p_obj.check_is_absence(1))

    @patch('qman.date.now', datetime(2019, 12, 19, 8, 11))
    def test_return_true_when_absence(self):
        self.assertTrue(self.t_p_obj.check_is_absence(1))


class AbsenceLog(unittest.TestCase):

    def setUp(self) -> None:
        self.t_p_obj = DayVisitPlan(fake_data)

    def tearDown(self) -> None:
        for patient in self.t_p_obj.visits:
            self.t_p_obj.visits[patient]['absences'] = []

        self.t_p_obj.queue.sort()

    def test_all_patients_zero_absences_at_start(self):
        res = True
        for patient in self.t_p_obj.visits:
            if self.t_p_obj.visits[patient]['absences']:
                res = False
        self.assertTrue(res)

    def test_patient_with_absence_lost_position(self):
        b_position = self.t_p_obj.queue.index(1)
        self.t_p_obj.log_absence(1)
        a_position = self.t_p_obj.queue.index(1)
        self.assertEqual(a_position, b_position + 2)

    def test_patient_with_two_absences_lost_position(self):
        self.t_p_obj.visits[1]['absences'] = [datetime(2019, 12, 19, 8, 10)]
        b_position = self.t_p_obj.queue.index(1)
        self.t_p_obj.log_absence(1)
        a_position = self.t_p_obj.queue.index(1)
        self.assertEqual(a_position, b_position + 4)

    def test_patient_with_three_absences_removed(self):
        self.t_p_obj.visits[1]['absences'] = [datetime(2019, 12, 19, 8, 10),
                                              datetime(2019, 12, 19, 8, 50)]
        self.t_p_obj.log_absence(1)
        self.assertFalse(1 in self.t_p_obj.queue)

    def test_move_patient_to_last_position(self):
        self.t_p_obj.log_absence(8)
        self.assertTrue(8 in self.t_p_obj.queue[-1:])


class ShowAbsences(unittest.TestCase):
    def setUp(self) -> None:
        self.t_p_obj = DayVisitPlan(fake_data)

    def test_empty_str_when_no_absences(self):
        self.assertEqual('', self.t_p_obj.show_absences(1))

    def test_valid_output(self):
        self.t_p_obj.visits[1]['absences'] = [
            datetime(2019, 12, 19, 8, 10),
            datetime(2019, 12, 19, 8, 30),
            datetime(2019, 12, 19, 10, 40)
        ]
        self.assertEqual('08:10, 08:30, 10:40', self.t_p_obj.show_absences(1))


class Visit(unittest.TestCase):

    def setUp(self) -> None:
        self.t_p_obj = DayVisitPlan(fake_data)

    def test_remove_patient_from_queue_after_visit(self):
        self.t_p_obj.visit(1)
        self.assertFalse(1 in self.t_p_obj.queue)

    def test_raise_ValueError(self):
        self.assertRaises(ValueError, self.t_p_obj.visit, 10)


if __name__ == '__main__':
    unittest.main()
