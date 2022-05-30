import socket
import time
import urllib.request
from enum import Enum
from random import randint

import click

from easy_logger import easy_logger as logger
from now_time import get_now_time


class ConnectionResult(Enum):
    """ request results """
    OK = True
    FAILED = False


def check_connection(host: str = 'https://google.com') -> ConnectionResult:
    """ Try request <host> site. By default - google.com

    :param host: sitename for requests
    :return: ConnectionResult.OK- if successfull, else - ConnectionResult.FAILED
    """
    try:
        urllib.request.urlopen(host, timeout=3)
        return ConnectionResult.OK
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout):
        if __name__ == '__main__':
            # rerise error if runned as main, else return with error flag
            raise
    return ConnectionResult.FAILED


#################################################
#               internal functions              #
#################################################


def _cycle(host: str, last: bool = False) -> None:
    """ Main check function """
    timeout = randint(1, 10)
    try:
        result = check_connection(host)
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout) as e:
        result = ConnectionResult.FAILED
        logger.write(f"{get_now_time()} - Error with {e}")

    check_str = f"Connection - {result.name} (Errors: {logger.lines_written}). {'' if last else f'Wait {timeout} s'}"
    print(f"{get_now_time()} - {check_str}")
    print(f"{get_now_time()} Done") if last else time.sleep(timeout)


@click.command()
@click.option('-i', '--infinity', is_flag=True,
              help='Infinity loop', show_default=True)
@click.option('-r', '--repeats', default=3, help='Number repeats', show_default=True)
@click.option('-h', '--host', default='https://google.com',
              help='The site to which requests will be sent, including the protocol (http/https)', show_default=True)
@click.option('-l', '--logname', default='check.log',
              help='Log-filename, in same directory (!)', show_default=True)
def _main(infinity: bool, repeats: int, host: str, logname: str) -> None:
    """ Main function with commandline arguments processing """
    logger.set_new_name_and_create(logname)
    print(f"Check connection with {host}. With random (1-10 s) timeouts after check.")
    print(f"Log-file: {logger.log_file_with_path}")

    try:
        if infinity:
            while True:
                _cycle(host)
        else:
            for counter in range(1, repeats + 1):
                _cycle(host, counter == repeats)
    except (KeyboardInterrupt, SystemExit):
        print(f"{get_now_time()} ❗ Interrupted")


if __name__ == '__main__':
    _main()
