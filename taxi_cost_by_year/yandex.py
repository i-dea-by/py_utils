"""
скрипт анализирует mbox-файл полученный из экспорта почты с гугла
ищет письма от Убера за указанный год и суммирует стоимость поездок взятых из тела письма

Как получить файл .mbox:
    - https://takeout.google.com/settings/takeout
    - Выбрать только «Почта», можно уточнить что именно из ящика экспортировать нажав кнопку «Выбраны все данные почты»
    - Потом Далее, выбрать когда и как получать экспорт и нажать «Создать экспорт»

История изменений:
    23.01.01    - Яндекс.Такси в html-е оказывается даёт json-строку с данными поездки
    23.01.01    - с 23 года перешел на Яндекс.Такси
    22.12.30    - в 22 году  декабре, примерно, стали приходить глючные письма без данных, поэтому если нету, тогда 0
                - в 21 году километров не было !!!

"""
import json
import mailbox
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default
from operator import attrgetter

from bs4 import BeautifulSoup
from tqdm import tqdm

from taxi_cost_by_year.json_files import PathLike, save_as_jsonfile, load_jsonfile
from taxi_cost_by_year.typings import RideData, CustomJSONencoder, CustomJSONdecoder


YANDEX_MAIL = 'taxi.yandex.com'


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


def get_mail_html_content(message: EmailMessage) -> str:
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
        print(f"Дата: {ride.ride_dt.date()}, {ride.ride_dt.time()}\n"
              f"От: {ride.ride_from}\n"
              f"До: {ride.ride_to}\n"
              f"Длительность: {ride.duration}\n"
              f"Расстояние: {ride.ride_distance}\n"
              f"Цена: {ride.ride_cost}\n"
              f"{'-' * 60}")


def try_timedelta(duration: str) -> timedelta | None:
    """ Переводит длительность поездки из строки в timedelta, или None если не удалось
    :param duration: Длительность поездки, должно быть вида '0:8:25'
    :return: timedelta длительности поездки или None если не получилось
    """
    try:
        hours, minutes, seconds = duration.split(":")
        return timedelta(
            hours=float(hours),
            minutes=float(minutes),
            seconds=float(seconds)
        )
    except ValueError:
        # return timedelta(0)
        return None


def try_datetime(date: str) -> datetime | None:
    """ Переводит дату поездки в datetime, или None если не удалось
    :param date: Дата поездки, должно быть вида '1.1.2023 2:15:8'
    :return: datetime поездки или None если не получилось
    """
    try:
        result = datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        return result
    except ValueError:
        return None


def extract_ride_data(html: str) -> RideData:
    """ Достаёт из письма json-строку с данными поездки
    Пример строки:
    {
        "arr": "город, улица, дом",
        "cost": 12.7,
        "dep": "город, улица, дом",
        "car": "Kia Rio",
        "time_dep": "0.0.0 2:19:53",
        "city_dep": "Минск",
        "trip_class": "econom",
        "duration": "0:8:25",
        "order_date": "1.1.2023 2:15:8",
        "time_arr": "0.0.0 2:28:18",
        "city_dep_geoid": 157,
        "dist": 3.194
    }

    :param html: содержимое письма в формате html
    :return: датаклас с данными поездки
    """
    soup = BeautifulSoup(html, 'lxml')
    json_str = soup.find('script', {'type': 'application/ld+json'}).text.strip()
    ride_json = json.loads(json_str)['taxi'][0]

    result = RideData(
        ride_from=ride_json.get('dep'),
        ride_to=ride_json.get('arr'),
        duration=try_timedelta(ride_json.get('duration')),
        ride_dt=try_datetime(ride_json.get('order_date')),
        ride_cost=ride_json.get('cost'),
        ride_distance=ride_json.get('dist')
    )

    return result


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
        mail_from = message.get('from').lower()
        mail_dt = str2datetime(message.get('date'))
        if YANDEX_MAIL in mail_from and mail_dt.year == year:
            content = get_mail_html_content(message)
            ride_data = extract_ride_data(content)
            result_data.append(ride_data)

    # сортирнём список поездок по дате
    result_data.sort(key=attrgetter('ride_dt'))

    if print_log:
        log_printer(result_data)

    return result_data


if __name__ == '__main__':
    year = 2023
    mbox_file = 'dont_vcs/inbox2023.mbox'

    print('Год : ', year)
    print(f"Загрузка файла {mbox_file} ...")

    rides = collect_rides(year, mbox_file=mbox_file, print_log=False)

    # # сохраним полученные данные
    # save_as_jsonfile(rides, f"_{year}.json", encoder=CustomJSONencoder)
    #
    # # загрузим сохраненные данные
    # rides = load_jsonfile(f"_{year}.json", decoder=CustomJSONdecoder)

    all_km = all_cost = 0
    for ride in rides:
        all_km += ride.ride_distance
        all_cost += ride.ride_cost

    print('Игого деняк: ', all_cost)
    print('Игого км: ', all_km)
