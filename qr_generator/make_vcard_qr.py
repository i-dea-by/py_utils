import segno
from segno import helpers
from decouple import config

from typings import DCvCard


def create_qr_files(data: list[DCvCard], prefix: str = '', postfix: str = 'ru'):
    """ Создает .svg файлы с QR. Файлы создаются в каталоге out/ в том же месте
        где и этот .py файл 
        Шаблон имени файла: out/{file_prefix}_{card.displayname}_{postfix}.svg
    """
    for index, card in enumerate(data, 1):
        print(f"[{index}/{len(cards)}] {card.displayname}")
        vcard_str = helpers.make_vcard_data(**card.to_dict())
        # перед запятыми ставит слэш, оно может почеу-то и надо, но
        # на iPhone когда читает такой QR в строке адреса появляются
        # ненужные символы перед запятыми
        vcard_str = vcard_str.replace('\\', '')
        print(vcard_str)
        qr = segno.make(vcard_str, error='L', encoding='utf-8')

        filename = f'out/{prefix}_{card.displayname}_{postfix}.svg'
        qr.save(filename, scale=10)


if __name__ == '__main__':
    # модуль с функциями с данными клиентов, чтоб не попали в git
    # пример функции с импортом из .csv см. в inner.py.example
    import _inner

    # читает из .env файла. Пример заполнения в .env.example
    PATH_TO_CSV = config('PATH_TO_CSV')
    FILE_PREFIX = config('PREFIX')
    FILE_POSTFIX = config('POSTFIX', default='ru')
    # префикс и постфикс нужны для формирования имени файла .svg типа:
    # {file_prefix}_{card.displayname}_{postfix}.svg
    
    cards = _inner.import_from_vcs(PATH_TO_CSV)
    create_qr_files(cards, FILE_PREFIX, FILE_POSTFIX)

    """
        L recovers 7% of data
        M recovers 15% of data
        Q recovers 25% of data
        H recovers 30% of data

    Возможно с русским поможет
        BEGIN:VCARD
        VERSION:3.0
        N;CHARSET=UTF-8:ФИРМА.РФ
        FN;CHARSET=UTF-8:ФИРМА.РФ
        TEL:+7123456789
        EMAIL:info@info.ru
        ORG;CHARSET=UTF-8:Название фирмы
        URL;CHARSET=UTF-8:http://фирма.рф
        NOTE:https://instagram.com/name
        END:VCARD

    """
