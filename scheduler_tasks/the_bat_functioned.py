from loguru import logger
import winreg

FIND_STR = 'The Bat!'
REGISTRY_KEY = r'SOFTWARE\Clients\Mail'


def open_key(write: bool = False) -> winreg.HKEYType | bool:
    """ Открывает ключ реестра для чтения и возвращает его или False если неудачно
        Если write=True открывает на запись
    :param write: флаг открытия на запись
    :return: ключ реестра типа winreg.HKEYType или False
    """
    access_mode = winreg.KEY_SET_VALUE if write else winreg.KEY_READ
    try:
        return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_KEY, 0, access_mode)
    except OSError as ex:
        logger.error(f"Something wrong! Error: {ex}")
        return False


def get_key() -> str | bool:
    """ Запрашивает значение ключа из реестра и возвращает его. Если происходит ошибка возвращает False
    :return:
    """
    key = open_key()
    if key:
        value = winreg.QueryValue(key, None)
        key.Close()
        return value
    return False


def set_key(new_value: str = FIND_STR) -> bool:
    """ Устанавливает значение ключа реестра. Если удачно, возвращает True
    :param new_value: новое значение ключа
    :return:
    """
    key = open_key(write=True)
    if key:
        winreg.SetValueEx(key, None, 0, winreg.REG_SZ, new_value)
        key.Close()
        return True
    return False


def main():
    value = get_key()
    if value != FIND_STR and set_key():
        logger.info(f"Changed from '{value}' to '{FIND_STR}'")
    else:
        logger.info('OK')


if __name__ == '__main__':
    logger.add("the_bat.log", rotation="1 day", level='DEBUG')
    main()
