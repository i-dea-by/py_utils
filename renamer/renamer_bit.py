"""
    переименование кореловских файлов с визитками

    было:
        BITdc_dbpbnrb_(01)_<фамилия>.cdr
    нужно:
        BIT_виз_<фамилия>_(версия).cdr

"""
import pathlib

from tqdm import tqdm


def get_new_name(old_name):
    a_list = old_name.split('_')
    # DITdc_dbpbnrb_(01)_<фамилия>_out
    # из всего получается нужно [2]='(01)' [3]='фио' и если есть [4]='out'
    result = ['BIT', 'виз', a_list[3], a_list[2]]
    if len(a_list) > 4:
        result.append(a_list[4])
    return '_'.join(result)


if __name__ == '__main__':
    pattern = '*.cdr'
    path = pathlib.Path(r"t:\trashcan\--").glob(pattern)
    for item in tqdm(path, ncols=100):
        item.rename(item.with_stem(get_new_name(item.stem)))
