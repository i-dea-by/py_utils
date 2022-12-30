import dataclasses
import json
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar

from uber_cost_by_year.typings import RideData

PathLike = TypeVar("PathLike", str, Path)


class CustomJSONencoder(json.JSONEncoder):
    """ Класс для сериализации json """

    def default(self, obj):
        # если попался dataclass
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        # если попался datetime
        if isinstance(obj, datetime):
            return obj.replace(tzinfo=None).isoformat()
        if isinstance(obj, Path):
            return obj.name
        return super().default(obj)


class CustomJSONdecoder(json.JSONDecoder):
    """ Класс для десериализации json """

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def try_datetime(value):
        try:
            result = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            return False
        return result

    @staticmethod
    def try_ride_data(value: dict):
        # если не None значит это данные поездки
        if value.get('ride_dt') is not None:
            return RideData(
                mail_to=value['mail_to'],
                mail_from=value['mail_from'],
                subject=value['subject'],
                ride_dt=CustomJSONdecoder.try_datetime(value['ride_dt']),
                ride_week_day=value['ride_week_day'],
                ride_cost=value['ride_cost'],
            )
        return False

    @staticmethod
    def object_hook(obj):
        """ Перебор объектов на предмет того, что это за структура """

        if result := CustomJSONdecoder.try_ride_data(obj):
            return result

        result = {}
        for key, value in obj.items():
            if _value := CustomJSONdecoder.try_datetime(value):
                result[key] = _value
            else:
                result[key] = value
        return result


def save_as_jsonfile(obj: Any, filename: PathLike, indent: int = 4):
    """ Сохраняет объект в json-файл """
    json_str = json.dumps(obj, cls=CustomJSONencoder, ensure_ascii=False, indent=indent)
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(json_str)


def load_jsonfile(filename: PathLike) -> list | dict:
    """ Загружает json-файл в объект """
    with open(filename, 'r', encoding='utf-8') as f:
        raw_str = f.read()
        json_str = json.loads(raw_str, cls=CustomJSONdecoder)
        return json_str
