from random import randrange
from datetime import datetime, timedelta


date = datetime(2019, 12, 19, 8, 0, 0)


def show_date():
    global date
    return date.strftime('%c')


def advance_date(minutes=10):
    global date
    date += timedelta(minutes=minutes)


def show_queue(num=None):
    return harmonogram['q'][:num]


def check_is_absance(p_indx):
    global date

    if harmonogram[p_indx]['end'] < date:
        return True
    else:
        return False


def log_absance(p_indx):
    # TODO list of absences(dates) instead of absences number
    harmonogram[p_indx]['absences'] += 1
    c_pos = harmonogram['q'].index(p_indx)

    if harmonogram[p_indx]['absences'] == 1:
        try:
            harmonogram['q'].remove(p_indx)
            harmonogram['q'].insert(c_pos + 2, p_indx)
        except IndexError:
            harmonogram['q'].append(
                harmonogram['q'].pop(harmonogram['q'][p_indx]))

    if harmonogram[p_indx]['absences'] == 2:
        try:
            harmonogram['q'].remove(p_indx)
            harmonogram['q'].insert(c_pos+6, p_indx)
        except IndexError:
            harmonogram['q'].append(
                harmonogram['q'].pop(harmonogram['q'][p_indx]))

    if harmonogram[p_indx]['absences'] >= 3:
        harmonogram['q'].remove(p_indx)


def visit(p_indx):
    c_pos = harmonogram['q'].index(p_indx)

    for p in harmonogram['q'][:c_pos]:
        if check_is_absance(p):
            log_absance(p)

    global date
    advance_date(randrange(5, 25))
    harmonogram['q'].remove(p_indx)




harmonogram = {
    'q': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    1: {'name': 'pat1', 'start': datetime(2019, 12, 19, 8, 0, 0), 'end': datetime(2019, 12, 19, 8, 10, 0), 'absences': 0},
    2: {'name': 'pat2', 'start': datetime(2019, 12, 19, 8, 10, 0), 'end': datetime(2019, 12, 19, 8, 20, 0), 'absences': 0},
    3: {'name': 'pat3', 'start': datetime(2019, 12, 19, 8, 20, 0), 'end': datetime(2019, 12, 19, 8, 40, 0), 'absences': 0},
    4: {'name': 'pat4', 'start': datetime(2019, 12, 19, 8, 40, 0), 'end': datetime(2019, 12, 19, 8, 50, 0), 'absences': 0},
    5: {'name': 'pat5', 'start': datetime(2019, 12, 19, 8, 50, 0), 'end': datetime(2019, 12, 19, 9, 20, 0), 'absences': 0},
    6: {'name': 'pat6', 'start': datetime(2019, 12, 19, 9, 20, 0), 'end': datetime(2019, 12, 19, 9, 30, 0), 'absences': 0},
    7: {'name': 'pat7', 'start': datetime(2019, 12, 19, 9, 30, 0), 'end': datetime(2019, 12, 19, 9, 50, 0), 'absences': 0},
    8: {'name': 'pat8', 'start': datetime(2019, 12, 19, 9, 50, 0), 'end': datetime(2019, 12, 19, 10, 0, 0), 'absences': 0},
    9: {'name': 'pat9', 'start': datetime(2019, 12, 19, 10, 0, 0), 'end': datetime(2019, 12, 19, 10, 20, 0), 'absences': 0},
}