import os
import sys


def restarter():
    """ Перезапуск скрипта. Работает под линукс """
    os.execv(sys.executable, [sys.executable] + sys.argv)


if __name__ == '__main__':
    pass
