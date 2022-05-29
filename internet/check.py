import socket
import time
import urllib.request
from enum import Enum
from random import randint

import click

from easy_logger import easy_logger as logger
from now_time import get_now_time


class ConnectionResult(Enum):
    """ Результат опроса хоста """
    OK = True
    FAILED = False


def check_connection(host: str = 'https://google.com') -> ConnectionResult:
    """ Попытка подключения к указанному хосту. По умолчанию: google.com

    :param host: хост к которому будем пробовать подключится
    :return: ConnectionResult.OK- если удачно, ConnectionResult.FAILED - если нет
    """
    try:
        urllib.request.urlopen(host, timeout=3)
        return ConnectionResult.OK
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout):
        if __name__ == '__main__':
            # если запущен этот файл то рерайзим ошибку дальше, если импортирован - делаем return
            raise
    return ConnectionResult.FAILED


#################################################
#               внутренние функции              #
#################################################


def _cycle(host: str, last: bool = False) -> None:
    """ Основная функция проверки соединения """
    timeout = randint(1, 10)
    try:
        result = check_connection(host)
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout) as e:
        result = ConnectionResult.FAILED
        logger.write(f"{get_now_time()} - Error with {e}")

    check_str = f"Подключение - {result.name} (Ошибок: {logger.lines_written}). {'' if last else f'Ждём {timeout} c'}"
    print(f"{get_now_time()} - {check_str}")
    print(f"{get_now_time()} Завершено") if last else time.sleep(timeout)


@click.command()
@click.option('-i', '--infinity', is_flag=True,
              help='Если указан, то будет бесконечный цикл запросов', show_default=True)
@click.option('-r', '--repeats', default=3, help='Количество повторений запросов', show_default=True)
@click.option('-h', '--host', default='https://google.com',
              help='Сайт к которому будут направлятся запросы, включая протокол (http/https)', show_default=True)
@click.option('-l', '--logname', default='check.log',
              help='Имя файла с ошибками, в той же директории (!)', show_default=True)
def _main(infinity: bool, repeats: int, host: str, logname: str) -> None:
    """ Главная функция программы, с обработкой параметров коммандной строки """
    logger.set_new_name_and_create(logname)
    print(f"Проверка соединения с {host}. Со случайными (1-10 с) таймаутами после проверки.")
    print(f"Файл с логами: {logger.log_file_with_path}")

    try:
        if infinity:
            while True:
                _cycle(host)
        else:
            for counter in range(1, repeats + 1):
                _cycle(host, counter == repeats)
    except (KeyboardInterrupt, SystemExit):
        print(f"{get_now_time()} ❗ Прервано")


if __name__ == '__main__':
    _main()
