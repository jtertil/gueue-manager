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


# fake data about planned patients visits(will be changed by database query)
fake_data = {
    1: {'name': 'pat1', 'start': datetime(2019, 12, 19, 8, 0, 0),
        'end': datetime(2019, 12, 19, 8, 10, 0), 'absences': 0},
    2: {'name': 'pat2', 'start': datetime(2019, 12, 19, 8, 10, 0),
        'end': datetime(2019, 12, 19, 8, 20, 0), 'absences': 0},
    3: {'name': 'pat3', 'start': datetime(2019, 12, 19, 8, 20, 0),
        'end': datetime(2019, 12, 19, 8, 40, 0), 'absences': 0},
    4: {'name': 'pat4', 'start': datetime(2019, 12, 19, 8, 40, 0),
        'end': datetime(2019, 12, 19, 8, 50, 0), 'absences': 0},
    5: {'name': 'pat5', 'start': datetime(2019, 12, 19, 8, 50, 0),
        'end': datetime(2019, 12, 19, 9, 20, 0), 'absences': 0},
    6: {'name': 'pat6', 'start': datetime(2019, 12, 19, 9, 20, 0),
        'end': datetime(2019, 12, 19, 9, 30, 0), 'absences': 0},
    7: {'name': 'pat7', 'start': datetime(2019, 12, 19, 9, 30, 0),
        'end': datetime(2019, 12, 19, 9, 50, 0), 'absences': 0},
    8: {'name': 'pat8', 'start': datetime(2019, 12, 19, 9, 50, 0),
        'end': datetime(2019, 12, 19, 10, 0, 0), 'absences': 0},
    9: {'name': 'pat9', 'start': datetime(2019, 12, 19, 10, 0, 0),
        'end': datetime(2019, 12, 19, 10, 20, 0), 'absences': 0},
}

# fake datetime object; eventually will be changed by datetime.now()
fake_date = FakeDatetime()

fake_day_plan = DayVisitPlan(fake_data)


def show_queue(num=None):
    """
    returns string representation of queue,
    optional argument (n) can be used to result slice: 1-st, 2-nd, ..., n-th
    """
    return fake_day_plan.queue[:num]


def check_is_absance(p):
    """
    returns True when specified patient visit time has passed
    """

    if fake_day_plan.visits[p]['end'] < fake_date.now:
        return True
    else:
        return False


def log_absance(p):
    """
    for the queue example: [p1, p2, p3, p4, ...]
    p1 patient's absence occurs when a p2 patient goes to the doctor's office
    and the time of p1 patient visit has passed

    the first and second absence results in the loss of position in the queue,
    the third causes removal from the queue
    """
    # TODO data validation, list of absences(dates) instead of absences number
    fake_day_plan.visits[p]['absences'] += 1
    c_pos = fake_day_plan.queue.index(p)

    if fake_day_plan.visits[p]['absences'] == 1:
        try:
            fake_day_plan.queue.remove(p)
            fake_day_plan.queue.insert(c_pos + 2, p)
        except IndexError:
            fake_day_plan.queue.append(
                fake_day_plan.queue.pop(fake_day_plan.queue[p]))

    if fake_day_plan.visits[p]['absences'] == 2:
        try:
            fake_day_plan.queue.remove(p)
            fake_day_plan.queue.insert(c_pos + 6, p)
        except IndexError:
            fake_day_plan.queue.append(
                fake_day_plan.queue.pop(fake_day_plan.queue[p]))

    if fake_day_plan.visits[p]['absences'] >= 3:
        fake_day_plan.queue.remove(p)


def visit(p):
    """
    removes from queue patient when doctor's office visit is done

    check for absence occurs
    when there are patients in queue before current patient
    """
    # TODO input validation

    c_pos = fake_day_plan.queue.index(p)
    for patient in fake_day_plan.queue[:c_pos]:
        if check_is_absance(patient):
            log_absance(patient)

    # simulating time passing
    fake_date.add_minutes(randrange(5, 25))

    fake_day_plan.queue.remove(p)
