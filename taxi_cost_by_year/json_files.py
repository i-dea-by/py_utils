import json
from pathlib import Path
from typing import Any, TypeVar, Type

PathLike = TypeVar("PathLike", str, Path)


def save_as_jsonfile(
        obj: Any,
        filename: PathLike,
        encoder: Type[json.JSONEncoder] | None = None,
        indent: int = 4
) -> None:
    """ Сохраняет объект в json-файл

    :param obj:
    :param filename:
    :param encoder: класс типа JSONEncoder преобразующий объекты в словарь
    :param indent: отсутпы в файле
    :return:
    """
    json_str = json.dumps(obj, cls=encoder, ensure_ascii=False, indent=indent)
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(json_str)


def load_jsonfile(
    filename: PathLike,
    decoder: Type[json.JSONDecoder] | None = None
) -> list | dict:
    """ Загружает json-файл в объект

    :param filename:
    :param decoder:
    :return: список или словарь объектов
    """
    with open(filename, 'r', encoding='utf-8') as f:
        raw_str = f.read()
        json_str = json.loads(raw_str, cls=decoder)
        return json_str
