"""
скрипт анализирует mbox-файл полученный из экспорта почты с гугла
ищет письма от Убера за указанный год и суммирует стоимость поездок взятых из тела письма
"""

import mailbox
from datetime import datetime
from email.parser import BytesParser
from email.policy import default
from operator import attrgetter

from bs4 import BeautifulSoup
from tqdm import tqdm

from uber_cost_by_year.json_files import PathLike, save_as_jsonfile, load_jsonfile
from uber_cost_by_year.typings import RideData


def str2datetime(time_string: str) -> datetime:
    """ Преобразует строку в формат datetime. Если не удается вызывает исключение ValueError
    :param time_string:
    :return: datetime
    """
    # форматы используемые в письмах
    time_formats = ['%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %z (%Z)']
    for fmt in time_formats:
        try:
            return datetime.strptime(time_string, fmt)
        except ValueError:
            continue
    raise ValueError(f"Неведомый формат времени: {time_string}")


def get_mail_content(message):
    """
    возвращает как текст содержимое письма
    """
    if message.is_multipart():
        contents = []
        for part in message.walk():
            maintype = part.get_content_maintype()
            if maintype == 'multipart' or maintype != 'text':
                # Reject containers and non-text types
                continue
            contents.append(part.get_content())
        content = '\n\n'.join(contents)
    else:
        content = message.get_content()
    return content


def log_printer(rides: list[RideData]):
    """ Функция печати данных из итогового списка поездок
    :return:
    """
    for ride in rides:
        print(f"date:  : {ride.ride_dt.date()}, {ride.ride_dt.time()}, {ride.ride_week_day}\n"
              f"to:    : {ride.mail_to}\n"
              f"from   : {ride.mail_from}\n"
              f"subject: {ride.subject}\n"
              f"price  : {ride.ride_cost if ride.ride_cost != 0 else 'FAILED'}\n"
              f"{'-' * 60}")


def get_data(message: mailbox.Message) -> RideData:
    """ Достает из письма необходимые данные и возвращает датакласс с ними
    :param message:
    :return:
    """
    mail_date = message.get('date')
    dt = str2datetime(mail_date)

    result = RideData(
        mail_to=message.get('to'),
        subject=message.get('subject', '<Unknown>'),
        mail_from=message.get('from'),
        ride_dt=dt,
        ride_week_day=dt.strftime("%A"),
        ride_cost=0
    )

    return result


def parse_ride_cost(message: str) -> float:
    """ Парсит стоимость поездки из html-тела письма
    :param message:
    :return: float Стоимость поездки
    """
    soup = BeautifulSoup(message, 'lxml')
    price_raw = soup.find('td', class_='check__value check__value_type_price').text.strip()
    if price_raw:
        price = price_raw.replace('\u202f', ' ').replace('\u2006', ' ').replace(',', '.').split()[0]
        return float(price)
    # в 22 году иногда приходили глючные письма
    return .0


def collect_rides(year: int, mbox_path: PathLike, print_log: bool = False) -> list[RideData]:
    """ Проходит по всем письмам в файле .mbox, находит письма от убера за нужный год и сортирует их по дате

    :param year: год за который ищутся письма
    :param print_log: если True - печатает данные писем, если False - выводит строку прогресса
    :param mbox_path: путь до файла .mbox относительно файла скрипта
    :return: float, сумма денег
    """
    mbox = mailbox.mbox(mbox_path, factory=BytesParser(policy=default).parse)
    result_cost = 0
    result_data = []

    for message in tqdm(mbox, ncols=80):
        message_data = get_data(message)
        if 'uber' in message_data.mail_from.lower() and message_data.ride_dt.year == year:
            content = get_mail_content(message)
            message_data.ride_cost = parse_ride_cost(content)
            result_cost += message_data.ride_cost
            result_data.append(message_data)

    # сортирнём список поездок по дате
    result_data.sort(key=attrgetter('ride_dt'))

    if print_log:
        log_printer(result_data)

    return result_data


if __name__ == '__main__':
    year = 2022
    mbox_file = 'dont_vcs/inbox2022.mbox'

    print('Год : ', year)
    print('Файл: ', mbox_file)

    rides = collect_rides(year, mbox_path=mbox_file, print_log=False)

    # # сохраним полученные данные
    # save_as_jsonfile(rides, f"_{year}.json")
    #
    # # загрузим сохраненные данные
    # rides = load_jsonfile(f"_{year}.json")

    print('Игого = ', sum(ride.ride_cost for ride in rides))
