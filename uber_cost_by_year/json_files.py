import json
from typing import Any

from uber_cost_by_year.typings import PathLike, _JSONencoder, _JSONdecoder


def save_as_jsonfile(obj: Any, filename: PathLike):
    """ Сохраняет объект в json-файл """
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(to_json_str(obj))


def load_jsonfile(filename: PathLike) -> list | dict:
    """ Загружает json-файл в объект """
    with open(filename, 'r', encoding='utf-8') as f:
        return from_json_str(f.read())


def to_json_str(obj: Any, indent: int = 4) -> str:
    """ Возвращает json-строку из переданного объекта на основе json.dumps """
    return json.dumps(obj, cls=_JSONencoder, ensure_ascii=False, indent=indent)


def from_json_str(_str: str) -> list | dict:
    """ Декодирует json-строку в объект, на основе json.loads """
    return json.loads(_str, cls=_JSONdecoder)
