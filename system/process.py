import psutil


def is_running(search_str: str, attrs: list = None) -> int:
    """ Search for a process that has the desired string in any of its parameters. By default, the search is performed
    in the launch line .cmdline()
    List possible attrs: list(psutil.Process().as_dict().keys())
    :param search_str: search string
    :param attrs: см. https://psutil.readthedocs.io/en/latest/#psutil.Process.as_dict
    :return: 0 if there is no such process, or pid if there is, and -1 if non-existent parameter in attrs
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
