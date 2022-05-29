import psutil


def is_running(search_str: str, attrs: list = None) -> int | bool:
    """ Поиск процесса у которого в каких-либо параметрах есть искомая строка. По-умолчанию поиск производится
    в сроке запуска .cmdline()
    Список доступных атрибутов: list(psutil.Process().as_dict().keys())
    :param search_str: строка для поиска
    :param attrs: см. https://psutil.readthedocs.io/en/latest/#psutil.Process.as_dict
    :return: False если нет такого процесса, или pid если есть и -1 если в attrs только несуществующий параметр
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
            results_list = []
            for attr in attrs:
                result_attr = getattr(process, attr)()
                if result_attr == '':
                    continue
                elif isinstance(result_attr, (list, tuple)):
                    results_list.append(' '.join(result_attr))
                else:
                    results_list.append(result_attr)
            if search_str in ' '.join(results_list):
                print(f"{process.name()=} | {process.exe()=} | {process.cwd()=} | {process.cmdline()=}")
                return process.pid
        except psutil.Error:
            pass
    return False


if __name__ == '__main__':
    res = is_running('5.252.21.14')
    print('запущен' if res else 'не запущен')

    res = is_running('Total')
    print(res)
