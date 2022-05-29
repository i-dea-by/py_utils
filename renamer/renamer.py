"""
    сделал дл того, чтобы переименовать кучку кореловских файлов у <client> с визитками

    пример
    было : непомню уже как :) но версия в скобках была где-то ближе к началу изза чего сортировалось плохо
    стало: client_viz_представители_<фио>_(00)
"""
import pathlib


def get_new_name(old_name):
    a_list = old_name.split('_')
    del a_list[3]
    a_list[3], a_list[4] = a_list[4], a_list[3]
    return '_'.join(a_list)


if __name__ == '__main__':
    pattern = '*.cdr'
    path = pathlib.Path(r"t:\trashcan\-").glob(pattern)
    for item in path:
        print(get_new_name(item.stem))
        item.rename(item.with_stem(get_new_name(item.stem)))
