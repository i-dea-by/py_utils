"""
    Подсчёт чего-нибудь в файлах ))) Пока понадобилось только кол-во строк
"""
import glob
import sys
from pathlib import Path


def lines_counter_sum(filename: str | Path) -> int:
    """ Подсчёт количества строк с использованием функции sum

    :param filename: имя файла
    :return: Количество строк
    """
    with open(filename, 'r', encoding='utf8') as file:
        return sum((1 for _ in file))


def lines_counter_summ(filename: str | Path) -> int:
    """ Подсчёт количества строк с использованием +=

    :param filename: имя файла
    :return: Количество строк
    """
    lines = 0
    with open(filename, 'r') as file:
        for _ in file:
            lines += 1
    return lines


def print_help():
    print('Вызов: fcounter [имя файла или путь]')


def main():
    # path = Path(file_or_dir)
    args_len = len(sys.argv)
    if args_len == 1:
        print_help()
        exit()

    files = glob.glob(sys.argv[1], recursive=True)

    total_lines = 0
    for _file in files:
        count_lines = lines_counter_sum(_file)
        print(f"{_file} - {count_lines} строк")
        total_lines += count_lines
    print('-' * 50)
    print(f"Всего строк в {len(files)} файлах - {total_lines}")



if __name__ == '__main__':
    main()
    # print(lines_counter_sum('fcounter.py'))
    # print(lines_counter_summ('fcounter.py'))
