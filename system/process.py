import psutil


def is_running(search_str: str, attrs: list = None) -> int:
    """ Поиск процесса у которого в каких-либо параметрах есть искомая строка. По-умолчанию поиск производится
    в сроке запуска .cmdline()
    Список доступных атрибутов: list(psutil.Process().as_dict().keys())
    :param search_str: строка для поиска
    :param attrs: см. https://psutil.readthedocs.io/en/latest/#psutil.Process.as_dict
    :return: 0 если нет такого процесса, или pid если есть и -1 если в attrs только несуществующий параметр
    """
    if attrs is None:
        attrs = ['cmdline']
    else:
        valid_attrs = psutil.Process().as_dict().keys()
        attrs = set(attrs) & set(valid_attrs)
        if not attrs:
            return -1
    for process in psutil.process_iter(attrs):
        try:
            if search_str in ' '.join(_filter_invalid_attrs(process, attrs)):
                return process.pid
        except psutil.Error:
            pass
    return 0


#################################################
#               internal functions              #
#################################################

def _filter_invalid_attrs(process: psutil.Process, attrs: list) -> list:
    """ Filter bad attributes that will prevent results from join into a search string """
    result = []
    for attr in attrs:
        result_attr = getattr(process, attr)()
        if result_attr == '':
            continue
        elif isinstance(result_attr, (list, tuple)):
            result.append(' '.join(result_attr))
        else:
            result.append(result_attr)
    return result


if __name__ == '__main__':
    searching_str = 'chrome.exe'
    print(f"Searching {searching_str}...")
    res = is_running(searching_str)
    if res:
        print(f" PID: {res}")
        print(f" {psutil.Process(res).name()=}\n"
              f" {psutil.Process(res).exe()=}\n"
              f" {psutil.Process(res).cwd()=}\n"
              f" {psutil.Process(res).cmdline()=}"
              )
    else:
        print(f"{searching_str} not found")
