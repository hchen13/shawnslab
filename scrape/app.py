import os
import sys
from datetime import datetime
from time import sleep

from sqlalchemy.exc import OperationalError

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import scrape.core as core


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
                core.save(nv, Session)

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
    core.save(nv, Session)


if __name__ == '__main__':
    run_once()
