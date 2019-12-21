from datetime import datetime, timedelta
from random import randrange


class FakeDatetime:
    def __init__(self):
        self.now = datetime(2019, 12, 19, 8, 0, 0)

    def add_minutes(self, minutes=10):
        """
        helper function; advance fake datetime object for a certain
        amount of minutes (10 minutes by default)
        """
        self.now += timedelta(minutes = minutes)

    def show_date(self):
        """
        returns string representation of datetime object
        """
        return self.now.strftime('%c')


class DayVisitPlan:
    def __init__(self, d):
        self.visits = d
        self.queue = [p for p in d.keys()]

    def show_queue(self, num=None):
        """
        returns list representation of queue,
        optional argument (n) can be used to result slice: 1-st, 2-nd, .., n-th
        """
        return self.queue[:num]

    def check_is_absence(self, p):
        """
        returns True when specified patient visit time has passed
        """
        if self.visits[p]['end'] < date.now:
            return True
        else:
            return False

    def log_absence(self, p):
        """
        for the queue example: [p1, p2, p3, p4, ...]
        p1 patient's absence occurs when a p2 patient goes to the
        doctor's office and the time of p1 patient visit has passed

        the first and second absence results in the loss of position
        in the queue, the third causes removal from the queue
        """
        # TODO data validation
        self.visits[p]['absences'].append(date.now)
        c_pos = self.queue.index(p)

        if len(self.visits[p]['absences']) == 1:
            self.queue.remove(p)
            self.queue.insert(c_pos + 2, p)

        if len(self.visits[p]['absences']) == 2:
            self.queue.remove(p)
            self.queue.insert(c_pos + 4, p)

        if len(self.visits[p]['absences']) >= 3:
            self.queue.remove(p)

    def show_absences(self, p):
        """returns string representation of absences list"""
        return ', '.join(
            [a.strftime('%H:%M') for a in self.visits[p]['absences']])

    def visit(self, p):
        """
        removes from queue patient when doctor's office visit is done

        check for absence occurs
        when there are patients in queue before current patient
        """
        # TODO input validation

        c_pos = self.queue.index(p)
        for patient in self.queue[:c_pos]:
            if self.check_is_absence(patient):
                self.log_absence(patient)

        # time passing simulation
        date.add_minutes(randrange(5, 25))

        self.queue.remove(p)


# fake data about planned patients visits(will be changed by database query)
fake_data = {
    1: {'name': 'pat1', 'start': datetime(2019, 12, 19, 8, 0, 0),
        'end': datetime(2019, 12, 19, 8, 10, 0), 'absences': []},
    2: {'name': 'pat2', 'start': datetime(2019, 12, 19, 8, 10, 0),
        'end': datetime(2019, 12, 19, 8, 20, 0), 'absences': []},
    3: {'name': 'pat3', 'start': datetime(2019, 12, 19, 8, 20, 0),
        'end': datetime(2019, 12, 19, 8, 40, 0), 'absences': []},
    4: {'name': 'pat4', 'start': datetime(2019, 12, 19, 8, 40, 0),
        'end': datetime(2019, 12, 19, 8, 50, 0), 'absences': []},
    5: {'name': 'pat5', 'start': datetime(2019, 12, 19, 8, 50, 0),
        'end': datetime(2019, 12, 19, 9, 20, 0), 'absences': []},
    6: {'name': 'pat6', 'start': datetime(2019, 12, 19, 9, 20, 0),
        'end': datetime(2019, 12, 19, 9, 30, 0), 'absences': []},
    7: {'name': 'pat7', 'start': datetime(2019, 12, 19, 9, 30, 0),
        'end': datetime(2019, 12, 19, 9, 50, 0), 'absences': []},
    8: {'name': 'pat8', 'start': datetime(2019, 12, 19, 9, 50, 0),
        'end': datetime(2019, 12, 19, 10, 0, 0), 'absences': []},
    9: {'name': 'pat9', 'start': datetime(2019, 12, 19, 10, 0, 0),
        'end': datetime(2019, 12, 19, 10, 20, 0), 'absences': []},
}
# fake datetime object; eventually will be changed by datetime.now()
date = FakeDatetime()
day_plan = DayVisitPlan(fake_data)



