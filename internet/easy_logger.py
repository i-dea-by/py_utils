import sys
from pathlib import Path

from .now_time import get_now_time


class EasyLogger:
    """
        Класс для ведения лог-файла. При создании экземпляра создаёт по-умолчанию файл с именем
        из __file__ из раздела __main__ и расширением .log
    """

    def __init__(self, filename: str | None = None) -> None:
        if filename is None:
            self.log_file_with_path = Path(sys.modules['__main__'].__file__).with_suffix('.log')
            self.log_filename = self.log_file_with_path.name
        else:
            self.set_new_name_and_create(filename)
        self.lines_written = 0

    def create(self):
        """ Создание файла лога с отметкой даты и времени создания """
        if not self.log_file_with_path.is_file():
            self.write(f"Created at {get_now_time()}", dont_inc_lines=True)

    def write(self, msg: str, dont_inc_lines: bool = False) -> None:
        """ Запись строки в файл логов """
        with open(self.log_filename, 'a') as f:
            f.write(msg + '\n')
        if not dont_inc_lines:
            self.lines_written += 1

    def set_new_name_and_create(self, filename: str) -> None:
        """ Задаёт новое имя файла и создаёт его, сохраняя в нём дату и время создания """
        self.log_filename = filename
        self.log_file_with_path = Path.cwd() / filename
        self.create()


easy_logger = EasyLogger()
