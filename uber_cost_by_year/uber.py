"""
скрипт анализирует mbox-файл полученный из экспорта почты с гугла
ищет письма от Убера за указанный год и суммирует стоимость поездок взятых из тела письма
"""

import mailbox
from datetime import datetime
from email.parser import BytesParser
from email.policy import default

from bs4 import BeautifulSoup
from tqdm import tqdm


def str2datetime(time_string: str) -> datetime:
    """ Преобразует строку в формат datetime. Если не удается вызывает исключение ValueError
    :param time_string:
    :return: datetime
    """
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


def log_printer(message, dt, price):
    """ Функция печати данных из письма
    :param message:
    :param dt:
    :param price: цена поездки
    :return:
    """
    mail_to = message.get('to')
    subject = message.get('subject', '<Unknown>')
    mail_from = message.get('from')

    date = dt.date().isoformat()
    time = dt.time().isoformat()
    week_day = dt.strftime("%A")

    print(f"date:  : {date}, {time}, {week_day}\n"
          f"to:    : {mail_to}\n"
          f"from   : {mail_from}\n"
          f"subject: {subject}\n"
          f"price  : {price}\n"
          f"{'-' * 60}")


def get_price(message):
    soup = BeautifulSoup(message, 'lxml')
    price_raw = soup.find('td', class_='check__value check__value_type_price').text.strip()
    price = price_raw.replace('\u202f', ' ').replace('\u2006', ' ').replace(',', '.').split()[0]
    return price


def get_uber_summ_by_year(year: int = 2021, print_log: bool = False, mbox_path: str = '') -> float:
    """ Проходит по всем письмам в файле .mbox находит письма от убера

    :param year: год за который ищутся письма, по умолчанию равно 2021
    :param print_log: если True - печатает данные писем, если False - выводит строку прогресса
    :param mbox_path: путь до файла .mbox относительно файла скрипта
    :return: float, сумма денег
    """
    mbox = mailbox.mbox(mbox_path, factory=BytesParser(policy=default).parse)

    result = 0

    loop_source = mbox if print_log else tqdm(mbox, ncols=80)
    for message in loop_source:
        mail_date = message.get('date')
        mail_from = message.get('from')
        dt = str2datetime(mail_date)

        if 'Uber' in mail_from and dt.year == year:
            content = get_mail_content(message)
            price = get_price(content)
            result += float(price)

            if print_log:
                log_printer(message, dt, price)

    return result


if __name__ == '__main__':
    year_sum = get_uber_summ_by_year(2021, print_log=True, mbox_path='dont_vcs/inbox.mbox')
    print('Игого = ', year_sum)
