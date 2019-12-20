from random import randrange
from datetime import datetime, timedelta

# fake date object; eventually will be changed by datetime.now()
date = datetime(2019, 12, 19, 8, 0, 0)

# fake data about planned patients visits(will be changed by database query)
fake_data = {
    'q': [1, 2, 3, 4, 5, 6, 7, 8, 9],
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


def show_date():
    """
    returns string representation of fake / real datetime object
    """
    global date
    return date.strftime('%c')


def advance_date(minutes=10):
    """
    helper function; advance fake datetime object for a certain
    amount of minutes (10 minutes by default)
    """
    global date
    date += timedelta(minutes=minutes)


def show_queue(num=None):
    """
    returns string representation of queue,
    optional argument (n) can be used to result slice: 1-st, 2-nd, ..., n-th
    """
    # TODO data validation - IndexError, when num > len(fake_data['q'])
    return fake_data['q'][:num]


def check_is_absance(p_indx):
    """
    returns True when specified patient visit time has passed
    """
    # TODO data validation
    global date

    if fake_data[p_indx]['end'] < date:
        return True
    else:
        return False


def log_absance(p_indx):
    """
    for the queue example: [p1, p2, p3, p4, ...]
    p1 patient's absence occurs when a p2 patient goes to the doctor's office
    and the time of p1 patient visit has passed

    the first and second absence results in the loss of position in the queue,
    the third causes removal from the queue
    """
    # TODO data validation, list of absences(dates) instead of absences number
    fake_data[p_indx]['absences'] += 1
    c_pos = fake_data['q'].index(p_indx)

    if fake_data[p_indx]['absences'] == 1:
        try:
            fake_data['q'].remove(p_indx)
            fake_data['q'].insert(c_pos + 2, p_indx)
        except IndexError:
            fake_data['q'].append(
                fake_data['q'].pop(fake_data['q'][p_indx]))

    if fake_data[p_indx]['absences'] == 2:
        try:
            fake_data['q'].remove(p_indx)
            fake_data['q'].insert(c_pos + 6, p_indx)
        except IndexError:
            fake_data['q'].append(
                fake_data['q'].pop(fake_data['q'][p_indx]))

    if fake_data[p_indx]['absences'] >= 3:
        fake_data['q'].remove(p_indx)


def visit(p_indx):
    """
    removes from queue patient when doctor's office visit is done

    check for absence occurs
    when there are patients in queue before current patient
    """
    # TODO input validation

    c_pos = fake_data['q'].index(p_indx)
    for p in fake_data['q'][:c_pos]:
        if check_is_absance(p):
            log_absance(p)

    # simulating time passing
    global date
    advance_date(randrange(5, 25))

    fake_data['q'].remove(p_indx)




