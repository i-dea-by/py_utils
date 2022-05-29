"""
скрипт анализирует mbox-файл полученный из экспорта почты с гугла
ищет письма от Убера за указанный год и суммирует стоимость поездок взятых из тела письма
"""

import mailbox
import sys
from datetime import datetime
from email.parser import BytesParser
from email.policy import default

from bs4 import BeautifulSoup
from tqdm import tqdm

timeformat = '%a, %d %b %Y %H:%M:%S %z'
timeformatGMT = '%a, %d %b %Y %H:%M:%S %z (%Z)'

# это для того если используется перенаправление вывода в файл при вызове из териминала, типа "uber.py > 1.txt"
# просто глюки начинаются поскольку в винде такое перенаправление идет с кодировкой win-1251
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def create_date_time(time_string):
    if is_time_format(time_string, timeformat):
        dt = datetime.strptime(time_string, timeformat)
        return dt

    elif is_time_format(time_string, timeformatGMT):
        dt = datetime.strptime(time_string, timeformatGMT)
        return dt

    else:
        print(time_string)
        raise


def get_date(dt):
    return dt.date().isoformat()


def get_time(dt):
    return dt.time().isoformat()


def get_day_of_week(dt):
    return dt.strftime("%a")


def is_time_format(input, format):
    try:
        datetime.strptime(input, format)
        return True
    except ValueError:
        print(input)


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


def get_uber_summ_by_year(year, print_log=False):
    """
    возвращает сумму за год по письмам из Uber. если print_log=True тогда печатает. но тогда начнутся глюки с tqdm
    """
    mbox = mailbox.mbox('dont_vcs/inbox.mbox', factory=BytesParser(policy=default).parse)

    result = 0

    loop_source = mbox if print_log else tqdm(mbox, ncols=100)

    for message in loop_source:
        mail_date = message.get('date')
        mail_to = message.get('to')
        mail_from = message.get('from')

        dt = create_date_time(mail_date)
        date = get_date(dt)
        time = get_time(dt)
        week_day = get_day_of_week(dt)

        if 'Uber' in mail_from and dt.year == year:
            print("date:  :", date, time, week_day) if print_log else []
            print("to:    :", mail_to) if print_log else []
            print("from   :", mail_from) if print_log else []

            subject = message.get('subject')
            print("subject:", 'None' if subject is None else subject) if print_log else []

            content = get_mail_content(message)
            soup = BeautifulSoup(content, 'lxml')

            price_raw = soup.find('td', class_='check__value check__value_type_price').text.strip()
            price = price_raw.replace('\u202f', ' ').replace('\u2006', ' ').replace(',', '.').split()[0]
            print(f'price  : {price}') if print_log else []

            result += float(price)

            # print("content:", content)
            print("–" * 60) if print_log else []
    return result


if __name__ == '__main__':
    year_sum = get_uber_summ_by_year(2021)
    print('Игого = ', year_sum)
