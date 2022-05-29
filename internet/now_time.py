from datetime import datetime


def get_now_time() -> str:
    """ Возвращает текущую дату и время """
    return datetime.now().strftime("%m.%d %H:%M:%S")
