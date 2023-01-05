"""
скрипт анализирует mbox-файл полученный из экспорта почты с гугла
ищет письма от Убера за указанный год и суммирует стоимость поездок взятых из тела письма
"""

import mailbox
from datetime import datetime
from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default
from operator import attrgetter

from bs4 import BeautifulSoup
from tqdm import tqdm

from taxi_cost_by_year.json_files import PathLike, save_as_jsonfile, load_jsonfile
from taxi_cost_by_year.typings import RideDataUber as RideData, CustomJSONencoder, CustomJSONdecoder


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


def get_mail_content(message: EmailMessage) -> str:
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


def log_printer(rides_list: list[RideData]):
    """ Функция печати данных из итогового списка поездок
    :return:
    """
    for ride in rides_list:
        print(f"date:  : {ride.ride_dt.date()}, {ride.ride_dt.time()}, {ride.ride_week_day}\n"
              f"to:    : {ride.mail_to}\n"
              f"from   : {ride.mail_from}\n"
              f"subject: {ride.subject}\n"
              f"price  : {ride.ride_cost if ride.ride_cost else 'FAILED'}\n"
              f"km     : {ride.ride_distance if ride.ride_distance else 'FAILED'}\n"
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
        ride_cost=0,
        ride_distance=0
    )

    return result


def parse_ride_data(message: str) -> tuple:
    """ Парсит стоимость поездки из html-тела письма и возвращает кортеж рассятояни и стоимости поездки
    :param message:
    :return: tuple (distance, price)
    """
    # в 21 году километров не было !!!
    # в 22 году иногда приходили глючные письма без данных, поэтому если нету, тогда 0

    soup = BeautifulSoup(message, 'html.parser')

    price_raw = soup.find('td', class_='check__value check__value_type_price').text.strip()
    if price_raw:
        price = float(price_raw.replace('\u202f', ' ').replace('\u2006', ' ').replace(',', '.').split()[0])
    else:
        price = 0

    distance_desc_td = [td for td in soup.find_all('td') if td.text.strip() == 'Время в пути']
    if distance_desc_td:
        distance_raw = distance_desc_td[0].find_next('td').find('p', class_='hint')
        if distance_raw is None:
            distance = 0
        else:
            distance_text = distance_raw.text.strip()  # '30,1 км'
            distance = float(distance_text.replace(',', '.').split(' ')[0])
    else:
        # когда не нашло ничего
        distance = 0

    return distance, price


def collect_rides(year: int, mbox_file: PathLike, print_log: bool = False) -> list[RideData]:
    """ Проходит по всем письмам в файле .mbox, находит письма от убера за нужный год,
    собирает их и сортирует их по дате

    :param year: год за который ищутся письма
    :param print_log: если True - печатает данные писем, если False - выводит строку прогресса
    :param mbox_file: путь до файла .mbox относительно файла скрипта
    :return: список с данными писем убера
    """
    mbox = mailbox.mbox(mbox_file, factory=BytesParser(policy=default).parse)

    result_data = []

    for message in tqdm(mbox, ncols=80, desc='Обработка писем'):
        message_data = get_data(message)
        if 'uber' in message_data.mail_from.lower() and message_data.ride_dt.year == year:
            content = get_mail_content(message)
            message_data.ride_distance, message_data.ride_cost = parse_ride_data(content)
            result_data.append(message_data)

    # сортирнём список поездок по дате
    result_data.sort(key=attrgetter('ride_dt'))

    if print_log:
        log_printer(result_data)

    return result_data


if __name__ == '__main__':
    year = 2022
    mbox_file = 'dont_vcs/inbox2023.mbox'

    print('Год : ', year)
    print(f"Загрузка файла {mbox_file} ...")

    rides = collect_rides(year, mbox_file=mbox_file, print_log=True)

    # # сохраним полученные данные
    # save_as_jsonfile(rides, f"_{year}.json", encoder=CustomJSONencoder)
    #
    # загрузим сохраненные данные
    # rides = load_jsonfile(f"_{year}.json", decoder=CustomJSONdecoder)

    all_km = all_cost = 0
    for ride in rides:
        all_km += ride.ride_distance
        all_cost += ride.ride_cost

    print('Игого деняк: ', all_cost)
    print('Игого км: ', all_km)
