# import os
import sys
from datetime import datetime
from time import sleep

from sqlalchemy.exc import OperationalError

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import core


def is_every_n_minutes(n_minutes):
    fired = False

    def check(time):
        nonlocal fired
        if time.minute % n_minutes == 0 and not fired:
            fired = True
            return True
        elif time.minute % n_minutes != 0:
            fired = False
        return False
    return check


def main():
    try:
        Session = core.init_db()
    except OperationalError as e:
        print("数据库初始化失败: {}".format(e))
        print("程序即将终止")
        exit()

    frequency = is_every_n_minutes(5)

    while True:

        current = datetime.now()

        if frequency(current):
            nv = core.extract_data()
            if nv is not None:
                core.save(Session, nv)

        sys.stdout.flush()
        sleep(30)


def run_once():
    try:
        Session = core.init_db()
    except OperationalError as e:
        print("数据库初始化失败: {}".format(e))
        print("程序即将终止")
        exit()

    nv = core.extract_data()
    core.save(Session, nv)


def scan():
    try:
        Session = core.init_db()
    except OperationalError as e:
        print("数据库初始化失败: {}".format(e))
        print("程序即将终止")
        exit()

    data = core.scan()
    for i in data:
        value, date_str = i['value'], i['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        core.save(Session, value, date)


if __name__ == '__main__':
    scan()
    # run_once()
